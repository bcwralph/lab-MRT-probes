import sys, pygame, numpy, random, EasyDialogs, datasaver, text_wrapper
pygame.init()
clock=pygame.time.Clock()

#collect subject information
subject = int(EasyDialogs.AskString("Please enter the subject number:")) #int. says it must be an integer
sona_id = int(EasyDialogs.AskString("Please enter the subject's sona id:"))
subject_sex = str(EasyDialogs.AskString("Enter participant's sex (m or f):"))
subject_age = str(EasyDialogs.AskString("Enter participant's age:"))

#create data file
datasaver.save("data/"+str(subject),("subject", "sona_id", "sex", "age", "trial", "omission", "RT_from_metronome", "ProbeResponses"))

#set window, center, and mouse
window=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
center = window.get_rect().center
pygame.mouse.set_visible(False)

#fonts
fontName = pygame.font.match_font('Times New Roman')
font = pygame.font.Font(fontName, 28)

#colours
black = (0, 0, 0)
white = (255, 255, 255)
grey = (112,112,112)
green = (0,200,0)

#set keys
exitKey = pygame.K_e
continueKey = pygame.K_SPACE
skipKey = pygame.K_n
terminate = pygame.K_t
startKey = pygame.K_s
selfCaughtKey = pygame.K_m
#Probe 1=On task or MW, if MW, Probe 2 = Spontaneous or Deliberate
#Self caught -- Probe 2

#display messages
text_pos = (100,100)

instructionsP1 = text_wrapper.drawText('For this experiment, you will hear a metronome sound presented at a constant rate via the headphones.' 
+'\n\nYour task is to press the SPACEBAR in synchrony with the onset of the metronome,'
+' so that you press the space bar exactly when each metronome sound is presented.'
+' Please keep your eyes fixated on the monitor while you complete this task.'
+'\n\nEvery once in a while, the task will temporarily stop and you will be presented with a thought-sampling screen'
+' that will ask you to indicate whether you were ON TASK or MIND WANDERING just before the thought-sampling screen appeared.', 
white, surface=pygame.transform.scale(window, (1200,1200)), lineSpacing = 3, font=font)

instructions= [instructionsP1[0]] #add instructions to this array
    
practice_over = text_wrapper.drawText('The practice trials are now over.'
+'\n\n\nPlease remove your headphones and wait for further instructions from the researcher.', 
white, surface=pygame.transform.scale(window, (1200,1200)), lineSpacing = 3, font=font)
# s key to start

thank_you = text_wrapper.drawText('The metronome task is now over. Please inform the researcher you are finished the experiment.'
+'\n\nThe researcher is located at the end of the hallway in PAS 2257 (there is a small map beside the door to help you find your way'
+'; walk straight and it is the first door after you turn right).'
+'\n\nThank you!', 
white, surface=pygame.transform.scale(window, (1200,1200)), lineSpacing = 3, font=font)

probeScreenOne = text_wrapper.drawText('STOP!'
+'\nWhich of the following best characterizes your mental state JUST BEFORE this screen appeared:',
white, surface=pygame.transform.scale(window, (1200,1200)), lineSpacing = 3, font=font)

#load sound
metronome = pygame.mixer.Sound('metronomeMono.wav')

#load image
resume = text_wrapper.drawText('Please press the space bar to resume the task', white, surface=pygame.transform.scale(window, (1200,1200)), lineSpacing = 3, font=font)

#trial parameters
pre_targ = 650 #in milliseconds
targ_time = 75
post_targ = 575 #total trial time = 1300 ms

num_practice = 18
num_trials = 900 #19 minutes

num_probes = 18 # in 50 trial blocks (900 / 50) = 18
#press space bar to resume
probeBlocks=range(0,950,50)
probeList = []
for i in range(num_probes):
    probeList.append(random.randint(probeBlocks[i],probeBlocks[i+1]-1))

