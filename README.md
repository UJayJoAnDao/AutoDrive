# 自動駕駛 Auto_Drive
操作指南:

空白鍵切換模式
0:draw，draw模式可以按下a切換畫(True)與不畫(False)，常按左鍵滑鼠可以畫地圖
1:setting，此模式按左鍵可以設定重生點(x_spawn, y_spawn)
2.play，此模式實際上就是會讓汽車開始偵測碰撞

汽車只要少於、等於 2 台 或是 play模式按下 r 鍵，就會重新設置位置並且根據上一帶好的生成一批子代，以此達到物競天擇的效果。

# 遊戲設定
初始玩家方向(direction)朝上(0度)，逆時針為正，順時針為負
前進會朝自身的方向前進

## 作業測試
line 99:將畫布的藍色區域清除，註解後可以原先的碰撞矩形
'''self.image.set_colorkey((0,0,255))'''

line 172:可以讓玩家跟著滑鼠方便測試
'''player.rect.center = (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])'''

## 車
* 使用`car.stepFoward()`可根據speed前進
* 使用`car.turn(angle)`可以轉動車，根據`angle`決定改變大小，+:左 -:右
* 使用`car.add_sensor(Sensor)`，加入該車一個感測器

## 感測器
* 使用`Sensor(car, angle)`設定感測器面朝向`car`方向為基準的`angle`度
* 可使用Sensor.get_length()取得線段長度

* 先將感測器根據角度new(屬性:center(x, y), angle, collidion[])
* 再算出感測器單位向量
* 循序檢查每個wall的單位向量(wall.x-start.x, -1*(wall.y-start.y))，並轉換為角度是否為相近
* 若相近，加入串列
* 取串列中長度最短的並畫線:起點(x, y) 終點 (wall.x, wall.y)


[參考資料](https://stackoverflow.com/questions/45420223/pygame-vector2-as-polar-and-vector2-from-polar-methods)