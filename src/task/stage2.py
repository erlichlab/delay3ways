# learning stage 2 : learn to fix in the init port
import functions as fc

#--------------------------Main Code--------------------------------
def stage2(session,var,doo,myPoints,dbc,mouse):
    fc.dataRecordStart2(var,dbc)
    var.stg = 2 # specify number of stage
    var.goodPokesInARoll = 0 # reset counter
    var.rewardGot = 0 # reset total points 
    var.sessid = session # specify sessid
    while var.trialCounter < var.trial: # run given number of trials
        if not var.sameInitPos: # get a new init and fix position if no violation made in the last trial
            fc.getInitPos(var)
            fc.getFixmag(var)
        var,doo,myPoints = fc.draw_initCircle(var,doo,myPoints) # start the first state
        while var.state != 'none': # go through all connected states in one trial
            mouse.clickReset() # reset mouse before each state
            var,doo,myPoints = fc.funcDic[var.state](var,doo,myPoints)
        fc.dataRecord2(var,dbc) # record data
        if fc.again_or_next(var) == 'again': # if any violations made
            var.trialCounter+=1 # plus 1 in trialCounter
            var.sameInitPos = True # next trial will use the same init position
            var.goodPokesInARoll = 0 # reset goodPokesInARoll to 0
            var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
            var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
            continue # start over the same trial
        else: # if no violation made
            var.trialCounter+=1 # plus 1 in trialCounter
            var.fixation_clicks = []# reset fixation_clicks record list
            var.reward_clicks=[]# reset reward_clicks record list
        if fc.passStageTest(var) == 'pass':# if this stage is passed, break the loop
            break
    fc.show_bigCoins(var,myPoints) # show total coins earned
    return var
    
if __name__ == "__main__":
    stage2(var.sessid,var,doo,myPoints,dbc) # call main function