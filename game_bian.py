from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
from game_skin import install, should_leave

import random
import time
import threading
import pygame
import policy_animation as mythread
from sys import exit

screen_width = 1400
screen_height = 700
policy_alpha = 70
arrow_alpha = 100

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SCALED)
pygame.display.set_caption('Secret Bian')

background_image_filename = str(BASE_DIR / 'assets/bian/background.png')
blue_flag_image = str(BASE_DIR / 'assets/bian/blue.png')
green_flag_image = str(BASE_DIR / 'assets/bian/green.png')
bullet_image = str(BASE_DIR / 'assets/bian/execute.png')
investigation_image = str(BASE_DIR / 'assets/bian/search.png')
up_arrow_image = str(BASE_DIR / 'assets/bian/arrow.png')
yes_btn_image = str(BASE_DIR / 'assets/bian/yes.png')
no_btn_image = str(BASE_DIR / 'assets/bian/no.png')
bian_image = str(BASE_DIR / 'assets/bian/leader.png')
dead_image = str(BASE_DIR / 'assets/bian/dead.png')

background = pygame.image.load(background_image_filename).convert_alpha()
blue_flag  = pygame.image.load(blue_flag_image).convert_alpha()
green_flag = pygame.image.load(green_flag_image).convert_alpha()
blue_flag_alpha  = pygame.image.load(blue_flag_image).convert_alpha()
green_flag_alpha = pygame.image.load(green_flag_image).convert_alpha()
bullet_alpha     = pygame.image.load(bullet_image).convert_alpha()
investigation_alpha = pygame.image.load(investigation_image).convert_alpha()
bian = pygame.image.load(bian_image).convert_alpha()
up_arrow = pygame.image.load(up_arrow_image).convert_alpha()
yes_btn = pygame.image.load(yes_btn_image).convert_alpha()
no_btn = pygame.image.load(no_btn_image).convert_alpha()
dead = pygame.image.load(dead_image).convert_alpha()

blue_flag_s = pygame.transform.scale(blue_flag, (60, 45))
green_flag_s = pygame.transform.scale(green_flag, (60, 45))

left_arrow = pygame.transform.rotate(up_arrow, 90)
down_arrow = pygame.transform.rotate(up_arrow, 180)
right_arrow = pygame.transform.rotate(up_arrow, 270)
up_arrow2 = pygame.image.load(up_arrow_image).convert_alpha()
left_arrow2 = pygame.transform.rotate(up_arrow, 90)
down_arrow2 = pygame.transform.rotate(up_arrow, 180)
right_arrow2 = pygame.transform.rotate(up_arrow, 270)

up_arrow2.set_alpha(arrow_alpha)
left_arrow2.set_alpha(arrow_alpha)
down_arrow2.set_alpha(arrow_alpha)
right_arrow2.set_alpha(arrow_alpha)
blue_flag_alpha.set_alpha(policy_alpha)
green_flag_alpha.set_alpha(policy_alpha)
bullet_alpha.set_alpha(policy_alpha)
investigation_alpha.set_alpha(policy_alpha)

p1  = u"小鷹"
p2  = u"小賣"
p3  = u"小熊"
p4  = u"小倉"
p5  = u"小力"
p6  = u"小站"
p7  = u"小魚"
p8  = u"小鯨"
p9  = u"小冏"
p10 = u"小牆"

p1_loc  = (990, 675)
p2_loc  = (690, 675)
p3_loc  = (390, 675)
p4_loc  = (0, 490)
p5_loc  = (0, 190)
p6_loc  = (390, 0)
p7_loc  = (690, 0)
p8_loc  = (990, 0)
p9_loc  = (1360, 190)
p10_loc = (1360, 490)

r1_loc  = (920, 655)
r2_loc  = (620, 655)
r3_loc  = (320, 655)
r4_loc  = (0, 435)
r5_loc  = (0, 135)
r6_loc  = (320, 0)
r7_loc  = (620, 0)
r8_loc  = (920, 0)
r9_loc  = (1340, 135)
r10_loc = (1340, 435)

#id 0~2, left to right or up to down
po1_loc  = [(850, 550), (950, 550), (1050, 550)]
po2_loc  = [(550, 550), (650, 550), (750, 550)]
po3_loc  = [(250, 550), (350, 550), (450, 550)]
po4_loc  = [(100, 355), (100, 430), (100, 505)]
po5_loc  = [(100, 130), (100, 205), (100, 280)]
po6_loc  = [(250, 60), (350, 60), (450, 60)   ]
po7_loc  = [(550, 60), (650, 60), (750, 60)   ]
po8_loc  = [(850, 60), (950, 60), (1050, 60)  ]
po9_loc  = [(1190, 130), (1190, 205), (1190, 280)]
po10_loc = [(1190, 355), (1190, 430), (1190, 505)]

status_loc   = (390, 250)
broken_loc   = (650, 330)
b_status_loc = (650, 435)

draw_policy_thread = mythread.mythread(1, screen, blue_flag_image, green_flag_image)

green_win_num = 0
blue_win_num = 0
player_num = 10
policy_card_ini_num = 3
broken_num = 0
green_policy_num = 0
blue_policy_num = 0
already_set_policy_num = 0
# 3: triple score, 0: ini
triple_s = 0
president = -1
chancellor = -1
pre_president = -1
pre_chancellor = -1
# -2, ini, No human. 0~9, human player id
human_player = -2
already_set_broken = 0
broken_current = 0
#0: ini. 1: blue win, bian is dead
#2: blue win, blue policy 5
#3: green win, bian is chancellor and green policy >= 4
#4: green win, green policy 6
victory_result = 0
victory_counted = False
kill_player = -1
inv_player = -1
human_inv = -1
#0: blue, 1: green, -1: None policy(ini)
policy_current = -1
#mode == 0, ini. mode == 1, after select president candidate
#mode == 2, for human select chancellor.
#mode == 3, agree chancellor or not.
#mode == 4, president and chancellor candidate is done.
#mode == 5, election result
#mode == 6, select policy, human president
#mode == 7, select policy, computer president
#mode == 8, select policy, human chancellor
#mode == 9, select policy, computer chancellor
#mode ==10, enact policy result
#mode ==11, president power, human president
#mode ==12, president power, computer president
#mode ==13, check if bian for killing (part2)
#mode ==14, kill part 3
#mode ==15, investigation result
#mode ==16, human player is chancellor candidate
#mode ==17, check if bian to be chancellor candidate
#mode ==69, final result
mode = 0

