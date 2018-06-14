# learning stage 0 : learn to click the reward port for getting reward
import functions as fc

#--------------------------Main Code--------------------------------
def stage0(session,var,doo,myPoints,dbc,mouse):
    fc.dataRecordStart0(var,dbc) # set up data record file
    var.stg = 0 # specify stage 
    var.goodPokesInARoll = 0 # reset counter
    var.rewardGot = 0 # reset total points 
    var.sessid = session # specify sessid
    while var.trialCounter < var.trial: # run given number of trials
        var,doo,myPoints = fc.draw_rewardCircle(var,doo,myPoints) # start the first state
        while var.state != 'none': # go through all connected states in one trial
            mouse.clickReset() # reset mouse before each state
            var,doo,myPoints = fc.funcDic[var.state](var,doo,myPoints)
        fc.dataRecord0(var,dbc) # record data
        if fc.again_or_next(var) == 'again': # if any violations made
            var.trialCounter +=1 # plus 1 in trialCounter
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
    stage0(var.sessid,var,doo,myPoints,dbc,mouse) # call main function