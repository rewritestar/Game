import pygame as pg
import sys
from pygame.locals import *
import math
import random

WHITE = (255,255,255)
BLACK = (0,0,0)

WIDTH = 800
HEIGHT = 600

mouse_x = WIDTH/2
mouse_y = HEIGHT/2

SCREEN_L = 0
SCREEN_R = 800
SCREEN_T = 0
SCREEN_B = 600

HERO_X = 350
HERO_Y = 365
HERO_LIFE = 100


RIGHT = 0
LEFT = 1


hr_x = 1200
hr_y = HERO_Y

hr_jy = 0
hr_sx = HERO_X
hr_d = RIGHT
hr_an = 0
hr_an_idx = 0
hr_life = HERO_LIFE
hr_gm = 0


jump = False
jump_v = [-50,-40,-30,-20,-15,-10,-5,5,10,15,20,30,40,50]
jump_vm = [-40,-30,-20,-15,-10,-5, -2, 2, 5,10,15,20,30,40]
JUMP_MAX = 100
j_idx = 0
jm_idx = 0

attack = False

key_spc = 0
tmr = 0
key_x = 0
bg_x = 0

idx_g = 1
stage = 1

MSG_X = 0

FIREBALL_MAX = 200
#MOB_MAX = [0,1,1,1]
MOB_MAX = [0,8,7,8]
MOB_CL = 0
MOB_LIFE = [0, 5,7,8]
mob_f = [False]*MOB_MAX[0]
mob_x = [0]*MOB_MAX[0]
mob_y = [410]*MOB_MAX[0]
mob_d = [LEFT]*MOB_MAX[0]
mob_life = [0]*MOB_MAX[0]
mob_tm = [0]*MOB_MAX[0]
mob_idx = 0
mob_jump = [False]*MOB_MAX[0]
mob_gm = [0]*MOB_MAX[0]
mob_rand = [0]*MOB_MAX[1]


fib_f = [False]*FIREBALL_MAX
fib_x = [0]*FIREBALL_MAX
fib_y = [0]*FIREBALL_MAX
fib_d = [RIGHT]*FIREBALL_MAX
fib_idx = 0
img_fib_rt = [None]*FIREBALL_MAX

bg_x = 0
bg_y = 0


img_mouse = pg.image.load("./images_game1/mouse.png")
img_bg = [
    pg.image.load("./images_game1/mobHunt_bg.png"),
    pg.image.load("./images_game1/base_bg.png")
    ]
img_hero = [
    pg.image.load("./images_game1/hero00.png"),
    pg.image.load("./images_game1/hero01.png"),
    pg.image.load("./images_game1/hero00.png"),
    pg.image.load("./images_game1/hero02.png"),
    pg.image.load("./images_game1/hero03.png"),
    pg.image.load("./images_game1/hero04.png"),
    pg.image.load("./images_game1/hero03.png"),
    pg.image.load("./images_game1/hero05.png")
    ]

img_fib = pg.image.load("./images_game1/fib.png")
img_mob = [
    pg.image.load("./images_game1/mob00.png"),
    pg.image.load("./images_game1/mob01.png"),
    pg.image.load("./images_game1/mob02.png"),
    pg.image.load("./images_game1/mob03.png"),
    pg.image.load("./images_game1/mob04.png"),
    pg.image.load("./images_game1/mob05.png"),
    pg.image.load("./images_game1/mob06.png"),
    pg.image.load("./images_game1/mob07.png")
    ]

img_itm = [
    pg.image.load("./images_game1/msg_bg.png"),
    pg.image.load("./images_game1/msg.png")
    ]
img_hp = [
    pg.image.load("./images_game1/hp_bar.png"),
    pg.image.load("./images_game1/hp_bar_r.png"),
    pg.image.load("./images_game1/hp_bar_mob.png")
    ]


