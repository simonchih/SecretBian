"""Bilingual guided sandbox. Each lesson requires a meaningful action."""
import pygame
from visual import *

EN = [
 ('Your secret identity', 'Ten players: you are Tina, alongside nine AI players. Six Democrats face three Republicans and D.T.; D.T. belongs to the Republican side. Reveal your practice role.', ['Reveal my role']),
 ('Who knows what?', 'Only ordinary Republicans recognize the other ordinary Republicans at the start. Democrats and D.T. know only their own role. Which role knows its Republican teammates?', ['Democrat', 'Republican', 'D.T.']),
 ('Nominate a chancellor', 'You are president. Choose a living candidate who is neither the previous president nor the previous chancellor. Click the eligible player.', ['Dunn · previous president', 'Tate · previous chancellor', 'Dyer · eliminated', 'Dan · eligible']),
 ('Cast your vote', 'Every living player votes. A strict majority is required; a tie fails. The nine AI players cast 5 YES and 4 NO. Try either vote to see the result.', ['YES', 'NO']),
 ('Three failed elections', 'A failed election raises the breakdown tracker. At three failures a policy is enacted automatically, without executive powers. Cause three failures to see the tracker reset.', ['Fail an election']),
 ('President: discard one', 'The president draws three policies and discards one. The other two go to the chancellor. Policy draws favor the Republican side, with a Democratic : Republican ratio of 10 : 19. Click a card to DISCARD it.', []),
 ('Chancellor: discard one', 'Now act as chancellor. Discard one of the two remaining cards. The last card is enacted. Your choice here really uses the cards you passed in the previous lesson.', []),
 ('Executive powers', 'Republican policy 3 or 5: eliminate one other living player. Policy 4: privately investigate a party. D.T. appears Republican during investigation. Which power can reveal a party without eliminating anyone?', ['Investigation', 'Elimination']),
 ('The nomination trap', 'After 4 Republican policies, nominating D.T. as chancellor immediately wins for Republicans, BEFORE a vote. This differs from Secret Hitler. Practice nominating D.T. now.', ['Nominate D.T.']),
 ('Victory & rotation', 'Democrats win with 5 policies or by eliminating D.T. Republicans win with 6 policies or the nomination shortcut. After a round or restart, the next living player clockwise becomes president. Which action wins immediately for Democrats?', ['Eliminate D.T.', 'Enact a fourth Democratic policy']),
]
ZH = [
 ('你的祕密身分', '共有十位玩家：你是「小鷹」，其餘九位由電腦扮演。六位國冥黨員屬於藍營；三位冥進黨員與一位扁維拉屬於綠營。先翻開練習用的身分牌。', ['翻開我的身分牌']),
 ('誰知道誰的身分？', '只有一般冥進黨員，能在開局辨識其他一般冥進黨員。國冥黨員與扁維拉起初只知道自己的身分。哪一種角色知道冥進黨隊友？', ['國冥黨員', '冥進黨員', '扁維拉']),
 ('提名院長候選人', '現在你是總統。請提名一位仍存活，而且不是上屆總統或上屆院長的玩家。請點選符合資格的候選人。', ['小賣 · 上屆總統', '小熊 · 上屆院長', '小倉 · 已死亡', '小力 · 符合資格']),
 ('投下你的一票', '每位存活玩家都能投票。同意票必須超過半數；平票也算失敗。九位電腦已投下五票同意、四票反對，試著投票，看看結果如何改變。', ['同意', '反對']),
 ('三次協商破局', '競選失敗會增加一次協商破局。累積三次時，強制頒布一項政策，並且不執行總統權力。請製造三次破局，觀察計數歸零。', ['讓這次選舉失敗']),
 ('總統：排除一張政策', '總統拿到三張政策，選一張排除，另外兩張交給院長。藍營與綠營政策的出現機率是十比十九，因此更容易抽到綠營政策。請點選一張要排除的牌。', []),
 ('院長：再排除一張', '現在換你扮演院長。從剛才留下的兩張牌中，再排除一張；最後一張就會頒布。這裡的牌，確實由上一個步驟的選擇決定。', []),
 ('總統的特殊權力', '第三、第五項綠營政策：暗殺一位其他存活玩家。第四項綠營政策：私下調查一位玩家的黨派。扁維拉的調查結果也是綠營。哪個權力能在不殺人的情況下得知黨派？', ['調查', '暗殺']),
 ('提名的陷阱', '綠營政策達四項後，只要提名扁維拉為院長候選人，綠營立即獲勝，不必投票。這與原版桌遊不同。現在試著提名扁維拉。', ['提名扁維拉']),
 ('勝利條件與輪替', '藍營頒布五項政策，或暗殺扁維拉，即獲勝。綠營頒布六項政策，或達成特殊提名條件，即獲勝。回合結束或重新開始時，由順時針下一位存活玩家接任總統。哪個行動讓藍營立即獲勝？', ['暗殺扁維拉', '頒布第四項藍營政策']),
]

