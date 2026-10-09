import pygame
import random
from game.ship import Ship
from game.meteor import Meteor
from game.laser import Laser
from game.powerup import ShieldOrb

WIDTH,HEIGHT=700,520
FPS=60
BG=(8,5,20)

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Meteor Dodge")
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont("monospace",26,bold=True)
        self.big_font=pygame.font.SysFont("monospace",46,bold=True)
        self.stars=[(random.randint(0,WIDTH),random.randint(0,HEIGHT),random.randint(1,3)) for _ in range(80)]
        self.reset()

    def reset(self):
        self.ship=Ship(WIDTH//2,HEIGHT-80)
        self.meteors=[]
        self.lasers=[]
        self.fire_cd=0
        self.orbs=[]
        self.orb_timer=random.randint(420,720)
        self.timer=0
        self.spawn_interval=60
        self.score=0
        self.frames=0
        self.streak=0
        self.multiplier=1
        self.game_over=False
        self.started=False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: return False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if self.game_over: self.reset()
                    elif not self.started:
                        self.started=True
                        self.fire_cd=15  # don't fire on the same press that launches
        return True

    def update(self):
        if self.game_over or not self.started: return
        keys=pygame.key.get_pressed()
        self.ship.move(keys,WIDTH,HEIGHT)
        # Task 1: laser firing (hold SPACE for auto-fire with cooldown)
        if self.fire_cd>0: self.fire_cd-=1
        if keys[pygame.K_SPACE] and self.fire_cd==0:
            self.lasers.append(Laser(self.ship.rect.centerx,self.ship.rect.top))
            self.fire_cd=12
        self.timer+=1
        if self.timer>=self.spawn_interval:
            self.meteors.append(Meteor(WIDTH))
            self.timer=0
            self.spawn_interval=max(20,self.spawn_interval-0.3)
        # Task 3: shield orbs spawn every ~7-12s and drift down
        self.orb_timer-=1
        if self.orb_timer<=0:
            self.orbs.append(ShieldOrb(WIDTH))
            self.orb_timer=random.randint(420,720)
        for o in self.orbs[:]:
            o.update()
            if o.collides(self.ship.rect):
                self.ship.shield=True
                self.orbs.remove(o)
        self.orbs=[o for o in self.orbs if not o.off_screen(HEIGHT)]
        for m in self.meteors[:]:
            m.update()
            if m.collides(self.ship.rect):
                if self.ship.shield:
                    self.ship.shield=False  # shield absorbs exactly one collision
                    self.streak=0  # taking a hit (even absorbed) resets the multiplier
                    self.meteors.remove(m)
                else:
                    self.game_over=True
        self.update_lasers()
        self.meteors=[m for m in self.meteors if not m.off_screen(HEIGHT)]
        # Task 4: +1 multiplier for every 10s (600 frames) survived without a hit
        self.frames+=1
        self.streak+=1
        self.multiplier=1+self.streak//600
        self.score+=self.multiplier

    def on_meteor_destroyed(self,m):
        self.meteors.extend(m.split())  # Task 2: large -> fragments, small -> gone

    def update_lasers(self):
        for l in self.lasers: l.update()
        for m in self.meteors[:]:
            for l in self.lasers:
                if l.hits(m):
                    self.lasers.remove(l)
                    self.meteors.remove(m)
                    self.on_meteor_destroyed(m)
                    break
        self.lasers=[l for l in self.lasers if not l.off_screen()]

    def draw(self):
        self.screen.fill(BG)
        for sx,sy,sr in self.stars:
            pygame.draw.circle(self.screen,(200,200,220),(sx,sy),sr)
        for o in self.orbs: o.draw(self.screen)
        for l in self.lasers: l.draw(self.screen)
        for m in self.meteors: m.draw(self.screen)
        self.ship.draw(self.screen)
        sc=self.font.render(f"Time: {self.frames//60}s",True,(200,200,240))
        self.screen.blit(sc,(10,10))
        pts=self.font.render(f"Score: {self.score//6}",True,(200,200,240))
        self.screen.blit(pts,(10,40))
        mcol=(255,220,80) if self.multiplier>1 else (160,160,200)
        mul=self.font.render(f"x{self.multiplier}",True,mcol)
        self.screen.blit(mul,(WIDTH-mul.get_width()-10,10))
        if self.started and not self.game_over:
            left=(600-self.streak%600)//60+1
            nxt=self.font.render(f"next x{self.multiplier+1} in {left}s",True,(120,120,160))
            self.screen.blit(nxt,(WIDTH-nxt.get_width()-10,40))
        if not self.started:
            msg=self.font.render("Press SPACE to launch",True,(180,180,240))
            self.screen.blit(msg,(WIDTH//2-msg.get_width()//2,HEIGHT//2))
            hint=self.font.render("WASD/Arrows move | SPACE shoots",True,(120,120,170))
            self.screen.blit(hint,(WIDTH//2-hint.get_width()//2,HEIGHT//2+40))
        if self.game_over:
            ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
            ov.fill((0,0,0,150))
            self.screen.blit(ov,(0,0))
            m=self.big_font.render("DESTROYED!",True,(220,80,60))
            s=self.font.render(f"Survived {self.frames//60}s | Score {self.score//6}",True,(200,200,200))
            r=self.font.render("SPACE to Restart",True,(200,200,200))
            self.screen.blit(m,(WIDTH//2-m.get_width()//2,HEIGHT//2-60))
            self.screen.blit(s,(WIDTH//2-s.get_width()//2,HEIGHT//2))
            self.screen.blit(r,(WIDTH//2-r.get_width()//2,HEIGHT//2+40))
        pygame.display.flip()

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()