MESSAGE = [
    None,
    "찢긴 일기장 조각 1                                                   숲을 걷다가, 그 길에서 우연히 누군가를 만나서, 그 누군가가 나를 알아봐 준다는 것은 기적 같은 일이다. 이 숲은 누구도 알 수 없는 곳이기에. 그래서 더욱 간절해진다.",
    "찢긴 일기장 조각 2                                                   몇 번째 손님일까. 십만 번의 숫자를 넘긴 이후로는 세는 것이 의미 없어 보였다. 그분들은 나의 존재를 전혀 모른다. 시간 관리자는 이렇게 없는 존재로서 살아가는 것이지만, 가끔씩은 그 사실이 못 견디게 힘들다.",
    "찢긴 일기장 조각 3                                                   세월이 흐르고, 나이를 먹는다는 것이 나에게는 전혀 의미가 없다. 시간의 흐름도 결국 타인이 바라봐 주어야만 흘러갈 수 있는 것이다. 늙는다는 것은 더할 나위 없는 기쁨이다."
]


scrn_btn_pressed = False

def draw_dlg_txt(txt_o,screen,x,y,ch_n,col):
    t_x = x
    t_y = y
    font = pg.font.SysFont("새굴림", 20, False, False)
    txt = ""
    escape = math.ceil(len(txt_o)/ch_n)
    for i in range(escape):
        txt = txt_o[ch_n*i:ch_n+ch_n*i]
        text = font.render(txt, True, col)
        screen.blit(text, [t_x, t_y])
        t_y += 25

def animation():
    global mob_y, jm_idx
    for m in range(MOB_MAX[stage]):
        if mob_jump[m] and mob_f[m]:
            mob_y[m] += jump_vm[jm_idx]

    jm_idx = (jm_idx+1)%len(jump_vm)
        
        
            
            

def move_mob(scrn):
    global mob_idx, mob_gm
    
    for m in range(MOB_MAX[stage]):
        if mob_f[m]:
            if mob_d[m] == LEFT and mob_x[m] > 0:
                mob_x[m] -= 10
            elif mob_d[m] == RIGHT and mob_x[m] < 2320:
                mob_x[m] += 10
            if tmr%5 == 0:
                mob_d[m] = random.choice([LEFT, RIGHT])


            #몬스터 타격감
            mob_gm[m] -= 1
            
            png = mob_idx+mob_d[m]+mob_rand[m]
            mw = img_mob[png].get_width()
            
            if mob_gm[m] < 0:
                mob_gm[m] = 0

            if mob_gm[m] % 2 == 0:
                scrn.blit(img_mob[png], [mob_x[m] + bg_x, mob_y[m]])
                
            hp_mob_x = mob_x[m] + bg_x + mw/2 - 50
            hp_m_life = 98/MOB_LIFE[stage]*mob_life[m]
            
            scrn.blit(img_hp[2], [hp_mob_x, 490])
            pg.draw.rect(scrn, BLACK, [hp_mob_x + 1 + hp_m_life,491, 98 - hp_m_life, 8],0)
            
            

def set_mob():
    global mob_f, mob_x, mob_y, mob_d, mob_life, mob_jump, mob_idx, mob_gm, mob_rand


    mob_f = [False]*MOB_MAX[stage]
    mob_x = [0]*MOB_MAX[stage]
    mob_y = [480]*MOB_MAX[stage]
    mob_d = [LEFT]*MOB_MAX[stage]
    mob_life = [stage]*MOB_MAX[stage]
    mob_jump = [False]*MOB_MAX[stage]
    mob_gm = [0]*MOB_MAX[stage]
    mob_rand = [0]*MOB_MAX[stage]
    
    for m in range(MOB_MAX[stage]):
        mob_f[m] = True
        mob_x[m] = random.randint(0, 2320)
        mob_d[m] = random.choice([LEFT, RIGHT])
        mob_life[m] = MOB_LIFE[stage]
        
        if stage == 1:
            mob_rand[m] = random.choice([0,2])
            mob_idx = 0
        else:
            mob_idx = stage*2
            if stage == 2:
                mob_jump[m] = True
            if stage == 3:
                mob_jump[m] = random.choice([False, True])

        mh = img_mob[mob_idx+mob_rand[m]].get_height()        
        mob_y[m] = 480 - mh


