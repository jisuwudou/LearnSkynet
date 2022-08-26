import pygame
from threading import Thread
from draw import InputBox
from draw import ButtonImage
import C_Websocket as wb

from pygame.sprite import Sprite,Group

from enum import Enum #枚举

class GAME_STATUS(Enum):
	LOGIN= 1

class EWIN(Enum):
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
	pass

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
class Win_Mgr():
	# _instance = None
	_winCls = {}
	_winList = {}

	_textNumber = 0

	def __init__(self):
		self._winCls[EWIN.LOGIN] = Win_Login
		self._winCls[EWIN.FIND_ROOM] = Win_FindRoom

	def ShowWin(self,ewin):
		if self._winList.get(ewin) is None:
			self._winList[ewin] = self._winCls.get(ewin)()
			print("Showwin ", ewin, self._winList[ewin])

		needDel = []
		for e in self._winList:
			if e != ewin:
				self._winList[e].Kill()
				# self._winList.pop(e)
				needDel.append(e)
				# break#目前默认只有一个弹窗

		for e in needDel:
			self._winList.pop(e)
			print("DELETEWIN", e)

	def Update(self,window):
		for ewin in self._winList:
			self._winList[ewin].update()
			self._winList[ewin].draw(window)

	def dealEvent(self,event):
		for ewin in self._winList:
			self._winList[ewin].dealEvent(event)

class Win_FindRoom(WinBase):
	# group1 = pygame.sprite.Group()
	findRandRoomBtn=None

	def __init__(self):
		super().__init__()
		# print("find room ")
		self.findRandRoomBtn = ButtonImage("find.png", 200,400,1)
		self.add(self.findRandRoomBtn)

	#override
	def draw(self,window):
		super().draw(window)
		# self.findRandRoomBtn.drawText(window)


	

###登录界面####
class Win_Login(WinBase):
	# spriteGrp = pygame.sprite.Group()
	# sureBtn = None
	def __init__(self):
		super().__init__()
		self.userInput = InputBox()
		self.sureBtn = ButtonImage("btnSure.png", 200,200,1)
		self.sureBtn.mousedownEvt = self.OnSureBtnDown

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

	def OnSureBtnDown(self):
		print("OnSureBtnDown", self.userInput.text)
		self.Login(self.userInput.text)

	def Login(self,user):
		self.userinfo = {"user":user,"srv":"cocos1"}
		self.loginDone = wb.socket_client(self.userinfo)
		# print("=======login ====",self.loginDone)

		Win_Mgr().ShowWin(EWIN.FIND_ROOM)



class MainLogic:

	loginDone = False
	userinfo = None
	gamestatus = {
		"Running",
		"Login"
	}

	
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
		
		win_mgr = Win_Mgr()
		win_mgr.ShowWin(EWIN.LOGIN)

		while True:
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					wb.close()
					raise SystemExit
				# win_login.dealEvent(event)
				
				win_mgr.dealEvent(event)
			
			win_mgr.Update(window)
			# window.clear()
			# pygame.display.flip()
			pygame.display.update()




if __name__ == "__main__":

	thread = Thread(target=NetworkData)       #发送数据后，就进行接收数据的循环线程中
	thread.daemon = True
	thread.start()  #启动线程

	mainLogic = MainLogic()
	mainLogic.LogicRun()