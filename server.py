import socket
import struct
import json
import os

BUFFER_SIZE=1024#分段传输文件时没段的最大长度



def server():
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#创建TCPsocket
    host = "192.168.247.128"#输入server 的ip地址
    port=9999
    sock.bind((host,port))#将socket绑定到制定地址
    sock.listen(1)#开始监听TCP传入连接

    while True:
        try:
            connection,address=sock.accept()#得到client的socket和ip
            print('会话开始！客户地址：{},等待客户信息...'.format(address))
            buf=''.encode('utf-8')
            while buf.decode('utf-8')!='bye':
                buf=connection.recv(BUFFER_SIZE)#接收来自client的信息

                #当接收到结束会话信息时
                if buf.decode('utf-8')=='bye':
                    print('client:{}'.format(buf.decode('utf-8')))
                    print('会话结束!')
                    break#跳出当前循环

                #当接收到client发送文件给server信息时
                elif buf.decode('utf-8')=='send_file':
                    print('client:{}'.format(buf.decode('utf-8')))
                    file_info_len=connection.recv(4)#接收文件信息的长度
                    if file_info_len:
                        print('正在接收文件...')
                    info_len=struct.unpack('i',file_info_len)[0]
                    file_info=connection.recv(info_len)#利用文件信息长度得到文件文件信息
                    info=json.loads(file_info.decode('utf-8'))
                    file_size=info['file_size']#文件大小
                    file_name=info['file_name']#文件名
                    file_name_new=input('请输入存储文件的文件夹路径（eg.\'/home/\'）：')+file_name
                    recved_len=0#已接收的文件大小
                    recv_data=b''
                    #开始接收文件
                    with open(file_name_new,'wb') as f:
                        while recved_len<file_size:
                            recv_len=BUFFER_SIZE if file_size-recved_len>BUFFER_SIZE else file_size-recved_len#选择此次分段接收文件的大小
                            recv_data=connection.recv(recv_len)
                            f.write(recv_data)#将文件写入指定位置
                            recved_len+=recv_len
                    print('文件接收完成！')
                    msg="已成功接收!"
                    connection.send(msg.encode('utf-8'))

                #当接收到client请求server的文件信息时
                elif buf.decode('utf-8')=='recv_file':
                    print('client:{}'.format(buf.decode('utf-8')))
                    file_name=connection.recv(BUFFER_SIZE).decode('utf-8')#接收要发送的文件路径
                    file_size = os.path.getsize(file_name)#文件大小
                    file_name_new = file_name.split('/')[-1]#文件名
                    info = {
                        'file_name': file_name_new,
                        'file_size': file_size,
                    }#文件信息
                    file_info = json.dumps(info)
                    file_info_len = struct.pack('i', len(file_info))#文件信息的字符串长度
                    connection.send(file_info_len)
                    connection.send(file_info.encode('utf-8'))#将文件信息发送给client
                    #将文件发送给client
                    with open(file_name, 'rb') as f:
                        data = f.read()
                        connection.sendall(data)
                    print('文件已发送')
                    buf = connection.recv(BUFFER_SIZE)
                    print('server:{}'.format(buf.decode('utf-8')))

                #当接收到普通字符串信息时
                else:
                    print('client:{}'.format(buf.decode('utf-8')))#输出信息
                    msg=input("You(server)：")
                    connection.send(msg.encode('utf-8'))#向client发送信息
        #异常处理，显示错误类型
        except socket.error as e:
            print('socket error:',str(e))
        finally:
            #断开连接
            connection.send('bye'.encode('utf-8'))
            connection.close()
            if_close_server = input('是否关闭服务器？(Y/N):')
            if if_close_server == 'Y':
                break
    sock.close()


if __name__=='__main__':
    server()