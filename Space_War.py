import pygame,sys,os,random
pygame.init()

###### TEMEL AYARLAR ########
widht = 966
height = 564

boyut = (widht,height)
##############################

level = 1

#Klasörler#
klasor = os.path.dirname(__file__)
resimKlasoru = os.path.join(klasor,"resimler")
sesKlasoru = os.path.join(klasor,"sesler")
#############

###### Patlama Klasörü ######
patlamaKlasoru = os.path.join(klasor,"patlama")
patlamaResimleri = []
for i in range(1,10):
    patlamaResimleri.append("{}.png".format(i))
############################

############# GÜÇLENDİRİCİ RESİMLERİ #########
powerUps = ["star_gold.png","bolt_gold.png","bolt_gold.png","bolt_gold.png","bolt_gold.png"]
##############################################

#####Çarpma Efektleri####
carpmaEfektleri = ["hefect1.wav","hefect2.ogg","hefect3.wav"]
#############

######################### RESİMLER ######################
background = pygame.image.load(os.path.join(resimKlasoru,"background.png"))
fire = pygame.image.load(os.path.join(resimKlasoru,"fire.png"))
ship = pygame.image.load(os.path.join(resimKlasoru,"ship.png"))
#############################

###### MÜZİK ####
pygame.mixer.music.load(os.path.join(sesKlasoru,"starblast.mp3"))
pygame.mixer.music.play()
################################

############## EFEKTLER ###############
hitEffect = pygame.mixer.Sound(os.path.join(sesKlasoru,"hit.flac"))
fireEffect = pygame.mixer.Sound(os.path.join(sesKlasoru,"laser1.ogg"))
speedGain = pygame.mixer.Sound(os.path.join(sesKlasoru,"speedUp.wav"))
liveGain = pygame.mixer.Sound(os.path.join(sesKlasoru,"lifeup.wav"))
####################################

###################### AYARLAR ##################
pencere = pygame.display.set_mode(boyut)

clock = pygame.time.Clock()

font = pygame.font.SysFont("Helvetica",50)



asteroidler = ["asteroid.png", "asteroid2.png", "asteroid3.png", "asteroid4.png",
               "asteroid.png", "asteroid2.png", "asteroid3.png", "asteroid4.png",
               "asteroid.png", "asteroid2.png", "asteroid3.png", "asteroid4.png",
               "asteroid.png", "asteroid2.png", "asteroid3.png", "asteroid4.png",
               "asteroidcan.png","asteroidcan.png"]

all_sprites = pygame.sprite.Group()
###################################################



#########       UZAY GEMİSİ       ########
class Parca(pygame.sprite.Sprite):
    def __init__(self,x = widht /2, y = height /2):
        super().__init__()
        self.image = ship.convert()
        self.can = 3
        self.image.set_colorkey((0,0,0))
        #self.image.fill((0,130,255))
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image,(255,0,0),self.rect.center,self.radius)
        self.rect.x = 0
        self.rect.y = y
        self.kalkan = 100
        self.mermiDelay = 250
        self.sonAtes = pygame.time.get_ticks()
        self.hider_time = 1500
        self.isHide = False
        self.lastHide = pygame.time.get_ticks()
        self.boostStart = 0

    def changeBulletSpeed(self,speed):
        self.mermiDelay = speed
        self.boostStart = pygame.time.get_ticks()


    def hide(self):
        self.isHide = True
        self.lastHide = pygame.time.get_ticks()
        self.rect.center = (-200,height/2)

    def update(self, *args):
        up,down,right,left,shoot = args

        if self.isHide and pygame.time.get_ticks() - self.lastHide > self.hider_time:
            self.isHide = False
            self.rect.x = 0
            self.rect.y = height/2

        if pygame.time.get_ticks() - self.boostStart > 5000:
            self.changeBulletSpeed(250)

        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y + self.rect.size[1] > height:
            self.rect.y = height - self.rect.size[1]

        if up:
            self.rect.y -= 10
        if down:
            self.rect.y += 10

        if shoot:
            self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.sonAtes > self.mermiDelay:
            self.sonAtes = now
            fireEffect.play()
            fuze = Fuze(self.rect.y)
            all_sprites.add(fuze)
            fuzeler.add(fuze)
