# this file contains all the functions needed for all experiments
# !!! Check the correct path for the code repository and correct dtb user first!
# you'll need custom module 'helpers' to import the dtb settings/connection

#-----------------imports---------------------------
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import event,core,gui,visual
import numpy as np  # whole numpy lib is available, prepend 'np.'
import time, datetime, os, random, copy, math
import setup, newPoints, variables,doodle,platform, sys
import SQL_call as sql

# set working path in the computer so that relative packages could work
def setpath():
    if platform.system() == 'Windows': # set path in windows machines
        sys.path.append('/Users/user/repos') # !!! put in correct path first
        sys.path.append('C:\\python27\\Lib\\site-packages')
    else: # set path in mac machines
        sys.path.append('/Users/user/repos') # !!! put in correct path first
        sys.path.append('/usr/local/lib/python2.7/site-packages')

setpath()

#--------------import helper------------------------
import helpers.DBUtilsClass as db
import helpers.net as net
import json

mouse = event.Mouse(setup.mywin)

# database setup at the beginning of learning stages
def initialSetup(var,dbc):
    # use settings for test_learn (minimum number of forced trials)
    # use settings for learn (forced trials = 16)
    settingsdtb = 'learn3'
    try:
        setiddtb = sql.r_settingsid(dbc,settingsdtb)
        varsetdtb = sql.r_varset(dbc,settingsdtb)
        var.forcedTrialNum = varsetdtb['forcedTrialNum']
        var.passThreshold = varsetdtb['passThreshold']
        var.delay = varsetdtb['delay']
        var.highLowDelay = [max(var.delay),min(var.delay)]
        var.delaydiscounter = varsetdtb['ddiscounter']
    except IndexError: # settings_ID is not in the system
        print("settings_ID is not in the system!")
    return setiddtb,var

# connect to database
def dbconnect():
    dbc = db.Connection() # connect to database
    sql.select_user(dbc,'user') # !!! put in correct user first
    return dbc

# ask subject for netid from a window shown on the screen
def get_netid(var,doo,dbc,fN):
    expN, extN = os.path.splitext(fN)    
    st = datetime.datetime.now()
    expD = datetime.datetime.now().strftime("%Y-%m-%d_T%H_%M_%S")
    host_ip=net.getIP()
    p_net = (var.expInfo['Net ID'])
    try:
        p_num = sql.r_subjid(dbc,p_net) # get subject id (p_num) given netid 
    except IndexError: # net_ID is not in the system
        print("net_ID is not in the system!")
        doo.mixNonInstruction.text = u'net_ID is not in the system'
        doo.mixNonInstruction.draw()
        setup.mywin.flip()
        core.wait(2)
        core.quit()
    return p_num, expD, st,expN, host_ip,p_net

# MixNonverbal database and data record setups
def exp_setup(var,doo,dbc,getName,sub_id,expName,expDate):
    stt = datetime.datetime.now()
    #-----------------data recording-----------------------------------
    if getName:
        dlg = gui.DlgFromDict(dictionary=var.expInfo, title=expName)
        if dlg.OK == False: 
            core.quit()  # user pressed cancel
        else:
            setup.mywin.winHandle.activate()
        p_net = (var.expInfo['Net ID'])
        try:
            p_num = sql.r_subjid(dbc,p_net)
        except IndexError: # net_ID is not in the system
            print("net_ID is not in the system!")
            doo.instruction.text = u'net_ID is not in the system'
            doo.instruction.draw()
            setup.mywin.flip()
            core.wait(2)
            core.quit() 
    else:
        p_net = sub_id
        p_num = sql.r_subjid(dbc,p_net)

    settingsdtb = 'seconds3'
    try:
        varsetdtb = sql.r_varset(dbc,settingsdtb)
        setiddtb = sql.r_settingsid(dbc,settingsdtb)
        var.delay = varsetdtb['delay']
        var.delaydiscounter = varsetdtb['ddiscounter']
        var.refresherNum = varsetdtb['refresherNum']
        var.blockTrial = varsetdtb['blockTrial']
        var.passThreshold = varsetdtb['passThreshold']
    except IndexError: # settings_ID is not in the system
        print("settings_ID is not in the system!")
        
    fileName = u'data/%s_%s_%s.csv' %(p_num, expName, expDate)
    var.dataFile = open(fileName, 'w') # note that MS Excel has only ASCII .csv, other spreadsheets do support UTF-8
    var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format("No.","block","Total ", "hit_No. ", 
        "initRT ", ' '*5+"initVT ",' '*5+"fixVT ",'fixDur',' '*2+'initPos',' '*2+'bluePos',' '*2+'yellowPos',' '*4+"decisionRT","choice",'yellowRew',"rewMag",
        ' '*2+'Dist',' '*2+'delay',' '*4+"decisionVT",' '*5+"rewRT ",' '*5+"rewVT ",' fix_click',' del_click',' rew_click'))
    var.dataFile.flush()
    #remove test_ to save real data
    host_ip=net.getIP()
    sql.w_before_mixnon(dbc,p_num, expDate, stt, expName, host_ip, setiddtb)
    sessid = sql.r_lastID(dbc)
    return sessid,p_num,p_net,setiddtb,host_ip,var,dbc

# MixNonverbal experiment setups
# this function generates the trial numbers for each block and the overall structure of this session
def nonverbalSetup(totalTrialNumber,magList,shortMag):
    blockInfoList = []
    smallerNum = 0
    biggerNum = 0
    biggerTotal = totalTrialNumber * 0.75
    smallerTotal = totalTrialNumber * 0.25
    for mag in magList:
        blockInfoList.append([mag])
        if mag < shortMag:
            smallerNum += 1
        elif mag > shortMag:
            biggerNum += 1
    for setNum in range(len(blockInfoList)):
        if blockInfoList[setNum][0] < shortMag:
            if setNum == smallerNum-1:
                totalBeforeLastSmaller = 0
                for i in range((setNum)):
                    totalBeforeLastSmaller+=blockInfoList[i][1]
                trialNum = int(smallerTotal- totalBeforeLastSmaller)
                blockInfoList[setNum].append(trialNum)
            elif setNum < smallerNum-1:
                if smallerTotal-(smallerTotal//smallerNum*smallerNum)  == 0 :
                    trialNum = random.randint(smallerTotal/smallerNum-2,smallerTotal/smallerNum+2)
                    blockInfoList[setNum].append(trialNum)
                else:
                    trialNum = random.randint(smallerTotal/smallerNum-1.5,smallerTotal/smallerNum+1.5)
                    blockInfoList[setNum].append(trialNum)
        elif blockInfoList[setNum][0] > shortMag:
            if setNum == len(blockInfoList)-1:
                totalBeforeLastBigger = 0
                for i in range(smallerNum,setNum):
                    totalBeforeLastBigger+=blockInfoList[i][1]
                trialNum = int(biggerTotal- totalBeforeLastBigger)
                blockInfoList[setNum].append(trialNum)
            elif setNum < len(blockInfoList)-1:
                if biggerTotal-(biggerTotal//biggerNum*biggerNum) == 0 :
                    trialNum = random.randint(biggerTotal/biggerNum-2,biggerTotal/biggerNum+2)
                    blockInfoList[setNum].append(trialNum)
                else:
                    trialNum = random.randint(biggerTotal/biggerNum-1.5,biggerTotal/biggerNum+1.5)
                    blockInfoList[setNum].append(trialNum)
    return blockInfoList

# Verbal experiment setups
# this function generates the trial numbers for each block and the overall structure of this session
def verbalSetup(totalTrialNumber,magList,shortMag):
    blockInfoList = [] # this function requires that maglist is ordered
    smallerNum = 0 # number of rewardmag that's smaller than surebet
    biggerNum = 0 # number of rewardmag that is greater than surebet
    smallerTotal = totalTrialNumber * 0.05 # total number of trials to have bigger rewmag
    biggerTotal = totalTrialNumber - smallerTotal# total number of trials to have smaller rewmag
    for mag in magList: # add all rewmag into blockInfoList as individual sublists and set smallerNum/biggerNum
        blockInfoList.append([mag])
        if mag < shortMag:
            smallerNum += 1
        elif mag > shortMag:
            biggerNum += 1
    smallerMean = round(smallerTotal/smallerNum)# average trial num for each smaller/bigger rewmag
    biggerMean = round(biggerTotal/biggerNum)
    for setNum in range(len(blockInfoList)):# loop over each sublist in blockInfoList
        if blockInfoList[setNum][0] < shortMag:# if rewmag in this sublist is smaller than surebet
            if setNum == smallerNum-1:# if the current sublist is the last smaller rewmag
                totalBeforeLastSmaller = 0
                for i in range(setNum):# calculate the sum of trial numbers of all the other smaller rewmags before it
                    totalBeforeLastSmaller+=blockInfoList[i][1]
                trialNum = max(1,int(smallerTotal- totalBeforeLastSmaller))# subtract the sum above from the total smaller trial number
                blockInfoList[setNum].append(trialNum)# append the trial num of this last smaller rewmag to its sublist
            elif setNum < smallerNum-1:# if the current sublist is not the last smaller rewmag
                trialNum = max(1,random.randint(smallerMean-1,smallerMean+1))# set the trialNum within +1/-1 range from the smallerMean value
                blockInfoList[setNum].append(trialNum)
        elif blockInfoList[setNum][0] > shortMag:# if rewmag in this sublist is greater than surebet
            if setNum == len(blockInfoList)-1:
                totalBeforeLastBigger = 0
                for i in range(smallerNum,setNum):
                    totalBeforeLastBigger+=blockInfoList[i][1]
                trialNum = int(biggerTotal- totalBeforeLastBigger)
                blockInfoList[setNum].append(trialNum)
            elif setNum < len(blockInfoList)-1:
                trialNum = random.randint(biggerMean-2, biggerMean+2)
                blockInfoList[setNum].append(trialNum)
    return blockInfoList

# this function selects one trial to actually pay for the participant
def paymentSelection(totalTrialNumber):
    return random.randint(1,totalTrialNumber)

# show verbal instructions between each verbal block
def block_instruction(var,doo):
    doo.instruction.text = u'Block '+str(var.blockName)
    doo.instruction.height = 30
    doo.instruction.pos=[0, 0]
    doo.instruction.draw()
    setup.mywin.flip()
    core.wait(3)

# present a break between each verbal block. Show the clock and the instructions
def block_break(var,doo):
    doo.instruction.text = u'Please take a %r-second break.\n\nPress in the clock to stop the break and you will continue to the next block.' % var.blockBreak
    doo.instruction.pos=[0,0]
    doo.instruction.height = 30
    delayStart = time.time()
    delayEnd = time.time()
    while delayEnd-delayStart<=var.blockBreak:
        var.secPos2 = 'TBD'
        var.secPos = np.floor(delayEnd-delayStart+60-var.oneRound)*360/60#NB floor will round down to previous second
        if var.secPos != var.secPos2:
            delayCircle(var,doo)
            scales(var,doo)
            doo.clock.visibleWedge = (0, var.secPos*(60/var.blockBreak)+1)
            doo.clock.draw()
            scales(var,doo)
            doo.instruction.draw()
            setup.mywin.flip()
        var.secPos2 = copy.copy(var.secPos)
        delayEnd = time.time()
        if mouse.isPressedIn(doo.pressCircle,buttons=[0]):
            breakCancel = time.time()
            var.blockBreakCancel = breakCancel-delayStart
            break
    delayCircleEmpty(var,doo)
    scales(var,doo)
    doo.instruction.draw()
    setup.mywin.flip()
    core.wait(0.2)

# instruction before the experiment
def instruction(var,doo):
    event.Mouse(visible=False)
    var.DBRSoundDur = 2
    toneMag=doo.toneMag(var.blockRewMag)
    setup.mywin.flip()
    core.wait(1)
    toneMag.play()
    core.wait(2)
    var.DBRSoundDur = 0.48
    event.Mouse(visible=True)
    return var

# this function makes the survey
def survey(doo):
    questions = [u'1. To what extent did you feel that you were out of money in the last two weeks?',
                 u'2. To what extent did you feel that you were out of time in the last two weeks?',
                 u'3. To what extent are you in a hurry today?']
    rate_ans = []
    dt_ans = []
    chhist_ans = []
    for question in questions:
        ratingScale = visual.RatingScale(setup.mywin)
        doo.instruction.text = question
        doo.instruction.pos = [0,80]
        while ratingScale.noResponse:
            doo.instruction.draw()
            doo.survey_instr.text = u'(Click on the scale to make your choice. Click the button at bottom to confirm your choice.)'
            doo.survey_instr.draw()
            ratingScale.draw()
            setup.mywin.flip()
        rating = ratingScale.getRating()
        decisionTime = ratingScale.getRT()
        choiceHistory = ratingScale.getHistory()
        rate_ans.append(rating)
        dt_ans.append(decisionTime)
        chhist_ans.append(choiceHistory)
    return rate_ans, dt_ans, chhist_ans

# this function is reminding the subject to focus. Experiment is about to start
def about_to_start(doo):
        doo.instruction.text = u'Experiment Starts Soon...'
        doo.instruction.pos = [0,0]
        doo.instruction.draw()
        setup.mywin.flip()
        core.wait(3)
        setup.mywin.flip()

#this function generates the  instruction between sessions
def break_instruction(doo):
    doo.instruction.text = u'You may take a short break now.\n\nPress enter if you are ready to start the decision stages.\n\nNote: Keep your headphones on, and if you don\'t hear any sound after pressing enter, please report to the experimenter.'
    doo.instruction.pos=[0,0]
    doo.instruction.height = 30
    doo.instruction.draw()
    setup.mywin.flip()
    press = event.waitKeys(keyList="return")
    while press[0]=="return":
        break

#-----------------data recording set up for learning stages-----------------------------------
def dataRecordStart0(var,dbc): 
    var.expInfo = setup.username()
    p_net = (var.expInfo['Net ID'])
    p_num = sql.r_subjid(dbc,p_net)
    expName = os.path.basename(__file__)[:-3]
    stt = datetime.datetime.now()
    expDate = datetime.datetime.now().strftime("%Y-%m-%d_T%H_%M_%S")
    fileName = u'data/%s_%s_%s.csv' %(p_num, expName, expDate)
    var.dataFile = open(fileName, 'w') # note that MS Excel has only ASCII .csv, other spreadsheets do support UTF-8
    var.dataFile.write("{} {} {} {} {} {} {} {}\n".format("trial_No. ","learned_trail_No. ","rewMag ", "totalPoints ", "trialsCorrect ", 
        "Reaciton Time ", "Violation Time ",' rew_click'))
    var.dataFile.flush()

def dataRecordStart1(var,dbc):
    var.expInfo = setup.username()
    p_net = (var.expInfo['Net ID'])
    p_num = sql.r_subjid(dbc,p_net)
    expName = os.path.basename(__file__)[:-3]
    stt = datetime.datetime.now()
    expDate = datetime.datetime.now().strftime("%Y-%m-%d_T%H_%M_%S")
    fileName = u'data/%s_%s_%s.csv' %(p_num, expName, expDate)
    var.dataFile = open(fileName, 'w') # note that MS Excel has only ASCII .csv, other spreadsheets do support UTF-8
    var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {}\n".format("trial_No. ","learned_init_No. ","learned_rew_No. ",'initPos',"rewMag ", "totalPoints ", "trialscorrect ", 
        "initReaciton Time ", "initViolation Time ","rewReaction Time ","rewViolation Time ",' rew_click'))
    var.dataFile.flush()

