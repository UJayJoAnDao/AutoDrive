# 自動駕駛 Auto_Drive
操作指南:

* 空白鍵切換模式:模式說明如下

    0：draw 模式，此模式可以按下ａ鍵切換可畫( paintable )與不畫( non paintable )，常按左鍵滑鼠變可以自己畫地圖樣貌。如需重新畫圖，可在此模式按下 delete 清除畫面。
        
    > 注意：此模式目前還看的到車並行走，但不會偵測碰撞，整體並不影響訓練，訓練只在 play 模式進行

    1：setting 模式，此模式按左鍵可以設定汽車重生初始位置( x_spawn, y_spawn)

    2：play 模式，此模式實際上就是會讓汽車開始偵測碰撞並訓練。
    > 注意：原先剩餘兩台車時會自動生成下一代汽車，而有時會有一台汽車一直存活在場上，所以新增按下 Ｒ鍵可以強制生成下一代汽車。

* 遊戲流程如下:
    
    1. 畫自定義的地圖供汽車訓練
    2. 設置重生點（無設定就是預設位置）
    3. 開始訓練
    
    > 汽車只要少於、等於 2 台 或是 play 模式按下 R 鍵，就會回到重生點並且根據上一帶基因生成一批子代，以此達到物競天擇的效果。

## 遊戲設定
初始玩家方向（direction）朝上（0度），逆時針為正，順時針為負
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

## 參考資料
[](https://stackoverflow.com/questions/45420223/pygame-vector2-as-polar-and-vector2-from-polar-methods)