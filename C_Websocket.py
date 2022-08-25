
import socket
import sys
import os
import base64 
import struct

loginSocket=None
requestSocket=None


#登录请求
def SendLogin(user,srvid, password):
    global loginSocket
    user = base64.b64encode(str(user).encode())
    srvid = base64.b64encode(str(srvid).encode())
    password = base64.b64encode(str(password).encode())

    ##格式：   user账号名@srvid服务器名称:密码password

    ret = str(user)[2:-1] + "@" + str(srvid)[2:-1] + ":" + str(password)[2:-1] + "\n"
    print(ret)
    loginSocket.send(ret.encode())

#握手，建立连接
def Handshake(user,srvid, subid, index):
    global requestSocket
    user = base64.b64encode(str(user).encode()).decode('utf-8')#decode('utf-8')为了去掉python字符串的 b 前缀
    srvid = base64.b64encode(str(srvid).encode()).decode('utf-8')
    subid = base64.b64encode(str(subid).encode()).decode('utf-8')
    # index = str(index)encode().decode('utf-8')#base64.b64encode(str(index).encode()).decode('utf-8')

    ret = str(user) + "@" + str(srvid) + "#" + str(subid) + ":" + str(index)

    secret = "123".encode()
    secret = ":"+base64.b64encode(secret).decode('utf-8')
    ret+=secret
    ret = ret.encode()
    slen = len(ret)


    print("Handshake ",ret)

    fmt = ">H"+str(slen)+"s"
    ret = struct.pack(fmt,slen, ret)
    # return ret.encode()
    requestSocket.send(ret)

#向服务端发送数据
def Send_request(v, session):
    global requestSocket
    v = str(v)
    size = len(v) + 4
    print("Send_request len=", size, v, session, struct.calcsize(">i"))
    # package = struct.pack(">H", size) + v.encode() + struct.pack(">i", session)
    package = struct.pack(">H", size) + v.encode() + struct.pack(">i", session)
    requestSocket.send(package)

def Send_package(value):
    global requestSocket

    blen = len(value)
    # if "str" == type(value):
    #     len = len(value)
    
    fmt = ">H"+str(blen)+"s"
    pack = struct.pack( fmt, blen, value.encode())
    print("Send_package ", fmt, struct.unpack(fmt, pack))
    requestSocket.send(pack)

def Unpack_package(value):
    blen = len(value)
    if blen < 2:
        print("Unpack_package header too short", blen, value)
        return

    print("Unpack_package ", value, blen, value[0:2], type(value[0]), value[1])
    headerLen = value[0]*256 + value[1]
    if headerLen <= 0:
        print("Unpack_package headerLen too small", headerLen, value[0:2])
        return    


    info = value[2:].decode()
    print("Unpack_package ",headerLen, info)
    # fmt = ">H" + str(headerLen) + "s"
    # uppackRet = struct.unpack(fmt, )
    return info.split(" ")


def close():
    global loginSocket,requestSocket
    if loginSocket:
        loginSocket.close()
    if requestSocket:
        requestSocket.close()


def socket_client(userinfo):
    ##开始登录##
    global loginSocket
    try:
        loginSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        loginSocket.connect(('101.33.201.116', 9947))
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    firstRecv = loginSocket.recv(1024)
    deFirstRecv = base64.b64decode(firstRecv)
    print(firstRecv, deFirstRecv)#目的在于接受：Accept new connection from (...

    
    SendLogin(userinfo.get("user"), userinfo.get("srv"), 123)


    # loginSocket.send(loginData)
    ##服务端返回的登录结果，如果成功就一起返回 subId
    loginRet = (loginSocket.recv(1024))
    loginRet = loginRet.decode('utf-8')
    print(loginRet)
    loginCode = (loginRet.split(" ")[0])
    subId = loginRet.split(" ")[1]
    subId = base64.b64decode(subId).decode('utf-8')
    print('loginRet=',loginRet, loginCode, subId,type(subId))
    ##关闭登录连接##
    loginSocket.close()
    if loginCode == '200':#账号登录成功
        print("===============LOGIN SUCCESS!!!!=======================")
    else:
        print("================LOGIN ERROR !!!!==============,loginCode")
        
        return
    #已完成登录请求#

    ########################### 建立连接  ###################################
    global requestSocket
    try:
        requestSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        requestSocket.connect(('101.33.201.116', 9948))
    except socket.error as msg:
        print("!!!connect requestSocket ",msg)
        sys.exit(1)

    index = 1
    ##握手阶段
    handshake = Handshake(userinfo.get("user"), userinfo.get("srv"),subId, index)
    handshakeret = requestSocket.recv(1024)

    print("handshakeret ",handshakeret)

    retCode,retInfo = Unpack_package(handshakeret)
    if int(retCode) == 200:
        print("============hand shake SUCCESS !!!!=============")
        return True
    else:
        print("============hand shake ERR !!!", retCode, retInfo)
        requestSocket.close()
        return False


    # handshakeretLen = struct.unpack(">H", handshakeret)
    # print("handshakeretLen ", handshakeretLen)

    # Send_request("echo", 0)

    # Send_package("clientsendpackage")

    # while 1:
    #     number = input('please input number with(BYTE:0-255): ')

    #     if number == 'exit':
    #         break

    #     number = int(number)
        
    #     print(number,type(number))
        
    #     # Send_request("echo", 0)
    #     Send_request(number, 0)

        
        
    #     # os.system("pause")
    #测试 断线重连
    # requestSocket.close()

    # try:
    #     requestSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     requestSocket.connect(('101.33.201.116', 9948))
    # except socket.error as msg:
    #     print("!!!connect requestSocket ",msg)
    #     sys.exit(1)
 

    
if __name__ == '__main__':
    socket_client()