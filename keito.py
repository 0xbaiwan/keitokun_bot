import websocket
import json
import time
import threading

# 配置参数
CONFIG = {
    'API_URL': 'wss://game.keitokun.com/api/v1/ws',
    'HEADERS': {
        'Origin': 'https://game.keitokun.com',
        'Cache-Control': 'no-cache',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'Cookie': '_ga=GA1.1.664420135.1739199804; _ga_LD12CVNEZ7=GS1.1.1739199803.1.1.1739199864.0.0.0'
    },
    'COLLECT_AMOUNT': 500,
    'COLLECT_NUM': 500,
    'RETRY_COUNT': 3,
    'RETRY_DELAY': 5,  # 重试延迟（秒）
    'REQUEST_DELAY': 0.5,  # 请求间隔（秒）
    'MAX_REQUESTS': 1000  # 最大请求次数
}

class WebSocketClient:
    def __init__(self, uid):
        self.uid = uid
        self.ws = None
        self.retry_count = 0

    def on_message(self, ws, message):
        try:
            msg_data = json.loads(message)
            print(f"收到服务器消息 [UID: {self.uid}]: {msg_data}")
        except json.JSONDecodeError:
            print(f"收到非JSON消息 [UID: {self.uid}]: {message}")

    def on_error(self, ws, error):
        print(f"发生错误 [UID: {self.uid}]: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print(f"连接已关闭 [UID: {self.uid}] 状态码: {close_status_code}, 消息: {close_msg}")
        # 断线重连逻辑
        if self.retry_count < CONFIG['RETRY_COUNT']:
            print(f"尝试重新连接 [UID: {self.uid}] 第 {self.retry_count + 1} 次")
            time.sleep(CONFIG['RETRY_DELAY'])
            self.retry_count += 1
            self.connect()

    def on_open(self, ws):
        print(f"连接已建立 [UID: {self.uid}]")
        self.retry_count = 0  # 重置重试计数
        
        def send_messages():
            message = {
                "id": 13,
                "cmd": 1001,
                "uid": self.uid,
                "data": {
                    "amount": CONFIG['COLLECT_AMOUNT'],
                    "collectNum": CONFIG['COLLECT_NUM'],
                    "timestamp": int(time.time() * 1000)
                }
            }
            
            try:
                for _ in range(CONFIG['MAX_REQUESTS']):
                    ws.send(json.dumps(message))
                    time.sleep(CONFIG['REQUEST_DELAY'])
                print(f"已完成所有消息发送 [UID: {self.uid}]")
            except Exception as e:
                print(f"发送消息时出错 [UID: {self.uid}]: {e}")

        # 在新线程中发送消息
        threading.Thread(target=send_messages).start()

    def connect(self):
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp(
            f"{CONFIG['API_URL']}?uid={self.uid}",
            header=CONFIG['HEADERS'],
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.run_forever()

def main():
    try:
        with open("account.txt", "r", encoding='utf-8') as f:
            uids = [line.strip() for line in f.readlines() if line.strip() and not line.strip().startswith("//")]
        
        if not uids:
            print("警告: account.txt 中没有找到有效的UID")
            return

        print(f"找到 {len(uids)} 个有效UID，开始处理...")
        
        # 创建并启动线程
        threads = []
        for uid in uids:
            client = WebSocketClient(uid)
            thread = threading.Thread(target=client.connect)
            threads.append(thread)
            thread.start()
            print(f"已启动UID {uid} 的处理线程")

        # 等待所有线程完成
        for thread in threads:
            thread.join()

    except FileNotFoundError:
        print("错误: 未找到account.txt文件。请创建该文件并在每行输入一个UID。")
    except Exception as e:
        print(f"程序运行出错: {e}")

if __name__ == "__main__":
    main()
