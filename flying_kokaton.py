import os
import random
import sys
import time
import pygame as pg

WIDTH = 1000  # ゲームウィンドウの幅
HEIGHT = 600  # ゲームウィンドウの高さ
NUM_OF_BOMBS = 0
ITEM_Y_POSITIONS = [100, 200, 300, 400, 500]
ITEM_INTERVAL = 5000
LANE_HEIGHT = HEIGHT // 5  # 画面を5つのレーンに分割


WIDTH = 1000  # ゲームウィンドウの幅
HEIGHT = 600  # ゲームウィンドウの高さ
ITEM_Y_POSITIONS = [100, 200, 300, 400, 500]
ITEM_INTERVAL = 5000
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数：こうかとんRect，または，爆弾Rect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    tate = True
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return tate


class Bird:
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    
    def __init__(self, xy: tuple[int, int]):
        """
        UFO画像Surfaceを生成する
          
        引数 xy：UFO画像の初期位置座標タプル
        """
        self.img = pg.transform.flip(pg.image.load("fig/pg_ufo.png"), True, False)
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy
        self.d = 0
        self.tm = 0
        self.bg_img = pg.image.load("fig/pg_space.jpg")
        self.bg_img2 = pg.transform.flip(self.bg_img, True, False)
        self.current_lane = 2  # 初期レーンの設定（中央）
        self.move_cooldown = 0
        self.warp_img = pg.image.load("fig/pg_warp.png")
        self.warp_positions = []
        self.warp_time = 0

    def change_img(self, num: int, screen: pg.Surface):
        """
        こうかとん画像を切り替え，画面に転送する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 screen：画面Surface
        """
        screen.blit(self.img, self.rct)

    def warp_effect(self, screen: pg.Surface):
        """
        UFOがレーンを移動する際のワープエフェクトを描画する
        引数 screen：画面Surface
        """
        current_time = pg.time.get_ticks()
        for pos, start_time in self.warp_positions[:]:
            if current_time - start_time < 1000:  # ワープエフェクトを1秒間表示
                warp_rct = self.warp_img.get_rect(center=pos)
                screen.blit(self.warp_img, warp_rct)
            else:
                self.warp_positions.remove((pos, start_time))

    def update(self, screen: pg.Surface):
        """
        押下キーに応じてUFOをレーン移動させる
        引数 screen：画面Surface
        """
        if self.move_cooldown > 0:
            self.move_cooldown -= 1

        key_lst = pg.key.get_pressed()
        self.d = 0
        if key_lst[pg.K_UP] and self.move_cooldown == 0:#上
            self.warp_positions.append((self.rct.center, pg.time.get_ticks()))
            self.current_lane -= 1
            if self.current_lane < 0:
                self.current_lane = 4
            self.d = -1
            self.move_cooldown = 20  # 一度の入力で一回の移動

        if key_lst[pg.K_DOWN] and self.move_cooldown == 0:#下
            self.warp_positions.append((self.rct.center, pg.time.get_ticks()))
            self.current_lane += 1
            if self.current_lane > 4:
                self.current_lane = 0
            self.d = 1
            self.move_cooldown = 20  # 一度の入力で一回の移動

        # レーンに基づいて位置を設定
        self.rct.centery = (self.current_lane + 0.5) * LANE_HEIGHT
        screen.blit(self.img, self.rct)
        self.warp_effect(screen)


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
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.left = bird.rct.right
        self.rct.centery = bird.rct.centery
        self.vx, self.vy = +10, 0

    def update(self, screen: pg.Surface):
        """
        ビームを速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        self.rct.move_ip(self.vx, self.vy)
        screen.blit(self.img, self.rct)


class Item:
    def __init__(self, color: tuple[int, int, int], rad: int):
        """
        アイテムとして赤い丸を生成する
        引数1 color：アイテムの色タプル
        引数2 rad：アイテムの半径
        """
        self.img = pg.Surface((2*rad, 2*rad))
        pg.draw.circle(self.img, color, (rad, rad), rad)
        self.img.set_colorkey((0, 0, 0))
        self.rct = self.img.get_rect()
        self.rct.center = random.randint(WIDTH, WIDTH+100), random.choice(ITEM_Y_POSITIONS)
        self.vx, self.vy = -5, 0

    def update(self, screen: pg.Surface):
        """
        アイテムを速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
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
    bg_img = pg.image.load("fig/pg_space.jpg")
    bird = Bird((100, (2 + 0.5) * LANE_HEIGHT))  # 初期位置を中央レーンに設定
    items = []
    beams = []
    beam = None
    beam_limit = 3
    last_item_time = 0
    clock = pg.time.Clock()
    score = Score()
    tmr = 0
    
    key_lst = pg.key.get_pressed()    
    emys = []
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                beam = Beam(bird)
                beams.append(beam)
                beam_limit -= 1

        screen.blit(bg_img, [0, 0])
        x = bird.tm % 2400
        screen.blit(bird.bg_img, [-x, 0])
        screen.blit(bird.bg_img2, [-x + 1200, 0])
        screen.blit(bird.bg_img, [-x + 2400, 0])
        screen.blit(bird.img, bird.rct)
        if tmr % 20 == 0:
            emy = Enemy()
            emys.append(emy)
        for emy in emys:
             emy.update(screen) 
        score.score += 0.02
        score.update(screen)
        pg.display.update()
        bird.tm += 1
        
        current_time = pg.time.get_ticks()
        if current_time - last_item_time > ITEM_INTERVAL:
            items.append(Item((255, 0, 0), 10))
            last_item_time = current_time

        for item in items:
            item.update(screen)
            if bird.rct.colliderect(item.rct):
                beam_limit += 1
                items.remove(item)

        for i,emy in enumerate(emys):
            if beam is not None:
                if beam.rct.colliderect(emy.rct):  
                    emys[i]=None
                    pg.display.update()
        emys=[emy for emy in emys if emy is not None]
        
        for i,beam in enumerate(beams):
            if emy is not None:
                if emy.rct.colliderect(beam.rct):  # ビームと爆弾が衝突したら
                    beams[i]=None
                    pg.display.update()
        beams=[beam for beam in beams if beam is not None]
        if beam is not None:
             beam.update(screen)

        bird.update(screen)
        score.update(screen)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
