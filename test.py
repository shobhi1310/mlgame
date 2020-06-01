import sys
import pygame


pygame.init()
display = pygame.display.set_mode([1000,600])
clock = pygame.time.Clock()
myfont = pygame.font.SysFont("Comic Sans MS",35,True,False)
fontcolor = pygame.Color("white")
label1 = myfont.render("Draw Card",1,(200,200,200))
label2 = myfont.render("Quite",1,(200,200,200))
label1_rect = label1.get_rect(topleft=(105, 470))
label2_rect = label2.get_rect(topleft=(750, 465))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if label1_rect.collidepoint(event.pos):  # event.pos is the mouse position.
                print("Hello love.")
            elif label2_rect.collidepoint(event.pos):
                print("No")

    display.fill((30, 30, 30))
    d = display.blit(label1, label1_rect)
    q = display.blit(label2, label2_rect)
    pygame.display.flip()
    clock.tick(30)