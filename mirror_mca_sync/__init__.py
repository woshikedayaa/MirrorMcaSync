from mcdreforged.api.types import PluginServerInterface
from mcdreforged.api.command import SimpleCommandBuilder
from mcdreforged.api.types import PluginCommandSource
from mcdreforged.api.all import new_thread
import time
import os
import shutil

import minecraft_data_api as api

from . import config
processing = False
aborted = False

def on_load(now:PluginServerInterface,old):
    # 初始化配置文件
    config.init_config(now)

    # 注册指令
    registry_command(now)

    now.register_help_message(config.get("command"),"同步镜像服")

def registry_command(psi:PluginServerInterface):
    b = SimpleCommandBuilder()
    b.command(config.get("command"),sync_pre)
    b.command(config.get("command")+" abort",sync_abort)
    b.register(psi)

@new_thread("mms")
def sync_pre(source:PluginCommandSource,ctx:dict):
    # 先检测是不是玩家调用的
    if source.is_player == False:
        config.psi.logger.warn(
            config.psi.rtr("mms.warn.sync.call_from_other",config.get("command")))
        return

    global aborted,processing
    if processing:
        config.psi.say(config.psi.rtr("mms.warn.sync.repeat",config.get("command")))
        return
    # 没有正在处理的 创建一个处理的
    # 获取玩家所在mca文件位置
    name = source.player
    pos = api.get_player_coordinate(name)
    mx = int(pos.x//16//32)
    mz = int(pos.z//16//32)
    dim = api.get_player_info(name,"Dimension")
    # 给玩家时间等待
    processing=True
    wt = int(config.get("waitTime"))
    for i in range(wt):
        if aborted:
            processing=False
            aborted=False
            return
        time.sleep(1)
        config.psi.say(config.psi.rtr("mms.info.sync.start",wt-i,config.get("command")))

    # 等待时间完了 开始执行备份
    # 构建源文件目录(生存)
    src_path = build_file_list(config.get("from"),mx,mz,dim)
    # 同步其他的
    src_path.append(os.path.join(config.get("from"),"entities"))
    src_path.append(os.path.join(config.get("from"),"poi"))
    src_path.append(os.path.join(config.get("from"),"data"))
    src_path.append(os.path.join(config.get("from"),"level.dat"))
    # 构建目标目录(镜像)
    dst_path = build_file_list(config.get("to"),mx,mz,dim)
    dst_path.append(os.path.join(config.get("to"),"entities"))
    dst_path.append(os.path.join(config.get("to"),"poi"))
    dst_path.append(os.path.join(config.get("to"),"data"))
    dst_path.append(os.path.join(config.get("to"),"level.dat"))
    # 同步
    # 2024-1-14 这里有个极端情况
    # 就是玩家刚好在边界 然后就会复制一个文件 
    # 然后只复制玩家的位置的 导致有很大的边界感
    # 所以解决方案就是 复制玩家周围的文件 大概 3x3 的mca`` 以玩家为中心
    #sync(src_path,dst_path) -> sync_single
    sync(src_path,dst_path)
    processing=False
    aborted=False
    return

# 你可以理解为 copy
def sync_single(src:str , dst : str):
    config.psi.logger.info(config.psi.rtr("mms.info.sync.copy_info",src,dst))
    if config.file_exist(src)== False:
        return
    else:
        # 开始备份
        # 处理文件夹
        if os.path.isdir(src):
            shutil.rmtree(dst)
            shutil.copytree(src,dst)
            return
        shutil.copyfile(src,dst)
    
def sync(src:list[str],dst:list[str]):
    # 先关闭服务器
    if config.psi.is_server_running():
        if config.psi.stop()==False:
            # 关闭失败 重启服务器
            config.psi.logger.error(config.psi.rtr("mms.error.sync.stop_server_fail"))
            config.psi.restart()
            return
    config.psi.wait_until_stop()
    try:
        # 复制文件 关键部分
        config.psi.logger.info(config.psi.rtr("mms.info.sync.copy"))
        for s,d in zip(src,dst):
            sync_single(s,d)    
    except Exception as e:
        # 这里备份失败了
        config.psi.logger.error(config.psi.rtr("mms.error.sync.copy_file_fail"))
    finally:
        # 启动服务器
        config.psi.start()
    # 同步完成
    return

# 中止同步
def sync_abort():
    global aborted,processing
    if processing:
        aborted = True
    return
 
# 构建一个列表 返回的是要 copy 的文件
def build_file_list(pre:str,centerx:int,centerz:int,dim:int)->list[str]:
    res = []
    # 主世界 地狱 末地
    div = {
        "minecraft:overworld":"region",
        "minecraft:the_nether":os.path.join("DIM-1","region"),
        "minecraft:the_end":os.path.join("DIM1","region")
    }
    # 构建文件
    for i in range(-1,2):
       for j in range(-1,2):
            mca_name = ".".join(["r",str(centerx+i),str(centerz+j),"mca"])
            target = os.path.join(pre,div[dim],mca_name)
            res.append(target)
    return res