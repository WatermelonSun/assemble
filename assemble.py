# -*- coding:utf-8 -*-
import psutil
import paramiko
import os,sys
import time

def select_nod():
	#打开系统资源使用情况获取文件
	f=open('detail_info.txt','r')
	line = f.read()
	#gpu="nvidia-smi"
	#创建实体
	con1=paramiko.Transport(("workstation1 ip", 22))
	con2=paramiko.Transport(("workstation2 ip", 22))
	#con1建立连接 
	con1.connect(username='***',password='***')
	ssh = paramiko.SSHClient()
	ssh._transport = con1
	sftp = paramiko.SFTPClient.from_transport(con1)  #使用trans的设置方式连接远程主机
	
	#处理和执行文件
	stdin,stdout,stderr = ssh.exec_command(line)

	time.sleep(3)
	sftp.get('/home/sxx/result.txt',"sys_status1.txt")

	# 关闭连接
	con1.close()

	#con2建立连接
	con2.connect(username='***',password='***')
	ssh = paramiko.SSHClient()
	ssh._transport = con2
	sftp = paramiko.SFTPClient.from_transport(con2)  #使用trans的设置方式连接远程主机

	#处理和执行文件
	stdin,stdout,stderr = ssh.exec_command(line)

	time.sleep(3)
	sftp.get('/home/sxx/result.txt',"sys_status2.txt")

	# 关闭连接
	con2.close()
	f.close()

	#比较系统资源
	count=0
	cot1=[]
	cot2=[]
	j=[]
	contents1={}
	contents2={}

	f1=open('sys_status1.txt','r')
	content1=f1.read()
	#print content1############################
	content1=content1.strip("{}\n")
	cot1=content1.split(',')
	for i in cot1:
		j=i.split(':')
		contents1[j[0]]=j[1]
	#print contents1
	f2=open('sys_status2.txt','r')
	content2=f2.read()	
	#print content2###################
	content2=content2.strip('{}\n')
	cot2=content2.split(',')
	for i in cot2:
		j=i.split(':')
		contents2[j[0]]=j[1]
	#print contents2


	if float(contents1[" 'mem_usage'"])>float(contents2[" 'mem_usage'"]):
		count=count+1
	else:
		count=count-1
	if float(contents1[" 'cpu_usage'"])>float(contents2[" 'cpu_usage'"]):
		count=count+1
	else:
		count=count-1
	if long(contents1[" 'mem_free'"])<long(contents2[" 'mem_free'"]):
		count=count+1
	else:
		count=count-1
	if float(contents1[" 'Free'"])<float(contents2[" 'Free'"]):
		count=count+1
	else:
		count=count-1
	if float(contents1["'disk_usage'"])>float(contents2["'disk_usage'"]):
		count=count+1
	else:
		count=count-1
	if count>0:
		return "workstation2"
	elif count<0:
		return "workstation1"
		

def trans_doc(filename):
	#将文件传入到执行文件的工作站
	#工作站地址
	addr=select_nod()
	base_dir=os.getcwd()
	#
	trans = paramiko.Transport((addr, 22))
    #建立连接 
	trans.connect(username='***',password='***')
	ssh = paramiko.SSHClient()
	ssh._transport = trans
	sftp = paramiko.SFTPClient.from_transport(trans)
	files = os.listdir(base_dir+'/'+filename)  # 上传多个文件
	for f in files:
		sftp.put(os.path.join(base_dir+'/'+filename, f), "/home/sxx" + '/' + f)  # 上传多个文件

	trans.close()    	

def tel_exec(name,parameter,output):
	#选择连接的工作站
	addr=select_nod()
	print "使用的工作站地址为：",addr
	trans = paramiko.Transport((addr, 22))
	#建立连接 
	trans.connect(username='***',password='***')
	ssh = paramiko.SSHClient()
	ssh._transport = trans
	sftp = paramiko.SFTPClient.from_transport(trans)  #使用trans的设置方式连接远程主机
	
	#判断文件是否存在
	if os.path.exists(name):
		# 
		lines="python3 "+name+" "+parameter

		#处理和执行文件
		stdin,stdout,stderr = ssh.exec_command(lines)
		#print stdout.read()

		#执行文件输出结果存入指定文件
		f=open(output,'w')
		f.write(stdout.read())
		f.close()
	
	# 关闭连接

	trans.close()


if __name__ == '__main__':
	filename=raw_input("输入执行依赖文件夹名：")
	trans_doc(filename)
	tel_exec(sys.argv[1],sys.argv[2],sys.argv[3])