def dataRecordStart2(var,dbc):
    var.expInfo = setup.username()
    p_net = (var.expInfo['Net ID'])
    p_num = sql.r_subjid(dbc,p_net)
    expName = os.path.basename(__file__)[:-3]
    stt = datetime.datetime.now()
    expDate = datetime.datetime.now().strftime("%Y-%m-%d_T%H_%M_%S")
    fileName = u'data/%s_%s_%s.csv' %(p_num, expName, expDate)
    var.dataFile = open(fileName, 'w') # note that MS Excel has only ASCII .csv, other spreadsheets do support UTF-8
    var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format("No. ","!init_No. ","!fix_No. ","!rew_No. ",'initPos','fixDur',"rewMag ", "totalPoints ", "trialscorrect ", 
        ' '*7+"initRT ", ' '*11+"initVT ",' '*11+"fixVT ",' '*12+"rewRT ",' '*10+"rewVT ",' fix_click',' rew_click'))
    var.dataFile.flush()

def dataRecordStart3(var,dbc):
    var.expInfo = setup.username()
    p_net = (var.expInfo['Net ID'])
    p_num = sql.r_subjid(dbc,p_net)
    expName = os.path.basename(__file__)[:-3]
    stt = datetime.datetime.now()
    expDate = datetime.datetime.now().strftime("%Y-%m-%d_T%H_%M_%S")
    fileName = u'data/%s_%s_%s.csv' %(p_num, expName, expDate)
    var.dataFile = open(fileName, 'w') # note that MS Excel has only ASCII .csv, other spreadsheets do support UTF-8
    var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format("No.","!init_","!fix_","!rew_","rewMag", "Total ", "hit_No. ", 
        "initRT ", ' '*11+"initVT ",' '*11+"fixVT ",'fixDur',' '*3+'initPos',' '*3+'bluePos',' '*11+"blueRT",' '*11+"blueVT",' '*12+"rewRT ",' '*10+"rewVT ",' fix_click',' rew_click'))
    var.dataFile.flush()


def dataRecordStart4(var,dbc):
    var.expInfo = setup.username()
    p_net = (var.expInfo['Net ID'])
    p_num = sql.r_subjid(dbc,p_net)
    expName = os.path.basename(__file__)[:-3]
    stt = datetime.datetime.now()
    expDate = datetime.datetime.now().strftime("%Y-%m-%d_T%H_%M_%S")
    fileName = u'data/%s_%s_%s.csv' %(p_num, expName, expDate)
    var.dataFile = open(fileName, 'w') # note that MS Excel has only ASCII .csv, other spreadsheets do support UTF-8
    var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format("totalNo.","No.","!init_","!fix_","!rew_","rewMag", "Total ", "hit_No. ", 
        "initRT ", ' '*11+"initVT ",' '*11+"fixVT ",'fixDur',' '*2+'initPos',' '*2+'yellowPos',' '*2+'Dist',' '*11+"yellowRT",' '*11+"yellowVT",' '*12+"rewRT ",' '*10+"rewVT ",' fix_click',' rew_click'))
    var.dataFile.flush()
    
def dataRecordStart5(var,dbc):
    var.expInfo = setup.username()
    p_net = (var.expInfo['Net ID'])
    p_num = sql.r_subjid(dbc,p_net)
    expName = os.path.basename(__file__)[:-3]
    stt = datetime.datetime.now()
    expDate = datetime.datetime.now().strftime("%Y-%m-%d_T%H_%M_%S")
    fileName = u'data/%s_%s_%s.csv' %(p_num, expName, expDate)
    var.dataFile = open(fileName, 'w') # note that MS Excel has only ASCII .csv, other spreadsheets do support UTF-8
    var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format("totalNo.","No.","!init_","!fix_","!rew_","rewMag","Total ", "hit_No. ", 
        "initRT ", ' '*11+"initVT ",' '*11+"fixVT ",'fixDur',' '*2+'initPos',' '*2+'yellowPos',' '*2+'Dist',' '*2+'delay',' '*11+"yellowRT",' '*11+"yellowVT",' '*12+"rewRT ",' '*10+"rewVT ",' fix_click',' del_click',' rew_click'))
    var.dataFile.flush()
#----------------------------------------------------------------------------

# draw all the circles 
def circles(var,doo): # draws all the circles
    for i in range(len(var.elX)): # loop over all circles
        doo.circle.fillColor = var.gray2 # set circle color to be gray
        doo.circle.pos = ([var.elX[i],var.elY[i]]) # set individual circle positions
        doo.circle.draw() # draw each circle

#  draw all the circles in black during violation
def wrongCircles(var,doo):
    for i in range(len(var.elX)): # loop over all circles
        doo.circle.fillColor = var.black # set circle color to be black
        doo.circle.pos = ([var.elX[i],var.elY[i]]) # set individual circle positions
        doo.circle.draw() # draw each circle

#this function transfers cart to polar for the clock
def cart2pol(var,x, y):
    rho = np.sqrt((x-var.clockX)**2 + (y-var.clockY)**2)
    phi = np.arctan2(y-var.clockY, x-var.clockX)
    return(rho, phi)

#this function transfers polar to cart for the clock
def pol2cart(var,rho, phi):
    x = rho * np.cos(phi)+var.clockX
    y = rho * np.sin(phi)+var.clockY
    return(x, y)

#this function get two randwom position codes for initiation port
def getInitPos(var):
    #init position only in the center!!!
    var.initPosCode = random.randint(1,2)
    for i in range(1,3):
        if var.initPosCode == i:
            var.initPos = i

#this function get one randwom position code for blue circle port
def getBluePos(var):
    # position not in the center
    while True:
        var.bluePosCode = random.randint(3,8)
        if var.bluePosCode != var.initPosCode:
            break
    for i in range(3,9):
        if var.bluePosCode == i:
            var.bluePos = i

#this function creates symmetric choice positions in MixNonverbal task
def symmetricYBPair(var):
    if var.bluePosCode == 3:
        var.yellowPosCode = 4
    elif var.bluePosCode == 4:
        var.yellowPosCode = 3
    elif var.bluePosCode == 5:
        var.yellowPosCode = 8
    elif var.bluePosCode == 8:
        var.yellowPosCode = 5
    elif var.bluePosCode == 6:
        var.yellowPosCode = 7
    elif var.bluePosCode == 7:
        var.yellowPosCode = 6
    for i in range(3,9):
        if var.yellowPosCode == i:
            var.yellowPos = i
    return var


#this function get one randwom position code for yellow circle port
def getYellowPos(var):
    #position not in the center
    while True:
        var.yellowPosCode = random.randint(3,8)
        if var.yellowPosCode != var.initPosCode and var.yellowPosCode != var.bluePosCode:
            break
    for i in range(3,9):
        if var.yellowPosCode == i:
            var.yellowPos = i

#this function gets a random duration of the fixation
def getFixmag(var):
    random.shuffle(var.fixmag)
    var.fixDur = var.fixmag[random.randint(0,len(var.fixmag)-1)]
    return var

#this function defines the pairs of distance sqr2 and sqr5 from each init port
def initDistancePair(var):
    if var.initPosCode == 1:
        var.D15Pairs = [3,4,6,7]
    elif var.initPosCode == 2:
        var.D15Pairs = [6,7,5,8]
    return var

#this function gets the forced yellow circle position
def get_forcedYellowPosCode(var):
    initDistancePair(var)
    var.yellowPosCode = var.D15Pairs[random.randint(0,len(var.D15Pairs)-1)]
    for i in range(3,9): # changed from (1,9)
        if var.yellowPosCode == i:
            var.yellowPos = i
    return var

#this function calculates the distance between the init port and the stimulus port
def getInitStimDis(var):
    X_init=var.elX[var.initPosCode]
    Y_init=var.elY[var.initPosCode]
    X_stim=var.elX[var.yellowPosCode]
    Y_stim=var.elY[var.yellowPosCode]
    InitStimDis_sq = (X_stim-X_init)**2+(Y_stim-Y_init)**2
    InitStimDis_real = (np.sqrt(InitStimDis_sq))
    var.initStimDis = InitStimDis_real/120.0
    return var

#this function calculates the distance between the init port and the stimulus port in mixNonverbal
def getInitStimDis_exp(var):
    X_init=var.elX[var.initPosCode]
    Y_init=var.elY[var.initPosCode]
    if var.choice == 'y':
        X_stim=var.elX[var.yellowPosCode]
        Y_stim=var.elY[var.yellowPosCode]
    elif var.choice =='b':
        X_stim=var.elX[var.bluePosCode]
        Y_stim=var.elY[var.bluePosCode]
    InitStimDis_sq = (X_stim-X_init)**2+(Y_stim-Y_init)**2
    InitStimDis_real = np.sqrt(InitStimDis_sq)
    var.initStimDis = InitStimDis_real/120
    return var

#this function get a random delay time
def getDelayTime(var):
    random.shuffle(var.delay)
    var.delaymag = var.delay[random.randint(0,len(var.delay)-1)] # Random nagnitude
    if var.delaymag ==1 or var.delaymag == 3:
        var.snddelaymag = 1
    elif var.delaymag ==2 or var.delaymag == 6.5:
        var.snddelaymag = 2
    elif var.delaymag ==4 or var.delaymag == 14:
        var.snddelaymag = 4
    elif var.delaymag ==8 or var.delaymag == 30:
        var.snddelaymag = 8
    else:
        var.snddelaymag = 16
    return var

#this function get a random delay time
def getHighLowDelayTime(var):
    random.shuffle(var.highLowDelay)
    var.delaymag = var.highLowDelay[random.randint(0,len(var.highLowDelay)-1)] # Random nagnitude
    if var.delaymag ==1 or var.delaymag == 3:
        var.snddelaymag = 1
    else:
        var.snddelaymag = 16
    return var

# this function generates a list of low and 'kind'high delay (no longer than 16s)
def getKindHighLowList(var):
    kindHigh = 'tbd'
    low = var.delay[0]
    var.highLowDelay = []
    for delay in var.delay:
        if delay <= 16:
            kindHigh = delay
        else:
            break
    for i in range(np.int(var.forcedTrialNum/2)):
        var.highLowDelay.append(low)
        var.highLowDelay.append(kindHigh)
    random.shuffle(var.highLowDelay)
    return var


# this function gets a random 'kind' end rewamg (no more than 16 s)
def getHighLowDelayTime_kind(var,index):
    var.delaymag = var.highLowDelay[index] # Random nagnitude
    if var.delaymag ==1 or var.delaymag == 3:
        var.snddelaymag = 1
    else:
        var.snddelaymag = 4
    return var
        
# this functions gets the delay time for the orderly block
def getDelaymag(var):
    var.delaymag = var.delay[var.delayIndex]
    if var.delaymag ==1 or var.delaymag == 3:
        var.snddelaymag = 1
    elif var.delaymag ==2 or var.delaymag == 6.5:
        var.snddelaymag = 2
    elif var.delaymag ==4 or var.delaymag == 14:
        var.snddelaymag = 4
    elif var.delaymag ==8 or var.delaymag == 30:
        var.snddelaymag = 8
    else:
        var.snddelaymag = 16
    return var


#this function draws the initiation circle
def initCircle(var,doo):
    doo.circle.pos = np.array([var.elX[var.initPosCode],var.elY[var.initPosCode]])
    doo.circle.fillColor = var.white
    doo.circle.size = var.circle_fullSize
    doo.circle.draw()
    doo.circle.fillColor=var.gray2
    doo.circle.size = var.circle_innerSize
    circleInitIn = doo.circle
    doo.circle.draw()
    doo.circle.size=var.circle_fullSize
    return circleInitIn

