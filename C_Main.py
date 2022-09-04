import pygame

from draw import InputBox
from draw import ButtonImage
import C_Websocket as ws
import time
from pygame.sprite import Sprite,Group

from enum import Enum #枚举
import  Manager.Event_Mgr as EvtMgr
import define.LogicCmd

def Singleton(cls):
	_instance={}
	def _singleton(*args,**kwagrs):
		if cls not in  _instance:
			_instance[cls]=cls(*args,**kwagrs)
		return _instance[cls]
	return _singleton

class EGAME_STATUS(Enum):
	INIT = 0
	REQ_LOGIN= 1
	PLAYING = 2

class EWIN(Enum):
	BACKGOURND = 0
	LOGIN = 1#登录界面
	FIND_ROOM = 2


class EROOM_STATUS(Enum):
	WAITING = 1#等待开局
	PLAYING = 2#游戏中


GAME_CONFIG = {
	'MaxMember': 2,
	'HEIGHT': 200,
	'WIDTH': 400,

}


# 添加系统时钟，用于设置帧的刷新
FPS = 40
clock = pygame.time.Clock()


class WinBase(Group):

	def __init__(self):
		super().__init__();

	def Kill(self):
		for sprite in self.sprites():
			sprite.kill()
			# print("sprite kill ", sprite)

	def dealEvent(self,event):
		for sprite in self.sprites():
			if sprite.dealEvent:
				sprite.dealEvent(event)



class Player(Sprite):
	speed = 2
	playerIdx=None# 在房间里的编号
	_name = None
	_lv = None
	_icon = None

	def __init__(self, playerIdx, name,lv,icon):
		super().__init__()

		self.playerIdx = playerIdx
		self._name = name
		self._lv = lv
		self._icon = icon

		self.image = pygame.Surface([50,50])
		self.image.fill("black")
		self.rect = self.image.get_rect()

	#根据服务端按键信息，执行操作
	def updatekeybroad(self,newkeybroadList):
		# print("update key ", newkeybroadList)

		player1 = newkeybroadList

		if player1 >> 1 & 1:
			self.rect.y -= self.speed
		if player1 >> 2 & 1:
			self.rect.y += self.speed
		if player1 >> 3 & 1:
			self.rect.x -= self.speed
		if player1 >> 4 & 1:
			self.rect.x += self.speed


		if self.rect.x < 0:
		    self.rect.x = 0
		if self.rect.y < 0:
		    self.rect.y = 0
		if self.rect.y > GAME_CONFIG['HEIGHT'] - self.rect.height:
		    self.rect.y = GAME_CONFIG['HEIGHT'] - self.rect.height

# print("keyxxxxxxxx ", pygame.K_UP)
class MainPlayer(Player):
	
	
	lastX=0
	lastY=0
	
	def __init__(self,subRoomIdx, name,lv,icon):
		super().__init__(subRoomIdx, name,lv,icon)

		self.image.fill("blue")
		self.lastX = self.rect.x
		self.lastY = self.rect.y
		

	def update(self, *args):
		keys = pygame.key.get_pressed()
		# print("KeyDown ", type(keys), keys)
		# if keys[pygame.K_UP]:
		#     self.rect.y -= self.speed
		# if keys[pygame.K_DOWN]:
		#     self.rect.y += self.speed
		# if keys[pygame.K_LEFT]:
		#     self.rect.x -= self.speed
		# if keys[pygame.K_RIGHT]:
		#     self.rect.x += self.speed
		# if keys[pygame.K_SPACE]:
		#     if self.ready_to_fire == 0:
		#         self.fire()
		#     self.ready_to_fire += 1
		#     if self.ready_to_fire > 5:
		#         self.ready_to_fire = 0
		# else:
		#     self.ready_to_fire = 0
		# if self.rect.x < 0:
		#     self.rect.x = 0
		# if self.rect.y < 0:
		#     self.rect.y = 0
		# if self.rect.y > GAME_CONFIG['HEIGHT'] - self.rect.height:
		#     self.rect.y = GAME_CONFIG['HEIGHT'] - self.rect.height
		
		# if self.lastX != self.rect.x or self.lastY != self.rect.y:
		# 	self.lastX = self.rect.x
		# 	self.lastY = self.rect.y

		commitkye=0
		if keys[pygame.K_UP]:
		    # self.rect.y -= self.speed
		    commitkye |= (1 << 1)
		if keys[pygame.K_DOWN]:
		    # self.rect.y += self.speed
		    commitkye |= (1 << 2)
		if keys[pygame.K_LEFT]:
			commitkye |= (1 << 3)
		    # self.rect.x -= self.speed
		if keys[pygame.K_RIGHT]:
			commitkye |= (1 << 4)
		    # self.rect.x += self.speed

		if commitkye > 0:
			# print("commitkye ",commitkye)
			pack = ws.AllocPackage(1,2)#提交按键状态
			pack.WriteInt(commitkye)
			pack.Flush(0)


