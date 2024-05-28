import os
import sys
import pygame as pg
import time

WIDTH = 800
HEIGHT = 600
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# class Result:
#     def __init__(self,bird):
#         self.img = pg.image.load("fig/kosyou.png")
#         screen = pg.display.set_mode((WIDTH, HEIGHT))


def main():
    pg.display.set_caption("はばたけ！こうかとん")
    screen = pg.display.set_mode((800, 600))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("fig/pg_space.jpg")
    bg_img2 = pg.transform.flip(bg_img, True, False)
    kk_img = pg.image.load("fig/3.png")
    kk_img = pg.transform.flip(kk_img, True, False)
    kk_img = pg.transform.rotozoom(kk_img, 10,1.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 100, 300
    key_lst = pg.key.get_pressed()
    tmr = 0
    d = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            #bird.rct.colliderect(emys.rct):
                        # ゲームオーバー時に，こうかとん画像を切り替え，1秒間表示させる
                kk_img = pg.transform.rotozoom(pg.image.load("fig/kosyou.png"), 100, 0.3)
                pg.display.update()
                time.sleep(1)
                fonto = pg.font.Font(None, 80)
                txt = fonto.render("result:", True, (0, 0, 0))
                screen.blit(txt, [WIDTH/2-150, HEIGHT/2])
                screen.blit(kk_img, kk_rct)
                pg.display.update()
                time.sleep(5)
                return

            elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
                d = -100
                kk_rct.move_ip((0,d))
            elif event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                d = 100
                kk_rct.move_ip((0,d))
            
            

        x = tmr%2200
        screen.blit(bg_img, [-x, 0])
        screen.blit(bg_img2,[-x+1100,0])
        screen.blit(bg_img, [-x+2200, 0])
        screen.blit(kk_img, kk_rct)
        pg.display.update()
        tmr += 1
        clock.tick(200)            

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()