#this function draws the initiation circle
def fixCircle(var,doo):
    doo.circle.pos = np.array([var.elX[var.initPosCode],var.elY[var.initPosCode]])
    doo.circle.fillColor=var.white
    doo.circle.size = var.circle_fullSize+2
    doo.circle.draw()
    circleFixIn = doo.circle
    doo.circle.size=var.circle_fullSize
    return circleFixIn

#this function draws the sure bet blue circle
def blueCircle(var,doo):
    doo.circle.pos = np.array([var.elX[var.bluePosCode],var.elY[var.bluePosCode]])
    doo.circle.fillColor = var.cyan
    doo.circle.size=var.circle_fullSize-1
    circleBlue = doo.circle
    doo.circle.draw()
    doo.circle.size=var.circle_fullSize
    return circleBlue

#this function draws the sure bet yellow circle
def yellowCircle(var,doo):
    doo.circle.pos = np.array([var.elX[var.yellowPosCode],var.elY[var.yellowPosCode]])
    doo.circle.fillColor = var.yellow
    doo.circle.size=var.circle_fullSize-1
    circleYellow = doo.circle
    doo.circle.draw()
    doo.circle.size=var.circle_fullSize
    return circleYellow

#this function generates the circle for the clock
def delayCircle(var,doo):
    doo.circle.size = 150
    doo.circle.pos = [0,240]
    doo.circle.fillColor=var.purple
    doo.circle.draw()
    doo.circle.size=var.circle_fullSize


#this function generates the empty circle for the clock
def delayCircleEmpty(var,doo):
    doo.circle.size = 150
    doo.circle.pos = [0,240]
    doo.circle.fillColor=var.gray2
    doo.circle.draw()
    doo.circle.size=var.circle_fullSize
    
#this function draws the scales on the clock
def scales(var,doo):
    pi = math.pi
    for i in range(12):
        startX,startY = pol2cart(var,65,i*pi/6)
        endX,endY = pol2cart(var,75,i*pi/6)
        doo.scale.start = (startX,startY)
        doo.scale.end = (endX,endY)
        doo.scale.draw()

# draw the reward circle
def rewardCircle(var,doo):
    doo.circle.pos = np.array([var.elX[var.rewPosCode],var.elY[var.rewPosCode]]) # set reward port position
    doo.circle.size = var.circle_fullSize # set the size of the outer reward circle
    doo.circle.fillColor = var.purple # set the corlor of the outer reward circle
    doo.circle.draw() # draw the outer reward circle
    doo.circle.size = var.circle_innerSize # set the size of the inner reward circle
    doo.circle.fillColor = var.white # set the corlor of the inner reward circle
    circleRewIn = doo.circle # make the inner circle a variable
    doo.circle.draw() # draw the inner reward circle
    doo.circle.size = var.circle_fullSize # set the circle size back to full size
    return circleRewIn # return the inner circle object for later use

#this function redraws everything while waiting for init poke
def reDrawInit(var,doo,myPoints):
    circles(var,doo)
    initCircle(var,doo)
    if not var.longVerbal:
        myPoints.totalUpdate(var.points)
    setup.mywin.flip()

#this function redraws everything while waiting for blue port poke
def reDrawBlue(var,doo,myPoints):
    circles(var,doo)
    blueCircle(var,doo)
    if not var.longVerbal:
        myPoints.totalUpdate(var.points)
    setup.mywin.flip()

#this function redraws everything while waiting for yellow port poke
def reDrawYellow(var,doo,myPoints):
    circles(var,doo)
    yellowCircle(var,doo)
    if not var.longVerbal:
        myPoints.totalUpdate(var.points)
    setup.mywin.flip(clearBuffer=True)

#this function draws everything while wairting for a choice
def reDrawStim(var,doo,myPoints):
    circles(var,doo)
    blueCircle(var,doo)
    yellowCircle(var,doo)
    myPoints.totalUpdate(var.points)
    setup.mywin.flip()
    
#this function draws everything while wairting for a choice
def reDrawStim_longVerbal(var,doo):
    circles(var,doo)
    blueCircle(var,doo)
    doo.instruction.text = u'%r coins\n  today' % (var.shortmag)
    doo.instruction.height = 18
    doo.instruction.pos = [var.elX[var.bluePosCode],var.elY[var.bluePosCode]]
    doo.instruction.draw()
    yellowCircle(var,doo)
    if var.rewmag==1:
        doo.instruction.text = u'%r coin in\n %r days' % (var.rewmag,var.delaymag)
    else:
        doo.instruction.text = u'%r coins in\n %r days' % (var.rewmag,var.delaymag)
    doo.instruction.pos = [var.elX[var.yellowPosCode],var.elY[var.yellowPosCode]]
    doo.instruction.draw()
    setup.mywin.flip()


#this function draws everything while wairting for a choice
def reDrawStim_shortVerbal(var,doo,myPoints):
    circles(var,doo)
    blueCircle(var,doo)
    doo.instruction.text = u'%r coins\n  now' % (var.shortmag)
    doo.instruction.height = 18
    doo.instruction.pos = [var.elX[var.bluePosCode],var.elY[var.bluePosCode]]
    doo.instruction.alignHoriz='center'
    doo.instruction.draw()
    yellowCircle(var,doo)
    if var.rewmag==1:
        doo.instruction.text = u'%r coin in\n %r secs' % (var.rewmag,var.delaymag)
    else:
        doo.instruction.text = u'%r coins in\n %r secs' % (var.rewmag,var.delaymag)
    #doo.instruction.text = u'%r coins in\n  %r secs' % (var.rewmag,var.delaymag)
    doo.instruction.pos = [var.elX[var.yellowPosCode],var.elY[var.yellowPosCode]]
    doo.instruction.alignHoriz='center'
    doo.instruction.draw()
    myPoints.totalUpdate(var.points)
    setup.mywin.flip()

#this functions draws everyting at the beginning of each trial while waiting for poke in initCircle
def draw_initCircle(var,doo,myPoints):
    circles(var,doo)
    initCircle(var,doo)
    mouse.clickReset()
    event.Mouse(win=setup.mywin, newPos=(var.elX[2],var.elY[2]))  # swiched 3 and 2
    if not var.longVerbal:
        myPoints.totalUpdate(var.points)
    setup.mywin.flip()
    var.state = 'wait_for_initPort_poke'
    return var,doo,myPoints



# redraw everything while waiting for a reward poke
def reDrawRew(var,doo,myPoints):
    circles(var,doo) # draw all the basic circles
    rewardCircle(var,doo) # draw the reward circle
    if not var.longVerbal:
        myPoints.totalUpdate(var.points)# draw the total points earned in nonverbal
    setup.mywin.flip() # show all the drawing

#this function draws the fixation circle 
def draw_fixCircle(var,doo,myPoints):
    var.timeStart2 = time.time()
    timeStartFix = time.time()
    timeEndFix = time.time()
    circles(var,doo)
    fixCircle(var,doo)
    mouse.clickReset()
    myPoints.totalUpdate(var.points)
    setup.mywin.flip()
    beingPressed = False
    while timeEndFix-timeStartFix <= var.fixDur:
        mouse.getPressed()
        if mouse.mouseMoved(distance=var.radius, reset=(var.elX[var.initPos],var.elY[var.initPos])):
            timeEnd = time.time()
            var.wait_for_fixViolation_poke_time = timeEnd-timeStartFix
            var.fixWrong = True
            var.state = 'violationSound'
            return var,doo,myPoints
        elif mouse.isPressedIn(initCircle(var,doo),buttons=[0]):
            if not beingPressed:
                timeEnd = time.time()
                fix_click_time = timeEnd-timeStartFix
                var.fixation_clicks.append(format(str(fix_click_time),'')+'-'+str(var.initPos))
                if len(var.fixation_clicks)>1:
                    timeEnd = time.time()
                    var.wait_for_fixViolation_poke_time = timeEnd-timeStartFix
                    var.fixWrong = True
                    var.state = 'violationSound'
                    return var,doo,myPoints
            beingPressed = True
        elif not mouse.isPressedIn(initCircle(var,doo),buttons=[0]):
            beingPressed = False
        timeEndFix = time.time()
    var.learnedFix +=1
    if var.stg == 2:
        var.goodPokesInARoll += 1
    if var.stg == 2:
        var.state = 'draw_rewardCircle'
    elif var.stg == 3:
        var.state = 'draw_blueCircle'
    elif var.stg >= 4:
        var.state = 'DBR_Sound'
    return var,doo,myPoints

#this function draws the sure bet blue circle and everything else
def draw_blueCircle(var,doo,myPoints):
    circles(var,doo)
    blueCircle(var,doo)
    mouse.clickReset()
    if not var.longVerbal:
        myPoints.totalUpdate(var.points)
    setup.mywin.flip()
    var.state = 'wait_for_bluePort_poke'
    return var,doo,myPoints

#this function draws the yellow circle and everything else
def draw_yellowCircle(var,doo,myPoints):
    circles(var,doo)
    yellowCircle(var,doo)
    mouse.clickReset()
    if not var.longVerbal:
        myPoints.totalUpdate(var.points)
    setup.mywin.flip(clearBuffer=True)
    var.state = 'wait_for_yellowPort_poke'
    return var,doo,myPoints

#this function draws the stimulus circles in MixNonverbal task
def draw_stimCircles(var,doo,myPoints):
    circles(var,doo)
    blueCircle(var,doo)
    yellowCircle(var,doo)
    mouse.clickReset()
    if not var.longVerbal:
        myPoints.totalUpdate(var.points)
    setup.mywin.flip()
    var.state = 'wait_for_choice_poke'
    return var,doo,myPoints

# draw everyting at the beginning of each trial while waiting for the choice
def draw_rewardCircle(var,doo,myPoints):
    circles(var,doo) # draw all the basic circles
    rewardCircle(var,doo) # draw the reward circle
    if var.stg == 0: # reset mouse position at the beginning of the each trial if in stage 0
        event.Mouse(win=setup.mywin, newPos=(var.elX[2],var.elY[2])) 
    mouse.clickReset()
    if not var.longVerbal:
        myPoints.totalUpdate(var.points) # draw the total points earned
    setup.mywin.flip() # show all the drawings
    var.state = 'wait_for_rewardPort_poke' # return the name of next state
    return var,doo,myPoints



#this function is checking whether the mouse clicks within init port
def wait_for_initPort_poke(var,doo,myPoints):
    reDrawInit(var,doo,myPoints)
    var.timeStart1 = time.time()
    while True:
        if mouse.isPressedIn(initCircle(var,doo),buttons=[0]):
            timeEnd1 = time.time()
            var.wait_for_init_poke_time = timeEnd1-var.timeStart1
            #var.trialsCorrect += 1 
            if var.wait_for_init_poke_time <= var.standardRT_get_reward:
                var.learnedInitPoke += 1
                if var.stg == 1:
                    var.goodPokesInARoll += 1
            else:
                var.goodPokesInARoll = 0
            if var.longVerbal or var.shortVerbal:
                var.state = 'draw_stimCircles'
            elif var.stg == 1:
                var.state = 'draw_rewardCircle'
            elif var.stg >= 2:
                var.state = 'draw_fixCircle'
                
            return var,doo,myPoints
        elif mouse.getPressed()[0]>0 and mouse.isPressedIn(initCircle(var,doo))==False:
            timeEnd2 = time.time()
            var.wait_for_initViolation_poke_time = timeEnd2-var.timeStart1
            var.initWrong = True
            var.state = 'violationSound'
            return var,doo,myPoints

#this function is checking whether the mouse clicks within init port
def wait_for_bluePort_poke(var,doo,myPoints):
    reDrawBlue(var,doo,myPoints)
    var.timeStart3 = time.time()
    while True:
        if sum(mouse.getPressed())==0:
            break
    while True:
        if mouse.isPressedIn(blueCircle(var,doo),buttons=[0]):
            timeEnd = time.time()
            var.wait_for_blue_poke_time = timeEnd-var.timeStart3
            if var.wait_for_blue_poke_time <= var.standardRT_get_reward:
                var.learnedBluePoke += 1
                if var.stg == 3:
                    var.goodPokesInARoll += 1
            else:
                var.goodPokesInARoll = 0
            var.state = 'draw_rewardCircle'
            return var,doo,myPoints
        elif mouse.getPressed()[0]>0 and mouse.isPressedIn(blueCircle(var,doo))==False:
            timeEnd = time.time()
            var.wait_for_blueViolation_poke_time = timeEnd-var.timeStart3
            var.blueWrong = True
            var.state = 'violationSound'
            return var,doo,myPoints

#this function is checking whether the mouse clicks within init port
def wait_for_yellowPort_poke(var,doo,myPoints):
    reDrawYellow(var,doo,myPoints)
    var.timeStart3 = time.time()
    while True:
        if sum(mouse.getPressed())==0:
            break
    while True:
        if mouse.isPressedIn(yellowCircle(var,doo),buttons=[0]):
            timeEnd = time.time()
            var.wait_for_yellow_poke_time = timeEnd-var.timeStart3
            if var.wait_for_yellow_poke_time <= var.standardRT_get_reward:
                var.learnedYellowPoke += 1
                if var.stg == 4:
                    if not var.forcedTrial:
                        var.goodPokesInARoll += 1
                    else:
                        var.goodPokesInARoll = 0
            if var.stg != 5:
                var.state = 'draw_rewardCircle'
            elif var.stg == 5:
                var.state = 'clock'
            return var,doo,myPoints
        elif mouse.getPressed()[0]>0 and mouse.isPressedIn(yellowCircle(var,doo))==False:
            timeEnd = time.time()
            var.wait_for_yellowViolation_poke_time = timeEnd-var.timeStart3
            var.yellowWrong = True
            var.state = 'violationSound'
            return var,doo,myPoints