#positive: blue party, negative: green party
party_score = []
# 0: blue policy, 1: green policy, blue : green = 10 : 19
policy_card_box = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
policy_card_loc = [po1_loc, po2_loc, po3_loc, po4_loc, po5_loc, po6_loc, po7_loc, po8_loc, po9_loc, po10_loc]
player_name_list = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
player_name_loc  = [p1_loc, p2_loc, p3_loc, p4_loc, p5_loc, p6_loc, p7_loc, p8_loc, p9_loc, p10_loc]
role_loc  = [r1_loc, r2_loc, r3_loc, r4_loc, r5_loc, r6_loc, r7_loc, r8_loc, r9_loc, r10_loc]
# 2: bian, 1: green, 0:blue
player_role = [0] * player_num
arrow_loc = list(player_name_loc)
talk_loc = [0] * player_num
yes_btn_loc = [0] * player_num
no_btn_loc = [0] * player_num
#1: Accepted, 0: No
election_ch = [0] * player_num
#1 : policy out, 0: NOT out
out = [0] * policy_card_ini_num
# 1: live, 0: dead
player_live = [1] * player_num
# -2 : unknown, 0~9 : player id is bian
know_bian = [-2] * player_num
# -1: unknown, 1: NOT bian
not_bian = [-1] * player_num

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

policy_interval_gap = 100

def write(msg="pygame is cool", color= (0,0,0), size = 14):
    myfont = pygame.font.Font(str(BASE_DIR / "assets/fonts/wqy-zenhei.ttf"), size)
    mytext = myfont.render(msg, True, color)
    mytext = mytext.convert_alpha()
    return mytext 

def fill_background():
    for y in range(0, screen_height, background.get_height()):
        for x in range(0, screen_width, background.get_width()):
            screen.blit(background, (x, y))

def draw_green_table():
    row_num = 3
    width = 1
   
    (mid_w, mid_h) = (screen_width/2, screen_height/2)
    x = mid_w + policy_interval_gap - 1
    y = mid_h - green_flag.get_height() - 1

    #row line
    for i in range(0, row_num):
        pygame.draw.line(screen, BLACK, (x, y + i*(green_flag.get_height()+1)), (x + 3*(green_flag.get_width()+1), y + i*(green_flag.get_height()+1)), width)
    
    #column line
    for i in range(0, row_num+1):
        pygame.draw.line(screen, BLACK, (x + i*(green_flag.get_width()+1), y), (x + i*(green_flag.get_width()+1), y + 2*(green_flag.get_height()+1)), width)
        
    victory_x = x + 2*(green_flag.get_width()+1) + 1
    victory_y = y + green_flag.get_height()+2
    
    pre_victory_x = victory_x-1-green_flag.get_width()
    
    x4 = pre_victory_x-1-green_flag.get_width()
    
    x3 = x + (row_num - 1)*(green_flag.get_width()+1)+1
    
    pygame.draw.rect(screen, RED, (pre_victory_x, victory_y, green_flag.get_width(), green_flag.get_height()))
    pygame.draw.rect(screen, RED, (victory_x, victory_y, green_flag.get_width(), green_flag.get_height()))
    
    screen.blit(bullet_alpha, (x3, y))
    screen.blit(investigation_alpha, (x4, victory_y))
    screen.blit(bullet_alpha, (pre_victory_x, victory_y))
    screen.blit(green_flag_alpha, (victory_x, victory_y))
    
def draw_blue_table():
    row_num = 3
    width = 1
   
    (mid_w, mid_h) = (screen_width/2, screen_height/2)
    x = mid_w - policy_interval_gap - 3*(blue_flag.get_width() + 1)
    y = mid_h - blue_flag.get_height() - 1

    #row line
    for i in range(0, row_num-1):
        pygame.draw.line(screen, BLACK, (x, y + i*(blue_flag.get_height()+1)), (x + 3*(blue_flag.get_width()+1), y + i*(blue_flag.get_height()+1)), width)
    
    pygame.draw.line(screen, BLACK, (x, y + 2*(blue_flag.get_height()+1)), (x + 2*(blue_flag.get_width()+1), y + 2*(blue_flag.get_height()+1)), width)
    
    #column line
    for i in range(0, row_num):
        pygame.draw.line(screen, BLACK, (x + i*(blue_flag.get_width()+1), y), (x + i*(blue_flag.get_width()+1), y + 2*(blue_flag.get_height()+1)), width)
    
    pygame.draw.line(screen, BLACK, (x + row_num*(blue_flag.get_width()+1), y), (x + row_num*(blue_flag.get_width()+1), y + blue_flag.get_height()+1), width)
    
    victory_x = x + blue_flag.get_width()+1 + 1
    victory_y = y + blue_flag.get_height()+2
    
    screen.blit(blue_flag_alpha, (victory_x, victory_y))
    
def draw_policy_table():
    draw_blue_table()
    draw_green_table()

def role_to_image(rid):
    if 0 == rid:
        return blue_flag_s
    elif 1 == rid:
        return green_flag_s
    elif 2 == rid:
        return bian
    
