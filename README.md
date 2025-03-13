# KeitoKun 自动收集助手

[![GitHub stars](https://img.shields.io/github/stars/0xbaiwan/keitokun_bot)](https://github.com/0xbaiwan/keitokun_bot/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/0xbaiwan/keitokun_bot)](https://github.com/0xbaiwan/keitokun_bot/network)
[![GitHub issues](https://img.shields.io/github/issues/0xbaiwan/keitokun_bot)](https://github.com/0xbaiwan/keitokun_bot/issues)

## 项目地址
- GitHub: [https://github.com/0xbaiwan/keitokun_bot](https://github.com/0xbaiwan/keitokun_bot)

## 功能介绍
这是一个用于KeitoKun游戏的自动收集助手，可以帮助您自动完成每日收集任务。

## 功能特点
- ✅ 多账号支持
- ✅ 自动控制收集频率
- ✅ 完整的错误处理
- ✅ 使用安全的WSS连接
- ✅ 断线自动重连
- ✅ 详细的运行日志
- ✅ 配置参数可调整
- ✅ 多线程并行处理

## 使用前准备

### 1. 获取代码
```bash
git clone https://github.com/0xbaiwan/keitokun_bot.git
cd keitokun_bot
```

### 2. 安装Python依赖
```bash
pip install websocket-client
```

### 3. 配置账号信息
1. 在项目根目录创建 `account.txt` 文件
2. 在文件中每行输入一个UID（支持多账号）
3. 使用 `//` 开头的行将被视为注释

account.txt 示例：
```
12345678
98765432
//这是一个注释行
```

### 4. 获取UID方法
![获取UID教程](https://github.com/user-attachments/assets/a4d835cd-a254-4d44-895b-d1aec0ac1bb6)

## 使用说明

### 运行程序
```bash
python keito.py
```

### 配置说明
程序中的主要参数都可以在代码顶部的 `CONFIG` 字典中调整：
- `COLLECT_AMOUNT`: 收集数量
- `COLLECT_NUM`: 收集次数
- `RETRY_COUNT`: 断线重连次数
- `RETRY_DELAY`: 重连等待时间（秒）
- `REQUEST_DELAY`: 请求间隔时间（秒）
- `MAX_REQUESTS`: 最大请求次数

### 注意事项
1. 程序中的收集数量(collectNum)已设置为每日上限
2. 建议每天运行一次即可
3. ⚠️ 温馨提示：任何自动化脚本都可能触发游戏的防护机制，请谨慎使用
4. 程序会自动处理断线重连，最多重试3次
5. 所有操作都会记录详细日志，方便排查问题

## 问题反馈
如遇到问题，请：
1. 确保account.txt文件格式正确
2. 确保UID输入正确
3. 检查网络连接是否正常
4. 查看程序输出的详细日志
5. 检查配置参数是否合理