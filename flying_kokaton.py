import os
import random
import sys
import time
import pygame as pg


WIDTH = 1000  # ゲームウィンドウの幅
HEIGHT = 600  # ゲームウィンドウの高さ
NUM_OF_BOMBS = 0
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数：こうかとんRect，または，爆弾Rect
    戻り値：縦方向のはみ出し判定結果（画面上：１／画面下：２）
    """
    tate = 0
    if obj_rct.bottom < 0 :
        tate = 1
    if HEIGHT < obj_rct.top:
        tate = 2
    return tate


class Bird:
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    
    def __init__(self, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数 xy：こうかとん画像の初期位置座標タプル
        """
        self.img = pg.transform.flip(pg.image.load("fig/3.png"), True, False)
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy
        self.d = 0
        self.tm = 0
        self.bg_img = pg.image.load("fig/pg_space.jpg")
        self.bg_img2 = pg.transform.flip(self.bg_img, True, False)

        

    def change_img(self, num: int, screen: pg.Surface):
        """
        こうかとん画像を切り替え，画面に転送する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 screen：画面Surface
        """
        screen.blit(self.img, self.rct)

    def update(self, screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数2 screen：画面Surface
        """
        tate = check_bound(self.rct)
        if tate == 1:
            d = 600
            self.rct.move_ip((0,d))
        if tate == 2:
            d = -600
            self.rct.move_ip((0,d))


class Enemy:
    """
    敵機に関するクラス
    """
    def __init__(self):
        self.img = pg.image.load("fig/pg_fall.png")
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.centerx = WIDTH
        self.rct.centery = random.choice([0, 60, 200, 260, 320, 380, 440, 500])
        self.vx, self.vy = -20, 0

    def update(self, screen: pg.Surface):
        """
        敵機を速度ベクトルself.vyに基づき移動（降下）させる
        ランダムに決めた停止位置_boundまで降下したら，_stateを停止状態に変更する
        引数 screen：画面Surface
        """
        self.rct.move_ip(self.vx, self.vy)
        screen.blit(self.img, self.rct)


class Beam:
    def __init__(self, bird: Bird):
        self.img = pg.transform.rotozoom(pg.image.load("fig/beam.png"), 0, 2.0)
        self.rct: pg.Rect = self.img.get_rect() #Rect
        self.rct.left = bird.rct.right
        self.rct.centery = bird.rct.centery
        self.vx, self.vy = +5, 0

    def update(self, screen: pg.Surface):
        """
        爆弾を速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        if check_bound(self.rct) == (True, True):
            self.rct.move_ip(self.vx, self.vy)
            screen.blit(self.img, self.rct)


def main():
    pg.display.set_caption("たたかえ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))    
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bird = Bird((100, 300))
    beam = None
    clock = pg.time.Clock()
    tmr = 0
    emys = []
    key_lst = pg.key.get_pressed()

            
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                beam = Beam(bird)
            if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                d = -100
                bird.rct.move_ip((0,d))
            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                d = 100
                bird.rct.move_ip((0,d))
                
        screen.blit(bg_img, [0, 0])
        x = bird.tm % 2400
        screen.blit(bird.bg_img, [-x, 0])
        screen.blit(bird.bg_img2,[-x+1200,0])
        screen.blit(bird.bg_img, [-x+2400, 0])
        screen.blit(bird.img, bird.rct)
        pg.display.update()
        bird.tm += 1


        if tmr % 20 == 0:
            emys.append(Enemy())
        for emy in emys:
            emy.update(screen)
            # if emys.rct.colliderect(bird.rct):

        #key_lst = pg.key.get_pressed()
        bird.update(screen)
        if beam is not None:
            beam.update(screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()