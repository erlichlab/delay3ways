# learning stage 1 : learn to click the init port
import functions as fc

#--------------------------Main Code--------------------------------
def stage1(session,var,doo,myPoints,dbc,mouse):
    fc.dataRecordStart1(var,dbc)
    var.stg = 1 # specify number of stage
    var.goodPokesInARoll = 0 # reset good pokes counter
    var.rewardGot = 0 # reset total points 
    var.sessid = session # specify sessid
    while var.trialCounter < var.trial: # run given number of trials
        if not var.sameInitPos: # get a new init position if no violation made in the last trial
            fc.getInitPos(var)
        var,doo,myPoints = fc.draw_initCircle(var,doo,myPoints) # start the first state
        while var.state != 'none': # go through all connected states in one trial
            mouse.clickReset() # reset mouse before each state
            var,doo,myPoints = fc.funcDic[var.state](var,doo,myPoints)
        fc.dataRecord1(var,dbc) # record data
        if fc.again_or_next(var) == 'again': # if any violations made
            var.trialCounter+=1 # plus 1 in trialCounter
            var.sameInitPos = True # next trial will use the same init position
            var.goodPokesInARoll = 0 # reset goodPokesInARoll to 0
            var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
            continue # start over the same trial
        else: # if no violation made
            var.trialCounter+=1 # plus 1 in trialCounter
            var.reward_clicks=[] # reset reward_clicks record list
        if fc.passStageTest(var) == 'pass': # if this stage is passed, break the loop
            break
    fc.show_bigCoins(var,myPoints) # show total coins earned
    return var

if __name__ == "__main__":
    stage1(var.sessid,var,doo,myPoints,dbc) # call main function