#this function gets a random hit mag
def getHitmag(var):
    ymag = copy.copy(var.mag)
    random.shuffle(ymag)
    var.rewmag = ymag[random.randint(0,len(ymag)-1)] 
    if var.rewmag ==1:
        var.hitmag = 1
    elif var.rewmag ==2:
        var.hitmag = 2
    elif var.rewmag ==4:
        var.hitmag = 3
    else:
        var.hitmag = 4
    return var

# this function generates a high low (6 in total) reward list
def makeHighLowRew(var):
    for i in range(np.int(var.forcedTrialNum/2)-1):
        var.highLowRew.append(var.maxRewMag)
        var.highLowRew.append(var.minRewMag)
        random.shuffle(var.highLowRew)
    return var

#this function gets a random end rewmag
def getHighLowRew(var,index):
    var.rewmag = var.highLowRew[index]
    return var

# this functions gets the reward mag for the orderly block
def getRewmag(var):
    var.rewmag = var.mag[var.rewIndex]
    return var
    
#this function generates and plays the sound of getting an delayed bigger reward(DBR)
def DBR_Sound(var,doo,myPoints):
    toneMag=doo.toneMag(var.rewmag)
    toneMag.play()
    DBRTimeStart = time.time()
    DBRTimeEnd = time.time()
    beingPressed=False
    while DBRTimeEnd-DBRTimeStart < var.DBRSoundDur:
        mouse.getPressed()
        if mouse.mouseMoved(distance=var.radius, reset=(var.elX[var.initPos],var.elY[var.initPos])):
            timeEnd = time.time()
            var.wait_for_fixViolation_poke_time = timeEnd-var.timeStart2
            var.fixWrong = True
            toneMag.stop()
            var.state = 'violationSound'
            return var,doo,myPoints
        elif mouse.isPressedIn(initCircle(var,doo),buttons=[0]):
            if not beingPressed:
                timeEnd = time.time()
                fix_click_time = timeEnd-var.timeStart2
                var.fixation_clicks.append(str(fix_click_time)+'-'+str(var.initPos))
            beingPressed = True
        elif not mouse.isPressedIn(initCircle(var,doo),buttons=[0]):
            beingPressed = False
        DBRTimeEnd = time.time()
    if var.stg == 4:
        var.state = 'draw_yellowCircle'
    elif var.stg >= 5:
        var.state = 'delaySound'
    return var,doo,myPoints

#this functions plays the delay sound 
def delaySound(var,doo,myPoints):
    toneDelay=doo.toneDelay(var.rewmag,var.snddelaymag, var.delaydiscounter)
    toneDelay.play()
    delayTimeStart = time.time()
    delayTimeEnd = time.time()
    beingPressed=False
    while delayTimeEnd-delayTimeStart < var.delaySoundDur:
        mouse.getPressed()
        if mouse.mouseMoved(distance=var.radius, reset=(var.elX[var.initPos],var.elY[var.initPos])):
            timeEnd = time.time()
            var.wait_for_fixViolation_poke_time = timeEnd-var.timeStart2
            var.fixWrong = True
            toneDelay.stop()
            var.state = 'violationSound'
            return var,doo,myPoints
        elif mouse.isPressedIn(initCircle(var,doo),buttons=[0]):
            if not beingPressed:
                timeEnd = time.time()
                fix_click_time = timeEnd-var.timeStart2
                var.fixation_clicks.append(str(fix_click_time)+'-'+str(var.initPos))
            beingPressed = True
        elif not mouse.isPressedIn(initCircle(var,doo),buttons=[0]):
            beingPressed = False
        delayTimeEnd = time.time()
    toneDelay.stop()
    if var.stg == 6:
        var.state = 'draw_stimCircles'
    else:
        var.state = 'draw_yellowCircle'
    return var,doo,myPoints


#this functions draws the delay countdown clock
def clock(var,doo,myPoints):
    var.delayStart = time.time()
    delayEnd = time.time()
    beingPressed = False
    while delayEnd-var.delayStart<=var.delaymag: 
        var.secPos2 = 'TBD'
        var.secPos = np.floor(delayEnd-var.delayStart+60-var.oneRound)*360/60#NB floor will round down to previous second
        if var.secPos != var.secPos2:
            circles(var,doo)
            myPoints.totalUpdate(var.points)
            delayCircle(var,doo)
            scales(var,doo)
            doo.clock.visibleWedge = (0, var.secPos*(60/var.delaymag)+1)
            doo.clock.draw()
            scales(var,doo)
            setup.mywin.flip()
        var.secPos2 = copy.copy(var.secPos)
        
        if mouse.isPressedIn(doo.circle0(),buttons=[0]):
            if not beingPressed:
                timeEnd = time.time()
                delay_click_time = timeEnd-var.delayStart
                var.delay_clicks.append(str(delay_click_time)+'-'+str(0))
            beingPressed = True
        elif mouse.isPressedIn(doo.circle1(),buttons=[0]):
            if not beingPressed:
                timeEnd = time.time()
                delay_click_time = timeEnd-var.delayStart
                var.delay_clicks.append(str(delay_click_time)+'-'+str(1))
            beingPressed = True
        elif mouse.isPressedIn(doo.circle2(),buttons=[0]):
            if not beingPressed:
                timeEnd = time.time()
                delay_click_time = timeEnd-var.delayStart
                var.delay_clicks.append(str(delay_click_time)+'-'+str(2))
            beingPressed = True
        elif mouse.isPressedIn(doo.circle3(),buttons=[0]):
            if not beingPressed:
                timeEnd = time.time()
                delay_click_time = timeEnd-var.delayStart
                var.delay_clicks.append(str(delay_click_time)+'-'+str(3))
            beingPressed = True
        elif mouse.isPressedIn(doo.circle4(),buttons=[0]):
            if not beingPressed:
                timeEnd = time.time()
                delay_click_time = timeEnd-var.delayStart
                var.delay_clicks.append(str(delay_click_time)+'-'+str(4))
            beingPressed = True
        elif mouse.isPressedIn(doo.circle5(),buttons=[0]):
            if not beingPressed:
                timeEnd = time.time()
                delay_click_time = timeEnd-var.delayStart
                var.delay_clicks.append(str(delay_click_time)+'-'+str(5))
            beingPressed = True
        elif mouse.isPressedIn(doo.circle6(),buttons=[0]):
            if not beingPressed:
                timeEnd = time.time()
                delay_click_time = timeEnd-var.delayStart
                var.delay_clicks.append(str(delay_click_time)+'-'+str(6))
            beingPressed = True
        elif mouse.isPressedIn(doo.circle7(),buttons=[0]):
            if not beingPressed:
                timeEnd = time.time()
                delay_click_time = timeEnd-var.delayStart
                var.delay_clicks.append(str(delay_click_time)+'-'+str(7))
            beingPressed = True
        elif mouse.isPressedIn(doo.circle8(),buttons=[0]):
            if not beingPressed:
                timeEnd = time.time()
                delay_click_time = timeEnd-var.delayStart
                var.delay_clicks.append(str(delay_click_time)+'-'+str(8))
            beingPressed = True
        elif mouse.getPressed()[0]>0 and not mouse.isPressedIn(doo.circle8(),buttons=[0]) and not mouse.isPressedIn(doo.circle7(),buttons=[0]) and not mouse.isPressedIn(doo.circle6(),buttons=[0]) and not mouse.isPressedIn(doo.circle5(),buttons=[0]) and not mouse.isPressedIn(doo.circle4(),buttons=[0]) and not mouse.isPressedIn(doo.circle3(),buttons=[0]) and not mouse.isPressedIn(doo.circle2(),buttons=[0]) and not mouse.isPressedIn(doo.circle1(),buttons=[0]) and not mouse.isPressedIn(doo.circle0(),buttons=[0]) :
            if not beingPressed:
                timeEnd = time.time()
                delay_click_time = timeEnd-var.delayStart
                var.delay_clicks.append(str(delay_click_time)+'-'+'other')
            beingPressed = True
        elif sum(mouse.getPressed())==0:
            beingPressed = False
        
        delayEnd = time.time()
    circles(var,doo)
    myPoints.totalUpdate(var.points)
    delayCircleEmpty(var,doo)
    scales(var,doo)
    setup.mywin.flip(clearBuffer=True)
    core.wait(0.2)
    var.state = 'draw_rewardCircle'
    return var,doo,myPoints

#this function is checking whether the mouse clicks within init port
def wait_for_choice_poke(var,doo,myPoints):
    if var.longVerbal:
        reDrawStim_longVerbal(var,doo)
    elif var.shortVerbal:
        reDrawStim_shortVerbal(var,doo,myPoints)
    else:
        reDrawStim(var,doo,myPoints)
    var.timeStart3 = time.time()
    while True:
        if sum(mouse.getPressed())==0:
            break
    while True:
        if mouse.isPressedIn(blueCircle(var,doo),buttons=[0]):
            var.rewmag = var.shortmag
            var.choice = 'b'
            getInitStimDis_exp(var)
            timeEnd = time.time()
            var.wait_for_choice_poke_time = timeEnd-var.timeStart3 # changed from blue
            if var.wait_for_choice_poke_time <= var.standardRT_get_reward:
                var.learnedChoicePoke += 1
                var.goodPokesInARoll += 1
            if var.longVerbal:
                var.state = 'draw_reward'
            else:
                var.state = 'draw_rewardCircle'
            return var,doo,myPoints
        elif mouse.isPressedIn(yellowCircle(var,doo),buttons=[0]):
            var.choice = 'y'
            getInitStimDis_exp(var)
            timeEnd = time.time()
            var.wait_for_choice_poke_time = timeEnd-var.timeStart3
            if var.wait_for_choice_poke_time <= var.standardRT_get_reward: # changed from yellow
                var.learnedChoicePoke += 1
                var.goodPokesInARoll += 1
                var.rewmag= var.blockRewMag
            var.delayStart = time.time()
            if var.longVerbal:
                var.state = 'draw_reward'
            else:
                var.state = 'clock'
            return var,doo,myPoints
        elif mouse.getPressed()[0]>0 and mouse.isPressedIn(blueCircle(var,doo))==False and mouse.isPressedIn(yellowCircle(var,doo))==False:
            timeEnd = time.time()
            var.wait_for_choiceViolation_poke_time = timeEnd-var.timeStart3
            var.choiceWrong = True
            var.state = 'violationSound'
            return var,doo,myPoints

# check and record whether the mouse clicks within a certain place
def wait_for_rewardPort_poke(var,doo,myPoints):
    reDrawRew(var,doo,myPoints) # redraw everything
    var.timeStart1 = time.time() # record start time of waiting for reward poke
    while True:
        if sum(mouse.getPressed())==0:
            break
    while True: # keep checking status
        if mouse.isPressedIn(rewardCircle(var,doo),buttons=[0]): # if mouse click in the reward port
            timeEnd1 = time.time() # record end time of waiting for reward poke
            var.wait_for_reward_poke_time = timeEnd1-var.timeStart1 # calculate the time taken to click in the reward port
            var.rewardGot += 1 # plus 1 in rewardGot
            if var.wait_for_reward_poke_time <= var.standardRT_get_reward: # check it's a quick enough click
                var.learnedRewPoke += 1 # plus 1 in learnedRewPoke if the click was quick enough (assume the subject learned)
                if var.stg == 0 or var.stg==5:
                    var.goodPokesInARoll += 1 #plus 1 in goodPokesInARoll to calculate number of correct pokes in a roll (for passing the stage)
            else: 
                var.goodPokesInARoll = 0 # set goodPokesInARoll to 0 if it's not a quick enough click
            var.state =  'hitSound' # return the name of next state
            return var,doo,myPoints
        elif mouse.getPressed()[0]>0 and mouse.isPressedIn(rewardCircle(var,doo))==False: # if mouse click NOT in the reward port
            timeEnd2 = time.time() # record end time of waiting for the wrong poke
            var.wait_for_rewViolation_poke_time = timeEnd2-var.timeStart1 # calculate the time taken to make the wrong click
            var.rewWrong = True # mark rewWrong to be true for later use
            var.state = 'violationSound' # return the name of next state
            return var,doo,myPoints

# Show the reward chosen by the subject in verbal tasks
def draw_reward(var,doo,myPoints):
    setup.mywin.flip()
    if var.choice=='b':
        doo.instruction.text=u'Your choice: %r coins today' %(var.rewmag)
    else:
        if var.rewmag ==1:
            doo.instruction.text=u'Your choice: %r coin in %r days' %(var.rewmag,var.delaymag)
        else:
            doo.instruction.text=u'Your choice: %r coins in %r days' %(var.rewmag,var.delaymag)
    doo.instruction.height = 30
    doo.instruction.pos=[0, 0]
    doo.instruction.draw()
    setup.mywin.flip()
    core.wait(1.5)
    var.points+=var.rewmag
    var.state = 'none'
    return var,doo,myPoints

# generate the result of a trial in long verbal experiments
def hitSound_longVerbal(var,doo,myPoints):
    myPoints.verbLongDelayMsg(var.choice,var.rewmag,var.delaymag)
    setup.mywin.flip()
    core.wait(2)
    var.points+=var.rewmag
    var.state = 'none'
    return var,doo,myPoints

