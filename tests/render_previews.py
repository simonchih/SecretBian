import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import pygame
from main import draw_menu
from tutorial import Tutorial
pygame.init()
screen=pygame.display.set_mode((1400,800))
out=ROOT/'artifacts'
out.mkdir(exist_ok=True)
bg=pygame.transform.smoothscale(pygame.image.load(str(ROOT/'assets/entrance.png')),(1400,800))
draw_menu(screen,bg,0,0)
pygame.image.save(screen,str(out/'menu.png'))
for edition in ('Trump','Bian'):
    for step in (2,5,9):
        t=Tutorial(edition);t.step=step;t.draw(screen,(0,0))
        pygame.image.save(screen,str(out/f'tutorial-{edition}-{step}.png'))
pygame.quit()
