# learning stage 5 : learn to wait for larger later reward and learn to associate modulation with reward delay
import functions as fc

#--------------------------Main Code--------------------------------
def stage5(session,var,doo,myPoints,dbc,mouse):
    fc.dataRecordStart5(var,dbc)
    var.stg = 5 # specify number of stage
    var.sessid = session
    highlowIndex = 0 # make high low reward delay index start from 0
    var = fc.getKindHighLowList(var)# generate a high & low (6 in total) delay list
    var.rewardGot = 0 # reset rewardGot to 0
    # the min and max delay trial block (6 trials)
    while var.rewardGot < var.highLowTrialNum:
        var.forcedTrial = True # set a boolean for later use
        if not var.sameInitPos:  # get a new setup if no violation made in the last trial
            fc.getInitPos(var)
            var.rewmag = var.shortmag 
            var = fc.get_forcedYellowPosCode(var)
            var = fc.getHighLowDelayTime_kind(var,highlowIndex)
            var = fc.getInitStimDis(var)
        var,doo,myPoints = fc.draw_initCircle(var,doo,myPoints) # start the first state
        while var.state != 'none': # go through all connected states in one trial
            mouse.clickReset()
            var,doo,myPoints = fc.funcDic[var.state](var,doo,myPoints)
        fc.dataRecord5(var,dbc) # record data
        if fc.again_or_next(var) == 'again': # if any violations made
            var.forcedTrialCounter+=1 # plus 1 in forcedTrialCounter
            var.totalTrialCounter+=1 # plus 1 in totalTrialCounter
            var.mergedTrialCounter+=1 # # plus 1 in mergedTrialCounter (will be reset to 0 after min-max block)
            var.sameInitPos = True # next trial will use the same init position
            var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
            var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
            var.delay_clicks=[] # reset delay_clicks(records the clicks during delay waiting time) list
            continue # start over the same trial
        else:
            var.forcedTrialCounter+=1 # plus 1 in forcedTrialCounter
            var.totalTrialCounter+=1 # plus 1 in totalTrialCounter
            var.mergedTrialCounter+=1 # # plus 1 in mergedTrialCounter (will be reset to 0 after min-max block)
            highlowIndex+=1 # proceed to next high & low reward mag
            var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
            var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
            var.delay_clicks=[] # reset delay_clicks(records the clicks during delay waiting time) list
    var.forcedTrial = False # after forced trials, set this to False
    var.mergedTrialCounter = 0 # resert mergedTrialCounter
    
    # the orderly trials (10 trials)
    var.forcedTrial = True # boolean for forced trials
    inc = True
    while var.delayIndex <= len(var.delay) and var.delayIndex >= 0: # go through all the ordered forced trials
        if not var.sameInitPos: # if no violation made in last trial
            if var.delayIndex < len(var.delay)-1: # let Delay magnitutude vary from 1 to 10 and back to 1
                fc.getDelaymag(var)
            else:
                inc = False
                fc.getDelaymag(var)
            if inc:
                var.delayIndex +=1
            else:
                var.delayIndex -=1
            # get variables for the new trial
            fc.getInitPos(var) 
            fc.getFixmag(var)
            fc.get_forcedYellowPosCode(var)
            fc.getInitStimDis(var)
        var,doo,myPoints = fc.draw_initCircle(var,doo,myPoints) # start the first state
        while var.state != 'none': # go through all connected states in one trial
            mouse.clickReset()
            var,doo,myPoints = fc.funcDic[var.state](var,doo,myPoints)
        fc.dataRecord5(var,dbc) # record data
        if fc.again_or_next(var) == 'again': # if any violations made
            var.totalTrialCounter+=1 # plus 1 in totalTrialCounter
            var.mergedTrialCounter+=1 # # plus 1 in mergedTrialCounter (will be reset to 0 after orderly forced block)
            var.sameInitPos = True # next trial will use the same init position
            var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
            var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
            continue # start over the same trial
        else:
            var.totalTrialCounter+=1 # plus 1 in totalTrialCounter
            var.mergedTrialCounter+=1 # # plus 1 in mergedTrialCounter (will be reset to 0 after orderly forced block)
            var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
            var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
    var.forcedTrial = False # after forced trials, set this to False
    var.mergedTrialCounter = 0 # resert mergedTrialCounter
    var.goodPokesInARoll = 0
        
    # normal trials (4 trials correct to pass)
    while var.trialCounter < var.trial: # run given number of trials
        if not var.sameInitPos: # get a new setup if no violation made in the last trial
            fc.getInitPos(var)
            fc.getFixmag(var)
            fc.getYellowPos(var)
            fc.getHitmag(var)
            fc.getDelayTime(var)
            fc.getInitStimDis(var)
        var,doo,myPoints = fc.draw_initCircle(var,doo,myPoints) # start the first state
        while var.state != 'none': # go through all connected states in one trial
            mouse.clickReset()
            var,doo,myPoints = fc.funcDic[var.state](var,doo,myPoints)
        fc.dataRecord5(var,dbc) # record data
        if fc.again_or_next(var) == 'again': # if any violations made
            var.trialCounter+=1 # plus 1 in trialCounter
            var.totalTrialCounter+=1 # plus 1 in totalTrialCounter
            var.mergedTrialCounter+=1 # # plus 1 in mergedTrialCounter (will be reset to 0 after normal block)
            var.sameInitPos = True # next trial will use the same init position
            var.goodPokesInARoll = 0 # reset goodPokesInARoll to 0
            var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
            var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
            var.delay_clicks=[] # reset delay_clicks(records the clicks during delay waiting time) list
            continue # start over the same trial
        else: # if no violation made
            var.trialCounter+=1 # plus 1 in trialCounter
            var.totalTrialCounter+=1 # plus 1 in totalTrialCounter
            var.mergedTrialCounter+=1 # # plus 1 in mergedTrialCounter (will be reset to 0 after normal block)
            var.fixation_clicks = []# reset fixation_clicks record list
            var.reward_clicks=[]# reset reward_clicks record list
            var.delay_clicks=[] # reset delay_clicks(records the clicks during delay waiting time) list
        if fc.passStageTest(var) == 'pass':# if this stage is passed, break the loop
            break
    fc.show_bigCoins(var,myPoints) # show total coins earned
    return var

if __name__ == "__main__":
    stage5(session,var,doo,myPoints,dbc,mouse) # call main function