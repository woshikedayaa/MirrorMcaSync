# MirrorMcaSync
MirrorMcaSync 是一个 [Mcdreforged](https://github.com/Fallen-Breath/MCDReforged)插件    
适用于 vanilla_handler 等只有一个world文件夹的服务器  

# 设计初衷
在传统镜像服 同步 通常都是 复制整个生存服存档    
很多时候 我们只需要同步地形 玩家物品排行榜什么的 不太需要了  
这个插件就此诞生 它只同步输入时玩家所在mca为中心的 3x3 的mca文件  
以及其他必须的数据 这样一来就对硬盘压力小了很多  

# 实现原理
在镜像服中
玩家先输入对应 MCDR 指令 这里以 !!sync 为例  
输入后会获取玩家所在mca文件路径 (玩家所在维度的)  
再以玩家所在的mca为中心  获取其周围的mca文件  
再从生存服复制mca文件 同步至镜像服 最后重启  

# 配置
```json
# config/mirror_mca_sync.json
{
    "from":"survival/world", // mca文件来源 通常是生存服
    "to":"mirror/world", // mca文件目标 通常是镜像服
    "command":"!!sync", // 玩家需要输入的指令
     // 等待时间 给玩家的反应时间 
     // 玩家输入指令后会等待这个时间才会同步
     // 单位 : s
    "waitTime":"10"
}
```

# LICENSE
```text
MIT License

Copyright (c) 2024 Kedaya

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```