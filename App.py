import math
import random
import pygame
import os
import NN

runing = True
FPS = 60
WIDTH = 960
HEIGHT = 590
clock = pygame.time.Clock()

pen_size = 5
# 遊戲初始化、建立視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("自動駕駛車")

# 亂樹種子
random.seed(10)
#載入圖片
# circle_img = pygame.image.load(os.path.join("img","circle.png")).convert()
# player_img = pygame.image.load(os.path.join("img","spaceship.png")).convert_alpha()
car_img = pygame.image.load(os.path.join("img","car.png")).convert()
# wall_img = pygame.image.load(os.path.join("img","wall.png")).convert()

class Wall(pygame.sprite.Sprite):
    
    def __init__(self,x,y,r):
        self.r = r
        print("r:",self.r)
        pygame.sprite.Sprite.__init__(self)
        # self.image = wall_img
        # self.image = pygame.transform.scale(circle_img,(200,200))
        self.image = pygame.Surface((self.r*2, self.r*2))
        # self.image.fill((0, 0, 0))
        self.image.set_colorkey((0,0,0))#將黑色背景設為透明
        
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x
        self.y = y
        # pygame.draw.circle(self.image, (0, 255, 0), (self.image.get_width() // 2, self.image.get_height() // 2), self.r, 0)
    def update(self):
        pygame.draw.circle(self.image, (255, 0, 0), (self.image.get_width() // 2, self.image.get_height() // 2), self.r)
        # pygame.transform.scale(self.image,(self.r*2,self.r*2),self.image)

    def upper(self):
        print("upper 被呼叫了")
        self.x = (self.x + 5) if self.x > WIDTH/2 else (self.x - 5)
        self.y = (self.y + 5) if self.y > HEIGHT/2 else (self.y - 5)
        self.r += 0.5

        self.image = pygame.Surface((self.r*2, self.r*2))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
    def smaller(self):
        print("smaller 被呼叫了")
        self.x = (self.x - 5) if self.x > WIDTH/2 else (self.x + 5)
        self.y = (self.y - 5) if self.y > HEIGHT/2 else (self.y + 5)
        self.r -= 0.5
        
        self.image = pygame.Surface((self.r*2, self.r*2))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        
class Player(pygame.sprite.Sprite):#繼承pygame.sprite.Sprite的類別
    def __init__(self, x, y):
        #父類別初始化
        pygame.sprite.Sprite.__init__(self)
        #需先設定圖片、位置
        self.image_orig = car_img
        # self.image_orig = pygame.Surface((w+10, h+10))
        self.image = self.image_orig.copy()
        # self.image.fill((0, 255, 0))
        #將照片框起來
        self.image.set_colorkey((0,0,255))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # self.custom_center = (w//2, h//2)
        self.sensors = []
        # pygame.draw.rect(self.image, (255, 0, 0), self.rect, 1)
        #再設定位置
        
        #行走開關
        self.runing = True
        self.speed = 5
        # 中間是0度，順時針為負，逆時針為正
        self.direction = 0
        
        # 神經網路基因
        self.DNA = []
        self.fitness = 0

    # 根據方向將方塊朝向轉正
    def rotate(self):
        new_image = pygame.transform.rotate(self.image_orig, self.direction+90)
        old_center = self.rect.center
        self.image = new_image
        self.image.set_colorkey((0,0,255))
        self.rect = self.image.get_rect().inflate(-10,-10)
        self.rect.center = old_center
    def turn(self, bias_angle):
        if not self.runing:return
        self.direction += bias_angle
    # 根據方向往前移動speed步(如果是-45度，就是move_ip(x=1,y=1)))
    # math.radians(45) -> 0.7853981633974483
    def step_Forward(self):
        if not self.runing:return
        mov_x = self.speed * math.cos(math.radians(-1*(self.direction)-90))
        mov_y = self.speed * math.sin(math.radians(-1*(self.direction)-90))
        self.rect.move_ip(mov_x,mov_y)
        pygame.draw.line(self.image, (255, 0, 0), (50, 50), (self.speed*mov_x, self.speed*mov_y), 5)

    def add_sensor(self, Sensor):
        self.sensors.append(Sensor)
    def get_sensorData(self):#以陣列方式回傳sensor的長度
        sensorData = []
        for sensor in self.sensors:
            sensorData.append(sensor.get_length())
        return sensorData
    def update_sensor(self):
        pass
    def update(self):
        if not self.runing:return
        self.rotate()
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = HEIGHT
        self.direction %= 360
    def reset(self, x, y, direction):
        self.rect.center = (x, y)
        self.direction = direction
        self.runing = True
        self.fitness = 0
    def is_touch(self, sprites):
        if not self.runing:return False 
        hit = pygame.sprite.spritecollide(self, sprites, False,pygame.sprite.collide_circle)
        # if hit:self.runing = False
        return hit
class Sensor:
    def __init__(self, car, bias_angle):
        # 設定中心點
        self.car = car
        self.x = car.rect.centerx
        self.y = car.rect.centery
        self.bias_angle = bias_angle
        self.angle = (car.direction+90 + bias_angle)%360
        self.collidions = []
        self.shortest_collision = None
        car.add_sensor(self)

    def update(self, obstacles):
        # 更新位置、方向、reset碰撞點
        self.x = self.car.rect.centerx
        self.y = self.car.rect.centery
        self.angle = (self.car.direction+90 + self.bias_angle)%360
        self.collidions = []
        # 偵測碰撞
        self.detect_collision(obstacles)
        

    # 偵測碰撞、將同角度的碰撞點加入collisions
    def detect_collision(self, obstacles):
        self.collisions = []
        # print("車的偵測角度:",self.angle)
        for obstacle in obstacles:
            ob_vec = pygame.math.Vector2(obstacle.x-self.x, -1*(obstacle.y-self.y))

            # 解決角度為負的問題
            angle = round(ob_vec.as_polar()[1]) if ob_vec.as_polar()[1] >= 0 else round(ob_vec.as_polar()[1])+360
            
            # 角度差小於3度就加入碰撞點
            if abs(angle-self.angle) <= 5:
                # print("此圓和車的角度:",round(ob_vec.as_polar()[1]))
                self.collisions.append(ob_vec)
    def get_length(self):
        if self.shortest_collision != None:
            return self.shortest_collision.length()/10
        return 0
    # 找出碰撞點長度最短的位置 繪製sensor
    def draw(self, screen):
        self.shortest_collision = None if len(self.collisions) == 0 else self.collisions[0]
        for collision in self.collisions:
            # print("碰撞點:",collision,round(collision.length()),"\n原點:",(self.x,self.y))
            if self.shortest_collision.length() > collision.length():
                self.shortest_collision = collision
        if self.shortest_collision != None:
            pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (self.x+self.shortest_collision.x, self.y+ (-1*self.shortest_collision.y)), 5)
            
#腳色建立也要打包成一個群組:用於群體更新畫面
cars_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()

# 串列用於存取、操作所有感測器、車子
Sensors = []
cars = []

# 車的初始化位置
x_spawn = 0
y_spwan = 0
generation = 1

def create_population(length):
    pop = []
    for i in range(length):
        car = Player(x_spawn, y_spwan)
        car.DNA = NN.randomDNA(8)
        Sensors.append(Sensor(car, 0))
        Sensors.append(Sensor(car, 45))
        Sensors.append(Sensor(car, -45))
        cars_group.add(car)
        cars.append(car)
        pop.append(car)
        # for D in car.DNA:
        #     print("DNA:",round(D,3),"\n")
    return pop
def get_parents(car_list):
    # 只取前兩名
    for j in range(2):
        greatist_car = car_list[j]
        greatist_i = j
        for i in range(j+1, len(car_list)):
            if car_list[i].fitness > greatist_car.fitness:
                greatist_i = i
                greatist_car = car_list[i]
        car_list[j], car_list[greatist_i] = car_list[greatist_i], car_list[j]
    return car_list[:2]  
def crossover(a, b):
    child_DNA = []
    for i in range(len(a.DNA)):
        if random.random() > 0.5:
            child_DNA.append(a.DNA[i])
        else:
            child_DNA.append(b.DNA[i])
        if random.random() < 0.1:
            child_DNA.pop()
            child_DNA.append(random.random()*2-1)
    return child_DNA
def next_generation():
    global generation
    generation += 1
    print("下一代車")
    # 取得父母
    parents = get_parents(cars)
    # 交配
    for i in range(len(cars)):
        cars[i].reset(x_spawn, y_spwan, 0)
        cars[i].DNA = crossover(parents[0], parents[1])
    return    
# 生成汽車
populations = create_population(20)

# game_states = ["drawing","setting","playing"]
game_status = 0 # 索引代表上一行的狀態
drawing = False

while runing:
    clock.tick(FPS)
    car_alive = 0
    for player in cars_group:
        ## 操控角色
        output = NN.NN(player.get_sensorData(), player.DNA)
        player.turn(output*3)
        if player.runing:
            player.step_Forward()
            car_alive += 1
            player.fitness += 1
    if car_alive == 0:
        next_generation()
    print(car_alive)
    # 取得事件輸入:適用於短按
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            runing = False
        
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_DELETE and game_status == 0:
                print("delete")
                walls_group.empty()
            # 空白鍵狀態切換:0->1->2->0
            if e.key == pygame.K_SPACE:
                game_status = (game_status + 1)%3 # 狀態切換:0->1->2->0
                print("當前狀態",game_status)
                if game_status == 2:
                    for player in cars_group:player.reset(x_spawn, y_spwan, 0)
            # drawing狀態切換
            if e.key == pygame.K_a and game_status == 0:
                drawing = not drawing
                print("畫:",drawing)
            if e.key == pygame.K_s and game_status == 0:
                print("s:要縮小")
                for wall in walls_group:
                    wall.smaller()
                pen_size -= 1
            if e.key == pygame.K_d and game_status == 0:
                print("s:要放大")
                for wall in walls_group:
                    wall.upper()
                pen_size += 1
            if e.key == pygame.K_r and game_status == 2:
                print("手動產生下一代")
                next_generation()
        if e.type == pygame.MOUSEBUTTONDOWN and game_status == 1:
            # 左鍵按下：設定生成點
            if e.button == 1 and game_status == 1:
                x_spawn = e.pos[0]
                y_spwan = e.pos[1]
                print("x_spawn:",x_spawn,"y_spwan:",y_spwan)
    # 滑鼠事件(持續) 
    mouse_event = pygame.mouse.get_pressed()
    # mouse_event[0] -> 左鍵
    if mouse_event[0] and game_status == 0 and drawing:
        x, y = pygame.mouse.get_pos()
        # print(x,y)
        print("pen_size/2=:",pen_size/2)
        walls_group.add(Wall(x,y,pen_size/2))

    # if mouse_event[0] and game_status == 1:
    #     x, y = pygame.mouse.get_pos()

    # 鍵盤事件(持續)
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_LEFT]:
    #     player.turn(1)
    # if keys[pygame.K_RIGHT]:
    #     player.turn(-1)
    # if keys[pygame.K_UP]:

    # if game_status == 2:
    #     for player in cars_group:player.step_Forward()
    
    # 更新遊戲
    cars_group.update()
    for sensor in Sensors:
        sensor.update(walls_group)
    walls_group.update()
    
    if game_status == 2:
        for player in cars_group:
            # 碰撞偵測
            if player.runing and player.is_touch(walls_group):
                # print("碰撞偵測")
                player.runing = False
    
    # 繪製遊戲
    # 畫面顯示
    screen.fill((255,255,255))#畫面顏色
    
    # 顯示文字在畫面上
    font = pygame.font.Font(None, 36)
    text = font.render(str(generation)+"th generation", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = screen.get_rect().centerx
    screen.blit(text, textpos)

    for sensor in Sensors:
        if sensor.car.runing:sensor.draw(screen)
    cars_group.draw(screen)
    walls_group.draw(screen)
    pygame.display.update()

pygame.quit()