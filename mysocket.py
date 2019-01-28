import socket              
import threading
import re
import pdb
import time
import sys
HOST=socket.gethostname()
CLINET_MAP={}
CONN_POOL = []
TMP_MSG={"test":"demo"}
REG = re.compile(r'(.*)-(.*)-(.*)',re.I)

LOCKC = threading.Lock()
LOCK = threading.Lock()
class mysocketServer(threading.Thread):
	"""docstring for mysocket"""
	port=""
	s=""
	msg="成功建立连接！"
	reg=""
	def __init__(self, threadID, name,port):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.port = port
		self.s=socket.socket(
		    socket.AF_INET, socket.SOCK_STREAM)        
		self.s.bind((HOST,self.port))
		self.s.listen(5)
	def run(self):
		print ("服务启动：" + self.name)
		thread1 = threading.Thread(target=listenClient)
		thread1.setDaemon(True)
		thread1.start()
		runserve(self.s,self.msg,self.reg)
		print ("服务关闭：" + self.name)
"""def runserve(s,msg,reg):
	counter=5
	while True:
		c, addr = s.accept()     # 建立客户端连接。
		print ('连接地址：', addr[1])

		#c.send(msg.encode('utf-8'))
		msg=(c.recv(4096)).decode('utf-8')
		print(msg)
		reg = re.compile(r'(.*)-(.*)',re.I)
		match = reg.match(msg)
		if match:
			souname = match.group(1)
			msg = match.group(2)
			CLINET_MAP[souname] = addr[1]
		else:
			souname='system'
			msg='未接受到消息'
		
		if msg == 'quit':break
		c.send('这是来自服务器的测试消息'.encode('utf-8'))
		#counter -= 1
		#c.close()
	#s.close()"""

def runserve(s,msg,reg):
	while True:
		c, addr = s.accept()     # 建立客户端连接。
		#print ('连接地址：', addr)
		#print("client",c)
		CONN_POOL.append(c)
		 # 给每个客户端创建一个独立的线程进行管理
		thread = threading.Thread(target=message_handle, args=(c,))
		# 设置成守护线程
		thread.setDaemon(True)
		thread.start()

def message_handle(client):

	flag = client.sendall("Connection Success!".encode('utf8'))

	while True:
		try:
			msg = client.recv(4096).decode('utf8')	
			match = REG.match(msg)
			if match:
				desname = match.group(1)
				msg = match.group(2)
				souname = match.group(3)
				#zhuce yonghu

				CLINET_MAP[souname] = client

				#print("&&&&&&  user",CLINET_MAP)
			else:
				desname='system'
				msg='未接受到消息'
				souname = "unknown"
			print("需要发送给 %s 的客户端消息(来自用户 %s ): %s" % (desname,souname,msg))
			if len(msg) == 0:
				CONN_POOL.remove(client)
				LOCK.acquire()
				del CLINET_MAP[souname]
				LOCK.release()
				client.close()
				# 删除连接
				print("%s 下线了。" % souname)
				break
			if desname not in CLINET_MAP:
				#暂定 需要修改
				print("---------------- %s offline --------------" % (desname))
				LOCK.acquire()
				#print('desname not in TMP_MSG-----',desname not in TMP_MSG)
				if desname not in TMP_MSG:
					TMP_MSG[desname] = ''
				TMP_MSG[desname] += msg + ','
				LOCK.release()
				#print("TMP_MSG````````",TMP_MSG)
			else:
				print("----------------ready send Message---------------",msg)
				sendMsg(CLINET_MAP[desname],souname,'',msg)
				print("----------------send Message ok----------------")
		except Exception as e:
			print("Something error")
			del CLINET_MAP[souname]
			CONN_POOL.remove(client)
			sys.exit()
		except ConnectionResetError as e:
			print('用户异常掉线')
			sys.exit()
		else:
			pass
		finally:
			pass

def listenClient():
	print('start to listen client status...')
	while True:
		#字典在遍历时不能做CRUD操作
		for cliname in list(TMP_MSG.keys()):
			"""print('keys-------',list(TMP_MSG.keys()))
			print('cliname--------',cliname)
			print('CLINET_MAP------',CLINET_MAP)
			print(cliname in CLINET_MAP)"""
			if cliname in CLINET_MAP:
				print('user:%s online'% cliname)
				for m in TMP_MSG[cliname].split(','):
					try:
						#print("")
						CLINET_MAP[cliname].sendall(m.encode('utf-8'))
						#print("")
					except Exception as e:
						raise
					else:
						pass
					finally:
						pass
				LOCKC.acquire()
				del TMP_MSG[cliname]
				LOCKC.release()


class mysocketClient():
	souname="myclient"
	desname=""
	msg="今天天气不错"
	s=socket.socket(
		    socket.AF_INET, socket.SOCK_STREAM)          
	def __init__(self,souname , desname,msg):
		#threading.Thread.__init__(self)
		self.souname = souname
		self.desname = desname
		self.msg = msg
		try:
			self.s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1) #在客户端开启心跳维护
			self.s.connect((HOST,12345))
			sendMsg(self.s,"client_init",souname,"Hello MSQ")
		except Exception as e:
			print('网络错误！！')
			sys.exit()
		else:
			pass
		finally:
			pass
		
		"""if souname not in CLINET_MAP:
			CLINET_MAP[souname] = 0"""
	
	def sendM(self):
		#创建线程并且循环等待所接收消息
		thread = threading.Thread(target=recvMsg, args=(self.s,))

		thread.setDaemon(True)
		thread.start()
		while True:
			a = input()
			self.msg = a
			#print(self.s)
			sendMsg(self.s,self.desname,self.souname, self.msg)
			if a == 'quit':
				self.s.close()
				break
		#self.s.close()				

def sendMsg(socket,desname,souname,msg):
	msg = desname + '-' + msg + '-' + souname
	print("准备发送消息..." + msg)
	try:
		socket.sendall(msg.encode('utf-8'))
		
	except Exception as e:
		print("Something error perhaps connection aborted")
		#del CLINET_MAP[souname]
		#print(e)
		sys.exit()
	except ConnectionResetError as e:
		print('用户异常掉线')
	except:
		print("unexcepted error")
	else:
		print("send Message OK")
	finally:
		pass

def recvMsg(socket):
	while True:
		try:
			msg = socket.recv(4096).decode('utf-8')
		except Exception as e:
			print('receive Message error')
			sys.exit()
		else:
			match = REG.match(msg)
			if match:
				souname = match.group(1)
				msg = match.group(2)
				print("*********************************")
				print("消息来自 %s : \r\n %s" % (souname,msg))
				print("*********************************")
			elif msg == 'Connection Success!':
				print(msg)
			elif msg:
				print('=====================')
				print(msg)
		finally:
			pass
		
		