probeQ1 = "1. Were you mind wandering just now?"
probeQ2 = "2. Has your mind wandered away from the task since the last probe?"
probeQ3 = "3. Once I noticed my last (most recent) mind-wandering episode I tried to stop my mind wandering:"
probeQ4 = "4. How confident are you in the answer you just gave?"
probeQ5 = "5. Once I noticed my last (most recent) mind-wandering episode, I allowed my mind to continue wandering:"
probeQ6 = "6. How confident are you in the answer you just gave?"
probeQ7 = "7. I noticed how/when my last (most recent) episode of mind-wandering began:"
probeQ8 = "8. How confident are you in the answer you just gave?"
probeQ9 = "9. My last (most recent) mind-wandering episode started when something unrelated to the task spontaneously (unintentionally) 'popped' into my head:"
probeQ10 = "10. How confident are you in the answer you just gave?"

questionList = [probeQ1,probeQ2,probeQ3,probeQ4,probeQ5,probeQ6,probeQ7,probeQ8,probeQ9,probeQ10]
confidenceList = [probeQ4,probeQ6,probeQ8,probeQ10] #3, 5, 7, 9 positions of questionList

def text_objects(text,font):
    textSurface = font.render(text,True,white) #text, true, text colour, background colour
    return textSurface, textSurface.get_rect() #return rendered surface + rectangle

