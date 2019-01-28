#import mysocket
#myserver = mysocket.mysocket("1","server",12345)
from mysocket import mysocketServer
from mysocket import CONN_POOL
import sys
myserver = mysocketServer(1,"MSQ",12345)
myserver.setDaemon(True)
myserver.start()
while True:
	cmd = input("""--------------------------
			输入1:查看当前在线人数
			输入2:给指定客户端发送消息
			输入3:关闭服务端
				""")
	if cmd == '1':
		print("--------------------------")
		print("当前在线人数：", len(CONN_POOL))
	elif cmd == '2':
		print("--------------------------")
		index, msg = input("请输入“索引,消息”的形式：").split(",")
		CONN_POOL[int(index)].sendall(msg.encode(encoding='utf8'))
	elif cmd == '3':
		print('服务器已关闭！')
		sys.exit()
