#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a trial loop Step 2
Use this template to turn Step 1 into a loop
@author: katherineduncan
"""
#%% Required set up 
# this imports everything you might need and opens a full screen window
# when you are developing your script you might want to make a smaller window 
# so that you can still see your console 
import numpy as np
import pandas as pd
import os, sys
import ctypes
from psychopy import visual, core, event, gui, logging



# global shutdown key for debugging!
event.globalKeys.add(key='q',func=core.quit)


# Bring up a window asking for the subject number. Also creates the file name
# Alerts if a file of the same name already exists and asks if overwrite should occur
# Exits process if a number isn't provided
subgui = gui.Dlg()
subgui.addField("Subject ID:")
subgui.addField("Session Number:")

# show the gui
subgui.show()

# put the inputted data in easy to use variables
subjID = subgui.data[0]
sessNum = subgui.data[1]

#%% step 3: prepare output

outputFileName = 'data' + os.sep + 'sub' + subjID + '_sess' + sessNum + '_PS6.csv'
print(outputFileName)
if os.path.isfile(outputFileName) :
    sys.exit("data for this session already exists")



# create a dataframe to hold output
outVars = ['trial', 'image', 'degredation', 'response', 'rt', 'indoor/outdoor']    
out = pd.DataFrame(columns=outVars)

# write output file
out.to_csv(outputFileName, index = False)


# open a white full screen window
win = visual.Window(fullscr=True, allowGUI=False, color='gray', unit='height') 

#some constants
HICHARLOTTE = visual.TextStim(win, alignHoriz = 'center', height = .03, text = 'Hi Charlotte,\nThis is the quote endquote extreme version of the study phase of a project Im currently running.\n\nThis will randomly sample five trials from a conditions list, so the trials should be different each run through.\n\nThis is an incidental encoding task, so the responses arent checked for accuracy.\n\nPress any space to continue')
BASEINSTRUCTIONS = visual.TextStim(win, alignHoriz = 'center', height = .03, text='You will see a series of images and are required to make a judgement on them.\n\nSome of these items will be partially obsured. Do your best to make your judgements!\n\nPress any key to continue') 
INDOORINSTRUCTIONS = visual.TextStim(win, alignHoriz = 'center', height = .03, text ='For the next set of images, please make the following decision:\n\nIs the following object typically found indoors or outdoors?\n\n\n1 - Indoors\t\t\t\t\t\t2 - Outdoors\n\nPress any key to continue')
ENDINSTRUCTIONS = visual.TextStim(win, alignHoriz = 'center', height = .03, text='Thanks for playing.\n\nIn two seconds this window will close.')
INDOORMSG = visual.TextStim(win, alignHoriz = 'center', height = .03, text = 'You said indoor')
OUTDOORMSG = visual.TextStim(win, alignHoriz = 'center', height = .03, text = 'You said outdoor')
NOTHINGMSG = visual.TextStim(win, alignHoriz = 'center', height = .03, text = 'You pressed nothing')
NTRIALS = 5 #The study phase is actually 440 trials, but let's only do 5
ISI = 1 #The inter stimulus interval in seconds
fbDur = 1.5 #Duration of feedback message
fixation = visual.Circle(win, pos=(0,0), radius=(0.01), lineColor='black', fillColor='black') #fixation dot


# uncomment if you use a clock. Optional because we didn't cover timing this week, 
# but you can find examples in the tutorial code 
trialClock = core.Clock() # trial clock currently not used
eventClock = core.Clock() # event clock currently not used
respClock = core.Clock() # response clock
fbClock = core.Clock() #feedback clock


# make a list or a pd.DataFrame that contains trial-specific info (stimulus, etc)
conditionList = pd.read_csv('Sub-002_conditions_Study.csv')

# randomize trials
conditionList = conditionList.sample(frac=1)
conditionList = conditionList.reset_index()

#display instructions until a key is pressed

HICHARLOTTE.draw()
win.flip()
event.waitKeys()

BASEINSTRUCTIONS.draw()
win.flip()
event.waitKeys()

INDOORINSTRUCTIONS.draw()
win.flip()
event.waitKeys()

# make your loop
for thisTrial in np.arange(0,NTRIALS) :
    #clear events
    
    event.clearEvents()
    eventClock.reset()
    
    #set study pic
    studyPic = visual.ImageStim(win, size = None, pos = (0,0), image= 'Images/'+conditionList.loc[thisTrial,'Image'])
    
    #draw fixation
    while eventClock.getTime() < ISI:
        fixation.draw()
        win.flip()
        #core.wait(.001)
    
    
    #reset trial clock
    trialClock.reset()
    
    #display study image
    studyPic.draw()
    win.flip()
    
    #reset reponse clock and collect response
    #I removed the maxwait so it will just sit there until a viable key is pressed
    respClock.reset()
    keys = event.waitKeys(keyList=['1','2'],timeStamped=respClock)
    
    #record if if there is a response
    ANSWER = None
    trialRT = None
    if len(keys) > 0:
        ANSWER = keys[0][0]
        trialRT = keys[0][1]
    
    fbClock.reset()
    # show feedback
    if ANSWER=='1':
        INDOORMSG.draw()
    elif ANSWER=='2':
        OUTDOORMSG.draw()
    else:
        NOTHINGMSG.draw()
    win.flip()
    fbClock.reset()
    while fbClock.getTime() < fbDur:
        core.wait(.001)
    
    # satisfying the calculation requirement
    if ANSWER == '1':
        out.loc[thisTrial, 'indoor/outdoor'] = 'indoor'
    elif ANSWER == '2':
        out.loc[thisTrial, 'indoor/outdoor'] = 'outdoor'
    else:
        out.loc[thisTrial, 'indoor/outdoor'] = 'NA'
    
    #record study parameters
    out.loc[thisTrial,'trial'] = thisTrial + 1
    out.loc[thisTrial,'image'] = conditionList.loc[thisTrial,'Image']
    out.loc[thisTrial,'degredation'] = conditionList.loc[thisTrial,'Degredation']
    
    if ANSWER != None:
        out.loc[thisTrial, 'response'] = ANSWER
        out.loc[thisTrial, 'rt'] = trialRT
    
     # append trial info to file, to_csv must be in append mode
    out.loc[[thisTrial]].to_csv(outputFileName,mode='a',header=False,index=False)
    
    


#%% Required clean up
# this cell will make sure that your window displays for a while and then 
# closes properly



ENDINSTRUCTIONS.draw()
win.flip()

print(out)

core.wait(2)
win.close()