def responseSelectionAnimation(questionIndex,xmouse,ymouse,click_on_list,aRectArray,bRectArray,tempProbeData,conf1RectArray,conf2RectArray,conf3RectArray,conf4RectArray,conf5RectArray):
    if questionIndex not in [3,5,7,9]:
        if xmouse in range(aRectArray[questionIndex][0],aRectArray[questionIndex][0]+aRectArray[questionIndex][2]) and ymouse in range(aRectArray[questionIndex][1],aRectArray[questionIndex][1]+aRectArray[questionIndex][3]):
            pygame.draw.rect(window,green,(aRectArray[questionIndex][0]-5,aRectArray[questionIndex][1]-5,aRectArray[questionIndex][2]+10,aRectArray[questionIndex][3]+10),2)#Select A
            pygame.draw.rect(window,black,(bRectArray[questionIndex][0]-5,bRectArray[questionIndex][1]-5,bRectArray[questionIndex][2]+10,bRectArray[questionIndex][3]+10),2)#deselect B
            click_on_list[questionIndex][0] = True
            click_on_list[questionIndex][1] = False
            tempProbeData[questionIndex] = "Yes"

        elif xmouse in range(bRectArray[questionIndex][0],bRectArray[questionIndex][0]+bRectArray[questionIndex][2]) and ymouse in range(bRectArray[questionIndex][1],bRectArray[questionIndex][1]+bRectArray[questionIndex][3]):
            pygame.draw.rect(window,black,(aRectArray[questionIndex][0]-5,aRectArray[questionIndex][1]-5,aRectArray[questionIndex][2]+10,aRectArray[questionIndex][3]+10),2)#deselect A
            pygame.draw.rect(window,green,(bRectArray[questionIndex][0]-5,bRectArray[questionIndex][1]-5,bRectArray[questionIndex][2]+10,bRectArray[questionIndex][3]+10),2)#Select B
            click_on_list[questionIndex][0] = False
            click_on_list[questionIndex][1] = True
            tempProbeData[questionIndex] = "No"
    else:
        if xmouse in range(conf1RectArray[questionIndex][0],conf1RectArray[questionIndex][0]+conf1RectArray[questionIndex][2]) and ymouse in range(conf1RectArray[questionIndex][1],conf1RectArray[questionIndex][1]+conf1RectArray[questionIndex][3]):
            pygame.draw.rect(window,green,(conf1RectArray[questionIndex][0]-5,conf1RectArray[questionIndex][1]-5,conf1RectArray[questionIndex][2]+10,conf1RectArray[questionIndex][3]+10),2)#Select 1
            pygame.draw.rect(window,black,(conf2RectArray[questionIndex][0]-5,conf2RectArray[questionIndex][1]-5,conf2RectArray[questionIndex][2]+10,conf2RectArray[questionIndex][3]+10),2)#deselect 2
            pygame.draw.rect(window,black,(conf3RectArray[questionIndex][0]-5,conf3RectArray[questionIndex][1]-5,conf3RectArray[questionIndex][2]+10,conf3RectArray[questionIndex][3]+10),2)#deselect 3
            pygame.draw.rect(window,black,(conf4RectArray[questionIndex][0]-5,conf4RectArray[questionIndex][1]-5,conf4RectArray[questionIndex][2]+10,conf4RectArray[questionIndex][3]+10),2)#deselect 4
            pygame.draw.rect(window,black,(conf5RectArray[questionIndex][0]-5,conf5RectArray[questionIndex][1]-5,conf5RectArray[questionIndex][2]+10,conf5RectArray[questionIndex][3]+10),2)#deselect 5

            click_on_list[questionIndex][0] = True
            click_on_list[questionIndex][1] = False
            click_on_list[questionIndex][2] = False
            click_on_list[questionIndex][3] = False
            click_on_list[questionIndex][4] = False

            tempProbeData[questionIndex] = "1"

        elif xmouse in range(conf2RectArray[questionIndex][0],conf2RectArray[questionIndex][0]+conf2RectArray[questionIndex][2]) and ymouse in range(conf2RectArray[questionIndex][1],conf2RectArray[questionIndex][1]+conf2RectArray[questionIndex][3]):
            pygame.draw.rect(window,black,(conf1RectArray[questionIndex][0]-5,conf1RectArray[questionIndex][1]-5,conf1RectArray[questionIndex][2]+10,conf1RectArray[questionIndex][3]+10),2)#deselect 1
            pygame.draw.rect(window,green,(conf2RectArray[questionIndex][0]-5,conf2RectArray[questionIndex][1]-5,conf2RectArray[questionIndex][2]+10,conf2RectArray[questionIndex][3]+10),2)#Select 2
            pygame.draw.rect(window,black,(conf3RectArray[questionIndex][0]-5,conf3RectArray[questionIndex][1]-5,conf3RectArray[questionIndex][2]+10,conf3RectArray[questionIndex][3]+10),2)#deselect 3
            pygame.draw.rect(window,black,(conf4RectArray[questionIndex][0]-5,conf4RectArray[questionIndex][1]-5,conf4RectArray[questionIndex][2]+10,conf4RectArray[questionIndex][3]+10),2)#deselect 4
            pygame.draw.rect(window,black,(conf5RectArray[questionIndex][0]-5,conf5RectArray[questionIndex][1]-5,conf5RectArray[questionIndex][2]+10,conf5RectArray[questionIndex][3]+10),2)#deselect 5

            click_on_list[questionIndex][0] = False
            click_on_list[questionIndex][1] = True
            click_on_list[questionIndex][2] = False
            click_on_list[questionIndex][3] = False
            click_on_list[questionIndex][4] = False

            tempProbeData[questionIndex] = "2"

        elif xmouse in range(conf3RectArray[questionIndex][0],conf3RectArray[questionIndex][0]+conf3RectArray[questionIndex][2]) and ymouse in range(conf3RectArray[questionIndex][1],conf3RectArray[questionIndex][1]+conf3RectArray[questionIndex][3]):
            pygame.draw.rect(window,black,(conf1RectArray[questionIndex][0]-5,conf1RectArray[questionIndex][1]-5,conf1RectArray[questionIndex][2]+10,conf1RectArray[questionIndex][3]+10),2)#deselect 1
            pygame.draw.rect(window,black,(conf2RectArray[questionIndex][0]-5,conf2RectArray[questionIndex][1]-5,conf2RectArray[questionIndex][2]+10,conf2RectArray[questionIndex][3]+10),2)#deselect 2
            pygame.draw.rect(window,green,(conf3RectArray[questionIndex][0]-5,conf3RectArray[questionIndex][1]-5,conf3RectArray[questionIndex][2]+10,conf3RectArray[questionIndex][3]+10),2)#Select 3
            pygame.draw.rect(window,black,(conf4RectArray[questionIndex][0]-5,conf4RectArray[questionIndex][1]-5,conf4RectArray[questionIndex][2]+10,conf4RectArray[questionIndex][3]+10),2)#deselect 4
            pygame.draw.rect(window,black,(conf5RectArray[questionIndex][0]-5,conf5RectArray[questionIndex][1]-5,conf5RectArray[questionIndex][2]+10,conf5RectArray[questionIndex][3]+10),2)#deselect 5

            click_on_list[questionIndex][0] = False
            click_on_list[questionIndex][1] = False
            click_on_list[questionIndex][2] = True
            click_on_list[questionIndex][3] = False
            click_on_list[questionIndex][4] = False

            tempProbeData[questionIndex] = "3"

        elif xmouse in range(conf4RectArray[questionIndex][0],conf4RectArray[questionIndex][0]+conf4RectArray[questionIndex][2]) and ymouse in range(conf4RectArray[questionIndex][1],conf4RectArray[questionIndex][1]+conf4RectArray[questionIndex][3]):
            pygame.draw.rect(window,black,(conf1RectArray[questionIndex][0]-5,conf1RectArray[questionIndex][1]-5,conf1RectArray[questionIndex][2]+10,conf1RectArray[questionIndex][3]+10),2)#deselect 1
            pygame.draw.rect(window,black,(conf2RectArray[questionIndex][0]-5,conf2RectArray[questionIndex][1]-5,conf2RectArray[questionIndex][2]+10,conf2RectArray[questionIndex][3]+10),2)#deselect 2
            pygame.draw.rect(window,black,(conf3RectArray[questionIndex][0]-5,conf3RectArray[questionIndex][1]-5,conf3RectArray[questionIndex][2]+10,conf3RectArray[questionIndex][3]+10),2)#deselect 3
            pygame.draw.rect(window,green,(conf4RectArray[questionIndex][0]-5,conf4RectArray[questionIndex][1]-5,conf4RectArray[questionIndex][2]+10,conf4RectArray[questionIndex][3]+10),2)#Select 4
            pygame.draw.rect(window,black,(conf5RectArray[questionIndex][0]-5,conf5RectArray[questionIndex][1]-5,conf5RectArray[questionIndex][2]+10,conf5RectArray[questionIndex][3]+10),2)#deselect 5

            click_on_list[questionIndex][0] = False
            click_on_list[questionIndex][1] = False
            click_on_list[questionIndex][2] = False
            click_on_list[questionIndex][3] = True
            click_on_list[questionIndex][4] = False

            tempProbeData[questionIndex] = "4"

        elif xmouse in range(conf5RectArray[questionIndex][0],conf5RectArray[questionIndex][0]+conf5RectArray[questionIndex][2]) and ymouse in range(conf5RectArray[questionIndex][1],conf5RectArray[questionIndex][1]+conf5RectArray[questionIndex][3]):
            pygame.draw.rect(window,black,(conf1RectArray[questionIndex][0]-5,conf1RectArray[questionIndex][1]-5,conf1RectArray[questionIndex][2]+10,conf1RectArray[questionIndex][3]+10),2)#deselect 1
            pygame.draw.rect(window,black,(conf2RectArray[questionIndex][0]-5,conf2RectArray[questionIndex][1]-5,conf2RectArray[questionIndex][2]+10,conf2RectArray[questionIndex][3]+10),2)#deselect 2
            pygame.draw.rect(window,black,(conf3RectArray[questionIndex][0]-5,conf3RectArray[questionIndex][1]-5,conf3RectArray[questionIndex][2]+10,conf3RectArray[questionIndex][3]+10),2)#deselect 3
            pygame.draw.rect(window,black,(conf4RectArray[questionIndex][0]-5,conf4RectArray[questionIndex][1]-5,conf4RectArray[questionIndex][2]+10,conf4RectArray[questionIndex][3]+10),2)#deselect 4
            pygame.draw.rect(window,green,(conf5RectArray[questionIndex][0]-5,conf5RectArray[questionIndex][1]-5,conf5RectArray[questionIndex][2]+10,conf5RectArray[questionIndex][3]+10),2)#Select 5

            click_on_list[questionIndex][0] = False
            click_on_list[questionIndex][1] = False
            click_on_list[questionIndex][2] = False
            click_on_list[questionIndex][3] = False
            click_on_list[questionIndex][4] = True

            tempProbeData[questionIndex] = "5"

    return click_on_list, tempProbeData

