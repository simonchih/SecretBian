"""Unified launcher. Run: python main.py"""
import os
import subprocess
import sys
import math
import pygame
from visual import *
from tutorial import Tutorial

MENU_LABELS = ['Secret Trump Version','Tutorial for Trump','阿扁版','阿扁版遊戲教學']
MENU_RECTS = [pygame.Rect(450,385+i*83,500,67) for i in range(4)]
SELF_TEST_REPORT = None

def game_module(edition):
    # Explicit imports allow PyInstaller to discover both game modules.
    if edition == 'Trump':
        import game_trump
        return game_trump
    if edition == 'Bian':
        import game_bian
        return game_bian
    raise ValueError(edition)

def launch_game(edition):
    """Run each edition in its own process to isolate game state."""
    script={'Trump':'game_trump.py','Bian':'game_bian.py'}[edition]
    if getattr(sys,'frozen',False):
        command=[sys.executable,'--edition',edition]
    else:
        command=[sys.executable,str(ROOT/script)]
    if SELF_TEST_REPORT is not None:
        if not getattr(sys,'frozen',False):
            command=[sys.executable,str(ROOT/'main.py'),'--edition',edition]
        command+=['--self-test',str(SELF_TEST_REPORT.with_name(edition+'-self-test.json'))]
    pygame.display.quit()
    try:
        result=subprocess.run(command,cwd=str(ROOT),check=False)
    finally:
        pygame.display.init()
    return result.returncode

def display():
    pygame.display.set_caption('Secret Council · Secret Trump / 神祕阿扁')
    return pygame.display.set_mode((1400,800),pygame.SCALED)

def draw_menu(screen,background,selected,ticks):
    screen.blit(background,(0,0))
    # Restrained dust motion, kept outside the clickable controls.
    for i in range(24):
        x=(i*137+35)%1400
        y=(i*79-ticks*.012*(1+i%3))%800
        if x<400 or x>1000:
            pygame.draw.circle(screen,(110+i%4*18,95+i%4*12,64),(int(x),int(y)),1)
    label(screen,'S E C R E T   C O U N C I L',(700,282),45,TEXT,True)
    label(screen,'十人議局 · 兩種世界 · 一個祕密',(700,341),21,GOLD,True)
    for i,(text,rect) in enumerate(zip(MENU_LABELS,MENU_RECTS)):
        button(screen,rect,text,i==selected,size=25)
        label(screen,f'0{i+1}',(rect.x+25,rect.y+22),15,GOLD)
    label(screen,'↑ ↓  /  Enter     ·     Esc 離開',(700,758),16,MUTED,True)

def main():
    pygame.init()
    if any(not (ROOT/'assets'/edition/'blue.png').exists() for edition in ('trump','bian')):
        build_assets()
    screen=display()
    background=pygame.transform.smoothscale(pygame.image.load(str(ROOT/'assets/entrance.png')),(1400,800))
    clock=pygame.time.Clock()
    tutorial=None
    selected=0
    running=True
    error=''
    while running:
        action=None
        for event in pygame.event.get():
            if event.type==pygame.QUIT: running=False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    if tutorial: tutorial=None
                    else: running=False
                elif not tutorial:
                    if event.key in (pygame.K_DOWN,pygame.K_TAB): selected=(selected+1)%4
                    elif event.key==pygame.K_UP: selected=(selected-1)%4
                    elif event.key in (pygame.K_RETURN,pygame.K_SPACE): action=selected
            elif event.type==pygame.MOUSEMOTION and not tutorial:
                for i,rect in enumerate(MENU_RECTS):
                    if rect.collidepoint(event.pos): selected=i
            elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                if tutorial:
                    result=tutorial.click(event.pos)
                    if result=='menu': tutorial=None
                    elif result=='play': action=0 if tutorial.en else 2
                else:
                    for i,rect in enumerate(MENU_RECTS):
                        if rect.collidepoint(event.pos): action=i
        if not running: break
        if action in (1,3): tutorial=Tutorial('Trump' if action==1 else 'Bian')
        elif action in (0,2):
            try:
                code=launch_game('Trump' if action==0 else 'Bian')
                error='' if code==0 else f'Game exited with code {code}. See terminal / 請查看終端機。'
            except OSError as exc:
                error=str(exc)
            screen=display()
            tutorial=None
            pygame.event.clear()
        if tutorial: tutorial.draw(screen,pygame.mouse.get_pos())
        else:
            draw_menu(screen,background,selected,pygame.time.get_ticks())
            if error: label(screen,error,(20,5),18,RED)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

def entrypoint():
    import argparse
    global SELF_TEST_REPORT
    parser=argparse.ArgumentParser(description='Secret Council')
    parser.add_argument('--edition',choices=('Trump','Bian'))
    parser.add_argument('--self-test',type=Path,metavar='REPORT.json',help='Run automated native-window checks and save a report')
    args=parser.parse_args()
    if args.self_test:
        SELF_TEST_REPORT=args.self_test.resolve()
        from packaging_check import run_check
        run_check(sys.modules[__name__],args.edition,SELF_TEST_REPORT)
    elif args.edition:
        game_module(args.edition).main()
    else:
        main()

if __name__=='__main__':
    entrypoint()