def move_fireBall(scrn):
    global MOB_CL, MSG_X
    for f in range(FIREBALL_MAX):
        if fib_f[f]:
            if fib_d[f] == LEFT:
                fib_x[f] -= 40    
            else:
                fib_x[f] += 40
            if fib_x[f] > SCREEN_R+img_fib.get_height() or fib_x[f] < SCREEN_L-img_fib.get_height():
                fib_f[f] = False
            scrn.blit(img_fib_rt[f], [fib_x[f],fib_y[f]])
            for m in range(MOB_MAX[stage]):
                if mob_f[m]:
                    fw = img_fib.get_width()/2
                    fh = img_fib.get_height()/2
                    mw = img_mob[mob_idx+mob_rand[m]].get_width()/2
                    mh = img_mob[mob_idx+mob_rand[m]].get_height()/2
                    
                    m_mx = mob_x[m] + bg_x + mw
                    m_my = mob_y[m] + mh
                    f_mx = fib_x[f] + fw
                    f_my = fib_y[f] + fh
                  
                    if (f_mx-m_mx)*(f_mx-m_mx) + (f_my-m_my)*(f_my-m_my) < (fw+mw) * (fw+mw):
                        mob_life[m] -= 1
                        fib_f[f] = False
                        #mob 깜박임 액션
                        mob_gm[m] = 4
                        if mob_life[m] == 0:
                            mob_f[m] = False
                            MOB_CL += 1
                            MSG_X = mob_x[m]
                            

def set_fireBall():
    global fib_idx, fib_d
    fib_f[fib_idx] = True
    fib_x[fib_idx] = hr_sx
    fib_y[fib_idx] = hr_y+40
    if hr_d == LEFT:
        fib_d[fib_idx] = LEFT
        img_fib_rt[fib_idx] = pg.transform.rotozoom(img_fib, 180, 1.0)
    else:
        fib_d[fib_idx] = RIGHT
        img_fib_rt[fib_idx] = pg.transform.rotozoom(img_fib, 0, 1.0)
    fib_idx = (fib_idx+1)%FIREBALL_MAX
    
        
def draw_bg(scrn):
    global bg_x
    bg_x = HERO_X - hr_x
    
    if bg_x <= -1600:
        bg_x = -1600
    elif bg_x >= 0:
        bg_x = 0
    scrn.blit(img_bg[0], [bg_x,0])
    

def hero_move(scrn,key):
    global hr_x, hr_y, hr_sx, hr_d, hr_an, hr_an_idx, hr_life, hr_gm
    global idx_g, tmr, stage, bg_x, key_x, jump
    
    if key[K_RIGHT] and hr_x < 2320:
        hr_x += 20
        hr_d = RIGHT
    if key[K_LEFT] and hr_x > 0:
        hr_x -= 20
        hr_d = LEFT
    if key[K_UP] and not jump:
        jump = True

    key_x = (key_x+1) * key[K_x]
    if key_x % 20 == 1:
        set_fireBall()

    if key[K_RIGHT] or key[K_LEFT]:
        hr_an = hr_d*4 + (hr_an_idx%4)
        if not jump:
            #애니메이션 속도 조
            if tmr % 2 == 0:
                hr_an_idx += 1

    #몬스터와 접촉했을때
    for m in range(MOB_MAX[stage]):
        if mob_f[m]:
            hw = img_hero[hr_an].get_width()/2
            hh = img_hero[hr_an].get_height()/2
            mw = img_mob[mob_idx+mob_rand[m]].get_width()/2
            mh = img_mob[mob_idx+mob_rand[m]].get_height()/2

            h_mx = hr_sx+hw
            h_my = hr_y+hh
            m_mx = mob_x[m]+bg_x + mw
            m_my = mob_y[m] + mh

                
            if (h_mx-m_mx)*(h_mx-m_mx) + (h_my-m_my)*(h_my-m_my) < (hw+mw)*(hw+mw) and hr_gm == 0:                    
                hr_life -= 10
                if hr_life < 0:
                    hr_life = 0
                    tmr = 0
                    idx_g = 4
                    return
                hr_gm = 20


    hr_sx = hr_x+bg_x

    #몬스터 접촉
    if hr_gm > 0:
            hr_gm -= 1
    if hr_gm % 2 == 0:
        scrn.blit(img_hero[hr_an], [hr_sx, hr_y])
    #hp 그리기
    scrn.blit(img_hp[0], [30, 510])
    life_hp = 2.4*hr_life
    pg.draw.rect(scrn, BLACK, [35+life_hp,515,240-life_hp,17], 0)

    #hp 깜박거림
    if hr_gm % 15 > 7:
        scrn.blit(img_hp[1], [30, 510])
        
    #hp 시간에 따라 증가
    if tmr % 40 == 0 and hr_life <= HERO_LIFE:
        hr_life += 1
    
    

