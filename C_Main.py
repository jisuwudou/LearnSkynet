import pygame
from threading import Thread
from draw import InputBox
from draw import ButtonImage
import C_Websocket as ws
import time
from pygame.sprite import Sprite,Group

from enum import Enum #枚举
import  Manager.Event_Mgr as EvtMgr
import define.LogicCmd

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


def Singleton(cls):
	_instance={}
	def _singleton(*args,**kwagrs):
		if cls not in  _instance:
			_instance[cls]=cls(*args,**kwagrs)
		return _instance[cls]
	return _singleton


class WinBase(Group):

	def __init__(self):
		super().__init__();

	def Kill(self):
		for sprite in self.sprites():
			sprite.kill()
			print("sprite kill ", sprite)

	def dealEvent(self,event):
		for sprite in self.sprites():
			if sprite.dealEvent:
				sprite.dealEvent(event)


def NetworkData():
	# pass
	while True:
		time.sleep(2)
		data = ws.GetSrvData()
		print("Thread Test", data)
		# ret = ws.GetNetWorkData()
		# print("On Get NetworkData ", ret)


@Singleton
class GAME_CONFIG():
	MaxMember = 2

class Player(Sprite):
	_ID = None
	_name = None
	_lv = None
	_icon = None

	def __init__(self, actorId, name,lv,icon):
		super().__init__()

		self._ID = actorId
		self._name = name
		self._lv = lv
		self._icon = icon

		self.image = pygame.Surface([50,50])
		self.image.fill("black")
		self.rect = self.image.get_rect()

class MainPlayer(Player):
	

	def __init__(self):
		super().__init__()

		self.image.fill("blue")
		

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
		# data = struct.pack(">H")
		# ws.Send_request(123, 0)
		pack = ws.AllocPackage(ESYS.MovementSys, )
		pack.WriteWord(10)
		pack.WriteWord(20)
		ws.Flush()

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

		while True:
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
			
			EvtMgr.GetMgr().Run()

			
			pygame.display.update()


def MainThreadRun():
	mainLogic = MainLogic()
	mainLogic.LogicRun()

if __name__ == "__main__":

	thread = Thread(target=NetworkData)       #发送数据后，就进行接收数据的循环线程中
	thread.daemon = True
	thread.start()  #启动线程

	# thread1 = Thread(target=MainThreadRun)       #发送数据后，就进行接收数据的循环线程中
	# thread1.daemon = True
	# thread1.start()  #启动线程
	mainLogic = MainLogic()
	mainLogic.LogicRun()