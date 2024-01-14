import os # 用来 生成文件 读文件
import configparser
from mcdreforged.api.types import PluginServerInterface

default_config = {
    "from":"survival/world",
    "to":"mirror/world",
    "command":"!!sync",
    "waitTime":"10"
}

psi:PluginServerInterface = None

global_config:configparser.ConfigParser

consts = {
    "config.path":"config/mirror_mca_sync.json",
    "config.default":default_config,
}

def init_config(p:PluginServerInterface):
    global psi,global_config
    psi = p
    cfg = configparser.ConfigParser()
    try:
        # 判断配置文件是否存在
        if file_exist(consts["config.path"]) == False:
            psi.logger.info(psi.tr("mms.info.config.file_not_exist"))
            # 先读取默认配置文件
            cfg.read_dict(default_config)
            # 创建文件
            with open(consts["config.path"],"w") as file:
                # 写入默认配置文件
                cfg.write(file)
        else:
            # 直接读取配置文件
            cfg.read_file(consts["config.path"])
    except Exception as e:
        # 遇到异常
        psi.logger.error(psi.rtr("mms.error.config.file_read_error"),e)
        # 使用默认的配置
        tempc = configparser.ConfigParser()
        tempc.read_dict(default_config)
        global_config = tempc
    else:
        global_config = cfg
    return

def file_exist(path:str)->bool:
    return os.path.exists(path=path)

def get(key:str)->str:
    return global_config.get(key)