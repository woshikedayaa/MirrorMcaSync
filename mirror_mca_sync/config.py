import os # 用来 生成文件 读文件
import configparser
import json
from mcdreforged.api.types import PluginServerInterface

default_config = {
    "from":"survival/world",
    "to":"mirror/world",
    "command":"!!sync",
    "waitTime":"10"
}

psi:PluginServerInterface = None

global_config = default_config

consts = {
    "config.path":"config/mirror_mca_sync.json",
}

def init_config(p:PluginServerInterface):
    global psi,global_config,default_config
    psi = p
    try:
        # 判断配置文件是否存在
        if file_exist(consts["config.path"]) == False:
            psi.logger.info(psi.tr("mms.info.config.file_not_exist"))
            # 创建文件
            with open(consts["config.path"],"w") as file:
                # 写入默认配置文件
                json.dump(default_config,file,indent=4)
        else:
            # 直接读取配置文件
            with open(consts["config.path"],"r") as file:
                global_config = json.load(file)
    except Exception as e:
        # 遇到异常
        psi.logger.error(psi.rtr("mms.error.config.file_read_error"),e)
        # 使用默认的配置
        global_config = default_config
    return

def file_exist(path:str)->bool:
    return os.path.exists(path)

def get(key:str)->str:
    return global_config[key]