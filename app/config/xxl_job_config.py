import asyncio
from functools import wraps

import pyxxl.xxl_client
from pyxxl import ExecutorConfig, PyxxlRunner
from pyxxl.ctx import g

from app.common.utils.ip_util import *
from app.config.nacos_config import get_config
from app.config.trace_.request_context import set_trace_id

# from app.common.utils.wechat_msg_util import send_markdown_template_exception_message
# from app.common.const import WechatRobotEnum

# get the log folder address
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# scheduled task log storage path
xxl_executor_log_path = os.getenv("XXL_EXECUTOR_LOG_PATH", f"{BASE_DIR}/xxl_log/pyxxl.log")
xxl_log_path = os.getenv("XXL_LOG_PATH", f"{BASE_DIR}/xxl_log")


_executor = None

"""
load global configuration
"""
def _load_xxl_config() -> ExecutorConfig:
    config = get_config()
    xxl_config = config['xxl-job']

    executor_config = ExecutorConfig(
        xxl_admin_baseurl=xxl_config['url'],
        executor_app_name=xxl_config['app_name'],
        executor_listen_host=get_local_ip(),
        executor_listen_port=get_port(),
        access_token=xxl_config['access_token'],
        executor_log_path=xxl_executor_log_path,
        log_local_dir=xxl_log_path,
        graceful_close=True,
        http_retry_times = 9,
        http_retry_duration = 10,
        http_timeout = 60
    )
    return executor_config

def _load_executor():
    global _executor
    if _executor is None:
        _executor = PyxxlRunner(_load_xxl_config())
    return _executor

"""
    get actuator unified entry
"""
def get_executor() -> PyxxlRunner:
    global _executor
    if _executor is None:
        _load_executor()
    return _executor

"""
xxl-job automatic bind trace_id executor
"""
def traced_executor(name):

    def decorator(func):
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            trace_id = g.xxl_run_data.logId
            set_trace_id(trace_id)
            return func(*args, **kwargs)

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            trace_id = g.xxl_run_data.logId
            set_trace_id(trace_id)
            return await func(*args, **kwargs)

        wrapped_func = async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

        # register to pyxxl
        return _executor.register(name=name)(wrapped_func)
    return decorator



# save original method
_real_post = pyxxl.xxl_client.XXL._post

# expand the original method and add alarms
async def patched_post(self, *args, **kwargs):
    try:
        return await _real_post(self, *args, **kwargs)
    except Exception as e:
        log.exception(f"[XXL-JOB] Request Admin Error: {str(e)}")
        # send message to enterprise wechat (if necessary you can open it)
        # send_markdown_template_exception_message(WechatRobotEnum.ALGORITHM_DEFAULT, ["[XXL-JOB] Request Admin Error"], e)

# Patch (replacement method)
pyxxl.xxl_client.XXL._post = patched_post

"""
Global initialization
"""
_load_executor()
