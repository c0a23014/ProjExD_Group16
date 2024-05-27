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
        


class Bomb:
    """
    爆弾に関するクラス
    """
    def __init__(self, color: tuple[int, int, int], rad: int):
        """
        引数に基づき爆弾円Surfaceを生成する
        引数1 color：爆弾円の色タプル
        引数2 rad：爆弾円の半径
        """
        self.img = pg.Surface((2*rad, 2*rad))
        pg.draw.circle(self.img, color, (rad, rad), rad)
        self.img.set_colorkey((0, 0, 0))
        self.rct = self.img.get_rect()
        self.rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        self.vx, self.vy = +5, +5

    def update(self, screen: pg.Surface):
        """
        爆弾を速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        yoko, tate = check_bound(self.rct)
        if not yoko:
            self.vx *= -1
        if not tate:
            self.vy *= -1
        self.rct.move_ip(self.vx, self.vy)
        screen.blit(self.img, self.rct)
        self.update(screen)
        


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

class Score:
    def __init__(self):
        """
        フォントの設定
        文字色の設定：青
        スコアの初期値の設定
        文字列Surfaceの生成
        文字列の中心座標
        """
        self.fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 30)
        self.score = 0
        self.color = (255,255,0)
        self.img = self.fonto.render(f"経過時間: {int(self.score)}", 0, self.color)
        self.rct = self.img.get_rect()
        self.rct.center = 100,HEIGHT-50
    
    def update(self,screen: pg.Surface):
        """
        現在のスコアを表示させる文字列Surfaceの生成
        スクリーンにblit
        """
        self.img = self.fonto.render(f"経過時間: {int(self.score)}", 0, self.color)
        screen.blit(self.img, self.rct)




def main():
    pg.display.set_caption("たたかえ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))    
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bird = Bird((100, 300))
    #bomb = Bomb((255, 0, 0), 10)
    bombs = [Bomb((255, 0, 0), 10)for _ in range(NUM_OF_BOMBS)]
    beam = None
    clock = pg.time.Clock()
    score = Score()
    tmr = 0
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
        
        for bomb in bombs:
            if bird.rct.colliderect(bomb.rct):
                # ゲームオーバー時に，こうかとん画像を切り替え，1秒間表示させる
                bird.change_img(8, screen)
                fonto = pg.font.Font(None, 80)
                txt = fonto.render("Game Over", True, (255, 0, 0))
                screen.blit(txt, [WIDTH/2-150, HEIGHT/2])
                pg.display.update()
                time.sleep(5)
                return
        for i, bomb in enumerate(bombs):
            if beam is not None:
                if beam.rct.colliderect(bomb.rct):
                    beam = None
                    bombs[i] = None
                    bird.change_img(6, screen)
                    pg.display.update()
        bombs = [bomb for bomb in bombs if bomb is not None]

        key_lst = pg.key.get_pressed()
        bird.update(screen)
        for bomb in bombs:
            bomb.update(screen)
        if beam is not None:
            beam.update(screen)
        score.score += 0.02
        score.update(screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