def draw_player_name():
    global player_name_list, president, chancellor, player_role, human_inv

    # if human role is green party
    if 1 == player_role[human_player]:
        show_green_party = 1
    else:
        show_green_party = 0
    
    for i in range(player_num):
        if 0 == player_live[i]:
            screen.blit(dead, arrow_loc[i])
    
        if victory_result > 0:
            screen.blit(role_to_image(player_role[i]), role_loc[i])
        elif i == human_player:
            screen.blit(role_to_image(player_role[i]), role_loc[i])
        elif 1 == show_green_party and 1 == player_role[i]:
            screen.blit(role_to_image(player_role[i]), role_loc[i])
        elif i == human_inv:
            if 0 == player_role[i]:
                screen.blit(blue_flag_s, role_loc[i])
            else:
                screen.blit(green_flag_s, role_loc[i])
            
        if i == president:
            if 0 <= president <= 2 or 5 <= president <= 7:
                screen.blit(write(player_name_list[i]+u" 總統", BLACK, 20), (player_name_loc[i][0], player_name_loc[i][1]))
            else:
                screen.blit(write(player_name_list[i], BLACK, 20), (player_name_loc[i][0], player_name_loc[i][1]))
                screen.blit(write(u"總統", BLACK, 20), (player_name_loc[i][0], player_name_loc[i][1]+20))
        elif i == chancellor:
            if 0 <= chancellor <= 2 or 5 <= chancellor <= 7:
                screen.blit(write(player_name_list[i]+u" 院長", BLACK, 20), (player_name_loc[i][0], player_name_loc[i][1]))
            else:
                screen.blit(write(player_name_list[i], BLACK, 20), (player_name_loc[i][0], player_name_loc[i][1]))
                screen.blit(write(u"院長", BLACK, 20), (player_name_loc[i][0], player_name_loc[i][1]+20))
        else:
            screen.blit(write(player_name_list[i], BLACK, 20), (player_name_loc[i][0], player_name_loc[i][1]))

# find human player
def findhp(pnlist):
    for i in range(player_num):
        if pnlist[i] == u"小鷹":
            return i

def id_to_arrow_image(id):
    if 0 <= id <= 2:
        return down_arrow
    elif 3 <= id <= 4:
        return left_arrow
    elif 5 <= id <= 7:
        return up_arrow
    elif 8 <= id <= 9:
        return right_arrow

def id_to_arrow_alpha_image(id):
    if 0 <= id <= 2:
        return down_arrow2
    elif 3 <= id <= 4:
        return left_arrow2
    elif 5 <= id <= 7:
        return up_arrow2
    elif 8 <= id <= 9:
        return right_arrow2        
            
def draw_select_chancellor():
    screen.blit(write(u"%s 總統，您要選誰擔任院長呢？"%p1, BLACK, 20), status_loc)
    
    (MouseX, MouseY) = pygame.mouse.get_pos()
    
    for i in range(player_num):
        if 0 == player_live[i]:
            continue
        if i in [president, pre_president, pre_chancellor]:
            continue
        if arrow_loc[i][0] <= MouseX <= arrow_loc[i][0] + id_to_arrow_image(i).get_width() and arrow_loc[i][1] <= MouseY <= arrow_loc[i][1] + id_to_arrow_image(i).get_height():
            screen.blit(id_to_arrow_image(i), arrow_loc[i])
        else:
            screen.blit(id_to_arrow_alpha_image(i), arrow_loc[i])
            
def select_chancellor_ai():
    candidate = []
    
    # if blue party
    if 0 == player_role[president]:
        for i in range(player_num):
            if 0 == player_live[i]:
                continue
            if i in [president, pre_president, pre_chancellor]:
                continue
            elif party_score[president][i] < -1:
                continue
            elif -1 == party_score[president][i]:
                candidate.append(i)
            elif 0 == party_score[president][i]:
                candidate.extend([i]*3)
            elif 1 == party_score[president][i]:
                candidate.extend([i]*9)
            else: # party_score[i] > 1
                candidate.extend([i]*27)
    # ig green party and know bian
    elif know_bian[president] >= 0:
        return know_bian[president]
    # if green party
    elif 1 == player_role[president]:
        for i in range(player_num):
            if 0 == player_live[i]:
                continue
            if i in [president, pre_president, pre_chancellor]:
                continue
            elif green_policy_num >= 4 and 1 == not_bian[i]:
                continue
            # green can know green
            elif green_policy_num >= 4 and 1 == player_role[i]:
                continue
            elif party_score[president][i] > 1:
                continue
            elif 1 == party_score[president][i]:
                candidate.append(i)
            elif 0 == party_score[president][i]:
                candidate.extend([i]*3)
            elif -1 == party_score[president][i]:
                candidate.extend([i]*9)
            else: # party_score[i] < -1
                candidate.extend([i]*27)
    # if bian
    else:
        for i in range(player_num):
            if 0 == player_live[i]:
                continue
            if i in [president, pre_president, pre_chancellor]:
                continue
            elif party_score[president][i] > 1:
                continue
            elif 1 == party_score[president][i]:
                candidate.append(i)
            elif 0 == party_score[president][i]:
                candidate.extend([i]*3)
            elif -1 == party_score[president][i]:
                candidate.extend([i]*9)
            else: # party_score[i] < -1
                candidate.extend([i]*27)
    
    if 0 == len(candidate):
        for i in range(player_num):
            if 0 == player_live[i]:
                continue
            if i in [president, pre_president, pre_chancellor]:
                continue
            else:
                candidate.append(i)
    
    random.shuffle(candidate)
    
    return candidate[0]

def ini_arrow_loc():
    global arrow_loc
    
    for i in range(player_num):
        if 0 <= i <= 2:
            arrow_loc[i] = (arrow_loc[i][0], arrow_loc[i][1]-50)
        elif 3 <= i <= 4:
            arrow_loc[i] = (arrow_loc[i][0]+50, arrow_loc[i][1])
        elif 5 <= i <= 7:
            arrow_loc[i] = (arrow_loc[i][0], arrow_loc[i][1]+30)
        elif 8 <= i <= 9:
            arrow_loc[i] = (arrow_loc[i][0]-50, arrow_loc[i][1])

