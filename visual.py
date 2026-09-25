"""Shared, resolution-independent drawing language for both editions."""
from pathlib import Path
from functools import lru_cache
import math
import re
import pygame

ROOT = Path(__file__).resolve().parent
INK = (12, 20, 34)
PANEL = (23, 37, 55)
GOLD = (218, 184, 117)
TEXT = (237, 232, 218)
MUTED = (158, 175, 191)
BLUE = (74, 151, 217)
RED = (201, 91, 98)
GREEN = (63, 175, 139)

@lru_cache(maxsize=64)
def font(size):
    return pygame.font.Font(str(ROOT / 'assets/fonts/wqy-zenhei.ttf'), size)

def label(surface, text, pos, size=22, color=TEXT, center=False):
    image = font(size).render(text, True, color)
    rect = image.get_rect(center=pos) if center else image.get_rect(topleft=pos)
    surface.blit(image, rect)
    return rect

def wrap(surface, text, rect, size=23, color=TEXT):
    """Wrap English at word boundaries and Chinese between characters."""
    y = rect.y
    for paragraph in text.split('\n'):
        line = ''
        for token in re.findall(r'[A-Za-z0-9]+(?:[.:\x27’-][A-Za-z0-9]+)*|[^A-Za-z0-9]', paragraph):
            if line and font(size).size(line + token)[0] > rect.width:
                label(surface, line.rstrip(), (rect.x, y), size, color)
                y += size + 12
                line = ''
            if line or not token.isspace():
                line += token
        label(surface, line, (rect.x, y), size, color)
        y += size + 12
    return y

def panel(surface, rect, color=PANEL, border=GOLD, radius=16):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    pygame.draw.rect(surface, border, rect, 1, border_radius=radius)

def button(surface, rect, text, hover=False, enabled=True, size=23):
    color = (43, 61, 79) if hover and enabled else PANEL
    panel(surface, rect, color, GOLD if enabled else (57, 70, 85), 10)
    if hover and enabled:
        pygame.draw.rect(surface, GOLD, (rect.x+1, rect.y+12, 3, rect.h-24), border_radius=2)
    label(surface, text, rect.center, size, TEXT if enabled else MUTED, True)

def emblem(surface, kind, rect, color=GOLD):
    """Original geometric insignia; no dependence on old raster artwork."""
    x, y = rect.center
    r = min(rect.w, rect.h) * .32
    if kind == 'search':
        pygame.draw.circle(surface, color, (int(x-4), int(y-4)), int(r*.65), 3)
        pygame.draw.line(surface, color, (x+r*.4,y+r*.4), (x+r,y+r), 4)
    elif kind in ('execute', 'dead'):
        pygame.draw.circle(surface, color, (int(x),int(y)), int(r), 2)
        pygame.draw.line(surface,color,(x-r*.5,y-r*.5),(x+r*.5,y+r*.5),3)
        pygame.draw.line(surface,color,(x+r*.5,y-r*.5),(x-r*.5,y+r*.5),3)
    elif kind == 'arrow':
        pygame.draw.polygon(surface,color,[(x,y-r),(x+r,y+r*.6),(x,y+r*.15),(x-r,y+r*.6)])
    elif kind == 'leader':
        pygame.draw.polygon(surface,color,[(x-r,y-r*.6),(x-r*.6,y+r*.5),(x+r*.6,y+r*.5),(x+r,y-r*.6),(x+r*.35,y),(x,y-r),(x-r*.35,y)])
    elif kind == 'sun':
        for i in range(12):
            a = i*math.tau/12
            pygame.draw.line(surface,color,(x+math.cos(a)*r*.7,y+math.sin(a)*r*.7),(x+math.cos(a)*r,y+math.sin(a)*r),2)
        pygame.draw.circle(surface,color,(int(x),int(y)),int(r*.45))
    elif kind == 'leaf':
        pygame.draw.ellipse(surface,color,(x-r,y-r,r*2,r*1.6))
        pygame.draw.line(surface,INK,(x-r*.5,y+r*.5),(x+r*.6,y-r*.6),3)
    elif kind == 'donkey':
        pygame.draw.polygon(surface,color,[(x-r*.6,y+r*.7),(x+r*.5,y+r*.4),(x+r*.7,y-r*.1),(x+r*.2,y-r*.5),(x+r*.1,y-r*1.2),(x-r*.15,y-r*.4),(x-r*.45,y-r*1.1),(x-r*.6,y-r*.2)])
    else:  # elephant
        pygame.draw.ellipse(surface,color,(x-r,y-r*.7,r*1.7,r*1.25))
        pygame.draw.rect(surface,color,(x-r*.8,y,r*.35,r))
        pygame.draw.rect(surface,color,(x+r*.15,y,r*.35,r))
        pygame.draw.arc(surface,color,(x+r*.2,y-r*.5,r*.95,r*1.5),math.pi,math.tau,6)

def card(kind, color, size=(100,75)):
    s = pygame.Surface(size, pygame.SRCALPHA)
    panel(s,s.get_rect().inflate(-4,-4),PANEL,color,8)
    pygame.draw.rect(s,color,(8,10,3,size[1]-20),border_radius=2)
    emblem(s,kind,pygame.Rect(13,5,size[0]-20,size[1]-10),color)
    return s

def board_background():
    s = pygame.Surface((1400,700))
    for y in range(700):
        t = 1-abs(y-350)/350
        pygame.draw.line(s,(12+int(t*8),20+int(t*10),34+int(t*13)),(0,y),(1400,y))
    pygame.draw.ellipse(s,(42,57,70),(70,32,1260,625),2)
    pygame.draw.ellipse(s,(33,48,64),(90,48,1220,593),1)
    panel(s,pygame.Rect(225,225,950,268),(15,26,41),(60,75,91),24)
    return s

def build_assets():
    """Export every runtime image as a new PNG, reproducible without an API."""
    for edition in ('Trump','Bian'):
        target = ROOT / 'assets' / edition.lower()
        target.mkdir(parents=True,exist_ok=True)
        opposition = RED if edition == 'Trump' else GREEN
        images = {'background':board_background(),
                  'blue':card('donkey' if edition=='Trump' else 'sun',BLUE),
                  'green':card('elephant' if edition=='Trump' else 'leaf',opposition),
                  'leader':card('leader',GOLD,(60,45)),
                  'execute':card('execute',RED),'search':card('search',GOLD),
                  'arrow':card('arrow',GOLD,(30,30)),
                  'dead':card('dead',MUTED,(31,30))}
        for name,color in [('yes',BLUE),('no',opposition)]:
            s=pygame.Surface((100,50),pygame.SRCALPHA)
            panel(s,s.get_rect().inflate(-2,-2),PANEL,color,9)
            images[name]=s
        for name,s in images.items():
            pygame.image.save(s,str(target/(name+'.png')))

if __name__ == '__main__':
    pygame.init()
    build_assets()
    pygame.quit()
