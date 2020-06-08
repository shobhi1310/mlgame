
import pygame, math, sys, pylab, random
from pygame import *
from math import *
pygame.init()

font = pygame.font.SysFont('Verdana',16)
font2 = pygame.font.SysFont('Serif',24)
font3 = pygame.font.SysFont('Arial',14)

white = (255,255,255)
black = (0,0,0)
graphcolor = (200,0,200) #purple
gridcolor = (100,250,240) #light blue
titlecolor = (200,0,150) #darker purple
green = (0,200,50)
blue = (0,50,200)
red = (255,0,0)

width,height = 700, 600
extraW = 500
screen = pygame.display.set_mode((width+extraW,height))
pygame.display.set_caption("Overfitting and underfitting !!")

show = False
overfit = False
model = []
plot_x = [i for i in range(-13,14)]
plot_y = []


#scientific notation to lay man conversion LOL!
def decimal_str(x: float, decimals: int = 10) -> str:
    return format(x, f".{decimals}f").lstrip().rstrip('0')

# generating a noisy parabola WHEW!
def genNoisyParabolicData(a, b, c, xVals, fName):
    yVals = []
    for x in xVals:
        theoreticalVal = a*x**2 + b*x + c
        yVals.append(theoreticalVal + random.gauss(0, 1))
    f = open(fName,'w')
    f.write('x        y\n')
    for i in range(len(yVals)):
        f.write(str(xVals[i]) + ' ' + str(yVals[i]) + '\n')
    f.close()
    return yVals

#for creating overfit
def fitData1():
    xVals = pylab.array(plot_x)
    yVals = pylab.array(plot_y)         
    model = pylab.polyfit(xVals, yVals, 4)
    estYVals = pylab.polyval(model, xVals)
    return model
    

#graph paper function
# this code itself draws graphpaper
def graphpaper(k):
    screen.set_clip(0,0,width,height)
    screen.fill(white)

    #draw graph paper
    for i in range(int(width/k)):
        gridx = k*i
        gridy = k*i
        pygame.draw.line(screen, gridcolor, (gridx,0), (gridx,height), 1)
        pygame.draw.line(screen, gridcolor, (0,gridy), (width, gridy), 1)
    # extra thick line
    pygame.draw.line(screen, gridcolor, (width,0), (width, height), 5)

    # graph x and y axis
    midx, midy = width/(2*k), height/(2*k)
    pygame.draw.line(screen, black, (midx*k,0), (midx*k,height), 3)
    pygame.draw.line(screen, black, (0,midy*k), (width,midy*k), 3)

    #clip reset to all the window
    screen.set_clip(None)
    
