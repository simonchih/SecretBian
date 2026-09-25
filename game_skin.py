"""Presentation adapter: the original games keep their AI and state machines."""
import math
import pygame
from visual import *

BACK = pygame.Rect(18,18,200,42)

def vote_result_rect(index, player_positions):
    """A dedicated vote row outside each seat's name/title/role area."""
    x,y=player_positions[index]
    if index in (0,1,2):
        return pygame.Rect(x,y-80,100,32)
    if index in (5,6,7):
        return pygame.Rect(x,y+60,100,32)
    return pygame.Rect(55 if index in (3,4) else 1250,y+55,100,32)

def draw_vote_result(screen, index, accepted, player_positions, english):
    rect=vote_result_rect(index,player_positions)
    text=('Accepted' if accepted else 'Deny') if english else ('同意' if accepted else '否決')
    color=BLUE if accepted else RED
    panel(screen,rect,PANEL,color,8)
    label(screen,text,rect.center,18,color,True)

def install(g, edition):
    screen=g['screen']
    is_en=edition=='Trump'
    opposition=RED if is_en else GREEN
    g['BLACK']=TEXT
    g['BLUE']=BLUE
    g['RED']=opposition
    previous_mode=[None,0]
    def write(msg='',color=TEXT,size=14):
        return font(size).render(msg,True,color)
    g['write']=write
    g['draw_vote_result']=lambda i,accepted: draw_vote_result(screen,i,accepted,g['player_name_loc'],is_en)
    def background():
        screen.blit(g['background'],(0,0))
        for i,(x,y) in enumerate(g['role_loc']):
            if i in (0,1,2): rect=pygame.Rect(x-10,630,250,69)
            elif i in (5,6,7): rect=pygame.Rect(x-10,0,250,53)
            elif i in (3,4): rect=pygame.Rect(0,y-10,205,100)
            else: rect=pygame.Rect(1218,y-10,182,100)
            border=(83,102,117) if i==g['president'] else (38,55,73)
            panel(screen,rect,(18,30,46),border,10)
        button(screen,BACK,'ESC · Main menu' if is_en else 'ESC · 返回主選單',BACK.collidepoint(pygame.mouse.get_pos()),size=17)
        label(screen,'SECRET TRUMP' if is_en else '神祕阿扁',(30,77),19,GOLD)
        mode=g['mode']
        if previous_mode[0]!=mode:
            previous_mode[:]=[mode,pygame.time.get_ticks()]
        elapsed=pygame.time.get_ticks()-previous_mode[1]
        if elapsed<750:
            glow=pygame.Surface((954,272),pygame.SRCALPHA)
            pygame.draw.rect(glow,(*GOLD,int(110*(1-elapsed/750))),glow.get_rect(),2,border_radius=24)
            screen.blit(glow,(223,223))
        prompts={2:('Select a gold arrow to nominate','點選金色箭頭，提名院長'),
                 3:('Cast your vote beside your player name','請在你的名字旁投下同意或否決'),
                 6:('Choose one policy to discard','點選一張要排除的政策'),
                 8:('Choose one policy to discard','點選一張要排除的政策'),
                 11:('Select another living player','點選另一位存活玩家的箭頭'),
                 69:('All identities revealed · restart or return to menu','所有身分已公開 · 可重新開始或返回主選單')}
        hint=prompts.get(mode,('Continue using the center button','點選中央按鈕繼續'))
        label(screen,hint[0 if is_en else 1],(700,512),17,MUTED,True)
    g['fill_background']=background
    def tables():
        for party,locations,count,title,color in [
            (0,g['mythread'].b_loc,5,('DEMOCRATIC' if is_en else '藍營')+f" · {g['blue_policy_num']} / 5",BLUE),
            (1,g['mythread'].g_loc,6,('REPUBLICAN' if is_en else '綠營')+f" · {g['green_policy_num']} / 6",opposition)]:
            label(screen,title,(locations[0][0],225),16,color)
            for i,loc in enumerate(locations[:count]):
                rect=pygame.Rect(*loc,100,75)
                panel(screen,rect.inflate(-4,-4),(23,36,51),(61,77,93),7)
                caption=str(i+1)
                if party==1 and i in (2,3,4):
                    emblem(screen,'search' if i==3 else 'execute',rect,(80,96,109))
                label(screen,caption,(rect.right-16,rect.bottom-17),12,MUTED,True)
    g['draw_policy_table']=tables
    def draw_button(loc,text,image=None,size=16):
        rect=pygame.Rect(*loc,100,50)
        button(screen,rect,text,rect.collidepoint(pygame.mouse.get_pos()),size=size)
    g['draw_button']=draw_button
    def names():
        human=g['human_player']
        for i,name in enumerate(g['player_name_list']):
            x,y=g['player_name_loc'][i]
            x=min(x,1285)
            y=min(y,651)
            if i==human:
                pygame.draw.line(screen,GOLD,(x,y+28),(x+75,y+28),2)
            label(screen,name,(x,y),20,TEXT if g['player_live'][i] else MUTED)
            title=('President' if is_en else '總統') if i==g['president'] else ('Chancellor' if is_en else '院長') if i==g['chancellor'] else ''
            if title:
                label(screen,title,(x,y-18 if y>630 else y+26),13,GOLD)
            if not g['player_live'][i]:
                screen.blit(g['dead'],(min(1369,x+font(20).size(name)[0]+8),y))
            role=g['player_role'][i]
            if g['victory_result'] or i==human or (g['player_role'][human]==1 and role==1):
                screen.blit(g['role_to_image'](role),g['role_loc'][i])
            elif i==g['human_inv']:
                screen.blit(g['role_to_image'](int(role!=0)),g['role_loc'][i])
            else:
                rect=pygame.Rect(*g['role_loc'][i],60,45).inflate(-4,-4)
                panel(screen,rect,(22,36,53),(49,66,86),7)
                label(screen,'?',rect.center,23,MUTED,True)
    g['draw_player_name']=names

def should_leave(event):
    return (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE or
            event.type==pygame.MOUSEBUTTONDOWN and event.button==1 and BACK.collidepoint(event.pos))