def responseHighlightAnimation(questionIndex, xmouse, ymouse, click_on_list, aRectArray, bRectArray, conf1RectArray,conf2RectArray,conf3RectArray,conf4RectArray,conf5RectArray):
    if questionIndex not in [3,5,7,9]:
        if not click_on_list[questionIndex][0]:
            if xmouse in range(aRectArray[questionIndex][0],aRectArray[questionIndex][0]+aRectArray[questionIndex][2]) and ymouse in range(aRectArray[questionIndex][1],aRectArray[questionIndex][1]+aRectArray[questionIndex][3]):
                pygame.draw.rect(window,green,(aRectArray[questionIndex][0]-5,aRectArray[questionIndex][1]-5,aRectArray[questionIndex][2]+10,aRectArray[questionIndex][3]+10),2)
            else:
                pygame.draw.rect(window,black,(aRectArray[questionIndex][0]-5,aRectArray[questionIndex][1]-5,aRectArray[questionIndex][2]+10,aRectArray[questionIndex][3]+10),2)

        if not click_on_list[questionIndex][1]:
            if xmouse in range(bRectArray[questionIndex][0],bRectArray[questionIndex][0]+bRectArray[questionIndex][2]) and ymouse in range(bRectArray[questionIndex][1],bRectArray[questionIndex][1]+bRectArray[questionIndex][3]):
                pygame.draw.rect(window,green,(bRectArray[questionIndex][0]-5,bRectArray[questionIndex][1]-5,bRectArray[questionIndex][2]+10,bRectArray[questionIndex][3]+10),2)
            else:
                pygame.draw.rect(window,black,(bRectArray[questionIndex][0]-5,bRectArray[questionIndex][1]-5,bRectArray[questionIndex][2]+10,bRectArray[questionIndex][3]+10),2)
    else:
        if not click_on_list[questionIndex][0]:
            if xmouse in range(conf1RectArray[questionIndex][0],conf1RectArray[questionIndex][0]+conf1RectArray[questionIndex][2]) and ymouse in range(conf1RectArray[questionIndex][1],conf1RectArray[questionIndex][1]+conf1RectArray[questionIndex][3]):
                pygame.draw.rect(window,green,(conf1RectArray[questionIndex][0]-5,conf1RectArray[questionIndex][1]-5,conf1RectArray[questionIndex][2]+10,conf1RectArray[questionIndex][3]+10),2)
            else:
                pygame.draw.rect(window,black,(conf1RectArray[questionIndex][0]-5,conf1RectArray[questionIndex][1]-5,conf1RectArray[questionIndex][2]+10,conf1RectArray[questionIndex][3]+10),2)
        if not click_on_list[questionIndex][1]:
            if xmouse in range(conf2RectArray[questionIndex][0],conf2RectArray[questionIndex][0]+conf2RectArray[questionIndex][2]) and ymouse in range(conf2RectArray[questionIndex][1],conf2RectArray[questionIndex][1]+conf2RectArray[questionIndex][3]):
                pygame.draw.rect(window,green,(conf2RectArray[questionIndex][0]-5,conf2RectArray[questionIndex][1]-5,conf2RectArray[questionIndex][2]+10,conf2RectArray[questionIndex][3]+10),2)
            else:
                pygame.draw.rect(window,black,(conf2RectArray[questionIndex][0]-5,conf2RectArray[questionIndex][1]-5,conf2RectArray[questionIndex][2]+10,conf2RectArray[questionIndex][3]+10),2)
        if not click_on_list[questionIndex][2]:
            if xmouse in range(conf3RectArray[questionIndex][0],conf3RectArray[questionIndex][0]+conf3RectArray[questionIndex][2]) and ymouse in range(conf3RectArray[questionIndex][1],conf3RectArray[questionIndex][1]+conf3RectArray[questionIndex][3]):
                pygame.draw.rect(window,green,(conf3RectArray[questionIndex][0]-5,conf3RectArray[questionIndex][1]-5,conf3RectArray[questionIndex][2]+10,conf3RectArray[questionIndex][3]+10),2)
            else:
                pygame.draw.rect(window,black,(conf3RectArray[questionIndex][0]-5,conf3RectArray[questionIndex][1]-5,conf3RectArray[questionIndex][2]+10,conf3RectArray[questionIndex][3]+10),2)
        if not click_on_list[questionIndex][3]:
            if xmouse in range(conf4RectArray[questionIndex][0],conf4RectArray[questionIndex][0]+conf4RectArray[questionIndex][2]) and ymouse in range(conf4RectArray[questionIndex][1],conf4RectArray[questionIndex][1]+conf4RectArray[questionIndex][3]):
                pygame.draw.rect(window,green,(conf4RectArray[questionIndex][0]-5,conf4RectArray[questionIndex][1]-5,conf4RectArray[questionIndex][2]+10,conf4RectArray[questionIndex][3]+10),2)
            else:
                pygame.draw.rect(window,black,(conf4RectArray[questionIndex][0]-5,conf4RectArray[questionIndex][1]-5,conf4RectArray[questionIndex][2]+10,conf4RectArray[questionIndex][3]+10),2)
        if not click_on_list[questionIndex][4]:
            if xmouse in range(conf5RectArray[questionIndex][0],conf5RectArray[questionIndex][0]+conf5RectArray[questionIndex][2]) and ymouse in range(conf5RectArray[questionIndex][1],conf5RectArray[questionIndex][1]+conf5RectArray[questionIndex][3]):
                pygame.draw.rect(window,green,(conf5RectArray[questionIndex][0]-5,conf5RectArray[questionIndex][1]-5,conf5RectArray[questionIndex][2]+10,conf5RectArray[questionIndex][3]+10),2)
            else:
                pygame.draw.rect(window,black,(conf5RectArray[questionIndex][0]-5,conf5RectArray[questionIndex][1]-5,conf5RectArray[questionIndex][2]+10,conf5RectArray[questionIndex][3]+10),2)

