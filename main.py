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
try:
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    logger.info("配置文件 config.yaml 加载成功。")
    logger.debug(f"配置内容: {config}")
except FileNotFoundError:
    logger.error("配置文件 config.yaml 未找到，创建默认配置文件。")
    config = {
        "message_interval": 2,
        "host": "127.0.0.1",
        "port": 8080
    }
    with open("config.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config, f)
    logger.info("已创建默认配置文件 config.yaml。")

# 模拟一些弹幕内容
try:
    with open("messages.txt", "r", encoding="utf-8") as f:
        MESSAGES = [line.strip() for line in f if line.strip()]
    logger.info("弹幕内容 messages.txt 加载成功。")
except FileNotFoundError:
    logger.error("弹幕内容 messages.txt 未找到，创建默认弹幕内容文件。")
    MESSAGES = [
        "这就是传说中的弹幕吗？",
        "666666666",
        "测试一条超长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长的弹幕看看会不会重叠",
        "Vue + Tauri 看起来真不错",
        "Rust 写的后端就是稳",
        "前端避重叠算法生效了吗？"
    ]
    with open("messages.txt", "w", encoding="utf-8") as f:
        for msg in MESSAGES:
            f.write(msg + "\n")
    logger.info("已创建默认弹幕内容文件 messages.txt。")

# 模拟一些用户昵称
try:
    with open("users.txt", "r", encoding="utf-8") as f:
        USERS = [line.strip() for line in f if line.strip()]
    logger.info("用户昵称 users.txt 加载成功。")
except FileNotFoundError:
    logger.error("用户昵称 users.txt 未找到，创建默认用户昵称文件。")
    USERS = ["爱写代码的小王", "路人甲", "弹幕狂魔", "Tauri初学者", "Python后端"]
    with open("users.txt", "w", encoding="utf-8") as f:
        for user in USERS:
            f.write(user + "\n")
    logger.info("已创建默认用户昵称文件 users.txt。")

async def handler(websocket):
    logger.info(f"客户端已连接: {websocket.remote_address}")
    try:
        while True:
            # 构造符合要求的 JSON 数据
            data = {
                "user": random.choice(USERS),
                "text": random.choice(MESSAGES),
            }
            # 发送数据
            await websocket.send(json.dumps(data))
            logger.info(f"已发送: {data['text']}")
            # 每隔 2 秒发送一次
            await asyncio.sleep(config.get("message_interval", 2))
    except websockets.exceptions.ConnectionClosed:
        logger.warning(f"客户端已断开连接: {websocket.remote_address}")

async def main():
    # 监听本地 8080 端口
    async with websockets.serve(handler, config.get("host", "127.0.0.1"), config.get("port", 8080)):
        logger.info(f"服务已启动: ws://{config.get('host', '127.0.0.1')}:{config.get('port', 8080)}")
        # 修复行：创建一个永久等待的事件
        await asyncio.Event().wait() 

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("服务器已停止")