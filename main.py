import asyncio
import json
import random
import websockets
import yaml
import logging

# 配置日志
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# 读取配置文件
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 模拟一些弹幕内容
MESSAGES = [
    "这就是传说中的弹幕吗？",
    "666666666",
    "测试一条超长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长的弹幕看看会不会重叠",
    "Vue + Tauri 看起来真不错",
    "Rust 写的后端就是稳",
    "前端避重叠算法生效了吗？"
]

# 模拟一些用户昵称
USERS = ["爱写代码的小王", "路人甲", "弹幕狂魔", "Tauri初学者", "Python后端"]

async def handler(websocket):
    logging.info(f"客户端已连接: {websocket.remote_address}")
    try:
        while True:
            # 构造符合要求的 JSON 数据
            data = {
                "user": random.choice(USERS),
                "text": random.choice(MESSAGES),
            }
            # 发送数据
            await websocket.send(json.dumps(data))
            logging.info(f"已发送: {data['text']}")
            # 每隔 2 秒发送一次
            await asyncio.sleep(config.get("message_interval", 2))
    except websockets.exceptions.ConnectionClosed:
        logging.warning(f"客户端已断开连接: {websocket.remote_address}")

async def main():
    # 监听本地 8080 端口
    async with websockets.serve(handler, config.get("host", "127.0.0.1"), config.get("port", 8080)):
        logging.info(f"WS 服务器已启动: ws://{config.get('host', '127.0.0.1')}:{config.get('port', 8080)}")
        # 修复行：创建一个永久等待的事件
        await asyncio.Event().wait() 

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("服务器已停止")