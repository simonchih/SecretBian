import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest
from types import SimpleNamespace
from unittest.mock import patch
import main

class PackagingTests(unittest.TestCase):
    def test_frozen_game_launch_uses_edition_argument(self):
        with patch.object(sys,'frozen',True,create=True), \
             patch.object(main.subprocess,'run',return_value=SimpleNamespace(returncode=0)) as run, \
             patch.object(main.pygame.display,'quit'),patch.object(main.pygame.display,'init'):
            for edition in ('Trump','Bian'):
                self.assertEqual(main.launch_game(edition),0)
                self.assertEqual(run.call_args.args[0],[sys.executable,'--edition',edition])

    def test_display_restored_when_child_launch_fails(self):
        with patch.object(main.subprocess,'run',side_effect=OSError('test')), \
             patch.object(main.pygame.display,'quit'),patch.object(main.pygame.display,'init') as init:
            with self.assertRaises(OSError):main.launch_game('Trump')
            init.assert_called_once()

if __name__=='__main__':unittest.main()