def draw_button(loc, str, image = yes_btn, size = 16):
    (mouseX, mouseY) = pygame.mouse.get_pos()
        
    fontx = loc[0]+ 47 - int(len(str)/2*12)
    fonty = loc[1]+15
    screen.blit(image, loc)
    if loc[0] <= mouseX <= loc[0]+image.get_width() and loc[1] <= mouseY <= loc[1]+image.get_height():
        screen.blit(write(str, BLUE, size), (fontx, fonty))
    else:
        screen.blit(write(str, BLACK, size), (fontx, fonty))            
            
def yes_no_btn():
    global arrow_loc, yes_btn_loc, no_btn_loc
    
    for i in range(player_num):
        if 0 <= i <= 2:
            yes_btn_loc[i] = (arrow_loc[i][0]-100, arrow_loc[i][1]-30)
            no_btn_loc[i] = (arrow_loc[i][0]+25, arrow_loc[i][1]-30)
            talk_loc[i] = (arrow_loc[i][0]-100, arrow_loc[i][1]-30)
        elif 3 <= i <= 4:
            yes_btn_loc[i] = (arrow_loc[i][0]+20, arrow_loc[i][1]-50)
            no_btn_loc[i] = (arrow_loc[i][0]+20, arrow_loc[i][1]+25)
            talk_loc[i] = (arrow_loc[i][0]+20, arrow_loc[i][1]-15)
        elif 5 <= i <= 7:
            yes_btn_loc[i] = (arrow_loc[i][0]-100, arrow_loc[i][1]+30)
            no_btn_loc[i] = (arrow_loc[i][0]+25, arrow_loc[i][1]+30)
            talk_loc[i] = (arrow_loc[i][0]-100, arrow_loc[i][1]+30)
        elif 8 <= i <= 9:
            yes_btn_loc[i] = (arrow_loc[i][0]-95, arrow_loc[i][1]-50)
            no_btn_loc[i] = (arrow_loc[i][0]-95, arrow_loc[i][1]+25)
            talk_loc[i] = (arrow_loc[i][0]-200, arrow_loc[i][1]+15)
        
def ini_loc():
    ini_arrow_loc()
    yes_no_btn()

def yes_no_ai(i, role):
    
    score = 0
    ele = 0
    
    # if blue
    if 0 == role:
        b = 1
        g = 0
    # if green
    else:
        b = 0
        g = 1
    
    if party_score[i][president] >= 2:
        score += 2
    elif party_score[i][president] <= -2:
        score -= 2
    else:
        score += party_score[i][president]
        
    if party_score[i][chancellor] >= 2:
        score += 2
    elif party_score[i][chancellor] <= -2:
        score -= 2
    else:
        score += party_score[i][chancellor]   
    
    r = random.randint(1, 16)
    if score >= 4:
        ele = b
    elif 3 == score:
        if r > 1:
            ele = b
        else:
            ele = g
    elif 2 == score:
        if r > 2:
            ele = b
        else:
            ele = g
    elif 1 == score:
        if r > 4:
            ele = b
        else:
            ele = g
    elif 0 == score:
        if r > 8:
            ele = b
        else:
            ele = g
    elif -1 == score:
        if r > 12:
            ele = b
        else:
            ele = g
    elif -2 == score:
        if r > 14:
            ele = b
        else:
            ele = g
    elif -3 == score:
        if r > 15:
            ele = b
        else:
            ele = g
    elif -4 <= score:
        ele = g
    
    return ele
    
def election_ai():
    global election_ch
    
    score = 0
    
    for i in range(player_num):
        if 0 == player_live[i]:
            continue
        elif i in [president, chancellor]:
            election_ch[i] = 1
        elif i == human_player:
            continue
        else:
            election_ch[i] = yes_no_ai(i, player_role[i])

def election_result():
    global election_ch, broken_num, already_set_broken, broken_current
    
    y_num = 0
    n_num = 0
    
    for i in range(player_num):
        if 0 == player_live[i]:
            continue
        if 1 == election_ch[i]:
            draw_vote_result(i, True)
            y_num += 1
        else:
            draw_vote_result(i, False)
            n_num += 1
            
    if y_num > n_num:
        screen.blit(write(u"同意：%d票，否決：%d票， %s 就任總統， %s 就任院長，通過"%(y_num, n_num, player_name_list[president], player_name_list[chancellor]), BLACK, 20), status_loc)
        if 0 == already_set_broken:
            broken_num = 0
            broken_current = 0
            already_set_broken = 1
    else:
        screen.blit(write(u"同意：%d票，否決：%d票，政治協商破局"%(y_num, n_num), BLACK, 20), status_loc)
        if 0 == already_set_broken:
            broken_num += 1
            broken_current = 1
            already_set_broken = 1
            
    draw_button(b_status_loc,u"繼續", yes_btn)
    
def draw_broken():
    global broken_num, green_win_num, blue_win_num
    
    if broken_num > 0:
        screen.blit(write(u"破局 %d 次"%broken_num, BLACK, 20), broken_loc)
    
    if -2 == human_player:
        (gx, gy) = (broken_loc[0], broken_loc[1]-40)
        (bx, by) = (broken_loc[0], broken_loc[1]+40)
    
        screen.blit(write(u"綠營勝%d次"%green_win_num, BLACK, 20), (gx, gy))
        screen.blit(write(u"藍營勝%d次"%blue_win_num, BLUE, 20), (bx, by))

def president_enact_ai():
    global out, triple_s
    
    g_num = 0
    b_num = 0
    out_select = 0
    
    for i in range(policy_card_ini_num):
        # if blue
        if 0 == player_role[president]:
            if 1 == policy_card_box[i]:
                out_select = i
        else: # green
            if 0 == policy_card_box[i]:
                out_select = i
        
    out[out_select] = 1
    
    for i in range(policy_card_ini_num):
        # if blue
        if i == out_select:
            continue
        if 0 == policy_card_box[i]:
            b_num += 1
        else:
            g_num += 1
    
    if 1 == b_num and 1 == g_num:
        triple_s = 3

