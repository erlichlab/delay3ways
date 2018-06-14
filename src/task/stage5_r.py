# learning stage 5_r : learning stage5 for returning subjects. Just need to have 4 trials correct in a roll to pass
import functions as fc

#--------------------------Main Code--------------------------------
def stage5_r(session,var,doo,myPoints,dbc,mouse):
    fc.dataRecordStart5(var,dbc)
    var.stg = 5 # specify number of stage
    var.sessid = session
    highlowIndex = 0
    var.goodPokesInARoll = 0
    var.rewardGot = 0 # reset total points 
    var = fc.getKindHighLowList(var)
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
            var.totalTrialCounter+=1 # not in used here, just for consistency, see stage5.py
            var.mergedTrialCounter+=1 # not in used here, just for consistency, see stage5.py
            var.sameInitPos = True # next trial will use the same init position
            var.goodPokesInARoll = 0 # reset goodPokesInARoll to 0
            var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
            var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
            var.delay_clicks=[] # reset delay_clicks(records the clicks during delay waiting time) list
            continue # start over the same trial
        else: # if no violation made
            var.trialCounter+=1 # plus 1 in trialCounter
            var.totalTrialCounter+=1 # not in used here
            var.mergedTrialCounter+=1 # not in used here
            var.fixation_clicks = []# reset fixation_clicks record list
            var.reward_clicks=[]# reset reward_clicks record list
            var.delay_clicks=[] # reset delay_clicks(records the clicks during delay waiting time) list
        if fc.passStageTest(var) == 'pass':# if this stage is passed, break the loop
            break
    fc.show_bigCoins(var,myPoints) # show total coins earned
    return var
    
if __name__ == "__main__":
    stage5_r(var.sessid,var,doo,myPoints,dbc,mouse) # call main function