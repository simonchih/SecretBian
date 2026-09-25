"""Opt-in EXE diagnostics: real rendering, game loops and child processes.

Only used with --self-test REPORT.json. No effect on normal gameplay.
"""
import json
import random
import pygame

def run_check(app,edition,report):
    report.parent.mkdir(parents=True,exist_ok=True)
    frames=0
    completed=[]
    pos=(0,0)
    original_events=pygame.event.get
    original_mouse=pygame.mouse.get_pos
    original_launch=app.launch_game
    game=None
    try:
        if edition:
            random.seed(12)
            game=app.game_module(edition)
        def launch(version):
            code=original_launch(version)
            if code:
                raise RuntimeError(f'{version} exited with {code}')
            child=json.loads(report.with_name(version+'-self-test.json').read_text(encoding='utf-8'))
            if child.get('status')!='passed' or child.get('games_completed')!=1:
                raise RuntimeError(f'{version} child check failed: {child}')
            completed.append(version)
            return code
        def events():
            nonlocal frames,pos
            original_events()
            frames+=1
            if frames>2000:
                raise RuntimeError('Self-test failed to finish')
            if game:
                if game.mode==69:
                    completed.append(edition)
                    return [pygame.event.Event(pygame.KEYDOWN,key=pygame.K_ESCAPE)]
                pos=tuple(v+10 for v in game.b_status_loc)
                if game.mode in (2,11):
                    candidates=[i for i in range(10) if game.player_live[i] and i!=game.president and
                                (game.mode==11 or i not in (game.pre_president,game.pre_chancellor))]
                    pos=tuple(v+10 for v in game.arrow_loc[random.choice(candidates)])
                elif game.mode==3:
                    pos=tuple(v+10 for v in game.yes_btn_loc[game.human_player])
                elif game.mode in (6,8):
                    pos=tuple(v+10 for v in game.policy_card_loc[game.human_player][0])
                return [pygame.event.Event(pygame.MOUSEBUTTONDOWN,button=1,pos=pos)]
            keys={12:[pygame.K_RETURN],24:[pygame.K_DOWN,pygame.K_RETURN],36:[pygame.K_ESCAPE],
                  48:[pygame.K_DOWN,pygame.K_RETURN],60:[pygame.K_DOWN,pygame.K_RETURN],
                  72:[pygame.K_ESCAPE],84:[pygame.K_ESCAPE]}.get(frames,[])
            return [pygame.event.Event(pygame.KEYDOWN,key=key) for key in keys]
        pygame.event.get=events
        if game:
            pygame.mouse.get_pos=lambda:pos
            game.main()
            if completed!=[edition]:
                raise RuntimeError('Game did not reach victory')
            result={'status':'passed','edition':edition,'games_completed':1,'frames':frames}
        else:
            app.launch_game=launch
            app.main()
            if completed!=['Trump','Bian'] or frames!=84:
                raise RuntimeError('Launcher did not complete all routes')
            result={'status':'passed','routes':['Trump','English tutorial','Bian','Chinese tutorial'],
                    'child_processes':completed,'frames':frames}
        report.write_text(json.dumps(result,indent=2),encoding='utf-8')
    except Exception as exc:
        report.write_text(json.dumps({'status':'failed','error':repr(exc)},indent=2),encoding='utf-8')
        raise
    finally:
        pygame.event.get=original_events
        pygame.mouse.get_pos=original_mouse
        app.launch_game=original_launch