def chancellor_enact_ai():
    global out
    
    out_select = 0
    
    if 1 == out[0]:
        out_select = 1
    
    for i in range(policy_card_ini_num):
        if 1 == out[i]:
            continue
        # if blue
        if 0 == player_role[chancellor]:
            if 1 == policy_card_box[i]:
                out_select = i
        else: # green
            if 0 == policy_card_box[i]:
                out_select = i
                
    out[out_select] = 1
    
    enact_policy_from_policy_card()

def policy_card_id_to_image(id):
    if 0 == policy_card_box[id]:
        return blue_flag
    else: # 1 == policy_card_box[id]
        return green_flag
    
def draw_policy():
    global out

    rect_width = 2
    
    i = 0
    
    (mouseX, mouseY) = pygame.mouse.get_pos()
    
    for j in range(policy_card_ini_num):
        if 1 == out[j]:
            continue
        else:
            screen.blit(policy_card_id_to_image(j), policy_card_loc[human_player][i])
            
            if policy_card_loc[human_player][i][0] <= mouseX <= policy_card_loc[human_player][i][0]+policy_card_id_to_image(j).get_width() and policy_card_loc[human_player][i][1] <= mouseY <= policy_card_loc[human_player][i][1]+policy_card_id_to_image(j).get_height():
                pygame.draw.rect(screen, RED, (policy_card_loc[human_player][i][0], policy_card_loc[human_player][i][1], policy_card_id_to_image(j).get_width(), policy_card_id_to_image(j).get_height()), rect_width)
                
                start1_loc = policy_card_loc[human_player][i]
                end1_loc = (policy_card_loc[human_player][i][0]+policy_card_id_to_image(j).get_width(), policy_card_loc[human_player][i][1]+policy_card_id_to_image(j).get_height())
                start2_loc = (policy_card_loc[human_player][i][0], policy_card_loc[human_player][i][1]+policy_card_id_to_image(j).get_height())
                end2_loc = (policy_card_loc[human_player][i][0]+policy_card_id_to_image(j).get_width(), policy_card_loc[human_player][i][1])
                
                pygame.draw.line(screen, RED, start1_loc, end1_loc, rect_width)
                pygame.draw.line(screen, RED, start2_loc, end2_loc, rect_width)
            
            i += 1
    
def president_enact_human():
    screen.blit(write(u"%s 總統，您要排除哪個政策？"%player_name_list[president], BLACK, 20), status_loc)
    
    draw_policy()

def chancellor_enact_human():
    screen.blit(write(u"%s 院長，您要排除哪個政策？"%player_name_list[chancellor], BLACK, 20), status_loc)
    
    draw_policy()

def enact_policy_from_policy_card():
    global policy_card_box, out, policy_current
    
    for i in range(policy_card_ini_num):
        if 0 == out[i]:
            policy_current = policy_card_box[i]
            break

def draw_blue_policy(policy_num):
    if policy_num < 1:
        return
    for i in range(policy_num):
        screen.blit(blue_flag, mythread.b_loc[i])

def draw_green_policy(policy_num):
    if policy_num < 1:
        return
    for i in range(policy_num):
        screen.blit(green_flag, mythread.g_loc[i])
            
def draw_all_policy():
    global blue_policy_num, green_policy_num, draw_policy_thread
    
    if 255 == draw_policy_thread.img_alpha:
        draw_blue_policy(blue_policy_num)
        draw_green_policy(green_policy_num)
    else:
        # new policy is blue
        if 0 == policy_current:
            draw_blue_policy(blue_policy_num-1)
            draw_green_policy(green_policy_num)
        else:
            draw_blue_policy(blue_policy_num)
            draw_green_policy(green_policy_num-1)

def draw_arrow_except_president():
    
    (MouseX, MouseY) = pygame.mouse.get_pos()
    
    for i in range(player_num):
        if i == president or 0 == player_live[i]:
            continue
        if arrow_loc[i][0] <= MouseX <= arrow_loc[i][0] + id_to_arrow_image(i).get_width() and arrow_loc[i][1] <= MouseY <= arrow_loc[i][1] + id_to_arrow_image(i).get_height():
            screen.blit(id_to_arrow_image(i), arrow_loc[i])
        else:
            screen.blit(id_to_arrow_alpha_image(i), arrow_loc[i])

def check_if_bian(pl):
    global not_bian
    
    screen.blit(write(u" %s ，您是扁維拉麼？"%player_name_list[pl], BLACK, 20), talk_loc[president])
    if 2 == player_role[pl]:
        screen.blit(write(u"正是", RED, 20), arrow_loc[pl])
    else:
        screen.blit(write(u"不是", RED, 20), arrow_loc[pl])
        not_bian[pl] = 1
        
    draw_button(b_status_loc,u"繼續", yes_btn)

def execute_assassination():
    """Commit death before showing the execution result, regardless of role."""
    global mode, victory_result
    player_live[kill_player] = 0
    if player_role[kill_player] == 2:
        victory_result = 1
    mode = 14


def kill_part3():
    global kill_player
    
    screen.blit(write(u"%s，受死吧！砰砰！目標已死亡。"%player_name_list[kill_player], BLACK, 20), status_loc)
    if victory_result == 1:
        screen.blit(write(u"扁維拉已死亡，藍營獲勝。", BLUE, 20), (800, 445))
    
    draw_button(b_status_loc,u"繼續", yes_btn)
            
def human_kill():
    global p1

    screen.blit(write(u"%s 總統，您要暗殺誰呢？"%p1, BLACK, 20), status_loc)
    
    draw_arrow_except_president()

def human_investigate():
    global p1
    
    screen.blit(write(u"%s 總統，您要調查誰呢？"%p1, BLACK, 20), status_loc)
    
    draw_arrow_except_president()

def investigation_part2():
    global human_inv
    
    if human_player == president:
        human_inv = inv_player
    
    screen.blit(write(u"%s 總統，進行調查 %s 的黨派？"%(player_name_list[president], player_name_list[inv_player]), BLACK, 20), status_loc)
     
    draw_button(b_status_loc,u"繼續", yes_btn)
    
