# -*- coding: UTF-8 -*-
import socket
import sys
import os
import base64 
import struct
from threading import Thread


loginSocket=None
requestSocket=None
canRecv = False
curPackage = None


class Package():
    pLen = 0
    buffer = bytes()

    def __init__(self, sys, cmd):
        self.pLen += 2
        self.buffer += struct.pack(">BB", sys, cmd)

    def WriteBytes(self,value):
        self.pLen += 1

        if value > 255:
            print("Package WriteBytes too big ", value)
            return False

        self.buffer += struct.pack(">B", value)

    def WriteWord(self,value):
        self.pLen += 2

        if value > 65535:
            print("Package WriteWord too big ", value)
            return False

        # value = str(value)
        self.buffer += struct.pack(">H", value)

        # print("WriteWord ", self.buffer)
    def WriteInt(self,value):
        self.pLen += 4
        self.buffer += struct.pack(">i", value)


    def GetBuffer(self, session):
        
        self.pLen += 4
        # print("GetBuffer len=", self.pLen,self.buffer)
        self.buffer = struct.pack(">H",self.pLen) + self.buffer + struct.pack(">I",session)
        # print(self.buffer)
        # self.buffer = struct.pack(">BBHHI",1,1,10,20,0) 
        # print("Send Data ",self.buffer, struct.unpack(">HBBHHI", self.buffer))
        # b'\x00\x04\x00\n\x00\x14\x00\x00\x00\x00' (4, 10, 20, 0)
        return self.buffer

    

    def Clear(self):

        self.buffer = None
        self.pLen = 0

    def Flush(self,session):
        global requestSocket
        if requestSocket:
            self.buffer = self.GetBuffer(session)
            requestSocket.send(self.buffer)
            self.Clear()
            # curPackage = None
        else:
            print("ERRRRRRRR Flush not requestSocket")

class PackageRead():
    buffer = None
    def __init__(self, data):
        self.buffer = data

    ########## READ ##############
    def ReadInit(self,data):
        self.buffer = data

    def ReadByte(self):
        # ret = struct.unpack(">B", self.buffer[0])
        ret  = self.buffer[0]
        self.buffer = self.buffer[1:]
        return ret

    def ReadWord(self):
        ret = struct.unpack(">H", self.buffer[:2])
        self.buffer = self.buffer[2:]
        return ret[0]

    def ReadUInt(self):
        ret = struct.unpack(">I", self.buffer[:4])
        self.buffer = self.buffer[4:]
        return ret[0]

     ########## READ END##############

def AllocPackage(sys, cmd):
    curPackage = Package(sys, cmd)
    return curPackage


#????????????
def SendLogin(user,srvid, password):
    global loginSocket
    user = base64.b64encode(str(user).encode())
    srvid = base64.b64encode(str(srvid).encode())
    password = base64.b64encode(str(password).encode())

    ##?????????   user?????????@srvid???????????????:??????password

    ret = str(user)[2:-1] + "@" + str(srvid)[2:-1] + ":" + str(password)[2:-1] + "\n"
    print(ret)
    loginSocket.send(ret.encode())

#?????????????????????
def Handshake(user,srvid, subid, index):
    global requestSocket
    user = base64.b64encode(str(user).encode()).decode('utf-8')#decode('utf-8')????????????python???????????? b ??????
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

#????????????????????????
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


# m_session = 0
# def Flush(session):
#     global curPackage
#     if None == curPackage :
#         print("========= ERRRRRRRRRRRRRRRRRRRRR ,flush no package ===============")
#         return None

#     global requestSocket
#     if requestSocket:
#         buffer = curPackage.GetBuffer(session)
#         requestSocket.send(buffer)
#         curPackage.Clear()
#         curPackage = None

        # m_session += 1
        # print(m_session)

def close():
    global loginSocket,requestSocket
    if loginSocket:
        loginSocket.close()
    if requestSocket:
        requestSocket.close()




networkInfoList = []
def GetNetWorkInfo():
    if len(networkInfoList) > 0:
        info = networkInfoList.pop(0)
        return info

def GetSrvData():
    global requestSocket
    while True:
        
        try:
            if requestSocket :
                data = requestSocket.recv(1024)
                
                networkInfoList.append(data)   
                        

                # waitingDatas.add(data)
                
        except Exception as e:
            raise e
    


def socket_client(userinfo):
    ##????????????##
    global loginSocket
    try:
        loginSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        loginSocket.connect(('101.33.201.116', 9947))
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    firstRecv = loginSocket.recv(1024)
    deFirstRecv = base64.b64decode(firstRecv)
    print(firstRecv, deFirstRecv)#?????????????????????Accept new connection from (...

    
    SendLogin(userinfo.get("user"), userinfo.get("srv"), 123)


    # loginSocket.send(loginData)
    ##???????????????????????????????????????????????????????????? subId
    loginRet = (loginSocket.recv(1024))
    loginRet = loginRet.decode('utf-8')
    print(loginRet)
    loginCode = (loginRet.split(" ")[0])
    
    ##??????????????????##
    loginSocket.close()
    if loginCode == '200':#??????????????????
        print("===============LOGIN SUCCESS!!!!=======================")
    else:
        print("================LOGIN ERROR !!!!==============,loginCode")
        
        return

    subId = loginRet.split(" ")[1]
    subId = base64.b64decode(subId).decode('utf-8')
    print('loginRet=',loginRet, loginCode, subId,type(subId))

    #?????????????????????#

    ########################### ????????????  ###################################
    global requestSocket
    try:
        requestSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # requestSocket.setblocking(True)
        requestSocket.connect(('101.33.201.116', 9948))
    except socket.error as msg:
        print("!!!connect requestSocket ",msg)
        sys.exit(1)

    index = 1
    ##????????????
    handshake = Handshake(userinfo.get("user"), userinfo.get("srv"),subId, index)
    handshakeret = requestSocket.recv(1024)

    print("handshakeret ",handshakeret)

    retCode,retInfo = Unpack_package(handshakeret)
    if int(retCode) == 200:
        print("============hand shake SUCCESS !!!!=============")
        # return True
    else:
        print("============hand shake ERR !!!", retCode, retInfo)
        requestSocket.close()
        return False

    # pack = ws.AllocPackage(1,2)#ESYS.MovementSys, )
    # pack.WriteWord(5)#?????????
    # pack.Flush(1)#??????????????????

    canRecv = True
    print("")
    thread = Thread(target=GetSrvData)       #?????????????????????????????????????????????????????????
    thread.daemon = True
    thread.start()  #????????????

    return True
    

        
        
    #     # os.system("pause")
    #?????? ????????????
    # requestSocket.close()

    # try:
    #     requestSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     requestSocket.connect(('101.33.201.116', 9948))
    # except socket.error as msg:
    #     print("!!!connect requestSocket ",msg)
    #     sys.exit(1)
 

    
# if __name__ == '__main__':
#     socket_client()