import pygame
from threading import Thread
from draw import InputBox
from draw import ButtonImage
import C_Websocket as wb

from pygame.sprite import Sprite,Group

from enum import Enum #枚举

class GAME_STATUS(Enum):
	LOGIN= 1


def NetworkData():
	pass


class Win_FindRoom(pygame.sprite.Sprite):
	group1 = pygame.sprite.Group()
	findRandRoomBtn=None

	def __init__(self):
		print("find room ")

class Win_Login(Group):
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

	def OnSureBtnDown(self):
		print("OnSureBtnDown", self.userInput.text)
		self.Login(self.userInput.text)

	def dealEvent(self,event):
		self.userInput.dealEvent(event)
		self.sureBtn.handle_event(event)

	def Login(self,user):
		self.userinfo = {"user":user,"srv":"cocos1"}
		self.loginDone = wb.socket_client(self.userinfo)
		# print("=======login ====",self.loginDone)

class MainLogic:

	loginDone = False
	userinfo = None
	gamestatus = {
		"Running",
		"Login"
	}

	# findRoomGroup = pygame.sprite.Group()
	# 
	



	
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
		
		win_login = Win_Login()

	
		while True:
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					wb.close()
					raise SystemExit
				win_login.dealEvent(event)
				
				# sureBtn.handle_event(event)
			
			win_login.update()
			win_login.draw(window)
	
			pygame.display.update()




if __name__ == "__main__":

	thread = Thread(target=NetworkData)       #发送数据后，就进行接收数据的循环线程中
	thread.daemon = True
	thread.start()  #启动线程

	mainLogic = MainLogic()
	mainLogic.LogicRun()