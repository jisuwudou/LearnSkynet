import pygame
from threading import Thread
from draw import InputBox
from draw import ButtonImage
import C_Websocket

def NetworkData():
	pass


class MainLogic:
	userInput = None

	def OnSureBtnDown(self):
		print("OnSureBtnDown", self.userInput.text)
	
	
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
		
		self.userInput = InputBox()
		sureBtn = ButtonImage("btnSure.png", 15,16,1)
		sureBtn.mousedownEvt = self.OnSureBtnDown
	
		while True:
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					raise SystemExit
	
				self.userInput.dealEvent(event)
				sureBtn.handle_event(event)
	
			self.userInput.draw(window)
			sureBtn.draw(window)
			pygame.display.flip()





if __name__ == "__main__":

	thread = Thread(target=NetworkData)       #发送数据后，就进行接收数据的循环线程中
	thread.setDaemon(True)    
	thread.start()  #启动线程

	mainLogic = MainLogic()
	mainLogic.LogicRun()