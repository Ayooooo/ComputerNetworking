import socket
import os
import struct
import json

BUFFER_SIZE=1024 #分段传输文件时一次最大传输量

def Client():
    try:
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host="192.168.247.128" #输入server的ip地址
        port = 9999
        sock.connect((host, port))#向server服务器发送连接请求
        print('会话开始！如需结束对话请回复\'bye\',如需传输文件请输入\'send_file\',如需接收文件请输入\'recv_file\'')
        buf = ''.encode('utf-8')#接收到的字符串数据
        while buf.decode('utf-8')!='bye':
            msg = input("You(client)：")
            sock.send(msg.encode('utf-8'))
            #当发送send_file字符串时，表明要向server发送文件。
            if msg=='send_file':
                file_name=input("send_file:")#要发送文件的路径
                file_name_new=file_name.split('\\')[-1]#要发送的文件名
                file_size=os.path.getsize(file_name)#要发送的文件大小
                info={
                    'file_name':file_name_new,
                    'file_size': file_size,
                }#要发送的文件信息
                file_info=json.dumps(info)
                file_info_len=struct.pack('i',len(file_info))
                sock.send(file_info_len)
                sock.send(file_info.encode('utf-8'))#向server发送文件信息
                #发送文件内容
                with open(file_name,'rb') as f:
                    data=f.read()
                    sock.sendall(data)
                print('文件已发送')
                buf=sock.recv(BUFFER_SIZE)
                print('server:{}'.format(buf.decode('utf-8')))
            #当发送recv_file字符串时，表明要从server接收文件
            elif msg=='recv_file':
                msg = input("recv_file:")#要接收的文件路径
                sock.send(msg.encode('utf-8'))
                file_info_len = sock.recv(4)
                if file_info_len:
                    print('正在接收文件...')
                info_len = struct.unpack('i', file_info_len)[0]
                file_info = sock.recv(info_len)#接收文件信息
                info = json.loads(file_info.decode('utf-8'))
                file_size = info['file_size']#文件大小
                file_name = info['file_name']#文件名
                file_name_new = input('请输入将接收文件存储位置（eg.\'f：\\file\\\'）：') + file_name
                recved_len = 0#已接受的文件大小
                recv_data = b''
                #接收文件，并放入指定位置
                with open(file_name_new, 'wb') as f:
                    while recved_len < file_size:
                        recv_len = BUFFER_SIZE if file_size - recved_len > BUFFER_SIZE else file_size - recved_len#本次分段接收数据的大小
                        recv_data = sock.recv(recv_len)
                        f.write(recv_data)
                        recved_len += recv_len
                print('文件接收完成！')
                msg = "已成功接收!"
                sock.send(msg.encode('utf-8'))
            #发送普通字符串信息时
            else:
                buf=sock.recv(BUFFER_SIZE)
                print('server:{}'.format(buf.decode('utf-8')))
        print('会话结束!')
    # 当try中运行错误时跳入except，显示为错误原因
    except socket.error as e:
        print('socket error:',str(e))
    finally:
        sock.close()#关闭socket


if __name__=='__main__':
    Client()