import os
import socket

from app.common.logger import log


"""
get the ip address of the local executor
"""
def get_local_ip():
    try:
        # UDP, is not a real link, it only obtains a unique export IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        log.info(f"resolve local ip address:{ip}")
        s.close()
        return ip
    except Exception as e:
        log.exception(f"resolve local ip error:{str(e)}")
        return '127.0.0.1'

"""
get port
"""
def get_port():
    env_port = os.getenv("PROCESS_PORT")
    log.info(f"get the port:{env_port}")
    if env_port:
        return int(env_port)

    # default port
    return 8080

