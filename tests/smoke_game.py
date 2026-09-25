"""Exercise original game state machines through synthetic mouse input."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import sys
import random
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
edition=sys.argv[1]
random.seed(int(sys.argv[2]) if len(sys.argv)>2 else 12)
sys.path.insert(0,str(ROOT))
import pygame
# Dummy driver has no window scaling implementation.
real_mode=pygame.display.set_mode
pygame.display.set_mode=lambda size,*a,**k:real_mode(size)
spec=importlib.util.spec_from_file_location('game',ROOT/f'game_{edition.lower()}.py')
game=importlib.util.module_from_spec(spec)
spec.loader.exec_module(game)
frames=0
wins=0
seen=set()
pos=(0,0)
class FastClock:
    def tick(self,*args):return 16
pygame.time.Clock=FastClock
pygame.mouse.get_pos=lambda:pos
def events():
    global frames,wins,pos
    frames+=1
    if frames==1 or game.mode not in seen and game.mode in (5,6,10,15,69):
        (ROOT/'artifacts').mkdir(exist_ok=True)
        name=f'game-{edition}.png' if frames==1 else f'game-{edition}-{game.mode}.png'
        pygame.image.save(game.screen,str(ROOT/'artifacts'/name))
    seen.add(game.mode)
    if game.mode==69:
        wins+=1
        total=game.blue_win_num+game.green_win_num
        for _ in range(3):game.final_result()
        assert game.blue_win_num+game.green_win_num==total==wins, 'Victory tally must increment once per game'
    if wins>=5:
        return [pygame.event.Event(pygame.KEYDOWN,key=pygame.K_ESCAPE)]
    if frames>5000:raise AssertionError(f'Stuck in mode {game.mode}; visited {seen}')
    pos=tuple(x+10 for x in game.b_status_loc)
    if game.mode in (2,11):
        eligible=[i for i in range(10) if game.player_live[i] and i!=game.president and (game.mode==11 or i not in (game.pre_president,game.pre_chancellor))]
        pos=tuple(x+10 for x in game.arrow_loc[random.choice(eligible)])
    elif game.mode==3:
        pos=tuple(x+10 for x in (game.yes_btn_loc if random.random()<.8 else game.no_btn_loc)[game.human_player])
    elif game.mode in (6,8):pos=tuple(x+10 for x in game.policy_card_loc[game.human_player][0])
    return [pygame.event.Event(pygame.MOUSEBUTTONDOWN,button=1,pos=pos)]
pygame.event.get=events
game.main()
assert wins>=5
print(f'{edition}: {wins} games completed; {frames} frames; modes {sorted(seen)}; ESC returned cleanly')
