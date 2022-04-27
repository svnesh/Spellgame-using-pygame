import pygame
import os
from pygame import mixer

img_dir = "img/bodyparts"
img = {}
#counter = 1
limit = len(os.listdir(img_dir))

applause = "sound/applause.mp3"
error = "sound/error.mp3"

#Read all images from folder, correct answer will be file name eg. nose.jpg -- nose is the (answer)
for num,item in enumerate(os.listdir(img_dir)):
    img_details = []
    img_details.append(item.split('.')[0])
    img_details.append(os.path.join(img_dir, item))
    tempD = 'page' + str(num)
    img[tempD] = img_details

pygame.init()
pygame.mixer.init()

#window sizing
width = 600
height = 600

#image position/sizing
img_width = 200
img_x = 200
img_y = 100

#input text position/sizing
text_width = 200
text_height = 55
text_x = 100
text_y = 350

#submit button
btn_height = 80
btn_width = 100
btn_x = 320
btn_y = 330

#Frames count
FPS = 10

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 55, True)
user_txt = ''

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Spell Game")

#rectangle for text field
input_rect = pygame.Rect(text_x, text_y, text_width, text_height)
#color active
color_active = pygame.Color('chartreuse3')
color_passive = pygame.Color('azure')
text_color = color_passive

#button
submit_btn = pygame.image.load('img/common/submit.png')
submit_rect = submit_btn.get_rect()
submit_btn = pygame.transform.scale(submit_btn, (btn_height, btn_height))
mask = pygame.mask.from_surface(submit_btn)

correct_btn = pygame.image.load('img/common/correct.png')
correct_btn = pygame.transform.scale(correct_btn, (btn_height, btn_height))
correct_x = 440
correct_y = 330

wrong_btn = pygame.image.load('img/common/wrong.png')
wrong_btn = pygame.transform.scale(wrong_btn, (btn_height, btn_height))

next_btn = pygame.image.load('img/common/next.png')
next_rect = next_btn.get_rect()
next_btn = pygame.transform.scale(next_btn, (btn_height, btn_height))
next_x = 500
next_y = 450
next_mask = pygame.mask.from_surface(next_btn)

global pic1, correct_ans, Mypage
Mypage = 0

def checkSpelling(user_txt):
    if user_txt == correct_ans:
        return True
    else:
        return False

#picture
if Mypage == 0:
    pic1 = pygame.image.load(img['page0'][1])
    pic1 = pygame.transform.scale(pic1, (img_width, img_width))
    correct_ans = img['page0'][0]

run = True
text_active = False
correct = False
wrong = False
next_page = False

while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                text_active = True
            elif submit_rect.collidepoint(event.pos):
                if user_txt != '':
                    musicLoop = 0
                    if checkSpelling(user_txt):
                        correct = True
                        wrong = False
                        Mypage += 1
                        user_txt = ''
                        text_active = False
                        if Mypage > limit:
                            break
                    else:
                        wrong = True
                        correct = False
            elif next_rect.collidepoint(event.pos):
                next_page = True
                correct = False
                wrong = False
                user_txt = ''
            else:
                text_active = False
                next_page = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_txt = user_txt[:-1]
            else:
                user_txt += event.unicode

    if text_active:
        text_color = color_active
    else:
        text_color = color_passive

    win.fill((0,0,0))

    #blit main picture
    if Mypage == 0:
        win.blit(pic1, (img_x, img_y))

    #blit the text field
    pygame.draw.rect(win, text_color, input_rect)
    text_surface = font.render(user_txt, True, (0,0,0))
    win.blit(text_surface, (input_rect.x+5, input_rect.y-14))
    
    #blit submit button
    win.blit(submit_btn, (btn_x, btn_y))

    if correct:
        win.blit(correct_btn, (correct_x, correct_y))
        if musicLoop == 0:
            mixer.music.load(applause)
            mixer.music.play()
            while mixer.music.get_busy(): 
                clock.tick(1)
            musicLoop += 1
        if Mypage < limit:
            win.blit(next_btn, (next_x, next_y))
        else:
            next_page = False
    elif wrong:
        win.blit(wrong_btn, (correct_x, correct_y))
        if musicLoop == 0:
            mixer.music.load(error)
            mixer.music.play()
            while mixer.music.get_busy(): 
                clock.tick(1)
            musicLoop += 1
    
    if next_page:
        temp_obj = 'page' + str(Mypage)
        myImage = img[temp_obj][1]
        pic1 = pygame.image.load(myImage)
        pic1 = pygame.transform.scale(pic1, (img_width, img_width))
        win.blit(pic1, (img_x, img_y))
        correct_ans = img[temp_obj][0]       


    pygame.display.update()