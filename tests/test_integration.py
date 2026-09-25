import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import unittest
from unittest.mock import patch
import pygame
from tutorial import Tutorial
from visual import build_assets, wrap, font

class TutorialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.screen=pygame.display.set_mode((1400,800))

    def test_both_complete_paths(self):
        for edition in ('Trump','Bian'):
            t=Tutorial(edition)
            for step in range(10):
                self.assertEqual(t.step,step)
                t.move(1)
                self.assertEqual(t.step,step,'Unanswered lesson must be gated')
                if step in (1,2,7,9):
                    correct={1:1,2:3,7:0,9:0}[step]
                    t.choose((correct+1)%len(t.choices()))
                    self.assertFalse(t.done)
                if step==4:
                    t.choose(0);t.choose(0)
                    self.assertFalse(t.done)
                t.choose({1:1,2:3,5:1}.get(step,0))
                self.assertTrue(t.done)
                t.draw(self.screen,(0,0))
                if step==5:self.assertEqual(t.passed,[0,1])
                if step==6:self.assertEqual(t.enacted,1)
                if step<9:t.move(1)
            self.assertEqual(t.click((1200,746)),'play')

    def test_every_discard_combination(self):
        for a in range(3):
            for b in range(2):
                t=Tutorial('Trump');t.step=5;t.choose(a);t.move(1);t.choose(b)
                cards=[0,1,1];cards.pop(a);cards.pop(b)
                self.assertEqual(t.enacted,cards[0])

    def test_reset_and_back(self):
        t=Tutorial('Bian');t.step=4;t.choose(0);t.move(0)
        self.assertEqual(t.failures,0)
        self.assertFalse(t.done)
        t.move(-1);self.assertEqual(t.step,3)

    def test_lesson_copy_fits(self):
        for edition in ('Trump','Bian'):
            t=Tutorial(edition)
            for step,(_,description,_) in enumerate(t.lessons):
                t.step=step
                bottom=wrap(self.screen,description,pygame.Rect(530,205,770,105),21)
                self.assertLessEqual(bottom,t.targets()[0].top, (edition,step,bottom))

    def test_launcher_all_four_routes_and_return(self):
        import main
        def key(k):return pygame.event.Event(pygame.KEYDOWN,key=k)
        batches=[
            [key(pygame.K_RETURN)],
            [key(pygame.K_DOWN),key(pygame.K_RETURN)],
            [key(pygame.K_ESCAPE)],
            [key(pygame.K_DOWN),key(pygame.K_RETURN)],
            [key(pygame.K_DOWN),key(pygame.K_RETURN)],
            [key(pygame.K_ESCAPE)],
            [key(pygame.K_ESCAPE)],
        ]
        with patch.object(main,'display',return_value=self.screen), \
             patch.object(main,'launch_game',return_value=0) as launch, \
             patch.object(main,'Tutorial',wraps=Tutorial) as lessons, \
             patch.object(pygame.event,'get',side_effect=batches), \
             patch.object(pygame,'quit'):
            main.main()
        self.assertEqual([c.args[0] for c in launch.call_args_list],['Trump','Bian'])
        self.assertEqual([c.args[0] for c in lessons.call_args_list],['Trump','Bian'])

if __name__=='__main__':unittest.main()