def human_president_power():
    if 3 == green_policy_num or 5 == green_policy_num:
        human_kill()
    elif 4 == green_policy_num:
        human_investigate()

def ai_kill():
    global kill_player
    
    score = 0
    kill_list = []
    
    for i in range(player_num):
        if i == president:
            continue
        elif 0 == player_live[i]:
            continue
        elif 1 == player_role[president] and 1 == player_role[i]:
            continue
        else:
            kill_list.append(i)
            
            #if president is blue
            if 0 == player_role[president]:
                if party_score[president][i] < score:
                    score = party_score[president][i]
                    kill_player = i
            
            #else if president is green
            else:
                if party_score[president][i] > score:
                    score = party_score[president][i]
                    kill_player = i
            
    if -1 == kill_player:
        random.shuffle(kill_list)
        kill_player = kill_list[0]
            
def ai_investigate():
    global inv_player

    inv_list = []
    
    for i in range(player_num):
        if i == president:
            continue
        elif 0 == player_live[i]:
            continue
        elif 1 == player_role[president] and 1 == player_role[i]:
            continue
        else:
            inv_list.append(i)
    
    random.shuffle(inv_list)
    
    inv_player = inv_list[0]
    
def ai_president_power():
    global mode

    if 3 == green_policy_num or 5 == green_policy_num:
        ai_kill()
        mode = 13
    elif 4 == green_policy_num:
        ai_investigate()
        mode = 15

def final_result():
    global green_win_num, blue_win_num, victory_counted
    if not victory_counted:
        if victory_result in (1, 2):
            blue_win_num += 1
        else:
            green_win_num += 1
        victory_counted = True
    
    if 0 == player_live[human_player]:
        player_result = u"玩家此局已經死亡…"
    elif 1 == victory_result or 2 == victory_result:
        if 0 == player_role[human_player]:
            player_result = u"玩家獲勝！"
        else:
            player_result = u"玩家失敗！"
    else: # victory_result == 3 or 4
        if 0 == player_role[human_player]:
            player_result = u"玩家失敗！"
        else:
            player_result = u"玩家獲勝！"
            
    if 1 == victory_result:
        screen.blit(write(u"扁維拉已死，藍營勝利。%s"%player_result, BLACK, 20), status_loc)
    elif 2 == victory_result:
        screen.blit(write(u"藍營勝利。%s"%player_result, BLACK, 20), status_loc)
    elif 3 == victory_result:
        screen.blit(write(u"扁維拉獲得提名為院長，綠營勝利。%s"%player_result, BLACK, 20), status_loc)
    elif 4 == victory_result:
        screen.blit(write(u"綠營勝利。%s"%player_result, BLACK, 20), status_loc)
        
    draw_button(b_status_loc,u"重新開始", yes_btn)
        
