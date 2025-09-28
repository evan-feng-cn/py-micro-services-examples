from threading import Lock

import nacos
import yaml

from app.common.utils.ip_util import *
from app.common.const import APP_ENV, TEST_ENV

# base dir
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class NacosConfigManager:
    _instance = None
    _lock = Lock()
    _initialized = False
    _config_raw = None
    _config_yaml = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, server_addr=None, namespace=None, data_id=None, group=None, username=None, password=None):
        # avoid duplicate initialization
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self.client = nacos.NacosClient(
                        server_addr,
                        namespace=namespace,
                        username=username,
                        password=password
                    )
                    self.data_id = data_id
                    self.group = group

                    # Pull the latest configuration during initialization
                    self.fetch_config()

                    # registration service (if you need it)
                    self.client.add_naming_instance(service_name=data_id, ip=get_local_ip(), port=get_port(), group_name=group,
                                                    cluster_name="DEFAULT", ephemeral=True, weight=1.0,
                                                    heartbeat_interval=10)

                    # monitor configuration change events
                    # self.client.add_config_watcher(self.data_id, self.group, self.refresh)
                    self._initialized = True

    def fetch_config(self):
        try:
            no_snapshot = TEST_ENV == APP_ENV
            log.info(f"does NACOS close the local disaster recovery snapshot: {no_snapshot}")
            content = self.client.get_config(self.data_id, self.group, no_snapshot=no_snapshot)
            if content is None:
                log.warning(f"received nacos configuration content is empty, dataId={self.data_id}")
                return
            self._config_raw = content
            self._config_yaml = yaml.safe_load(content)
            log.info(f"successfully loaded and parsed nacos configuration, dataId={self.data_id}")
        except Exception as e:
            log.error(f"failed to retrieve or parse configuration: {e}")

    def get_raw_config(self):
        if self._config_raw is None:
            self.fetch_config()
        return self._config_raw

    def get_yaml_config(self):
        if self._config_yaml is None:
            self.fetch_config()
        return self._config_yaml

    def refresh(self):
        # manually refresh configuration
        self.fetch_config()


"""
Get Nacos client information for a single instance"""
def get_nacos_client() -> NacosConfigManager:
    env = APP_ENV
    config = _load_config(env)
    nacos_config = config['nacos']
    host = nacos_config.get('host')
    username = nacos_config.get('username')
    password = nacos_config.get('password')
    group = nacos_config.get('group')
    namespace = nacos_config.get('namespace')
    data_id = nacos_config.get('data_id')
    return NacosConfigManager(host, namespace, data_id, group, username, password)

_nacos_base_config = None

"""
read nacos yaml file configuration
"""
def _load_config(env: str):
    """Load config.yaml and return the parsed configuration."""
    global _nacos_base_config
    if _nacos_base_config is None:
        try:
            config_path = f'config_{env}.yaml'
            CONFIG_PATH = os.path.join(BASE_DIR, config_path)
            with open(CONFIG_PATH, 'r') as f:
                _nacos_base_config = yaml.safe_load(f)
            log.info(f"Loaded configuration from {CONFIG_PATH}")
        except Exception as e:
            log.error(f"Failed to load config.yaml: {str(e)}")
            raise
    return _nacos_base_config

"""
get all configurations yoml dict
"""
def get_config():
    return get_nacos_client().get_yaml_config()

"""
get database configuration
"""
def get_db_config():
    return get_config()['database']