def mymain(Graphs,eq):
    #pixle per grid (always use a k that is a factor of width and height) // for ease of axis plotting
    global show
    global plot_x
    global plot_y

    k = 25
    # show = False

    # start an array that will hold equation
    if Graphs == 1:        
        screen.fill(white)
        graphpaper(k)
        equation=[]
        eq2= ' '
    else:
        screen.set_clip(width, 0, width+extraW, height)
        screen.fill(white)
        screen.set_clip(None)
        eq2 = eq
        equation=[]
    
    #instructions and results
    title = font2.render("Overfitting and Underfitting",1,titlecolor)
    screen.blit(title, (width+10, 20))

    instruct = font.render("Type in any equation. Ex -0.1*x^2+7",1,black) # -0.1*x^2+7
    screen.blit(instruct, (width+10, 70))

    instruct = font.render("Select 'Enter' when done or 'q' to start over.",1,black)
    screen.blit(instruct, (width+10, 100))

    instruct = font.render("Select 'd' to display scatter plots",1,red)
    screen.blit(instruct, (width+10, 130))

    instruct = font.render("Select 'Backspace' to clear.",1,black)
    screen.blit(instruct, (width+10, 160))
    
    instruct = font3.render("s=sin(), c=cos(), t=tan(), r=sqrt(), a=abs(), l=log10(), n=log(), e=e, p=pi",1,black)
    screen.blit(instruct, (width+10, 190))

    done=False  

    # active loop     
    active = True
    while active:
        # update the screen
        screen.set_clip(width+10, height-30, width+extraW, height)
        screen.fill(white)
 
        #join equation array without commas.
        eq = ",".join(equation)
        eq = eq.replace(",","")

        #render and blit equation
        eqshow = font.render("Function:  y = "+eq,1,titlecolor)
        screen.blit(eqshow, (width+10,height-30))
        
        pygame.display.update()

        #for plotting scatter
        
        #keyboard and mouse actions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
                done = True


            elif event.type == pygame.KEYDOWN:

                #math operations and symbols for the equation
                if event.unicode == u'*':
                    equation.append("*")
                elif event.unicode == u'+':
                    equation.append("+")
                elif event.unicode == u'/':
                    equation.append("/")
                elif event.unicode == u'-':
                    equation.append("-")
                elif event.unicode == u'.':
                    equation.append(".")
                elif event.unicode == u'(':
                    equation.append("(")
                elif event.unicode == u')':
                    equation.append(")")
                elif event.unicode == u'^':
                    equation.append("**")

                    

                # numbers typed in for equation and the x variable
                elif event.key == K_1:
                    equation.append("1")
                elif event.key == K_2:
                    equation.append("2")
                elif event.key == K_3:
                    equation.append("3")
                elif event.key == K_4:
                    equation.append("4")
                elif event.key == K_5:
                    equation.append("5")
                elif event.key == K_6:
                    equation.append("6")
                elif event.key == K_7:
                    equation.append("7")
                elif event.key == K_8:
                    equation.append("8")
                elif event.key == K_9:
                    equation.append("9")
                elif event.key == K_0:
                    equation.append("0")

                #math function commands
                elif event.key == K_s:
                    equation.append("sin(")
                elif event.key == K_c:
                    equation.append("cos(")                
                elif event.key == K_t:
                    equation.append("tan(")                
                elif event.key == K_r:
                    equation.append("sqrt(")
                elif event.key == K_a:
                    equation.append("abs(")                
                elif event.key == K_l:
                    equation.append("log10(")                
                elif event.key == K_n:
                    equation.append("log(")                
                elif event.key == K_e:
                    equation.append("e")                
                elif event.key == K_p:
                    equation.append("pi")                
                elif event.key == K_x:
                    equation.append("x")

                elif event.key == K_RETURN:
                    active = False
                elif event.key == K_BACKSPACE:
                    equation = []
                elif event.key == K_d:
                    print('Clicked')
                    plot_y = genNoisyParabolicData(-0.1,0,7,plot_x,'D:/knn_game/score.txt')
                    show = True
                    active = False
                elif event.key == K_q:
                    mymain(1,' ')
        
    # an option to quit at entering equation or to graph
    if done:
        # only thing left to do is quit
        pygame.quit()
    else:
        # clip right side of the screen (except equation)
        screen.set_clip(width,0,width+extraW,height-30)
        screen.fill(white)
        screen.set_clip(None)

        #graph equation function called
        print(eq)
        GraphEq(eq,eq2,k)
    sys.exit()
