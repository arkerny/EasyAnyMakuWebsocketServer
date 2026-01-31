import asyncio
import json
import random
import websockets

# 模拟一些弹幕内容
MESSAGES = [
    "这就是传说中的弹幕吗？",
    "666666666",
    "测试一条超长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长长的弹幕看看会不会重叠",
    "Vue + Tauri 看起来真不错",
    "Rust 写的后端就是稳",
    "前端避重叠算法生效了吗？"
]

USERS = ["爱写代码的小王", "路人甲", "弹幕狂魔", "Tauri初学者", "Python后端"]

async def handler(websocket):
    print(f"客户端已连接: {websocket.remote_address}")
    try:
        while True:
            # 构造符合你前端预期的 JSON 数据
            data = {
                "user": random.choice(USERS),
                "text": random.choice(MESSAGES),
            }
            
            # 发送数据
            await websocket.send(json.dumps(data))
            print(f"已发送: {data['text']}")
            
            # 每隔 2 秒发送一次
            await asyncio.sleep(2)
    except websockets.exceptions.ConnectionClosed:
        print("客户端已断开连接")

async def main():
    # 监听本地 8080 端口
    async with websockets.serve(handler, "127.0.0.1", 8080):
        print("WS 服务器已启动: ws://127.0.0.1:8080")
        # 修复行：创建一个永久等待的事件
        await asyncio.Event().wait() 

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n服务器已停止")