###### UZAY GEMİSİ BİTİŞ ######



###### METEOR #######
class Mermi(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.secim = random.choice(asteroidler)
        asteroid = pygame.image.load(os.path.join(resimKlasoru, self.secim))
        self.image = asteroid.convert()
        self.orjinal_resim = self.image
        self.image.set_colorkey((0,0,0))
        #self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.radius = int((self.rect.width * 0.70) / 2)
        #pygame.draw.circle(self.image, (255, 0, 0), self.rect.center, self.radius)

        self.rect.y = random.randrange(height-self.rect.height)
        self.rect.x = random.randrange(widht+40,widht+100)
        self.speedx = random.randrange(5,15)
        self.speedy = random.randrange(-2,2)

        self.rot = 0
        self.rotateSpeed = random.randrange(-20,20)
        self.lastUpdate = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.lastUpdate > 50:
            self.lastUpdate = now
            self.rot = (self.rot + self.rotateSpeed) % 360
            new_image = pygame.transform.rotate(self.orjinal_resim,self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self, *args):
        self.rotate()
        self.rect.x -= self.speedx
        self.rect.y += self.speedy

        if self.rect.right < 0:
            self.rect.y = random.randrange(height - self.rect.height)
            self.rect.x = random.randrange(widht + 40, widht + 100)
            self.speedx = random.randrange(10,13)
            self.speedy = random.randrange(-3, 3)
            global score
            score += 1
########### METEOR BİTİŞ ##########

############ Patlama Sınıfı #########
class Patlama(pygame.sprite.Sprite):
    def __init__(self,meteor,klasor,liste):
        super().__init__()
        self.meteor = meteor
        self.klasor =  klasor
        self.liste = liste
        self.sayac = 1
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(klasor,self.liste[self.sayac])),self.meteor.image.get_size())
        self.rect = self.image.get_rect()
        self.rect.center = self.meteor.rect.center
        self.delay = 75
        self.sonDegisim = pygame.time.get_ticks()

    def update(self, *args):
        now = pygame.time.get_ticks()
        if now - self.sonDegisim > self.delay:
            self.sonDegisim = now
            self.image = pygame.transform.scale(pygame.image.load(os.path.join(self.klasor,self.liste[self.sayac])),self.meteor.image.get_size())
            self.rect = self.image.get_rect()
            self.rect.center = self.meteor.rect.center
            self.sayac += 1

        if self.sayac == len(self.liste):
            self.kill()
#####################################



######### GÜÇLENDİRİCİ #############
class PowerUp(pygame.sprite.Sprite):
    def __init__(self,center):
        super().__init__()
        self.choice = random.choice(powerUps)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(resimKlasoru,self.choice)),(25,25))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedX = 5
    def update(self, *args):
        self.rect.x -= self.speedX
####################################



######### ATEŞ ETME ############
class Fuze(pygame.sprite.Sprite):
    def __init__(self,parcay):
        super().__init__()
        self.image = fire
        #self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = parcay + 20

    def update(self, *args):
        self.rect.x += 8

        if self.rect.left > widht:
            self.kill()
####### ATEŞ ETME BTİŞ ############


sayacSifirlama = True


