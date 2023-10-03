import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1600, 900


def main():
    # ウィンドウの初期化
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    # 画像の読み込みと初期化
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img_right = pg.image.load("ex02/fig/3.png")
    kk_img_left = pg.transform.flip(kk_img_right, True, False)
    kk_img_right = pg.transform.rotozoom(kk_img_right, 0, 2.0)
    kk_img_left = pg.transform.rotozoom(kk_img_left, 0, 2.0)
    kk_img_up = pg.transform.flip(kk_img_left, True, False)
    kk_img_up = pg.transform.rotozoom(kk_img_left, 90, 1.0)
    kk_img_down = pg.transform.rotozoom(kk_img_left, -90, 1.0)
    kk_img_up_right = pg.transform.rotozoom(kk_img_left, -45, 1.0)
    kk_img_down_right = pg.transform.rotozoom(kk_img_left, 45, 2.0)
    kk_img_up_left = pg.transform.rotozoom(kk_img_right, -135, 2.0)
    kk_img_down_left = pg.transform.rotozoom(kk_img_right, 135, 2.0)
    kk_img = kk_img_right

    # Rectが画面内にあるかどうかを判定する関数
    def is_inside_screen(rect):
        return (
            0 <= rect.left <= WIDTH and
            0 <= rect.right <= WIDTH and
            0 <= rect.top <= HEIGHT and
            0 <= rect.bottom <= HEIGHT
        )

    # 爆弾の画像のリストを生成
    bomb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r), pg.SRCALPHA)
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bomb_imgs.append(bb_img)
    
    clock = pg.time.Clock()

    # こうかとんと爆弾の初期位置の設定
    kk_rect = kk_img.get_rect(topleft=(900, 400))
    bomb_rect = bomb_imgs[0].get_rect(topleft=(random.randint(0, WIDTH - bomb_imgs[0].get_width()), random.randint(0, HEIGHT - bomb_imgs[0].get_height())))

    # 移動の設定
    move_dict = {
        pg.K_UP: (0, -5), # 上矢印
        pg.K_DOWN: (0, 5), # 下矢印
        pg.K_LEFT: (-5, 0), # 左矢印
        pg.K_RIGHT: (5, 0), # 右矢印
        pg.K_UP | pg.K_RIGHT: (5, -5), # 右上
        pg.K_DOWN | pg.K_RIGHT: (5, 5), # 右下
        pg.K_DOWN | pg.K_LEFT: (0, 5), # 左下
        pg.K_UP | pg.K_LEFT: (0, -5) #左上
    }

    vx, vy = 5, 5
    accs = [a for a in range(1, 11)]

    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        # キーの押下状態リストを取得   
        key_states = pg.key.get_pressed()

        # 合計移動量を求める
        total_movement = [0, 0]
        for key, movement in move_dict.items():
            if key_states[key]:
                total_movement[0] += movement[0]
                total_movement[1] += movement[1]

        # こうかとんの位置を移動
        kk_rect.move_ip(*total_movement)

        if not is_inside_screen(kk_rect):
            kk_rect.move_ip(*[-movement for movement in total_movement])

        # 爆弾がこうかとんに近づくように移動する
        diff_vector = [kk_rect.x - bomb_rect.x, kk_rect.y - bomb_rect.y]

        #  ベクトルのノルムが√50になるように正規化
        norm = (diff_vector[0]**2 + diff_vector[1]**2)**0.5
        normalized_vector = [diff_vector[0] / norm, diff_vector[1] / norm]

        # 爆弾とこうかとんの距離が500未満だったら，慣性として前の方向に移動させる
        if norm < 500:
            avx, avy = vx * accs[min(tmr // 500, 9)] * normalized_vector[0], vy * accs[min(tmr // 500, 9)] * normalized_vector[1]
            bomb_rect.move_ip(avx, avy)
            bomb_img = bomb_imgs[min(tmr // 500, 9)] # 新しい爆弾の大きさを反映
        else:
            avx, avy = vx * accs[min(tmr // 500, 9)], vy * accs[min(tmr // 500, 9)]
            bomb_rect.move_ip(avx, avy)
            bomb_img = bomb_imgs[min(tmr // 500, 9)] # 新しい爆弾の大きさを反映

        # 爆弾が跳ね返る処理
        if not is_inside_screen(bomb_rect):
            vx = -vx
            vy = -vy
            bomb_rect.move_ip(vx, vy)
        
        # こうかとんと爆弾が衝突したらreturn
        if kk_rect.colliderect(bomb_rect):
            kk_img_collision = pg.image.load("ex02/fig/8.png")
            screen.blit(bg_img, [0, 0])
            screen.blit(kk_img_collision, kk_rect.topleft)
            #screen.blit(bomb_img_collision, bomb_rect.topleft)
            pg.display.update()
            pg.time.wait(1000)
            return
        
        # 飛ぶ方向に応じてこうかとんを切り替える
        for key, movement in move_dict.items():
            if key_states[key]:
                if movement[0] == 0 and movement[1] < 0:
                    kk_img = kk_img_up
                elif movement[0] == 0 and movement[1] > 0:
                    kk_img = kk_img_down
                elif movement[0] > 0:
                    kk_img = kk_img_left
                elif movement[0] < 0:
                    kk_img = kk_img_right
                elif movement[0] < 0 and movement[1] < 0:
                    kk_img = kk_img_up_left
                elif movement[0] > 0 and movement[1] < 0:
                    kk_img = kk_img_up_right
                elif movement[0] < 0 and movement[1] > 0:
                    kk_img = kk_img_down_left
                elif movement[0] > 0 and movement[1] > 0:
                    kk_img = kk_img_down_right

        # 画面の描画
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rect.topleft)
        screen.blit(bomb_img, bomb_rect.topleft)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()