def drawProbe(stop, questionList, confidenceList):
    pygame.event.clear()
    pygame.mouse.set_visible(True)
    #at every probe, make a temp data file the length of questionList to store responses
    tempProbeData = []
    for i in range(len(questionList)):
        tempProbeData.append('')

    optionA = "Yes"
    optionB = "No"

    yesnoOptions = [optionA,optionB]

    qSurfaceArray = [] #array of question surfaces
    aSurfaceArray = [] #array of option A surfaces
    bSurfaceArray = [] #array of option B surfaces

    qRectArray = [] #array of question rectangles
    aRectArray = [] #array of option A rectangles
    bRectArray = [] #array of option B rectangles

    conf1 = "Not at all confident"
    conf2 = "Somewhat confident"
    conf3 = "Confident"
    conf4 = "Very confident"
    conf5 = "Extremely confident"

    conf1SurfaceArray = [] #array of confidence 1 surfaces
    conf2SurfaceArray = [] #array of confidence 2 surfaces
    conf3SurfaceArray = [] #array of confidence 3 surfaces
    conf4SurfaceArray = [] #array of confidence 4 surfaces
    conf5SurfaceArray = [] #array of confidence 5 surfaces

    conf1RectArray = [] #array of confidence 1 rectangles
    conf2RectArray = [] #array of confidence 2 rectangles
    conf3RectArray = [] #array of confidence 3 rectangles
    conf4RectArray = [] #array of confidence 4 rectangles
    conf5RectArray = [] #array of confidence 5 rectangles

    confOptions = [conf1,conf2,conf3,conf4,conf5]
    confRespSurfaceArray = [conf1SurfaceArray,conf2SurfaceArray,conf3SurfaceArray,conf4SurfaceArray,conf5SurfaceArray]
    confRespRectArray = [conf1RectArray,conf2RectArray,conf3RectArray,conf4RectArray,conf5RectArray]

    font = pygame.font.Font(fontName,18)
    yspace_from_top = 50
    yspace_from_question = 50
    xspace_from_center = 50

    #Create Textures for every item in questionList (12)
    for i in range(len(questionList)):
        
        #Questions
        textSurface,textRect = text_objects(questionList[i],font)
        qSurfaceArray.append(textSurface) #a list of all the rendered question text
        qRectArray.append(textRect) #a list of all the rendered question text rectangles
        
        #Option A
        textSurface,textRect = text_objects(optionA,font)
        aSurfaceArray.append(textSurface) #a list of all the rendered question text
        aRectArray.append(textRect) #a list of all the rendered question text rectangles

        #Option B
        textSurface,textRect = text_objects(optionB,font)
        bSurfaceArray.append(textSurface) #a list of all the rendered question text
        bRectArray.append(textRect) #a list of all the rendered question text rectangles
        
        #Create 5-point confidence array
        
        #conf1
        textSurface,textRect = text_objects(conf1,font)
        conf1SurfaceArray.append(textSurface) #a list of all the rendered question text
        conf1RectArray.append(textRect) #a list of all the rendered question text rectangles
        #conf2
        textSurface,textRect = text_objects(conf2,font)
        conf2SurfaceArray.append(textSurface) #a list of all the rendered question text
        conf2RectArray.append(textRect) #a list of all the rendered question text rectangles
        #conf3
        textSurface,textRect = text_objects(conf3,font)
        conf3SurfaceArray.append(textSurface) #a list of all the rendered question text
        conf3RectArray.append(textRect) #a list of all the rendered question text rectangles
        #conf4
        textSurface,textRect = text_objects(conf4,font)
        conf4SurfaceArray.append(textSurface) #a list of all the rendered question text
        conf4RectArray.append(textRect) #a list of all the rendered question text rectangles
        #conf5
        textSurface,textRect = text_objects(conf5,font)
        conf5SurfaceArray.append(textSurface) #a list of all the rendered question text
        conf5RectArray.append(textRect) #a list of all the rendered question text rectangles
        

    #Create Positions
    modifier = 0
    for i in range(len(qRectArray)):
        qx,qy = qSurfaceArray[i].get_size()
        qRectArray[i].center = (center[0],yspace_from_top+modifier)
        aRectArray[i].center = (center[0]-xspace_from_center,yspace_from_top+yspace_from_question+modifier)
        bRectArray[i].center = (center[0]+xspace_from_center,yspace_from_top+yspace_from_question+modifier)

        conf1RectArray[i].center = (center[0]-xspace_from_center*8,yspace_from_top+yspace_from_question+modifier)
        conf2RectArray[i].center = (center[0]-xspace_from_center*4,yspace_from_top+yspace_from_question+modifier)
        conf3RectArray[i].center = (center[0],yspace_from_top+yspace_from_question+modifier)
        conf4RectArray[i].center = (center[0]+xspace_from_center*4,yspace_from_top+yspace_from_question+modifier)
        conf5RectArray[i].center = (center[0]+xspace_from_center*8,yspace_from_top+yspace_from_question+modifier)

        modifier+=yspace_from_question+50 #incremental spacing between each question

    window.fill(black)
    
    #blit selected items only (made textures for everything)
    for i in range(len(questionList)):
        window.blit(qSurfaceArray[i],qRectArray[i])
        if questionList[i] not in confidenceList:
            window.blit(aSurfaceArray[i],aRectArray[i])
            window.blit(bSurfaceArray[i],bRectArray[i])
        else:
            window.blit(conf1SurfaceArray[i],conf1RectArray[i])
            window.blit(conf2SurfaceArray[i],conf2RectArray[i])
            window.blit(conf3SurfaceArray[i],conf3RectArray[i])
            window.blit(conf4SurfaceArray[i],conf4RectArray[i])
            window.blit(conf5SurfaceArray[i],conf5RectArray[i])

    pygame.display.update()
    
    click_on_A = False
    click_on_B = False

    click_on_list = []
    for i in range(len(questionList)):
        if  questionList[i] not in confidenceList:
            click_on_list.append([click_on_A,click_on_B])
        else:
            click_on_list.append([False,False,False,False,False])

    done=False
    while done == False:
        mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == exitKey: stop = True
            elif event.type == pygame.KEYDOWN and event.key == startKey: done = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(questionList)):
                    #if questionList[i] not in confidenceList:
                    click_on_list, tempProbeData = responseSelectionAnimation(i,mouse[0],mouse[1],click_on_list, aRectArray, bRectArray, tempProbeData, conf1RectArray,conf2RectArray,conf3RectArray,conf4RectArray,conf5RectArray)
                    #else:
                    #click_on_list, tempProbeData = responseSelectionAnimationConfidence(i,mouse[0],mouse[1],click_on_list,tempProbeData,conf1RectArray,conf2RectArray,conf3RectArray,conf4RectArray,conf5RectArray)

        for i in range(len(questionList)):
           responseHighlightAnimation(i, mouse[0], mouse[1], click_on_list, aRectArray, bRectArray, conf1RectArray,conf2RectArray,conf3RectArray,conf4RectArray,conf5RectArray)
                                
        if stop:break

        pygame.display.update()
        clock.tick(15)

    pygame.event.clear()
    window.fill(black)
    window.blit(resume[0],text_pos)
    pygame.display.flip()
    done = False
    quitEarly = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: done = True; quitEarly = True
            if event.type == pygame.KEYDOWN:
                if event.key == exitKey: done = True; quitEarly = True
                if event.key == continueKey: done = True
    if quitEarly:
        pygame.quit()
        sys.exit()
    
    window.fill(black)
    pygame.mouse.set_visible(False)
    pygame.display.flip()

    return stop, tempProbeData

