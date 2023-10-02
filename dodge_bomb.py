import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1600, 900


def is_inside_screen(rect):
    """Rectが画面内にあるかどうかを判定する関数."""
    return (
        0 <= rect.left <= WIDTH and
        0 <= rect.right <= WIDTH and
        0 <= rect.top <= HEIGHT and
        0 <= rect.bottom <= HEIGHT
    )

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)

    kk_img_right = pg.image.load("ex02/fig/3.png")
    kk_img_left = pg.transform.flip(kk_img_right, True, False)
    kk_img_right = pg.transform.rotozoom(kk_img_right, 0, 2.0)
    kk_img_left = pg.transform.rotozoom(kk_img_left, 0, 2.0)
    kk_img = kk_img_right

    bomb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r), pg.SRCALPHA)
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bomb_imgs.append(bb_img)
    bomb_img = bomb_imgs[0]

    #bomb_surface.set_colorkey((0, 0, 0))

    bomb_rect = bomb_img.get_rect(topleft=(random.randint(0, WIDTH-bomb_img.get_width()), random.randint(0, HEIGHT - bomb_img.get_height())))

    clock = pg.time.Clock()

    kk_rect = kk_img.get_rect(topleft=(900, 400))

    move_dict = {
        pg.K_UP: (0, -5),    # 上矢印
        pg.K_DOWN: (0, 5),   # 下矢印
        pg.K_LEFT: (-5, 0),  # 左矢印
        pg.K_RIGHT: (5, 0)   # 右矢印
    }

    vx, vy = 5, 5
    accs = [a for a in range(1, 11)]

    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        key_lst = pg.key.get_pressed()

        total_movement = [0, 0]
        for key, movement in move_dict.items():
            if key_lst[key]:
                total_movement[0] += movement[0]
                total_movement[1] += movement[1]


        kk_rect.move_ip(*total_movement)

        if not is_inside_screen(kk_rect):
            kk_rect.move_ip(*[-movement for movement in total_movement])

        # 加速度と拡大爆弾Surfaceを選択
        avx, avy = vx * accs[min(tmr // 500, 9)], vy * accs[min(tmr // 500, 9)]
        bomb_img = bomb_imgs[min(tmr // 500, 9)]

        bomb_rect.move_ip(avx, avy)

        if not is_inside_screen(bomb_rect):
            vx = -vx
            vy = -vy
            bomb_rect.move_ip(vx, vy)
        
        if kk_rect.colliderect(bomb_rect):
            return
        
        if total_movement[0] < 0:
            kk_img = kk_img_right
        elif total_movement[0] > 0:
            kk_img = kk_img_left

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