def hero_jump():
    global hr_y, jump, j_idx
    if jump:
        hr_y += jump_v[j_idx]
        j_idx += 1
        if j_idx == len(jump_v):
            j_idx = 0
            jump = False


def btn_click():
    global scrn_btn_pressed
    scrn_btn_pressed = True


def message(scrn,x):
    global idx_g, stage
    scrn.blit(img_itm[1], [x+bg_x,410])
    if hr_sx >= x+bg_x-20 and hr_sx <= x+bg_x+20:
        scrn.blit(img_itm[0], [0,0])
        tx = MESSAGE[stage]
        draw_dlg_txt(tx,scrn,140,70,31,BLACK)
        if scrn_btn_pressed:
            stage += 1
            idx_g = 1
        if stage > 3:
            idx_g = 3

    
def main():
    global mouse_x, mouse_y, left_m, fill, right_m
    global idx_g, tmr, stage, bg_x, jm_idx, hr_x, hr_y, hr_gm, hr_life, j_idx, jump
    global scrn_btn_pressed
    global MOB_CL, mob_idx
    pg.init()
    screen = pg.display.set_mode([WIDTH, HEIGHT])
    pg.display.set_caption("Abandoned Forest")
    clock = pg.time.Clock()
        
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONUP:
                btn_click()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F1:
                    screen = pg.display.set_mode([WIDTH, HEIGHT], pg.FULLSCREEN)
                if event.key == pg.K_ESCAPE:
                    screen = pg.display.set_mode([WIDTH, HEIGHT])
        tmr += 1
        key = pg.key.get_pressed()

        screen.blit(img_bg[0], [0,0])
        screen.blit(img_bg[1],[0,0])


        #초기화
        if idx_g == 1:
            tmr = 0
            hr_x = 1200
            hr_y = HERO_Y
            hr_gm = 0
            j_idx = 0
            jump = False
            jm_idx = 0
            MOB_CL = 0
            set_mob()
            idx_g = 2
            
            
        #몬스터 게임  
        if idx_g == 2:
            draw_bg(screen)
            move_mob(screen)
            hero_jump()
            move_fireBall(screen)
            hero_move(screen, key)
            animation()
                        
            if MOB_CL == MOB_MAX[stage]:
                message(screen, MSG_X)

           
        #게임 클리어
        if idx_g == 3:
            enter = "                              " 
            tx = "숲 곳곳마다 튀어나오는 몬스터를 무찌른 후, 주위를 둘러보자 숲 속 한 가운데에 어떤 낡은 오두막 같은 집이 있었다."
            tx += enter*2 + " "
            tx += "찢긴 일기장 조각..그것은 누구의 것이었을까?"
            tx += enter + "                             "
            tx += "이런 위험한 곳에 과연 누군가가 있을까?"
            tx += enter*2 + "   "
            tx += "가만히 있어도 답은 나오지 않았기에, 나는 위험을 무릅쓰고 더 깊은 곳으로 향했다. 찢긴 일기장들,.. 이 모든 진실을 알기 위해."
            draw_dlg_txt(tx,screen,50,50,42,WHITE)


        #게임 오버
        if idx_g == 4:
            if tmr < 30 * 3:
                font = pg.font.SysFont("새굴림", 60, False, False)
                txt = "GAME OVER"
                text = font.render(txt, True, (218,80,80))
                screen.blit(text, [WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2])
            else:
                hr_life = HERO_LIFE
                stage = 1
                idx_g = 1

        pg.mouse.set_visible(False)
        screen.blit(img_mouse, pg.mouse.get_pos())
                
        scrn_btn_pressed = False
        pg.display.update()
        clock.tick(15)


if __name__ == "__main__":
    main()
