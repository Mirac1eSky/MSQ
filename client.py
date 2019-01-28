from mysocket import mysocketClient
if __name__ == '__main__':
	mysocketClient = mysocketClient("huihui","laoxiong","ou~ou~")
	mysocketClient.sendM()
	#mysocketClient.setDaemon(True)
	#mysocketClient.start()


"""	print('程序自身在运行')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          # 创建 socket 对象
	host = socket.gethostname() # 获取本地主机名
	port = 12345                # 设置端口号
	s.connect((host, port))

	print('这是客户端')
	print ((s.recv(1024)).decode('utf-8'))
	s.close()  """