## KALKAN GÖRSEL ##
def kalkanCiz(pencere,x,y,deger):
    if deger < 0:
        deger = 0
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = ( deger / 100 ) * BAR_LENGHT
    outline_rect = pygame.Rect(x,y,BAR_LENGHT,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(pencere,(255,255,255),outline_rect,3)
    if deger >= 60:
        pygame.draw.rect(pencere,(0,255,0),fill_rect)
    elif deger > 30 and deger < 60:
        pygame.draw.rect(pencere, (204, 204, 0), fill_rect)
    elif deger < 30:
        pygame.draw.rect(pencere, (255, 0, 0), fill_rect)
################################################

########### CAN GÖRSEL #################
def canCiz(pencere,x,y,can):
    img = pygame.transform.scale(pygame.image.load(os.path.join(resimKlasoru,"canShip.png")),(20,15))
    img_rect = img.get_rect()
    for i in range(can):
        img_rect.x = x + (40*i)
        img_rect.y = y
        pencere.blit(img,img_rect)
########################################

game_over = True
def show_gameover_screen():
    kontrol = True
    endstart = pygame.image.load(os.path.join(resimKlasoru,"endstart.png"))
    pencere.blit(endstart,endstart.get_rect())
    pygame.display.update()
    while kontrol:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    kontrol = False



### OYUN LOOP ###
while True:
    if game_over:
        show_gameover_screen()
        game_over = False

        # GRUPLAR
        all_sprites = pygame.sprite.Group()
        mermiler = pygame.sprite.Group()
        fuzeler = pygame.sprite.Group()
        powerGains = pygame.sprite.Group()

        # MERMİ SAYISI
        for i in range(15):
            mermi = Mermi()
            all_sprites.add(mermi)
            mermiler.add(mermi)

        parca1 = Parca()
        all_sprites.add(parca1)


        score = 0



    pencere.fill((255, 255, 255))
    pencere.blit(background,background.get_rect())
    mermiSayisi = len(mermiler)

    keys = pygame.key.get_pressed()


    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:sys.exit()

    up,down,right,left,shoot = keys[pygame.K_UP],keys[pygame.K_DOWN],keys[pygame.K_RIGHT],keys[pygame.K_LEFT],keys[pygame.K_SPACE]
    all_sprites.update(up,down,right,left,shoot)

    fontScore = font.render("Kalan Meteor : {} ".format(mermiSayisi),1,(255,0,0),)

    all_sprites.draw(pencere)

    pencere.blit(fontScore, (widht - fontScore.get_size()[0], height - fontScore.get_size()[1]))

    durum = pygame.sprite.spritecollide(parca1,mermiler,True,collided=pygame.sprite.collide_circle)

    isHit = pygame.sprite.groupcollide(fuzeler,mermiler,True,True)

    if isHit:
        hitEffect.play()
        for metorlar in isHit.values():
            for meteor in metorlar:
                kaboom = Patlama(meteor,patlamaKlasoru,patlamaResimleri)
                all_sprites.add(kaboom)
                if random.random() > 0.90:
                    powerGain = PowerUp(meteor.rect.center)
                    powerGains.add(powerGain)
                    all_sprites.add(powerGain)
                if meteor.secim == "asteroidcan.png":
                    if parca1.kalkan + 10 < 100:
                        parca1.kalkan += 10
                    else:
                        parca1.kalkan = 100

    isPowerGain = pygame.sprite.spritecollide(parca1,powerGains,True)

    if isPowerGain:
        for powerType in isPowerGain:
            if powerType.choice == "bolt_gold.png":
                speedGain.play()
                parca1.changeBulletSpeed(130)
            else:
                liveGain.play()
                parca1.can += 1

    if durum:
        pygame.mixer.Sound(random.choice(carpmaEfektleri)).play()
        for meteor in durum:
            boom = Patlama(meteor,patlamaKlasoru,patlamaResimleri)
            all_sprites.add(boom)
            parca1.kalkan -= meteor.radius * 2
            
    kalkanCiz(pencere,5,5,parca1.kalkan)
    canCiz(pencere,5,25,parca1.can)
    
    if durum or mermiSayisi == 0:
        if parca1.kalkan <= 0:
            pygame.mixer.music.load(os.path.join(sesKlasoru, "explode.mp3"))
            pygame.mixer.music.play()
            parca1.can -= 1
            parca1.hide()

            if parca1.can == 0:
                game_over = True

            parca1.kalkan = 100

        if mermiSayisi == 0:
            if sayacSifirlama:
                bitisDegeri = pygame.time.get_ticks()
                sayacSifirlama = False
                levelYaziFont = pygame.font.SysFont("Helvetica",50)
                yazi = levelYaziFont.render("Level{}".format(level+1),1,(0,255,0))
            pencere.blit(yazi,(10,20))
            
            if pygame.time.get_ticks() - bitisDegeri > 4000:
                sayacSifirlama = True
                level += 1
                for i in range(level * 15):
                    mermi = Mermi()
                    all_sprites.add(mermi)
                    mermiler.add(mermi)

    pygame.display.update()
