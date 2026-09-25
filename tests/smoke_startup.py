"""Launch real entry points and child processes; inject only navigation input.

Use --native to verify real SDL windows instead of the headless driver.
"""
import os
import sys
import runpy
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NATIVE = '--native' in sys.argv
if not NATIVE:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
sys.path.insert(0, str(ROOT))
import pygame

if not NATIVE:
    original_display = pygame.display.set_mode
    pygame.display.set_mode = lambda size, *a, **kw: original_display(size)

original_events = pygame.event.get
frames = 0
child = '--child' in sys.argv
launched = []

def events():
    global frames
    original_events()
    frames += 1
    if child:
        keys = [pygame.K_ESCAPE] if frames == 12 else []
    else:
        actions = {
            12: [pygame.K_RETURN],  # Trump child, then return
            24: [pygame.K_DOWN, pygame.K_RETURN],  # English tutorial
            36: [pygame.K_ESCAPE],
            48: [pygame.K_DOWN, pygame.K_RETURN],  # Bian child, then return
            60: [pygame.K_DOWN, pygame.K_RETURN],  # Chinese tutorial
            72: [pygame.K_ESCAPE],
            84: [pygame.K_ESCAPE],
        }
        keys = actions.get(frames, [])
    if frames > 120:
        raise AssertionError('Entry point did not exit after navigation')
    return [pygame.event.Event(pygame.KEYDOWN, key=key) for key in keys]

pygame.event.get = events

if child:
    script = Path(sys.argv[sys.argv.index('--child') + 1])
    sys.argv=[str(script)]
    runpy.run_path(str(script), run_name='__main__')
    assert frames == 12
    print(f'{script.name}: started, rendered, ESC exited')
else:
    original_run = subprocess.run

    def child_run(command, **kwargs):
        # Preserve the exact executable, script and cwd selected by the launcher.
        script = Path(command[1])
        assert script.parent == ROOT and script.is_file()
        assert Path(kwargs['cwd']) == ROOT
        wrapped = [command[0], str(Path(__file__).resolve()), '--child', str(script)]
        if NATIVE:
            wrapped.append('--native')
        result = original_run(wrapped, timeout=30, **kwargs)
        assert result.returncode == 0, f'{script.name} failed to launch'
        launched.append(script.name)
        return result

    subprocess.run = child_run
    # Start the launcher from another directory to catch relative-path mistakes.
    os.chdir(ROOT / 'tests')
    sys.argv=[str(ROOT / 'main.py')]
    runpy.run_path(str(ROOT / 'main.py'), run_name='__main__')
    assert launched == ['game_trump.py', 'game_bian.py']
    assert frames == 84
    print('PASS: all four routes, real child processes, return to menu, foreign cwd')