# generate and play the hit sound
def hitSound(var,doo,myPoints):
    mouse.clickReset() # reset mouse click
    circles(var,doo) # draw all the basic circles
    myPoints.nowtotalUpdate(var.rewmag) # draw the coins earned in this trial
    myPoints.totalUpdate(var.points) # draw the total coins earned
    setup.mywin.flip() # show all the drawings
    showCoinTimeStart = time.time() # record start time of showing coins
    showCoinTimeEnd = time.time() #  record end time of showing coins
    while showCoinTimeEnd-showCoinTimeStart<= var.showCoinDur: # show the coins for certain duration
        showCoinTimeEnd = time.time()
    var.points+=var.rewmag # add reward magnitude of this trial to total points earned
    circles(var,doo) # draw all the basic circles 
    myPoints.totalUpdate(var.points) # draw the total coins earned (new earned added)
    setup.mywin.flip() # show all the drawings (total coins updated, coins in the reward port disappeared)
    var.rew_sound.play(loops = var.rewmag-1) # play the reward sound
    playRewTimeStart = time.time() # record start time of playing reward sound
    playRewTimeEnd = time.time() #  record end time of showing coins
    beingPressed = False # set a boolean to indicate whether mouse is clicked
    while playRewTimeEnd-playRewTimeStart<= var.hitSoundDur*var.rewmag:  # play the reward sound for certain duration, at the same time record any clicks
        if mouse.isPressedIn(doo.circle0(),buttons=[0]): # check if click in circle 0
            if not beingPressed:
                timeEnd = time.time() 
                reward_click_time = timeEnd-playRewTimeStart # calculate the time taken to make the click
                var.reward_clicks.append(str(reward_click_time)+'-'+str(0)) # record the click during reward sound
            beingPressed = True # set the boolean beingPressed to be True
        elif mouse.isPressedIn(doo.circle1(),buttons=[0]): # check if click in circle 1
            if not beingPressed:
                timeEnd = time.time()
                reward_click_time = timeEnd-playRewTimeStart
                var.reward_clicks.append(str(reward_click_time)+'-'+str(1))
            beingPressed = True
        elif mouse.isPressedIn(doo.circle2(),buttons=[0]): # check if click in circle 2
            if not beingPressed:
                timeEnd = time.time()
                reward_click_time = timeEnd-playRewTimeStart
                var.reward_clicks.append(str(reward_click_time)+'-'+str(2))
            beingPressed = True
        elif mouse.isPressedIn(doo.circle3(),buttons=[0]): # check if click in circle 3
            if not beingPressed:
                timeEnd = time.time()
                reward_click_time = timeEnd-playRewTimeStart
                var.reward_clicks.append(str(reward_click_time)+'-'+str(3))
            beingPressed = True
        elif mouse.isPressedIn(doo.circle4(),buttons=[0]): # check if click in circle 4
            if not beingPressed:
                timeEnd = time.time()
                reward_click_time = timeEnd-playRewTimeStart
                var.reward_clicks.append(str(reward_click_time)+'-'+str(4))
            beingPressed = True
        elif mouse.isPressedIn(doo.circle5(),buttons=[0]): # check if click in circle 5
            if not beingPressed:
                timeEnd = time.time()
                reward_click_time = timeEnd-playRewTimeStart
                var.reward_clicks.append(str(reward_click_time)+'-'+str(5))
            beingPressed = True
        elif mouse.isPressedIn(doo.circle6(),buttons=[0]): # check if click in circle 6
            if not beingPressed:
                timeEnd = time.time()
                reward_click_time = timeEnd-playRewTimeStart
                var.reward_clicks.append(str(reward_click_time)+'-'+str(6))
            beingPressed = True
        elif mouse.isPressedIn(doo.circle7(),buttons=[0]): # check if click in circle 7
            if not beingPressed:
                timeEnd = time.time()
                reward_click_time = timeEnd-playRewTimeStart
                var.reward_clicks.append(str(reward_click_time)+'-'+str(7))
            beingPressed = True
        elif mouse.isPressedIn(doo.circle8(),buttons=[0]): # check if click in circle 8
            if not beingPressed:
                timeEnd = time.time()
                reward_click_time = timeEnd-playRewTimeStart
                var.reward_clicks.append(str(reward_click_time)+'-'+str(8))
            beingPressed = True
        elif mouse.getPressed()[0]>0 and not mouse.isPressedIn(doo.circle8(),buttons=[0]) \
        and not mouse.isPressedIn(doo.circle7(),buttons=[0]) and not mouse.isPressedIn(doo.circle6(),buttons=[0]) \
        and not mouse.isPressedIn(doo.circle5(),buttons=[0]) and not mouse.isPressedIn(doo.circle4(),buttons=[0]) \
        and not mouse.isPressedIn(doo.circle3(),buttons=[0]) and not mouse.isPressedIn(doo.circle2(),buttons=[0]) \
        and not mouse.isPressedIn(doo.circle1(),buttons=[0]) and not mouse.isPressedIn(doo.circle0(),buttons=[0]) : # check if click not in any circles
            if not beingPressed: # if didn't press in any circle before
                timeEnd = time.time()
                reward_click_time = timeEnd-playRewTimeStart
                var.reward_clicks.append(str(reward_click_time)+'-'+'other')
            beingPressed = True
        elif sum(mouse.getPressed())==0: # if didn't press anywhere during reward sound
            beingPressed = False # set boolean beingPressed to be false
        playRewTimeEnd = time.time()
    var.state = 'none'  # return the name of next state (end of a trial)
    return var,doo,myPoints

# generate and play the violation sound and the wrong circles
def violationSound(var,doo,myPoints):
    toneOut2 = doo.violationSound() # make a object of the violation sound
    mouse.clickReset() # reset mouse
    while True:
        toneOut2.setVolume(0.5) # set the volume of the violation sound
        toneOut2.play() # play the violation sound
        wrongCircles(var,doo) # draw the violation black circles
        if not var.longVerbal:
            myPoints.totalUpdate(var.points)# draw the total points earned in nonverbal
        setup.mywin.flip() # show all the drawings
        wrongTimeStart = time.time() 
        wrongTimeEnd = time.time()
        while wrongTimeEnd-wrongTimeStart<= var.vioSoundDur: # play the violation sound for a certain duration
            wrongTimeEnd = time.time()
        var.state = 'none'  # return the name of next state (end of a trial)
        return var,doo,myPoints

#this function generates the unordered list of reward/delay values in long verbal tasks
def generate_rewDelInfo(var):
    for i in var.mag:
        for j in var.delay:
            rewDelPair = [i,j]
            var.rewDelPairList.append(rewDelPair)
    random.shuffle(var.rewDelPairList)
    return var


#this function check whether there should a block break. If so, it will give a break and show the next block name
def block_break_check(var):
    if var.blockTrialCounter%var.blockTrial==0 :
        if var.blockName>1:
            block_break()
        block_instruction()
        var.blockName+=1
    return var

#this function assign new stimuli positions and new rewardMag and delayMag to the yellow choice
def new_trial_setup(var):
    getInitPos(var)
    getBluePos(var)
    symmetricYBPair(var)  # gets symmetric yellow position
    getDelayTime(var)
    var.rewmag = var.blockRewMag
    return var



# determine whether to run this trial again or go to next trial
def again_or_next(var):
    if var.rewWrong or var.initWrong or var.fixWrong or var.choiceWrong or var.blueWrong or var.yellowWrong: # if any violations are made, run this trial again with same settings
        if not var.longVerbal and not var.shortVerbal:
            var.rewWrong = False # reset the boolean for next trial
            var.initWrong = False # reset the boolean for next trial
            var.fixWrong = False # reset the boolean for next trial
            var.blueWrong = False # reset the boolean for next trial
            var.yellowWrong = False # reset the boolean for next trial
            var.choiceWrong = False # reset the boolean for next trial
        return 'again'
    else: # otherwise run next trial with new settings
        if not var.longVerbal and not var.shortVerbal:
            var.sameInitPos = False
        return 'next'
        
# determine whether the subject has learned the task
def passStageTest(var):
    if var.goodPokesInARoll >= var.passThreshold: # if the number of correct trials in a roll exceed certain number, assume the subject has learned the task
        return 'pass'

# this function reset all the wrong related variables at the end of each trial
def resetVar(var,again):
    if again:
        var.initWrong = False
        var.rewWrong = False
        var.choiceWrong = False
    else:
        var.sameInitPos = False