class Room():
	_number = None
	_members = None
	_status = None
	_maxMember = None
	def __init__(self, number):
		_number = number
		_members = []
		_status = EROOM_STATUS.WAITING

		_maxMember = GAME_CONFIG().MaxMember

	def AddMember(self, player:Player):
		count = len(self._members)
		if count >= _maxMember:
			return False


@Singleton
class Room_Mgr():
	_RoomList = []
	def __init__(self):
		print("INIT Fuben_Mgr")


@Singleton
class Game_Mgr():
	_gameStatus = EGAME_STATUS.INIT

@Singleton
class Win_Mgr():
	# _instance = None
	_winCls = {}
	_winList = {}
	_staticWinList={}
	_textNumber = 0

	def __init__(self):
		self._winCls[EWIN.LOGIN] = Win_Login
		self._winCls[EWIN.FIND_ROOM] = Win_FindRoom
		# self._winCls[EWIN.BACKGOURND] = BackGround



	def ShowWin(self,ewin):
		if self._winList.get(ewin) is None:
			self._winList[ewin] = self._winCls.get(ewin)()
			print("Showwin ", ewin, self._winList[ewin])

		needDel = []
		for e in self._winList:
			if e != ewin:
				self._winList[e].Kill()
				needDel.append(e)
				# break#目前默认只有一个弹窗

		for e in needDel:
			self._winList.pop(e)
			print("DELETEWIN", e)

	# def ShowWinStatic(self,ewin):
	# 	if self._staticWinList.get(ewin) is None:
	# 		self._staticWinList[ewin] = self._winCls.get(ewin)()

	def Update(self,window):

		# for win in self._staticWinList.values():
		# 	win.update()
		# 	win.draw(window)

		for ewin in self._winList:
			self._winList[ewin].update()
			self._winList[ewin].draw(window)



	def dealEvent(self,event):
		for win in self._winList.values():
			# print(len(self._winList))
			win.dealEvent(event)


class Win_FindRoom(WinBase):
	# group1 = pygame.sprite.Group()
	findRandRoomBtn=None

	def __init__(self):
		super().__init__()
		# print("find room ")
		self.findRandRoomBtn = ButtonImage("find.png", 200,400,1)
		self.add(self.findRandRoomBtn)

		EvtMgr.GetMgr().AddEvent(self.findRandRoomBtn, self.enterRoom)

	#override
	def draw(self,window):
		super().draw(window)
		# self.findRandRoomBtn.drawText(window)

	def enterRoom(self,btn):
		print("BTN enterroom ", self,btn)
		
		pack = ws.AllocPackage(1,1)#进入房间
		pack.WriteWord(10)
		# pack.WriteWord(self.lastY)
		pack.Flush(0)


		

###登录界面####
class Win_Login(WinBase):

	def __init__(self):
		super().__init__()
		self.userInput = InputBox()
		self.sureBtn = ButtonImage("btnSure.png", 200,200,1)
		# self.sureBtn.mousedownEvt = self.OnSureBtnDown
		EvtMgr.GetMgr().AddEvent(self.sureBtn, self.OnSureBtnDown)

		s = Sprite()
		# 创建一个图块并填色，或加载image
		s.image = pygame.Surface([33, 33])
		s.image.fill("yellow")
		s.rect = s.image.get_rect()
		
		self.add(self.userInput)
		self.add(self.sureBtn)

	#override
	def draw(self,window):
		super().draw(window)
		self.userInput.drawText(window)

	def OnSureBtnDown(self, btn):
		print("OnSureBtnDown", self.userInput.text)
		self.Login(self.userInput.text)

	def Login(self,user):
		self.userinfo = {"user":user,"srv":"cocos1"}
		Game_Mgr()._gameStatus = EGAME_STATUS.REQ_LOGIN
		self.loginDone = ws.socket_client(self.userinfo)
		# print("=======login ====",self.loginDone)
		if self.loginDone:
			Game_Mgr()._gameStatus = EGAME_STATUS.PLAYING
			Win_Mgr().ShowWin(EWIN.FIND_ROOM)
		else:
			Game_Mgr()._gameStatus = EGAME_STATUS.INIT
		