def GraphEq(eq,eq2,k):
    global model
    global overfit

    #graphing of the equation
    for i in range(width):
        try:
            x = (width/2-i)/float(k)
            y = eval(eq)
            pos1 = (width/2+x*k, height/2-y*k)

            nx = x = (width/2-(i+1))/float(k)
            ny = eval(eq)
            pos2 = (width/2+nx*k, height/2-ny*k)

            pygame.draw.line(screen, graphcolor, pos1, pos2, 3)
        except:
            pass
        try:
            x = (width/2-i)/float(k)
            y2 = eval(eq2)
            pos21 = (width/2+x*k, height/2-y2*k)

            nx = x = (width/2-(i+1))/float(k)
            ny2 = eval(eq2)
            pos22 = (width/2+nx*k, height/2-ny2*k)

            pygame.draw.line(screen, graphcolor, pos21, pos22, 3)
        except:
            pass

    #clip the screen to keep text clean
    screen.set_clip(width,0,width+extraW,height-30)
    screen.fill(white)
    #instructions and results
    title = font2.render("Use it as a plotter LOL!!",1,titlecolor)
    screen.blit(title, (width+10, 20))
    instruct = font.render("Select 'q' to start over.",1,black)
    screen.blit(instruct, (width+10, 70))

    #compute and display y-intercept
    x = 0
    try:
        yint = eval(eq)
        yint = round(yint,2)
    except:
        yint = 'dne'
    
    instruct = font.render("The y-intercept is at (0,"+str(yint)+")",1,green)
    screen.blit(instruct, (width+10, 100))

    if yint != 'dne':
        instruct = font.render("Select 'y' to plot the intercept",1,green)
        screen.blit(instruct, (width+10, 120))

    # resize of grid instructions
    instruct = font.render("Select 's' 'm' 'l' 'o' for grid sizes.",1,black)
    screen.blit(instruct, (width+10, height-70))

    #instruction for new graph
    instruct = font.render("Select 'g' to add another graph.",1,black)
    screen.blit(instruct, (width+10, height-100))

    instruct = font.render("Type in value, select 'Enter' to plot the point.",1,blue)
    screen.blit(instruct, (width+20, 150))

    #plotting of x values
    xValue = []
    xVal = '?'
    yVal = '?'  

    #reset clip of screen
    screen.set_clip(None)
    
    # run a infinite loop to control the window
    active=True
    while active:
        #clip the screen to show x and y value
        screen.set_clip(width+10,150, width+extraW,200)
        screen.fill(white)
        xDisplay = ",".join(xValue)
        xDisplay = xDisplay.replace(",","")
        plotx = font.render("x = "+str(xDisplay),1,blue)
        screen.blit(plotx, (width+10, 170))
        ploty = font.render("("+str(xVal)+","+str(yVal)+")",1,blue)
        screen.blit(ploty, (width+210, 170))
        screen.set_clip(None)

        #update the screen
        pygame.display.update()

        #graphing overfit curve
        if overfit:
            # fitting_equation = ''
            # for i in range(8):
            #     fitting_equation.append()
            fitting_equation = decimal_str(model[0])+'*x**4'+(decimal_str(model[1]) if model[1]<0 else ('+'+decimal_str(model[1])))+'*x**3'+(decimal_str(model[2]) if model[2]<0 else ('+'+decimal_str(model[2])))+'*x**2'+(decimal_str(model[3]) if model[3]<0 else ('+'+decimal_str(model[3])))+'*x'+(decimal_str(model[4]) if model[4]<0 else ('+'+decimal_str(model[4])))
            # fitting_equation = decimal_str(model[0])+'*x**4'+decimal_str(model[1])+'*x**3'+decimal_str(model[2])+'*x**2'+decimal_str(model[3])+'*x'+decimal_str(model[4])
            # print(fitting_equation)
            for i in range(width):
                try:
                    x = (width/2-i)/float(k)
                    y = eval(fitting_equation)
                    print(y)
                    pos1 = (width/2+x*k, height/2-y*k)

                    nx = x = (width/2-(i+1))/float(k)
                    ny = eval(eq)
                    pos2 = (width/2+nx*k, height/2-ny*k)

                    pygame.draw.line(screen, graphcolor, pos1, pos2, 3)
                except:
                    pass
                try:
                    x = (width/2-i)/float(k)
                    y2 = eval(fitting_equation)
                    pos21 = (width/2+x*k, height/2-y2*k)

                    nx = x = (width/2-(i+1))/float(k)
                    ny2 = eval(eq2)
                    pos22 = (width/2+nx*k, height/2-ny2*k)

                    pygame.draw.line(screen, graphcolor, pos21, pos22, 3)
                except:
                    pass
        
        if show:
            for i in range(len(plot_x)):
                # (int(width/2+x*k),int(height/2-yVal*k))
                pygame.draw.circle(screen,blue,(int(width/2+ plot_x[i]*k),int(height/2-plot_y[i]*k)),4)

        #keyboard and mouse actions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
            # commands for starting over and other features
            elif event.type == pygame.KEYDOWN:
                if event.key == K_q:
                    mymain(1,' ')
                elif event.key == K_y:
                    pygame.draw.circle(screen, green, (int(width/2),int(height/2-yint*k)),4)

                #resize commands
                elif event.key == K_s:
                    k = 25
                    graphpaper(k)
                    GraphEq(eq,eq2,k)
                elif event.key == K_m:
                    k = 20
                    graphpaper(k)
                    GraphEq(eq,eq2,k)
                elif event.key == K_l:
                    k = 10
                    graphpaper(k)
                    GraphEq(eq,eq2,k)
                elif event.key == K_o:
                    k = 5
                    graphpaper(k)
                    GraphEq(eq,eq2,k)

                elif event.key == K_r:
                    model = fitData1()
                    overfit = True
                    print(model)

                #add new graph and plot points
                elif event.key == K_g:
                    mymain(2,eq)
                           
                elif event.key == K_RETURN:
                    try:
                        x = xVal = float(xDisplay)
                        yVal = eval(eq)
                        ## there is some bug here its hard to identify
                        ## used for plotting the given x, y co-ordinates
                        pygame.draw.circle(screen, blue, (int(width/2+x*k),int(height/2-yVal*k)),4)
                        # xValue=[]
                    except:
                        pass

            # numbers typed in for equation and the x variable
                elif event.key == K_1:
                    xValue.append("1")
                elif event.key == K_2:
                    xValue.append("2")
                elif event.key == K_3:
                    xValue.append("3")
                elif event.key == K_4:
                    xValue.append("4")
                elif event.key == K_5:
                    xValue.append("5")
                elif event.key == K_6:
                    xValue.append("6")
                elif event.key == K_7:
                    xValue.append("7")
                elif event.key == K_8:
                    xValue.append("8")
                elif event.key == K_9:
                    xValue.append("9")
                elif event.key == K_0:
                    xValue.append("0")
                elif event.key == K_BACKSPACE:
                    xValue = xValue[:-1]
                elif event.unicode == u'.':
                    xValue.append(".")
                elif event.unicode == u'-':
                    xValue.append("-")

    pygame.quit()
    sys.exit()
        
    
if __name__=='__main__':
    mymain(1,' ')