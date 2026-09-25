"""Drive both games through selection, identity check, execution and outcome."""
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

def load_game(edition):
    pygame.init()
    original=pygame.display.set_mode
    spec=importlib.util.spec_from_file_location('execution_'+edition,ROOT/f'game_{edition}.py')
    game=importlib.util.module_from_spec(spec)
    with patch.object(pygame.display,'set_mode',side_effect=lambda size,*a,**k:original(size)):
        spec.loader.exec_module(game)
    return game

class AssassinationTests(unittest.TestCase):
    def test_execution_for_every_role_and_both_power_slots(self):
        for edition in ('bian','trump'):
            for policies in (3,5):
                for role in (0,1,2):
                    for human_president in (True,False):
                        with self.subTest(edition=edition,policies=policies,role=role,human=human_president):
                            game=load_game(edition)
                            initialized=False
                            executed=False
                            finished=False
                            frames=0
                            pos=(0,0)
                            original_background=game.fill_background
                            def background():
                                nonlocal initialized
                                if not initialized:
                                    initialized=True
                                    game.human_player=0
                                    game.president=0 if human_president else 1
                                    game.chancellor=3
                                    game.player_live=[1]*10
                                    game.player_role=[0]*10
                                    game.player_role[2]=role
                                    game.green_policy_num=policies
                                    game.victory_result=0
                                    game.mode=11 if human_president else 12
                                original_background()
                            def events():
                                nonlocal frames,pos,executed,finished
                                frames+=1
                                self.assertLess(frames,8)
                                pos=tuple(v+10 for v in game.b_status_loc)
                                if game.mode==11:
                                    pos=tuple(v+10 for v in game.arrow_loc[2])
                                elif game.mode==13:
                                    self.assertEqual(game.kill_player,2)
                                    self.assertEqual(game.player_live[2],1)
                                elif game.mode==14:
                                    self.assertEqual(game.player_live[2],0)
                                    self.assertEqual(game.victory_result,int(role==2))
                                    self.assertTrue(execution_draw.called,'Execution message was skipped')
                                    executed=True
                                else:
                                    self.assertTrue(executed)
                                    self.assertEqual(game.player_live[2],0)
                                    self.assertEqual(game.victory_result,int(role==2))
                                    self.assertEqual(game.mode==69,role==2)
                                    finished=True
                                    return [pygame.event.Event(pygame.QUIT)]
                                return [pygame.event.Event(pygame.MOUSEBUTTONDOWN,button=1,pos=pos)]
                            with patch.object(game,'fill_background',side_effect=background), \
                                 patch.object(game,'ai_kill',side_effect=lambda:setattr(game,'kill_player',2)), \
                                 patch.object(game,'kill_part3',wraps=game.kill_part3) as execution_draw, \
                                 patch.object(pygame.event,'get',side_effect=events), \
                                 patch.object(pygame.mouse,'get_pos',side_effect=lambda:pos), \
                                 patch.object(pygame,'quit'):
                                game.main()
                            self.assertTrue(finished)

    def test_nomination_identity_check_does_not_execute_candidate(self):
        for edition in ('bian','trump'):
            game=load_game(edition)
            game.ini_loc()
            game.president=0
            game.mode=17
            for role in (0,1,2):
                game.player_role[1]=role
                game.check_if_bian(1)
                self.assertEqual(game.player_live,[1]*10)
                self.assertEqual(game.victory_result,0)
                self.assertEqual(game.mode,17)

if __name__=='__main__':unittest.main()