class BackGround(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('./res/background.png')
        self.rect = self.image.get_rect()
        self.ready_to_move = 0

    def update(self, *args):
        self.rect.x -= 0
        if self.rect.right <= 0:
            self.rect.x = self.rect.width


    def draw(self, window):
    	super().draw(window)

#### 处理收到的网络消息 #####
def HandleNetWorkData():
	data = ws.GetNetWorkInfo()
	if not data:
		return


	global m_heroGroup,m_playerList,m_mplayer

	readCls = ws.PackageRead(data)
	readCls.ReadWord()#舍弃
	systemId = readCls.ReadByte()
	cmd = readCls.ReadByte()
	print("HandleNetWorkData ", systemId, cmd)
	if systemId == 1:
		if cmd == 1:#进入房间的结果
			enterRet = readCls.ReadByte()
			roomId = readCls.ReadWord()
			playerIdx = readCls.ReadWord()
			print(enterRet, roomId, playerIdx)
			
			if enterRet == 1:
				print("EnterRoom enterRet=", enterRet, "roomId=",roomId,"playerIdx=", playerIdx)
				
				if m_mplayer :
					print("ERRRRRRRR mainplayer has create")
					return
					
				m_mplayer = MainPlayer(playerIdx, "mainplayer",11,1)
				m_heroGroup.add(m_mplayer)
				m_playerList.append(m_mplayer)

			else:
				print("ERRRRRRR enter room wrong roomId=", roomId)
		elif cmd == 2:# "收到同步按键信息"
			global m_keyboradInfos
			dataLen = readCls.ReadByte()
			
			newKey = {}

			for i in range(dataLen):
				playerIdx = readCls.ReadByte()
				key = readCls.ReadUInt()
				newKey[playerIdx]=key
			if len(newKey) > 0:
			    m_keyboradInfos.append(newKey)

		elif cmd == 3:#出现了其他玩家
			# global m_heroGroup,m_playerList,m_mplayer
			playerIdx = readCls.ReadByte()
			print("Other Player EnterRoom ", playerIdx)
			otherPlayer = Player(playerIdx, "player_"+str(playerIdx),11,1)
			m_heroGroup.add(otherPlayer)
			m_playerList.append(otherPlayer)


m_keyboradInfos = []
def GetNewKeybroad():
	if len(m_keyboradInfos) > 0:
		info = m_keyboradInfos.pop(0)
		return info

m_heroGroup = Group()
m_playerList = []
m_mplayer = None
class MainLogic:
	
	def LogicRun(self):
	
		# 1初始化操作
		pygame.init()
		# 2创建游戏窗口
		# set_mode(大小）
		window = pygame.display.set_mode((400, 600))
		# 设置游戏名
		pygame.display.set_caption('我的游戏')
		# 设置背景颜色
		window.fill((255, 255, 255))

		bgGroup = Group()
		bgGroup.add(BackGround())
		
		win_mgr = Win_Mgr()
		# win_mgr.ShowWinStatic(EWIN.BACKGOURND)
		win_mgr.ShowWin(EWIN.LOGIN)
		global m_heroGroup

		
		
		# testtick = 0
		while True:

			clock.tick(FPS)


			
			window.fill((255, 255, 255))
			if Game_Mgr()._gameStatus == EGAME_STATUS.REQ_LOGIN:
				continue


			win_mgr.Update(window)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					ws.close()
					raise SystemExit
				
				win_mgr.dealEvent(event)
			HandleNetWorkData()
			newkeybroadList = GetNewKeybroad()
			if newkeybroadList:
				for player in m_playerList:
					print("update key player.playerIdx=", player.playerIdx, len(newkeybroadList.keys()))


					value = newkeybroadList.get(player.playerIdx)
					if value:
						player.updatekeybroad(value)
				


			m_heroGroup.update()
			m_heroGroup.draw(window)

			EvtMgr.GetMgr().Run()

			
			pygame.display.update()


def MainThreadRun():
	mainLogic = MainLogic()
	mainLogic.LogicRun()

if __name__ == "__main__":

	

	# thread1 = Thread(target=MainThreadRun)       #发送数据后，就进行接收数据的循环线程中
	# thread1.daemon = True
	# thread1.start()  #启动线程
	mainLogic = MainLogic()
	mainLogic.LogicRun()