def main():
    global victory_counted
    global p1, player_role, mode, player_name_list, president, chancellor, human_player, policy_card_box, out, pre_president, pre_chancellor, broken_current, broken_num, policy_current, already_set_broken, already_set_policy_num, blue_policy_num, green_policy_num, player_live, kill_player, inv_player, victory_result, human_inv, know_bian, not_bian, party_score, election_ch, triple_s
    
    first = 1
    # index 0: bian, 1~3: green party, 4~9: blue party
    player_ini_role = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    random.shuffle(player_name_list)
    ini_loc()
    human_player = findhp(player_name_list)
    clock = pygame.time.Clock()
    
    #human_player = -2 # test NO human
    
    while True:
        if 1 == first:
            victory_counted = False
            random.shuffle(player_ini_role)
            party_score = []
            for i in range(player_num):
                if 0 == i:
                    # 2 == bian role
                    player_role[player_ini_role[i]] = 2
                elif 0 < i < 4:
                    # 1 == green party
                    player_role[player_ini_role[i]] = 1
                else:
                    # 0 == blue party
                    player_role[player_ini_role[i]] = 0
                party_score.append([0]*player_num)
            for i in player_ini_role[1:4]:
                for j in player_ini_role[1:4]:
                    if i == j:
                        continue
                    party_score[i][j] = -60
            green_policy_num = 0
            blue_policy_num = 0
            inv_player = -1
            human_inv = -1
            victory_result = 0
            pre_president = -1
            pre_chancellor = -1
            broken_num = 0
            player_live = [1] * player_num
            know_bian = [-2] * player_num
            not_bian = [-1] * player_num
            # Test player_live
            # player_live = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            # End test player_live
            first = 0
            
        if 0 == mode:
            if -1 == president:
                president = random.randint(0, player_num-1)
            else:
                president_org = president
                for i in range(1, player_num):
                    president = (president_org + i)%player_num
                    if 1 == player_live[president]:
                        break
            chancellor = -1
            
            random.shuffle(policy_card_box)
            out = [0] * policy_card_ini_num
            election_ch = [0] * player_num
            triple_s = 0
            broken_current = 0
            kill_player = -1
            policy_current = -1
            already_set_broken = 0
            already_set_policy_num = 0
            draw_policy_thread.img_alpha = 255
            draw_policy_thread.party = -1
            
            #president = human_player #For test only
            mode = 1
    
        if 1 == mode:
            if president == human_player:
                mode = 2
            else:
                chancellor = select_chancellor_ai()
                if green_policy_num >= 4:
                    mode = 17
                else:
                    mode = 3
    
        fill_background()
        draw_policy_table()
        draw_player_name()
        draw_broken()
        draw_all_policy()
        draw_policy_thread.run()
        if 2 == mode:
            draw_select_chancellor()
        if 3 == mode:
            # Note: If human player is dead, human player will NOT be president candidate 
            if human_player != president and human_player != chancellor:
                if -2 == human_player:
                    mode = 4
                elif 0 == player_live[human_player]:
                    mode = 4
                else:
                    screen.blit(write(u"%s 代表，您是否贊成 %s 擔任總統以及 %s 擔任院長？"%(player_name_list[human_player], player_name_list[president], player_name_list[chancellor]), BLACK, 20), status_loc)
                    draw_button(yes_btn_loc[human_player],u"同意", yes_btn)
                    draw_button(no_btn_loc[human_player],u"否決", no_btn)
            elif human_player == chancellor:
                mode = 16
            else:
                mode = 4
        if 4 == mode:
            election_ai()
            mode = 5
        if 5 == mode:
            election_result()
        # Note: If human player is dead, human player will NOT be president candidate 
        if 6 == mode:
            president_enact_human()
        if 7 == mode:
            president_enact_ai()
            if chancellor == human_player:
                mode = 8
            else:
                mode = 9
        if 8 == mode:
            chancellor_enact_human()
        if 9 == mode:
            chancellor_enact_ai()
            mode = 10
        if 10 == mode:
            if 0 == already_set_policy_num:
                pre_president = president
                pre_chancellor = chancellor
                # if blue
                if 0 == policy_current:
                    p_score = 1
                    p_num = blue_policy_num
                    policy_text = u"藍營"
                    blue_policy_num += 1
                # else green
                else:
                    p_score = -1
                    p_num = green_policy_num
                    policy_text = u"綠營"
                    green_policy_num += 1
                
                for i in range(player_num):
                    if human_player == i:
                        continue
                    elif president == i:
                        party_score[i][chancellor] += (p_score*triple_s)
                    elif chancellor == i:
                        continue
                    else:
                        party_score[i][president]  += p_score
                        party_score[i][chancellor] += p_score
                draw_policy_thread.img_alpha = 0
                draw_policy_thread.party = policy_current
                draw_policy_thread.index = p_num
                already_set_policy_num = 1
            
            if 3 == broken_num:
                screen.blit(write(u"政治協商破局 %d 次，強制立法。 %s 法案通過"%(broken_num, policy_text), BLACK, 20), status_loc)
            else:
                screen.blit(write(u" %s 法案通過"%policy_text, BLACK, 20), status_loc)
            draw_button(b_status_loc,u"繼續", yes_btn)
        if 11 == mode:
            human_president_power()
        if 12 == mode:
            # ai_president_power will set next mode
            ai_president_power()
        if 13 == mode:
            check_if_bian(kill_player)
        if 14 == mode:
            kill_part3()
        if 15 == mode:
            investigation_part2()
        if 16 == mode:
            screen.blit(write(u" %s ，您被選為院長候選人，將投同意票。"%p1, BLACK, 20), status_loc)
            draw_button(b_status_loc,u"繼續", yes_btn)
        if 17 == mode:
            check_if_bian(chancellor)
        if 69 == mode:
            final_result()
        # Test location
        #for i in range(player_num):
        #    screen.blit(yes_btn, yes_btn_loc[i])
        #    screen.blit(no_btn, no_btn_loc[i])
        # End test location
        # Test policy card
        #for i in range(player_num):
        #    for j in range(policy_card_num):
        #        screen.blit(green_flag, policy_card_loc[i][j])
        # End test policy card
        
        pygame.display.update()
        clock.tick(60)
        
        if -2 == human_player:
            if 5 == mode:
                if 3 == broken_num:
                    broken_current = 0
                    policy_current = policy_card_box[0]
                    mode = 10
                elif 0 == broken_current:
                    broken_num = 0
                    if president == human_player:
                        mode = 6
                    else: #ai
                        mode = 7
                else: #broken
                    mode = 0
            elif 10 == mode:
                if 5 == blue_policy_num:
                    victory_result = 2
                    mode = 69
                elif 6 == green_policy_num:
                    victory_result = 4
                    mode = 69
                # if green policy and green policy number > 2
                elif 1 == policy_current and green_policy_num > 2:
                    if 3 == broken_num:
                        mode = 0
                    elif president == human_player:
                        mode = 11
                    else:
                        mode = 12
                else:
                    mode = 0
                broken_num = 0
            elif 13 == mode:
                execute_assassination()
            elif 14 == mode:
                mode = 69 if victory_result == 1 else 0
            elif 15 == mode:
                if president != human_player:
                    if 0 == player_role[inv_player]:
                        # Due to party_score is high. When knower is green, it almost impossible to be chancellor candidate for AI
                        party_score[president][inv_player] += 60
                    else:
                        party_score[president][inv_player] -= 60
                        if 1 == player_role[president]:
                            know_bian[president] = inv_player
                mode = 0
            elif 17 == mode:
                # check green policy >= 4, before
                if 2 == player_role[chancellor]:
                    victory_result = 3
                    mode = 69
                elif president == human_player:
                    mode = 4
                elif chancellor == human_player:
                    mode = 16
                else:
                    mode = 3
            elif 69 == mode:
                first = 1
                mode = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or should_leave(event):
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 2 == mode:
                    (MouseX, MouseY) = pygame.mouse.get_pos()
                    for i in range(player_num):
                        if 0 == player_live[i]:
                            continue
                        if i in [president, pre_president, pre_chancellor]:
                            continue
                        if arrow_loc[i][0] <= MouseX <= arrow_loc[i][0] + id_to_arrow_image(i).get_width() and arrow_loc[i][1] <= MouseY <= arrow_loc[i][1] + id_to_arrow_image(i).get_height():
                            chancellor = i
                            if green_policy_num >= 4:
                                mode = 17
                            else:
                                mode = 4
                            break
                    break
                elif 3 == mode:
                    (MouseX, MouseY) = pygame.mouse.get_pos()
                    if yes_btn_loc[human_player][0] <= MouseX <= yes_btn_loc[human_player][0]+yes_btn.get_width() and yes_btn_loc[human_player][1] <= MouseY <= yes_btn_loc[human_player][1]+yes_btn.get_height():
                        election_ch[human_player] = 1
                        mode = 4
                    elif no_btn_loc[human_player][0] <= MouseX <= no_btn_loc[human_player][0]+no_btn.get_width() and no_btn_loc[human_player][1] <= MouseY <= no_btn_loc[human_player][1]+no_btn.get_height():
                        election_ch[human_player] = 0
                        mode = 4
                    break
                elif 5 == mode:
                    (MouseX, MouseY) = pygame.mouse.get_pos()
                    if b_status_loc[0] <= MouseX <= b_status_loc[0] + yes_btn.get_width() and b_status_loc[1] <= MouseY <= b_status_loc[1] + yes_btn.get_height():
                        if 3 == broken_num:
                            broken_current = 0
                            policy_current = policy_card_box[0]
                            mode = 10
                        elif 0 == broken_current:
                            broken_num = 0
                            if president == human_player:
                                mode = 6
                            else: #ai
                                mode = 7
                        else: #broken
                            mode = 0
                    break
                elif 6 == mode:
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    
                    for i in range(policy_card_ini_num):
                        if policy_card_loc[human_player][i][0] <= mouseX <= policy_card_loc[human_player][i][0]+policy_card_id_to_image(i).get_width() and policy_card_loc[human_player][i][1] <= mouseY <= policy_card_loc[human_player][i][1]+policy_card_id_to_image(i).get_height():
                            out[i] = 1
                            mode = 9
                            break
                    break
                    
                elif 8 == mode:
                    i = 0
    
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    
                    for j in range(policy_card_ini_num):
                        if 1 == out[j]:
                            continue
                        elif policy_card_loc[human_player][i][0] <= mouseX <= policy_card_loc[human_player][i][0]+policy_card_id_to_image(j).get_width() and policy_card_loc[human_player][i][1] <= mouseY <= policy_card_loc[human_player][i][1]+policy_card_id_to_image(j).get_height():
                            out[j] = 1
                            enact_policy_from_policy_card()
                            mode = 10
                            break
                        i += 1
                    break
                elif 10 == mode:
                    (MouseX, MouseY) = pygame.mouse.get_pos()
                    if b_status_loc[0] <= MouseX <= b_status_loc[0] + yes_btn.get_width() and b_status_loc[1] <= MouseY <= b_status_loc[1] + yes_btn.get_height():
                        if 5 == blue_policy_num:
                            victory_result = 2
                            mode = 69
                        elif 6 == green_policy_num:
                            victory_result = 4
                            mode = 69
                        # if green policy and green policy number > 2
                        elif 1 == policy_current and green_policy_num > 2:
                            if 3 == broken_num:
                                mode = 0
                            elif president == human_player:
                                mode = 11
                            else:
                                mode = 12
                        else:
                            mode = 0
                        broken_num = 0
                    break
                elif 11 == mode:
                    (MouseX, MouseY) = pygame.mouse.get_pos()
                    
                    for i in range(player_num):
                        if i == president or 0 == player_live[i]:
                            continue
                        if arrow_loc[i][0] <= MouseX <= arrow_loc[i][0] + id_to_arrow_image(i).get_width() and arrow_loc[i][1] <= MouseY <= arrow_loc[i][1] + id_to_arrow_image(i).get_height():
                            if 3 == green_policy_num or 5 == green_policy_num:
                                kill_player = i
                                mode = 13
                            elif 4 == green_policy_num:
                                inv_player = i
                                mode = 15
                                
                    break
                elif 13 == mode:
                    (MouseX, MouseY) = pygame.mouse.get_pos()
                    if b_status_loc[0] <= MouseX <= b_status_loc[0] + yes_btn.get_width() and b_status_loc[1] <= MouseY <= b_status_loc[1] + yes_btn.get_height():
                        execute_assassination()
                    break
                elif 14 == mode:
                    (MouseX, MouseY) = pygame.mouse.get_pos()
                    if b_status_loc[0] <= MouseX <= b_status_loc[0] + yes_btn.get_width() and b_status_loc[1] <= MouseY <= b_status_loc[1] + yes_btn.get_height():
                        mode = 69 if victory_result == 1 else 0
                    break
                elif 15 == mode:
                    (MouseX, MouseY) = pygame.mouse.get_pos()
                    if b_status_loc[0] <= MouseX <= b_status_loc[0] + yes_btn.get_width() and b_status_loc[1] <= MouseY <= b_status_loc[1] + yes_btn.get_height():
                        if president != human_player:
                            if 0 == player_role[inv_player]:
                                # Due to party_score is high. When knower is green, it almost impossible to be chancellor candidate for AI
                                party_score[president][inv_player] += 60
                            else:
                                party_score[president][inv_player] -= 60
                                if 1 == player_role[president]:
                                    know_bian[president] = inv_player
                        mode = 0
                    break
                elif 16 == mode:
                    (MouseX, MouseY) = pygame.mouse.get_pos()
                    if b_status_loc[0] <= MouseX <= b_status_loc[0] + yes_btn.get_width() and b_status_loc[1] <= MouseY <= b_status_loc[1] + yes_btn.get_height():
                        mode = 4
                    break
                elif 17 == mode:
                    (MouseX, MouseY) = pygame.mouse.get_pos()
                    if b_status_loc[0] <= MouseX <= b_status_loc[0] + yes_btn.get_width() and b_status_loc[1] <= MouseY <= b_status_loc[1] + yes_btn.get_height():
                        # check green policy >= 4, before
                        if 2 == player_role[chancellor]:
                            victory_result = 3
                            mode = 69
                        elif president == human_player:
                            mode = 4
                        elif chancellor == human_player:
                            mode = 16
                        else:
                            mode = 3
                    break
                elif 69 == mode:
                    (MouseX, MouseY) = pygame.mouse.get_pos()
                    if b_status_loc[0] <= MouseX <= b_status_loc[0] + yes_btn.get_width() and b_status_loc[1] <= MouseY <= b_status_loc[1] + yes_btn.get_height():
                        first = 1
                        mode = 0
                    break
                    
    pygame.quit()
    quit()

install(globals(), 'Bian')

if __name__ == "__main__":
    main()