class Tutorial:
    def __init__(self, edition):
        self.edition=edition
        self.en=edition=='Trump'
        self.lessons=EN if self.en else ZH
        self.step=0
        self.done=False
        self.feedback=''
        self.failures=0
        self.hand=[0,1,1]
        self.passed=[0,1]
        self.enacted=None

    def choose(self,index):
        if self.done:
            return
        correct={1:1,2:3,7:0,9:0}
        if self.step in correct and index!=correct[self.step]:
            self.feedback=('Try again. Check the rule above.' if self.en else '再試一次，請留意上方的規則提示。')
            return
        self.done=True
        self.feedback='Correct. Continue when ready.' if self.en else '答對了，準備好就繼續下一步。'
        if self.step==0:
            self.feedback='Your practice role: Democrat. Keep your identity secret.' if self.en else '你的練習身分是國冥黨員。請保守身分祕密。'
        elif self.step==3:
            self.feedback=(('6 YES / 4 NO: government elected.' if index==0 else '5 YES / 5 NO: tie, election fails.') if self.en else ('六票同意、四票反對：順利當選。' if index==0 else '五票同意、五票反對：平票，競選失敗。'))
        elif self.step==4:
            self.failures+=1
            self.done=self.failures==3
            self.feedback=(f'Breakdowns: {self.failures}/3' if self.en else f'協商破局：{self.failures}／3') if not self.done else ('Automatic Republican policy. Tracker resets to 0. No power.' if self.en else '強制頒布綠營政策；破局次數歸零，不執行權力。')
        elif self.step==5:
            self.passed=self.hand[:index]+self.hand[index+1:]
            self.feedback='One discarded. The other two pass to the chancellor.' if self.en else '已排除一張，剩下兩張交給院長。'
        elif self.step==6:
            self.enacted=self.passed[1-index]
            self.feedback=(('Democratic' if self.enacted==0 else 'Republican')+' policy enacted.') if self.en else ('藍營' if self.enacted==0 else '綠營')+'政策已頒布。'
        elif self.step==7:
            self.feedback='Private result: Republican. This could be a Republican OR D.T.' if self.en else '私人調查結果：綠營。對方可能是冥進黨員，也可能是扁維拉。'
        elif self.step==8:
            self.feedback='Republicans win immediately. No election takes place.' if self.en else '綠營立即獲勝，不進行選舉。'
        elif self.step==9:
            self.feedback='Democrats win! You are ready to play.' if self.en else '藍營獲勝！你已完成教學，可以開始遊戲了。'

    def move(self,delta):
        if delta>0 and not self.done:
            return
        self.step=max(0,min(len(self.lessons)-1,self.step+delta))
        self.done=False
        self.feedback=''
        self.failures=0

    def choices(self):
        if self.step in (5,6):
            hand=self.hand if self.step==5 else self.passed
            return [('Democratic' if p==0 else 'Republican') if self.en else ('藍營政策' if p==0 else '綠營政策') for p in hand]
        return self.lessons[self.step][2]

    def targets(self):
        choices=self.choices()
        if self.step in (5,6):
            return [pygame.Rect(530+i*225,342,200,220) for i in range(len(choices))]
        return [pygame.Rect(530,310+i*72,780,58) for i in range(len(choices))]

    def draw(self,screen,mouse):
        screen.fill(INK)
        label(screen,'FIELD MANUAL / SECRET TRUMP' if self.en else '實戰手冊 ／ 神祕阿扁',(55,35),19,GOLD)
        label(screen,'Learn by playing' if self.en else '邊操作，邊學會',(55,85),42)
        label(screen,'Guided practice · no effect on your real game' if self.en else '獨立練習，不影響正式遊戲',(55,150),18,MUTED)
        for i,(title,_,_) in enumerate(self.lessons):
            color=GOLD if i==self.step else MUTED
            label(screen,f'{i+1:02d}  {title}',(60,222+i*43),18,color)
            if i==self.step:
                pygame.draw.circle(screen,GOLD,(43,236+i*43),4)
        panel(screen,pygame.Rect(490,85,860,595),PANEL,(58,75,92),20)
        title,description,_=self.lessons[self.step]
        label(screen,f'{self.step+1:02d} / 10',(530,110),18,GOLD)
        label(screen,title,(530,148),32)
        wrap(screen,description,pygame.Rect(530,205,770,105),21)
        for i,(text,rect) in enumerate(zip(self.choices(),self.targets())):
            button(screen,rect,text,rect.collidepoint(mouse),not self.done,20)
            if self.step in (5,6):
                party=(self.hand if self.step==5 else self.passed)[i]
                kind=('donkey' if self.en else 'sun') if party==0 else ('elephant' if self.en else 'leaf')
                emblem(screen,kind,pygame.Rect(rect.x+35,rect.y+15,130,75),BLUE if party==0 else RED if self.en else GREEN)
                label(screen,'DISCARD' if self.en else '排除這張',(rect.centerx,rect.bottom-36),18,GOLD,True)
        if self.step==4:
            for i in range(3):
                pygame.draw.circle(screen,GOLD if i<self.failures and not self.done else MUTED,(760+i*120,460),24,3)
                label(screen,str(i+1),(760+i*120,460),18,TEXT,True)
        if self.feedback:
            wrap(screen,self.feedback,pygame.Rect(530,602,765,66),20,GOLD)
        pygame.draw.rect(screen,(45,59,76),(490,700,860,4),border_radius=2)
        pygame.draw.rect(screen,GOLD,(490,700,860*(self.step+int(self.done))/10,4),border_radius=2)
        button(screen,pygame.Rect(55,725,205,48),'Main menu' if self.en else '返回主選單',False,size=18)
        button(screen,pygame.Rect(490,725,170,48),'Back' if self.en else '上一步',False,self.step>0,18)
        button(screen,pygame.Rect(680,725,190,48),'Try again' if self.en else '重新練習',False,True,18)
        button(screen,pygame.Rect(1090,725,260,48),('Play Secret Trump' if self.en else '開始阿扁版') if self.step==9 else ('Continue' if self.en else '下一步'),False,self.done,18)

    def click(self,pos):
        if pygame.Rect(55,725,205,48).collidepoint(pos): return 'menu'
        if pygame.Rect(490,725,170,48).collidepoint(pos) and self.step>0: self.move(-1)
        elif pygame.Rect(680,725,190,48).collidepoint(pos): self.move(0)
        elif pygame.Rect(1090,725,260,48).collidepoint(pos) and self.done:
            if self.step==9: return 'play'
            self.move(1)
        else:
            for i,rect in enumerate(self.targets()):
                if rect.collidepoint(pos): self.choose(i)
        return None
