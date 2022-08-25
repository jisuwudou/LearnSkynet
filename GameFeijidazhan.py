# 导入两个库
import pygame
import random

# 常量，屏幕宽高
WIDTH, HEIGHT = 800, 600
# 初始化操作
pygame.init()
pygame.mixer.init()
# 创建游戏窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# 设置游戏标题
pygame.display.set_caption('飞机大战')

# 添加音乐
# pygame.mixer.music.load('./sound/bgLoop.wav')
# pygame.mixer.music.set_volume(0.5)  # 音量
# pygame.mixer.music.play(-1, 0)

# 添加系统时钟，用于设置帧的刷新
FPS = 40
clock = pygame.time.Clock()

# 创建用户自定义事件，每隔2000毫秒触发一次事件，随机创建敌人
CREATE_ENEMY = pygame.USEREVENT
# 每隔2000毫秒，会传递一个信号
pygame.time.set_timer(CREATE_ENEMY, 2000)

# 对于精灵定义了主角，子弹，敌人，爆炸，可移动背景四个。
#class Hero(pygame.sprite.Sprite)
#class Bullet(pygame.sprite.Sprite)
#class Enemy(pygame.sprite.Sprite)
#class Explode(pygame.sprite.Sprite)
#class BackGround(pygame.sprite.Sprite)
# 主角
class Hero(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()  # 调用父类的初始化方法
        self.image = pygame.image.load('./res/plane.png')
        self.rect = self.image.get_rect()
        # 对图片进行一些尺寸处理
        self.rect.width *= 0.5
        self.rect.height *= 0.5
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        # 主角初始化位置
        self.rect.x, self.rect.y = 0, 100
        self.speed = speed
        self.ready_to_fire = 0

    def update(self, *args):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE]:
            if self.ready_to_fire == 0:
                self.fire()
            self.ready_to_fire += 1
            if self.ready_to_fire > 5:
                self.ready_to_fire = 0
        else:
            self.ready_to_fire = 0
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > HEIGHT - self.rect.height:
            self.rect.y = HEIGHT - self.rect.height
    # 子弹发射
    def fire(self):
        bullet = Bullet(10)
        bullet.rect.x = self.rect.right
        bullet.rect.centery = self.rect.centery
        bullet_sprite.add(bullet)
        # 音效
        # sound = pygame.mixer.Sound('./sound/laser.wav')
        # sound.play()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.image.load('./res/bullet.png')
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self, *args):
        self.rect.x += self.speed
        if self.rect.x > WIDTH:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.image.load('./res/enemy.png')
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = random.randint(0, HEIGHT)
        self.speed = speed

    def update(self, *args):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()


class Explode(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [pygame.image.load('./res/explode' + str(i) + '.png') for i in range(1, 4)]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.readt_to_change = 0
        # sound = pygame.mixer.Sound('./sound/enemyExplode.wav')
        # sound.play()

    def update(self, *args):
        if self.image_index < 2:
            self.readt_to_change += 1
            if self.readt_to_change % 4 == 0:
                self.image_index += 1
                self.image = self.images[self.image_index]
        else:
            self.kill()


class BackGround(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('./res/background.png')
        self.rect = self.image.get_rect()
        self.ready_to_move = 0

    def update(self, *args):
        self.rect.x -= 3
        if self.rect.right <= 0:
            self.rect.x = self.rect.width


# 初始化精灵组
bg_sprite = pygame.sprite.Group()
hero_sprite = pygame.sprite.Group()
enemy_sprite = pygame.sprite.Group()
bullet_sprite = pygame.sprite.Group()
explode_sprite = pygame.sprite.Group()

# 定义人物

hero1 = Hero(4)
hero_sprite.add(hero1)

enemy1 = Enemy(5)
enemy2 = Enemy(7)

bg1 = BackGround()
bg2 = BackGround()
bg2.rect.x = bg2.rect.width
bg_sprite.add(bg1, bg2)

# 保持游戏运行状态(游戏循环）
while True:
    # ===========游戏帧的刷新===========
    clock.tick(FPS)

    # 检测事件
    for event in pygame.event.get():
        # 检测关闭按钮被点击的事件
        if event.type == pygame.QUIT:
            # 退出
            pygame.quit()
            exit()
        if event.type == CREATE_ENEMY:
            enemy_sprite.add(Enemy(random.randint(1, 7)))

    # 碰撞检测,返回字典，得到二者信息
    collision = pygame.sprite.groupcollide(enemy_sprite, bullet_sprite, True, True)
    for enemy in collision.keys():
        explode = Explode()
        explode.rect = enemy.rect
        explode_sprite.add(explode)

    # screen.fill((0,0,0))
    for group in [bg_sprite, hero_sprite, enemy_sprite, bullet_sprite, explode_sprite]:
        group.update()
        group.draw(screen)
    pygame.display.update()