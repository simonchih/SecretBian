"""Regression checks for vote badges over names and office titles."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import sys
from pathlib import Path
import importlib.util
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import pygame
import game_skin
from visual import font

class VoteLayoutTests(unittest.TestCase):
    def test_both_editions_all_seats_and_offices(self):
        pygame.init()
        original_display=pygame.display.set_mode
        for edition in ('bian','trump'):
            spec=importlib.util.spec_from_file_location('layout_'+edition,ROOT/f'game_{edition}.py')
            game=importlib.util.module_from_spec(spec)
            with patch.object(pygame.display,'set_mode',side_effect=lambda size,*a,**k:original_display(size)):
                spec.loader.exec_module(game)
            game.human_player=0
            game.player_role=[0]*10
            for president in range(10):
                game.president=president
                game.chancellor=(president+1)%10
                identity_rects=[pygame.Rect(*loc,60,45) for loc in game.role_loc]
                original_label=game_skin.label
                def record_label(*args,**kwargs):
                    rect=original_label(*args,**kwargs)
                    identity_rects.append(rect)
                    return rect
                with patch.object(game_skin,'label',side_effect=record_label):
                    game.draw_player_name()
                badges=[]
                for seat in range(10):
                    badge=game_skin.vote_result_rect(seat,game.player_name_loc)
                    self.assertTrue(game.screen.get_rect().contains(badge))
                    self.assertFalse(any(badge.colliderect(rect) for rect in identity_rects),
                                     (edition,president,seat,'vote overlaps identity'))
                    self.assertFalse(any(badge.colliderect(other) for other in badges))
                    badges.append(badge)
                    for accepted in (True,False):
                        text=('Accepted' if accepted else 'Deny') if edition=='trump' else ('同意' if accepted else '否決')
                        width,height=font(18).size(text)
                        self.assertLessEqual(width,badge.width-12)
                        self.assertLessEqual(height,badge.height)
                        game.draw_vote_result(seat,accepted)

if __name__=='__main__':unittest.main()