#-----------------------------data recording after one trial-----------------------------------
# record all the data in this trial(learning stage 0)
def dataRecord0(var,dbc):
    if var.rewWrong: # record variables if subject made a reward click violation
        var.dataFile.write("{} {} {} {} {} {} {} {}\n".format(" "*8+str(var.trialCounter+1), " "*14+str(var.learnedRewPoke)," "*7+str(0), " "*6+str(var.points), " "*12+str(var.rewardGot), 
            " "*15+'/', " "*8+str(var.wait_for_rewViolation_poke_time),var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'lrew': var.learnedRewPoke, 'rewMag': var.rewmag, 'points': var.points, 'trialsCorrect': var.rewardGot, 
            'rewVT': var.wait_for_rewViolation_poke_time, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    else: # record variables if subject didn't make any violations
        var.dataFile.write("{} {} {} {} {} {} {} {}\n".format(" "*8+str(var.trialCounter+1), " "*14+str(var.learnedRewPoke)," "*7+str(var.rewmag), " "*6+str(var.points), " "*12+str(var.rewardGot), 
            " "*8+str(var.wait_for_reward_poke_time), " "*15+'/',var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'lrew': var.learnedRewPoke, 'rewMag': var.rewmag, 'points': var.points, 'trialsCorrect': var.rewardGot, 
            'rewRT': var.wait_for_reward_poke_time, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    var.dataFile.flush() # clear the data file for next trial
    sql.w_after_LearningStages(dbc,var,sd)

#this function records all the data needed from each trial(learning stage 1)
def dataRecord1(var,dbc):
    if var.initWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*6+str(var.trialCounter+1), " "*10+str(var.learnedInitPoke)," "*13+str(var.learnedRewPoke),' '*3+str(var.initPos)," "*14+str(0), " "*9+str(var.points), " "*12+str(var.rewardGot), 
            " "*14+'/', " "*11+str(var.wait_for_initViolation_poke_time)," "*12+'/'," "*12+'/',var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'points': var.points, 'trialsCorrect': var.rewardGot, 
            'linit': var.learnedInitPoke,'initVT': var.wait_for_initViolation_poke_time, 'initPos': var.initPos, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    elif var.rewWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*6+str(var.trialCounter+1), " "*10+str(var.learnedInitPoke)," "*13+str(var.learnedRewPoke), ' '*3+str(var.initPos),
            " "*14+str(0), " "*9+str(var.points), " "*12+str(var.rewardGot), 
            " "*8+str(var.wait_for_init_poke_time), " "*12+'/', " "*12+'/'," "*13+str(var.wait_for_rewViolation_poke_time),var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'lrew': var.learnedRewPoke, 'rewMag': var.rewmag, 'points': var.points, 'trialsCorrect': var.rewardGot,  
            'rewVT': var.wait_for_rewViolation_poke_time, 'linit': var.learnedInitPoke, 'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    else:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*6+str(var.trialCounter+1), " "*10+str(var.learnedInitPoke),
            " "*13+str(var.learnedRewPoke), ' '*3+str(var.initPos)," "*14+str(var.rewmag), " "*9+str(var.points), " "*12+str(var.rewardGot), 
            " "*8+str(var.wait_for_init_poke_time)," "*12+'/'," "*9+str(var.wait_for_reward_poke_time), " "*12+'/',var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'lrew': var.learnedRewPoke, 'rewMag': var.rewmag, 'points': var.points, 'trialsCorrect': var.rewardGot, 
            'rewRT': var.wait_for_reward_poke_time, 'linit': var.learnedInitPoke, 'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    var.dataFile.flush()
    sql.w_after_LearningStages(dbc,var,sd)

#this function records all the data needed from each trial(learning stage 2)
def dataRecord2(var,dbc):
    if var.initWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*2+str(var.trialCounter+1), 
            " "*5+str(var.learnedInitPoke)," "*10+str(var.learnedFix)," "*8+str(var.learnedRewPoke),
            ' '*3+str(var.initPos),' '*3+'/'," "*8+str(0), " "*9+str(var.points), " "*12+str(var.rewardGot), 
            " "*14+'/', " "*11+str(var.wait_for_initViolation_poke_time)," "*10+'/'," "*12+'/'," "*12+'/',var.fixation_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter+1,'points': var.points, 'trialsCorrect': var.rewardGot, 
            'linit': var.learnedInitPoke, 'initVT': var.wait_for_initViolation_poke_time, 'initPos': var.initPos, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    elif var.fixWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*2+str(var.trialCounter+1), 
            " "*5+str(var.learnedInitPoke)," "*10+str(var.learnedFix)," "*8+str(0),' '*3+str(var.initPos),
            ' '*3+str(var.fixDur)," "*8+str(0), " "*9+str(var.points), " "*12+str(var.rewardGot), 
            " "*8+str(var.wait_for_init_poke_time), " "*12+'/'," "*10+str(var.wait_for_fixViolation_poke_time), 
            " "*12+'/'," "*13+'/',var.fixation_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'rewMag': var.rewmag, 'points': var.points, 'trialsCorrect': var.rewardGot, 
            'linit': var.learnedInitPoke, 'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos,
            'lfix': var.learnedFix,'fixDur': var.fixDur, 'fixVT': var.wait_for_fixViolation_poke_time, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    elif var.rewWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*2+str(var.trialCounter+1), " "*5+str(var.learnedInitPoke)," "*10+str(var.learnedFix)," "*8+str(var.learnedRewPoke),' '*3+str(var.initPos),
            ' '*3+str(var.fixDur)," "*8+str(0), " "*9+str(var.points), " "*12+str(var.rewardGot), 
            " "*8+str(var.wait_for_init_poke_time), " "*12+'/', " "*15+'/'," "*12+'/'," "*17+str(var.wait_for_rewViolation_poke_time),var.fixation_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'lrew': var.learnedRewPoke, 'rewMag': var.rewmag, 'points': var.points, 'trialsCorrect': var.rewardGot, 
            'rewVT': var.wait_for_rewViolation_poke_time, 'linit': var.learnedInitPoke, 'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos,
            'lfix': var.learnedFix,'fixDur': var.fixDur, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    else:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*2+str(var.trialCounter+1), " "*5+str(var.learnedInitPoke),
            " "*10+str(var.learnedFix)," "*8+str(var.learnedRewPoke),' '*3+str(var.initPos),' '*3+str(var.fixDur)," "*8+str(var.rewmag), " "*9+str(var.points), " "*12+str(var.rewardGot), 
            " "*8+str(var.wait_for_init_poke_time)," "*12+'/'," "*15+'/'," "*13+str(var.wait_for_reward_poke_time), " "*12+'/',var.fixation_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'lrew': var.learnedRewPoke, 'rewMag': var.rewmag, 'points': var.points, 'trialsCorrect': var.rewardGot, 
            'rewRT': var.wait_for_reward_poke_time, 'linit': var.learnedInitPoke, 'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos,
            'lfix': var.learnedFix,'fixDur': var.fixDur, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    var.dataFile.flush()
    sql.w_after_LearningStages(dbc,var,sd)

#this function records all the data needed from each trial(learning stage 3)
def dataRecord3(var,dbc):
    if var.initWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*1+str(var.trialCounter+1), 
            " "*3+str(var.learnedInitPoke)," "*5+str(var.learnedFix)," "*5+str(var.learnedRewPoke)," "*3+str(0), 
            " "*5+str(var.points), " "*5+str(var.rewardGot), 
            " "*8+'/', " "*7+str(var.wait_for_initViolation_poke_time)," "*10+'/',' '*3+'/',' '*3+str(var.initPos),
            ' '*3+'/',' '*10+'/',' '*10+'/'," "*12+'/'," "*12+'/',var.fixation_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'linit': var.learnedInitPoke, 
            'initVT': var.wait_for_initViolation_poke_time, 'initPos': var.initPos, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    elif var.fixWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*1+str(var.trialCounter+1), 
            " "*3+str(var.learnedInitPoke)," "*5+str(var.learnedFix)," "*5+str(0)," "*3+str(0), " "*5+str(var.points), 
            " "*5+str(var.rewardGot), 
            " "*4+str(var.wait_for_init_poke_time), " "*8+'/'," "*10+str(var.wait_for_fixViolation_poke_time), 
            ' '*3+str(var.fixDur),' '*3+str(var.initPos),' '*3+'/',' '*10+'/',' '*10+'/'," "*12+'/'," "*13+'/',var.fixation_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'linit': var.learnedInitPoke, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos, 'lfix': var.learnedFix,   
            'fixDur': var.fixDur, 'fixVT': var.wait_for_fixViolation_poke_time, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    elif var.blueWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*1+str(var.trialCounter+1), 
            " "*3+str(var.learnedInitPoke)," "*5+str(var.learnedFix)," "*5+str(0)," "*3+str(0), " "*5+str(var.points), 
            " "*5+str(var.rewardGot), " "*4+str(var.wait_for_init_poke_time), " "*8+'/'," "*10+'/',
            ' '*3+str(var.fixDur),' '*3+str(var.initPos),' '*3+str(var.bluePos),' '*10+'/',
            ' '*10+str(var.wait_for_blueViolation_poke_time), " "*12+'/'," "*13+'/',var.fixation_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'linit': var.learnedInitPoke, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos, 'lfix': var.learnedFix,   
            'fixDur': var.fixDur, 'bluePos': var.bluePos, 'decisionVT':var.wait_for_blueViolation_poke_time, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    elif var.rewWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*1+str(var.trialCounter+1), 
            " "*3+str(var.learnedInitPoke)," "*5+str(var.learnedFix)," "*5+str(var.learnedRewPoke)," "*3+str(0), 
            " "*5+str(var.points), " "*5+str(var.rewardGot), " "*4+str(var.wait_for_init_poke_time), " "*8+'/', 
            " "*15+'/',' '*3+str(var.fixDur),' '*3+str(var.initPos),' '*3+str(var.bluePos),
            ' '*10+str(var.wait_for_blue_poke_time),' '*10+'/'," "*12+'/'," "*17+str(var.wait_for_rewViolation_poke_time),var.fixation_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'lrew': var.learnedRewPoke,'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'rewVT': var.wait_for_rewViolation_poke_time,'linit': var.learnedInitPoke, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos, 'lfix': var.learnedFix,   
            'fixDur': var.fixDur, 'bluePos': var.bluePos, 'decisionRT':var.wait_for_blue_poke_time, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    else:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*1+str(var.trialCounter+1), 
            " "*3+str(var.learnedInitPoke)," "*5+str(var.learnedFix),
            " "*5+str(var.learnedRewPoke)," "*3+str(var.rewmag), " "*5+str(var.points), " "*5+str(var.rewardGot), 
            " "*4+str(var.wait_for_init_poke_time)," "*8+'/'," "*15+'/',' '*3+str(var.fixDur),' '*3+str(var.initPos),
            ' '*3+str(var.bluePos),' '*10+str(var.wait_for_blue_poke_time),' '*10+'/'," "*13+str(var.wait_for_reward_poke_time), " "*12+'/',var.fixation_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'lrew': var.learnedRewPoke,'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'rewRT': var.wait_for_reward_poke_time,'linit': var.learnedInitPoke, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos, 'lfix': var.learnedFix,   
            'fixDur': var.fixDur, 'bluePos': var.bluePos, 'decisionRT':var.wait_for_blue_poke_time, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    var.dataFile.flush()
    sql.w_after_LearningStages(dbc,var,sd)

#this function records all the data needed from each trial(learning stage 4)
def dataRecord4(var,dbc):
    if var.initWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "+str(var.totalTrialCounter+1)," "*1+str(var.mergedTrialCounter+1), " "*3+str(var.learnedInitPoke)," "*5+str(var.learnedFix)," "*5+str(var.learnedRewPoke)," "*3+str(0), " "*5+str(var.points), " "*5+str(var.rewardGot), 
            " "*8+'/', " "*7+str(var.wait_for_initViolation_poke_time)," "*10+'/',' '*3+'/',' '*4+str(var.initPos),
            ' '*4+'/',' '*4+'/',' '*10+'/',' '*10+'/'," "*12+'/'," "*12+'/',var.fixation_clicks,var.reward_clicks))
        d = {'ttrial': var.totalTrialCounter+1, 'trial': var.mergedTrialCounter+1, 'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'linit': var.learnedInitPoke, 
            'initVT': var.wait_for_initViolation_poke_time, 'initPos': var.initPos, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    elif var.fixWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "+str(var.totalTrialCounter+1)," "*1+str(var.mergedTrialCounter+1), " "*3+str(var.learnedInitPoke)," "*5+str(var.learnedFix)," "*5+str(0)," "*3+str(0), " "*5+str(var.points), " "*5+str(var.rewardGot), 
            " "*4+str(var.wait_for_init_poke_time), " "*8+'/'," "*10+str(var.wait_for_fixViolation_poke_time), 
            ' '*3+str(var.fixDur),' '*4+str(var.initPos),' '*4+'/',' '*4+'/',' '*10+'/',' '*10+'/'," "*12+'/'," "*13+'/',var.fixation_clicks,var.reward_clicks))
        d = {'ttrial': var.totalTrialCounter+1, 'trial': var.mergedTrialCounter+1, 'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'linit': var.learnedInitPoke, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos, 'lfix': var.learnedFix,   
            'fixDur': var.fixDur, 'fixVT':var.wait_for_fixViolation_poke_time, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    elif var.yellowWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "+str(var.totalTrialCounter+1)," "*1+str(var.mergedTrialCounter+1), " "*3+str(var.learnedInitPoke)," "*5+str(var.learnedFix)," "*5+str(0)," "*3+str(0), " "*5+str(var.points), " "*5+str(var.rewardGot), 
            " "*4+str(var.wait_for_init_poke_time), " "*8+'/'," "*10+'/',' '*3+str(var.fixDur),' '*4+str(var.initPos),' '*4+str(var.yellowPos),
            ' '*4+str(var.initStimDis),' '*10+'/',' '*10+str(var.wait_for_yellowViolation_poke_time), " "*12+'/'," "*13+'/',var.fixation_clicks,var.reward_clicks))
        d = {'ttrial': var.totalTrialCounter+1, 'trial': var.mergedTrialCounter+1, 'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'linit': var.learnedInitPoke, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos, 'lfix': var.learnedFix,   
            'fixDur': var.fixDur, 'yellowPos': var.yellowPos, 'decisionVT':var.wait_for_yellowViolation_poke_time, 'Distance':var.initStimDis, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    elif var.rewWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "+str(var.totalTrialCounter+1)," "*1+str(var.mergedTrialCounter+1), 
            " "*3+str(var.learnedInitPoke)," "*5+str(var.learnedFix)," "*5+str(var.learnedRewPoke)," "*3+str(0), 
            " "*5+str(var.points), " "*5+str(var.rewardGot), 
            " "*4+str(var.wait_for_init_poke_time), " "*8+'/', " "*15+'/',' '*3+str(var.fixDur),' '*4+str(var.initPos),
            ' '*4+str(var.yellowPos),
            ' '*4+str(var.initStimDis),' '*10+str(var.wait_for_yellow_poke_time),' '*10+'/'," "*12+'/',
            " "*17+str(var.wait_for_rewViolation_poke_time),var.fixation_clicks,var.reward_clicks))
        d = {'ttrial': var.totalTrialCounter+1, 'trial': var.mergedTrialCounter+1, 'lrew': var.learnedRewPoke,'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'rewVT': var.wait_for_rewViolation_poke_time,'linit': var.learnedInitPoke, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos, 'lfix': var.learnedFix,   
            'fixDur': var.fixDur, 'yellowPos': var.yellowPos, 'decisionRT':var.wait_for_yellow_poke_time, 'Distance':var.initStimDis, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    else:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "+str(var.totalTrialCounter+1)," "*1+str(var.mergedTrialCounter+1), 
            " "*3+str(var.learnedInitPoke)," "*5+str(var.learnedFix)," "*5+str(var.learnedRewPoke)," "*3+str(var.rewmag), 
            " "*5+str(var.points), " "*5+str(var.rewardGot), 
            " "*4+str(var.wait_for_init_poke_time)," "*8+'/'," "*15+'/',' '*3+str(var.fixDur),' '*4+str(var.initPos),
            ' '*4+str(var.yellowPos),' '*4+str(var.initStimDis),' '*10+str(var.wait_for_yellow_poke_time),' '*10+'/',
            " "*13+str(var.wait_for_reward_poke_time), " "*12+'/',var.fixation_clicks,var.reward_clicks))
        d = {'ttrial': var.totalTrialCounter+1, 'trial': var.mergedTrialCounter+1,'lrew': var.learnedRewPoke,'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'rewRT': var.wait_for_reward_poke_time,'linit': var.learnedInitPoke, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos, 'lfix': var.learnedFix,   
            'fixDur': var.fixDur, 'yellowPos': var.yellowPos, 'decisionRT':var.wait_for_yellow_poke_time, 'Distance':var.initStimDis, 'fixClicks': var.fixation_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    var.dataFile.flush()
    sql.w_after_LearningStages(dbc,var,sd)

#this function records all the data needed from each trial(learning stage 5)
def dataRecord5(var,dbc):
    if var.initWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "+str(var.totalTrialCounter+1)," "*1+str(var.mergedTrialCounter+1), " "*3+str(var.learnedInitPoke)," "*5+str(var.learnedFix)," "*5+str(var.learnedRewPoke)," "*3+str(0)," "*5+str(var.points)," "*5+str(var.rewardGot), 
            " "*8+'/', " "*7+str(var.wait_for_initViolation_poke_time)," "*10+'/',' '*3+'/',
            ' '*4+str(var.initPos),' '*4+'/',' '*4+'/',' '*4+'/',' '*10+'/',' '*10+'/'," "*12+'/'," "*12+'/',var.fixation_clicks,var.delay_clicks,var.reward_clicks))
        d = {'ttrial': var.totalTrialCounter+1, 'trial': var.mergedTrialCounter+1, 'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot,'linit': var.learnedInitPoke, 
            'initVT': var.wait_for_initViolation_poke_time, 'initPos': var.initPos, 'delay':var.delaymag, 'fixClicks': var.fixation_clicks, 'delayClicks':var.delay_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    elif var.fixWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "+str(var.totalTrialCounter+1)," "*1+str(var.mergedTrialCounter+1), " "*3+str(var.learnedInitPoke)," "*5+str(var.learnedFix)," "*5+str(0)," "*3+str(0), " "*5+str(var.points), " "*5+str(var.rewardGot), 
            " "*4+str(var.wait_for_init_poke_time), " "*8+'/'," "*10+str(var.wait_for_fixViolation_poke_time), 
            ' '*3+str(var.fixDur),' '*4+str(var.initPos),' '*4+'/',' '*4+'/',' '*4+'/',' '*10+'/',' '*10+'/'," "*12+'/'," "*13+'/',var.fixation_clicks,var.delay_clicks,var.reward_clicks))
        d = {'ttrial': var.totalTrialCounter+1, 'trial': var.mergedTrialCounter+1, 'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot,'linit': var.learnedInitPoke, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos, 'lfix': var.learnedFix,   
            'fixDur': var.fixDur, 'fixVT':var.wait_for_fixViolation_poke_time, 'delay':var.delaymag, 'fixClicks': var.fixation_clicks, 'delayClicks':var.delay_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    elif var.yellowWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "+str(var.totalTrialCounter+1)," "*1+str(var.mergedTrialCounter+1), " "*3+str(var.learnedInitPoke)," "*5+str(var.learnedFix)," "*5+str(0)," "*3+str(0), " "*5+str(var.points), " "*5+str(var.rewardGot), 
            " "*4+str(var.wait_for_init_poke_time), " "*8+'/'," "*10+'/',' '*3+str(var.fixDur),' '*4+str(var.initPos),
            ' '*4+str(var.yellowPos),' '*4+str(var.initStimDis),' '*4+'/',' '*10+'/',
            ' '*10+str(var.wait_for_yellowViolation_poke_time), " "*12+'/'," "*13+'/',var.fixation_clicks,var.delay_clicks,var.reward_clicks))
        d = {'ttrial': var.totalTrialCounter+1, 'trial': var.mergedTrialCounter+1, 'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot,'linit': var.learnedInitPoke, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos, 'lfix': var.learnedFix,   
            'fixDur': var.fixDur, 'yellowPos': var.yellowPos, 'decisionVT':var.wait_for_yellowViolation_poke_time, 
            'Distance':var.initStimDis, 'delay':var.delaymag, 'fixClicks': var.fixation_clicks, 'delayClicks':var.delay_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    elif var.rewWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "+str(var.totalTrialCounter+1)," "*1+str(var.mergedTrialCounter+1), " "*3+str(var.learnedInitPoke)," "*5+str(var.learnedFix)," "*5+str(var.learnedRewPoke)," "*3+str(0), " "*5+str(var.points), " "*5+str(var.rewardGot), 
            " "*4+str(var.wait_for_init_poke_time), " "*8+'/', " "*15+'/',' '*3+str(var.fixDur),
            ' '*4+str(var.initPos),' '*4+str(var.yellowPos),' '*4+str(var.initStimDis),' '*4+str(var.delaymag),
            ' '*10+str(var.wait_for_yellow_poke_time),' '*10+'/'," "*12+'/'," "*17+str(var.wait_for_rewViolation_poke_time),var.fixation_clicks,var.delay_clicks,var.reward_clicks))
        d = {'ttrial': var.totalTrialCounter+1, 'trial': var.mergedTrialCounter+1, 'lrew': var.learnedRewPoke,'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'rewVT': var.wait_for_rewViolation_poke_time,'linit': var.learnedInitPoke, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos, 'lfix': var.learnedFix,   
            'fixDur': var.fixDur, 'yellowPos': var.yellowPos, 'decisionRT':var.wait_for_yellow_poke_time, 
            'Distance':var.initStimDis, 'delay':var.delaymag, 'fixClicks': var.fixation_clicks, 'delayClicks':var.delay_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    else:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "+str(var.totalTrialCounter+1)," "*1+str(var.mergedTrialCounter+1), " "*3+str(var.learnedInitPoke)," "*5+str(var.learnedFix)," "*5+str(var.learnedRewPoke)," "*3+str(var.rewmag), " "*5+str(var.points), " "*5+str(var.rewardGot), 
            " "*4+str(var.wait_for_init_poke_time)," "*8+'/'," "*15+'/',' '*3+str(var.fixDur),' '*4+str(var.initPos),
            ' '*4+str(var.yellowPos),' '*4+str(var.initStimDis),' '*4+str(var.delaymag),' '*10+str(var.wait_for_yellow_poke_time),
            ' '*10+'/'," "*13+str(var.wait_for_reward_poke_time), " "*12+'/',var.fixation_clicks,var.delay_clicks,var.reward_clicks))
        d = {'ttrial': var.totalTrialCounter+1, 'trial': var.mergedTrialCounter+1, 'lrew': var.learnedRewPoke,'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'rewRT': var.wait_for_reward_poke_time,'linit': var.learnedInitPoke, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos, 'lfix': var.learnedFix,   
            'fixDur': var.fixDur, 'yellowPos': var.yellowPos, 'decisionRT':var.wait_for_yellow_poke_time, 
            'Distance':var.initStimDis, 'delay':var.delaymag, 'fixClicks': var.fixation_clicks, 'delayClicks':var.delay_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
    var.dataFile.flush()
    sql.w_after_LearningStages(dbc,var,sd)

#this function records all the data needed from each trial (mix nonverbal session)
def dataRecord_mixNon(var,dbc,sessid):
    if var.initWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*1+str(var.trialCounter+1)," "*2+str(var.blockName), " "*3+str(var.points), " "*5+str(var.rewardGot),
        " "*5+'/', " "*5+str(var.wait_for_initViolation_poke_time)," "*5+'/',' '*3+'/',' '*2+str(var.initPos),' '*2+'/',' '*2+'/',' '*5+'/',' '*2+'/',' '*2+str(var.blockRewMag),' '*2+'/',
        ' '*2+'/',' '*2+'/',' '*5+'/'," "*5+'/'," "*5+'/',var.fixation_clicks,var.delay_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'points': var.points,'trialsCorrect': var.rewardGot, 
            'initVT': var.wait_for_initViolation_poke_time, 'initPos': var.initPos,'delay':var.delaymag,'yellowRew':var.blockRewMag, 'fixClicks': var.fixation_clicks, 'delayClicks':var.delay_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
        sql.w_after_Mixnon(dbc,var,sessid,sd)
    elif var.fixWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*1+str(var.trialCounter+1)," "*2+str(var.blockName)," "*3+str(var.points), " "*5+str(var.rewardGot),
        " "*5+str(var.wait_for_init_poke_time)," "*5+'/'," "*5+str(var.wait_for_fixViolation_poke_time), ' '*3+str(var.fixDur),' '*2+str(var.initPos),' '*2+'/',' '*2+'/',
        ' '*5+'/',' '*2+'/',' '*2+str(var.blockRewMag),' '*2+'/',' '*2+'/',' '*2+'/',' '*5+'/'," "*5+'/'," "*5+'/',var.fixation_clicks,var.delay_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'points': var.points,'trialsCorrect': var.rewardGot, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos,'fixDur': var.fixDur,
            'fixVT': var.wait_for_fixViolation_poke_time,'delay':var.delaymag,'yellowRew':var.blockRewMag, 'fixClicks': var.fixation_clicks, 'delayClicks':var.delay_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
        sql.w_after_Mixnon(dbc,var,sessid,sd)
    elif var.yellowWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*1+str(var.trialCounter+1)," "*2+str(var.blockName), " "*3+str(var.points), " "*5+str(var.rewardGot),
        " "*5+str(var.wait_for_init_poke_time), " "*5+'/'," "*5+'/',' '*3+str(var.fixDur),' '*2+str(var.initPos),' '*2+'/',' '*2+str(var.yellowPos),' '*5+'/',' '*2+'/',' '*2+str(var.blockRewMag),' '*2+str(var.rewmag)+'*',
        ' '*2+str(var.initStimDis),' '*2+str(var.delaymag),' '*5+str(var.wait_for_yellowViolation_poke_time), " "*5+'/'," "*5+'/',var.fixation_clicks,var.delay_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter+1,'points': var.points,'trialsCorrect': var.rewardGot, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos,'fixDur': var.fixDur, 
            'bluePos': var.bluePos,'yellowPos': var.yellowPos, 'decisionVT': var.wait_for_yellowViolation_poke_time, 
            'delay':var.delaymag,'yellowRew':var.blockRewMag, 'fixClicks': var.fixation_clicks, 'delayClicks':var.delay_clicks, 'rewClicks': var.reward_clicks}  
        sd = json.dumps(d)
        sql.w_after_Mixnon(dbc,var,sessid,sd)
    elif var.blueWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*1+str(var.trialCounter+1)," "*2+str(var.blockName), " "*3+str(var.points), " "*5+str(var.rewardGot),
        " "*5+str(var.wait_for_init_poke_time), " "*5+'/'," "*5+'/',' '*3+str(var.fixDur),' '*2+str(var.initPos),' '*2+str(var.bluePos),' '*2+'/',' '*5+'/',' '*2+'/',' '*2+str(var.blockRewMag),' '*2+str(var.rewmag)+'*',
        ' '*2+str(var.initStimDis),' '*2+'/',' '*5+str(var.wait_for_blueViolation_poke_time), " "*5+'/'," "*5+'/',var.fixation_clicks,var.delay_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter+1,'points': var.points,'trialsCorrect': var.rewardGot, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos,'fixDur': var.fixDur, 
            'bluePos': var.bluePos,'yellowPos': var.yellowPos, 'decisionVT': var.wait_for_blueViolation_poke_time, 
            'delay':var.delaymag,'yellowRew':var.blockRewMag, 'fixClicks': var.fixation_clicks, 'delayClicks':var.delay_clicks, 'rewClicks': var.reward_clicks}  
        sd = json.dumps(d)
        sql.w_after_Mixnon(dbc,var,sessid,sd)
    elif var.choiceWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*1+str(var.trialCounter+1), " "*2+str(var.blockName),
            " "*3+str(var.points), " "*5+str(var.rewardGot)," "*5+str(var.wait_for_init_poke_time), 
            " "*5+'/'," "*5+'/',' '*3+str(var.fixDur),' '*2+str(var.initPos),' '*2+str(var.bluePos),' '*2+str(var.yellowPos),
            ' '*5+'/',' '*2+'/',' '*2+str(var.blockRewMag),' '*2+str(var.rewmag)+'*',
            ' '*2+'/',' '*2+str(var.delaymag),' '*5+str(var.wait_for_choiceViolation_poke_time), " "*5+'/'," "*5+'/',var.fixation_clicks,var.delay_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter+1,'points': var.points,'trialsCorrect': var.rewardGot, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos,'fixDur': var.fixDur, 
            'bluePos': var.bluePos,'yellowPos': var.yellowPos, 'decisionVT': var.wait_for_choiceViolation_poke_time, 
            'delay':var.delaymag,'yellowRew':var.blockRewMag, 'fixClicks': var.fixation_clicks, 'delayClicks':var.delay_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
        sql.w_after_Mixnon(dbc,var,sessid,sd)
    elif var.rewWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*1+str(var.trialCounter+1)," "*2+str(var.blockName), " "*3+str(var.points), " "*5+str(var.rewardGot),
         " "*5+str(var.wait_for_init_poke_time), " "*5+'/', " "*5+'/',' '*3+str(var.fixDur),' '*2+str(var.initPos),' '*2+str(var.bluePos),' '*2+str(var.yellowPos),' '*5+str(var.wait_for_choice_poke_time),
         ' '*2+str(var.choice),' '*2+str(var.blockRewMag),' '*2+str(var.rewmag)+'*',' '*2+str(var.initStimDis),' '*5+str(var.delaymag),' '*5+'/'," "*5+'/'," "*5+str(var.wait_for_rewViolation_poke_time),var.fixation_clicks,var.delay_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'rewVT': var.wait_for_rewViolation_poke_time, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos,'fixDur': var.fixDur, 
            'bluePos': var.bluePos,'yellowPos': var.yellowPos, 'decisionRT':var.wait_for_choice_poke_time, 
            'Distance':var.initStimDis, 'delay':var.delaymag,'yellowRew':var.blockRewMag,'choice': var.choice, 'fixClicks': var.fixation_clicks, 'delayClicks':var.delay_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
        sql.w_after_Mixnon(dbc,var,sessid,sd)

    else:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*1+str(var.trialCounter+1), " "*2+str(var.blockName)," "*3+str(var.points), " "*5+str(var.rewardGot),
         " "*5+str(var.wait_for_init_poke_time), " "*5+'/', " "*5+'/',' '*3+str(var.fixDur),' '*2+str(var.initPos),' '*2+str(var.bluePos),' '*2+str(var.yellowPos),' '*5+str(var.wait_for_choice_poke_time),
         ' '*2+str(var.choice),' '*2+str(var.blockRewMag),' '*2+str(var.rewmag),' '*2+str(var.initStimDis),' '*5+str(var.delaymag),' '*5+'/',
         " "*5+str(var.wait_for_reward_poke_time), " "*5+'/',var.fixation_clicks,var.delay_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter+1, 'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'rewRT': var.wait_for_reward_poke_time, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos,'fixDur': var.fixDur, 
            'bluePos': var.bluePos,'yellowPos': var.yellowPos, 'decisionRT':var.wait_for_choice_poke_time, 
            'Distance':var.initStimDis, 'delay':var.delaymag,'yellowRew':var.blockRewMag,'choice': var.choice, 'fixClicks': var.fixation_clicks, 'delayClicks':var.delay_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
        if var.choice == 'b':
            var.ychoice = 0
        elif var.choice =='y':
            var.ychoice = 1
        sql.w_after_Mixnon(dbc,var,sessid,sd)
    var.dataFile.flush()