#### trial builder
def doTrial(recordData, trial, probeList):
    RT = ''
    stop = False
    resp = False
    omission = 1
    #tempProbeData = ''
    
    trialOver = False
    trial_start = pygame.time.get_ticks()
    while not trialOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == exitKey: stop = True
            elif not resp and event.type == pygame.KEYDOWN and event.key == continueKey: 
                now = pygame.time.get_ticks() - trial_start
                RT = now - pre_targ # get RT in reference to when tone is presented
                resp = True
                omission = 0
            else: continue
       
        if trialOver==False:
            if (pygame.time.get_ticks() - trial_start) == pre_targ: metronome.play()
            elif (pygame.time.get_ticks() - trial_start) == 1300: trialOver = True        
        else:continue
        if stop: break
        #clock.tick(1)
        
    if trial in probeList:
        stop, tempProbeData = drawProbe(stop, questionList, confidenceList)
           
    if recordData: #True for experiment, False for practice
        data = [subject, sona_id, subject_sex, subject_age, trial, omission, RT]
        if trial in probeList:
            for i in range(len(tempProbeData)):
                data.append(tempProbeData[i]) #probe responses onto data

        datasaver.save("data/"+str(subject), data)   #Save Data

    return stop

#### Instructions
window.fill(black)
for i in range(len(instructions)):
    window.fill(black)
    window.blit(instructions[i],text_pos)
    pygame.display.flip()
    done = False
    quitEarly = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: done = True; quitEarly = True
            if event.type == pygame.KEYDOWN:
                if event.key == exitKey: done = True; quitEarly = True
                if event.key == startKey: done = True
    if quitEarly:
        pygame.quit()
        sys.exit()   

#### Practice Trials
window.fill(black)
pygame.display.flip()
recordData = False
practiceProbe = [num_practice/2]
for p in range(num_practice):
    stop = doTrial(recordData, p, practiceProbe)
    if stop:
        break
#### Intermission
window.fill(black)
window.blit(practice_over[0], text_pos)
pygame.display.flip()
done = False
quitEarly = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: done = True; quitEarly = True
        if event.type == pygame.KEYDOWN:
            if event.key == exitKey: done = True; quitEarly = True
            if event.key == startKey: done = True
if quitEarly:
    pygame.quit()
    sys.exit()

#### Experimental Trials
window.fill(black)
pygame.display.flip()
recordData = True
for trial in range(num_trials):
    stop = doTrial(recordData, trial, probeList)
    if stop:
        break

#### EXIT
window.fill(black)
window.blit(thank_you[0], text_pos)
pygame.display.flip()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: done = True
        elif event.type == pygame.KEYDOWN and event.key == terminate: done = True
pygame.quit()
sys.exit()
