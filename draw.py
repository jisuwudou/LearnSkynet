from calendar import c
import os
import random
import sys
 
import pygame
from pygame import font

from pygame.constants import MOUSEBUTTONDOWN, MOUSEMOTION

class InputBox(pygame.sprite.Sprite):
    surface = None
    txtSurface = None
    def __init__(self, rect: pygame.Rect = pygame.Rect(100, 100, 140, 32)) -> None:
        super().__init__()
        """
        rect，传入矩形实体，传达输入框的位置和大小
        """
        self.boxBody: pygame.Rect = rect
        self.color_inactive = pygame.Color('lightskyblue3')  # 未被选中的颜色
        self.color_active = pygame.Color('dodgerblue2')  # 被选中的颜色
        self.color = self.color_inactive  # 当前颜色，初始为未激活颜色
        self.active = False
        self.text = 'test1'
        self.done = False
        self.font = pygame.font.Font(None, 32)

        self.surface = pygame.Surface([rect.width, rect.height])

        self.image = pygame.Surface([self.boxBody.width, self.boxBody.height])
        # self.image.fill(self.color)
        self.rect = self.boxBody

    def dealEvent(self, event: pygame.event.Event):
        if(event.type == pygame.MOUSEBUTTONDOWN):
            if(self.boxBody.collidepoint(event.pos)):  # 若按下鼠标且位置在文本框
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if(
                self.active) else self.color_inactive
        if(event.type == pygame.KEYDOWN):  # 键盘输入响应

            print("inputbox ", event.key , pygame.K_BACKSPACE, self.active)
            if(self.active):
                if(event.key == pygame.K_RETURN):
                    print(self.text)
                    # self.text=''
                elif(event.key == pygame.K_BACKSPACE):
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                    print(self.text)

    def update(self):
        pass
        # self.image.blit(txtSurface, (self.boxBody.x+5, self.boxBody.y+5))
        # pygame.draw.rect(self.image, self.color, self.boxBody, 2)

    def drawText(self,surface):
        self.txtSurface = self.font.render( self.text, True, self.color)  # 文字转换为图片
        width = max(200, self.txtSurface.get_width()+10)  # 当文字过长时，延长文本框
        self.boxBody.w = width
        surface.blit(self.txtSurface, (self.boxBody.x+5, self.boxBody.y+5))

    # def update(self, screen: pygame.surface.Surface):
    #     txtSurface = self.font.render(
    #         self.text, True, self.color)  # 文字转换为图片
    #     width = max(200, txtSurface.get_width()+10)  # 当文字过长时，延长文本框
    #     self.boxBody.w = width
    #     screen.blit(txtSurface, (self.boxBody.x+5, self.boxBody.y+5))
    #     pygame.draw.rect(screen, self.color, self.boxBody, 2)


class Image(pygame.sprite.Sprite):
    def __init__(self, img_name: str, center_x, center_y, ratio=0.4):
        super().__init__()
        """
        img_name: 图片文件名，如'background.jpg'、'ink.png',注意为字符串
        ratio: 图片缩放比例，与主屏幕相适应，默认值为0.4
        """
        self.img_name = img_name
        self.ratio = ratio
        print("init ", ratio)
        self.image_1080x1920 = pygame.image.load(os.path.join('res/btn/', self.img_name)).convert_alpha()
        self.img_width = self.image_1080x1920.get_width()
        self.img_height = self.image_1080x1920.get_height()

        
        self.size_scaled = self.img_width * self.ratio, self.img_height * self.ratio
 
        self.image_scaled = pygame.transform.smoothscale(self.image_1080x1920, self.size_scaled)
        self.img_width_scaled = self.image_scaled.get_width()
        self.img_height_scaled = self.image_scaled.get_height()
        self.center_x = center_x
        self.center_y = center_y


        self.image = self.image_1080x1920
        self.rect = self.center_x, self.center_y, self.img_width, self.img_height

        print("image ", self.img_width, self.img_height, self.ratio)
 
    def draw(self, surface: pygame.Surface):
        """
        surface: 图片放置的表面
        center_x, center_y: 图片放置在表面的<中心坐标>
        """
        upperleft_x = self.center_x - self.img_width_scaled / 2
        upperleft_y = self.center_y - self.img_height_scaled / 2
        surface.blit(self.image_scaled, (upperleft_x, upperleft_y))

        # print("draw ", self.img_width, self.img_height, self.ratio)


class ButtonImage(Image):


    mousedownEvt = None
    def __init__(self, img_name: str,center_x, center_y, ratio=0.4):
        super().__init__(img_name, center_x, center_y, ratio)
        self.rect = self.image_scaled.get_rect()
        self.rect.center = center_x, center_y
 
    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        
 
    def dealEvent(self, event):
        # self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        # if self.hovered:
        #     command()
        if(event.type == pygame.MOUSEBUTTONDOWN):
            if(self.rect.collidepoint(event.pos)):  # 若按下鼠标且位置在文本框
                if self.mousedownEvt:
                    self.mousedownEvt()
        if(event.type == pygame.KEYDOWN):  # 键盘输入响应
            if(event.key == pygame.K_RETURN):
                print("button return")

                
# ————————————————
# 版权声明：本文为CSDN博主「Akinaze」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/weixin_44097528/article/details/123320286