#this function records all the data needed from each trial(long verbal session)
def dataRecord_longVerbal(var,dbc,sessid):
    if var.initWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*1+str(var.trialCounter)," "*2+str(var.blockName), " "*3+str(var.points), " "*5+str(var.rewardGot),
        " "*5+'/', " "*5+str(var.wait_for_initViolation_poke_time)," "*5+'/',' '*3+'/',' '*2+str(var.initPos),' '*2+'/',' '*2+'/',' '*5+'/',' '*2+'/',' '*2+str(var.blockRewMag),' '*2+'/',
        ' '*2+'/',' '*2+'/',' '*5+'/'," "*5+'/'," "*5+'/',var.fixation_clicks,var.delay_clicks,var.reward_clicks))
        d = {'pay_delay':var.pay_delay, 'pay_num':var.pay_num,'trial_pay':var.pay,'trial': var.trialCounter, 'points': var.points,'trialsCorrect': var.rewardGot, 
            'initVT': var.wait_for_initViolation_poke_time, 'initPos': var.initPos,'delay':var.delaymag,'yellowRew':var.blockRewMag, 'fixClicks': var.fixation_clicks, 'delayClicks':var.delay_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
        sql.w_after_longVerbal(dbc,var,sessid,sd)
    elif var.choiceWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*1+str(var.trialCounter), " "*2+str(var.blockName),
            " "*3+str(var.points), " "*5+str(var.rewardGot)," "*5+str(var.wait_for_init_poke_time), 
            " "*5+'/'," "*5+'/',' '*3+str(var.fixDur),' '*2+str(var.initPos),' '*2+str(var.bluePos),' '*2+str(var.yellowPos),
            ' '*5+'/',' '*2+'/',' '*2+str(var.blockRewMag),' '*2+str(var.rewmag)+'*',
            ' '*2+'/',' '*2+str(var.delaymag),' '*5+str(var.wait_for_choiceViolation_poke_time), " "*5+'/'," "*5+'/',var.fixation_clicks,var.delay_clicks,var.reward_clicks))
        d = {'pay_delay':var.pay_delay, 'pay_num':var.pay_num,'trial_pay':var.pay,'trial': var.trialCounter,'points': var.points,'trialsCorrect': var.rewardGot, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos, 
            'bluePos': var.bluePos,'yellowPos': var.yellowPos, 'decisionVT': var.wait_for_choiceViolation_poke_time, 
            'delay':var.delaymag,'yellowRew':var.blockRewMag, 'delayClicks':var.delay_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
        sql.w_after_longVerbal(dbc,var,sessid,sd)
    else:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*1+str(var.trialCounter), " "*2+str(var.blockName)," "*3+str(var.points), " "*5+str(var.rewardGot),
         " "*5+str(var.wait_for_init_poke_time), " "*5+'/', " "*5+'/',' '*3+str(var.fixDur),' '*2+str(var.initPos),' '*2+str(var.bluePos),' '*2+str(var.yellowPos),' '*5+str(var.wait_for_choice_poke_time),
         ' '*2+str(var.choice),' '*2+str(var.blockRewMag),' '*2+str(var.rewmag),' '*2+str(var.initStimDis),' '*5+str(var.delaymag),' '*5+'/',
         " "*5+str(var.wait_for_reward_poke_time), " "*5+'/',var.fixation_clicks,var.delay_clicks,var.reward_clicks))
        d = {'pay_delay':var.pay_delay, 'pay_num':var.pay_num,'trial_pay':var.pay,'trial': var.trialCounter, 'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'rewRT': var.wait_for_reward_poke_time, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos, 
            'bluePos': var.bluePos,'yellowPos': var.yellowPos, 'decisionRT':var.wait_for_choice_poke_time, 
            'Distance':var.initStimDis, 'delay':var.delaymag,'yellowRew':var.blockRewMag,'choice': var.choice, 'delayClicks':var.delay_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
        if var.choice == 'b':
            var.ychoice = 0
        elif var.choice =='y':
            var.ychoice = 1
        sql.w_after_longVerbal(dbc,var,sessid,sd)
    var.dataFile.flush()

#this function records all the data needed from each trial(short verbal session)
def dataRecord_shortVerbal(var,dbc,sessid):
    if var.initWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*1+str(var.trialCounter)," "*2+str(var.blockName), " "*3+str(var.points), " "*5+str(var.rewardGot),
        " "*5+'/', " "*5+str(var.wait_for_initViolation_poke_time)," "*5+'/',' '*3+'/',' '*2+str(var.initPos),' '*2+'/',' '*2+'/',' '*5+'/',' '*2+'/',' '*2+str(var.blockRewMag),' '*2+'/',
        ' '*2+'/',' '*2+'/',' '*5+'/'," "*5+'/'," "*5+'/',var.fixation_clicks,var.delay_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter, 'points': var.points,'trialsCorrect': var.rewardGot, 
            'initVT': var.wait_for_initViolation_poke_time, 'initPos': var.initPos,'delay':var.delaymag,'yellowRew':var.blockRewMag, 'fixClicks': var.fixation_clicks, 'delayClicks':var.delay_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
        sql.w_after_shortVerbal(dbc,var,sessid,sd)
    elif var.choiceWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*1+str(var.trialCounter), " "*2+str(var.blockName),
            " "*3+str(var.points), " "*5+str(var.rewardGot)," "*5+str(var.wait_for_init_poke_time), 
            " "*5+'/'," "*5+'/',' '*3+str(var.fixDur),' '*2+str(var.initPos),' '*2+str(var.bluePos),' '*2+str(var.yellowPos),
            ' '*5+'/',' '*2+'/',' '*2+str(var.blockRewMag),' '*2+str(var.rewmag)+'*',
            ' '*2+'/',' '*2+str(var.delaymag),' '*5+str(var.wait_for_choiceViolation_poke_time), " "*5+'/'," "*5+'/',var.fixation_clicks,var.delay_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter,'points': var.points,'trialsCorrect': var.rewardGot, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos, 
            'bluePos': var.bluePos,'yellowPos': var.yellowPos, 'decisionVT': var.wait_for_choiceViolation_poke_time, 
            'delay':var.delaymag,'yellowRew':var.blockRewMag, 'delayClicks':var.delay_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
        sql.w_after_shortVerbal(dbc,var,sessid,sd)
    elif var.rewWrong:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*1+str(var.trialCounter)," "*2+str(var.blockName), " "*3+str(var.points), " "*5+str(var.rewardGot),
         " "*5+str(var.wait_for_init_poke_time), " "*5+'/', " "*5+'/',' '*3+str(var.fixDur),' '*2+str(var.initPos),' '*2+str(var.bluePos),' '*2+str(var.yellowPos),' '*5+str(var.wait_for_choice_poke_time),
         ' '*2+str(var.choice),' '*2+str(var.blockRewMag),' '*2+str(var.rewmag)+'*',' '*2+str(var.initStimDis),' '*5+str(var.delaymag),' '*5+'/'," "*5+'/'," "*5+str(var.wait_for_rewViolation_poke_time),var.fixation_clicks,var.delay_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter, 'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'rewVT': var.wait_for_rewViolation_poke_time, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos,
            'bluePos': var.bluePos,'yellowPos': var.yellowPos, 'decisionRT':var.wait_for_choice_poke_time, 
            'Distance':var.initStimDis, 'delay':var.delaymag,'yellowRew':var.blockRewMag,'choice': var.choice, 'delayClicks':var.delay_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
        sql.w_after_shortVerbal(dbc,var,sessid,sd)
    else:
        var.dataFile.write("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format(" "*1+str(var.trialCounter), " "*2+str(var.blockName)," "*3+str(var.points), " "*5+str(var.rewardGot),
         " "*5+str(var.wait_for_init_poke_time), " "*5+'/', " "*5+'/',' '*3+str(var.fixDur),' '*2+str(var.initPos),' '*2+str(var.bluePos),' '*2+str(var.yellowPos),' '*5+str(var.wait_for_choice_poke_time),
         ' '*2+str(var.choice),' '*2+str(var.blockRewMag),' '*2+str(var.rewmag),' '*2+str(var.initStimDis),' '*5+str(var.delaymag),' '*5+'/',
         " "*5+str(var.wait_for_reward_poke_time), " "*5+'/',var.fixation_clicks,var.delay_clicks,var.reward_clicks))
        d = {'trial': var.trialCounter, 'rewMag': var.rewmag,'points': var.points, 
            'trialsCorrect': var.rewardGot, 'rewRT': var.wait_for_reward_poke_time, 
            'initRT': var.wait_for_init_poke_time, 'initPos': var.initPos, 
            'bluePos': var.bluePos,'yellowPos': var.yellowPos, 'decisionRT':var.wait_for_choice_poke_time, 
            'Distance':var.initStimDis, 'delay':var.delaymag,'yellowRew':var.blockRewMag,'choice': var.choice, 'delayClicks':var.delay_clicks, 'rewClicks': var.reward_clicks}
        sd = json.dumps(d)
        if var.choice == 'b':
            var.ychoice = 0
        elif var.choice =='y':
            var.ychoice = 1
        sql.w_after_shortVerbal(dbc,var,sessid,sd)
    var.dataFile.flush()

#this function shows all the big coins at final
def show_totalScore(var):
    results = visual.TextStim(setup.mywin, units='pix', ori=0, name='Results',text=u'You got %r coins' % (var.points),    font=u'Arial',
    pos=[0, 0], height=18, wrapWidth=None,color=u'black', colorSpace='rgb', opacity=1,depth=-12.0)
    results.draw()
    setup.mywin.flip()
    core.wait(1.5)

# show stage name to subjects in verbal sessions (eithe long or short delay stage)
def stage_instruction(stageName,var,doo):
    doo.instruction.text = str(stageName)+u' Delays Stage'
    doo.instruction.height = 30
    doo.instruction.pos=[0, 0]
    doo.instruction.draw()
    setup.mywin.flip()
    core.wait(1.5)

# show all the big coins at the end of a session/block
def show_bigCoins(var,myPoints):
    myPoints.stackAllbig(var.points) # draw all the big coins
    setup.mywin.flip() # show the drawings
    core.wait(2) # keep the drawings for 2 seconds
    var.dataFile.close() # close the data file


# get the total points and trial number of this stage
def total_Points_trialCounter(var):
    return var.points, var.trialCounter

# reset the total points and trial number to 0
def reset_Points_trialCounter(var):
    var.trialCounter = 0
    var.points = 0
    var.totalTrialCounter = 0

#  shows all the coins earned at the end of all learning stages
def show_bigCoins_total(totalProfits,myPoints):
    myPoints.stackAllbig(totalProfits) # draw all the big coins
    setup.mywin.flip() # show the drawings
    core.wait(2) # keep the drawings on the screen for 2 seconds

#  generate and show the end session instruction for learning stages
def end_instruction(doo):
    doo.instruction.text = u'This is the end of learning stages.\n\nThe real experiment is about to start. Please get ready.' # set the content of instruction
    doo.instruction.pos=[0,0] # set the position of the instruction
    doo.instruction.height = 30 # set the size of the instruction text
    doo.instruction.draw() # draw the instruction
    setup.mywin.flip() # show the drawings
    core.wait(10) # keep the drawings on the screen for 10 seconds

# generate the end session instruction for mix nonverbal stage
def end_instruction_mixNon(doo):
    doo.instruction.text = u'This is the end of the experimental session.\n\nPlease report to the experimenter. Thank you very much for your participating!\n\n Enjoy the rest of your day :)'
    doo.instruction.pos=[0,0]
    doo.instruction.height = 30
    doo.instruction.draw()
    setup.mywin.flip()
    core.wait(15)

# generate the end session instruction for verbal stage
def end_instruction_verbal(doo,trial_pay,session_pay,pay_num,pay_delay):
    doo.instruction.text = u'This is the end of the experimental session.\n\nTrial # %r from Long Delays Stage # %r was randomly chosen to pay you.\n\nYour choice in that trial was: %r coin(s) in %r days.\n\nPlease report to the experimenter. Thank you very much for your participation!' % (trial_pay,session_pay,pay_num,pay_delay)
    doo.instruction.pos=[0,0]
    doo.instruction.height = 30
    doo.instruction.draw()
    setup.mywin.flip()
    core.wait(15)

# this function randomly picks a trial from all long verbal trials to pay the subjects
def pick_pay(pick1,pick2):
    pay_session = random.choice([1,2])
    if pay_session == 1:
        return pay_session,pick1
    return pay_session,pick2

# this funcion assigns the final payment given the session selected to pay
def assign_pay(session_pay,pay_delay1,pay_delay2,pay_num1,pay_num2):
    if session_pay == 1:
        return pay_delay1, pay_num1
    else:
        return pay_delay2, pay_num2
    
#-------------------Function Nmae Dictionary(for recursive state calling)------------------------
funcDic = {'circles':circles, 'draw_fixCircle':draw_fixCircle,'draw_blueCircle':draw_blueCircle,'draw_yellowCircle':draw_yellowCircle,'draw_rewardCircle': draw_rewardCircle,
        'wait_for_rewardPort_poke':wait_for_rewardPort_poke,'wait_for_initPort_poke':wait_for_initPort_poke,'wait_for_yellowPort_poke':wait_for_yellowPort_poke,'hitSound':hitSound,
        'violationSound':violationSound,'reDrawRew':reDrawRew,'reDrawInit':reDrawInit,'reDrawYellow':reDrawYellow,'DBR_Sound':DBR_Sound,'wait_for_bluePort_poke':wait_for_bluePort_poke,
        'initDistancePair':initDistancePair,'get_forcedYellowPosCode':get_forcedYellowPosCode,'reDrawBlue':reDrawBlue,'DBR_Sound':DBR_Sound,'delaySound':delaySound,'clock':clock,
        'getHighLowDelayTime':getHighLowDelayTime,'draw_stimCircles':draw_stimCircles,'wait_for_choice_poke':wait_for_choice_poke,'draw_reward':draw_reward}
