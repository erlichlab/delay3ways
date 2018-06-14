# Mixnonverbal tasks
# Mixnonverbal tasks
#-------------------imports--------------------------------------------------------------------
import  os,gc, datetime, copy, random
import newPoints,setup,variables,doodle
from psychopy import event
import functions as fc
import SQL_call as sql
#-------------make necessary objects------------------------------
# generate objects for coins, variables, drawings, database connect, and mouse
myPoints = newPoints.NewPoints()
var = variables.Variables()
doo = doodle.Doodle()
dbc = fc.dbconnect()
mouse = event.Mouse(setup.mywin)
#--------------------------Main Code--------------------------------
def MixNonverbal(var,doo,myPoints,dbc,mouse,getName=True,sub_id=None):
    var.stg = 6 # specify stage number ( assign stage #6 for mixnonverbal)
    var. rewardGot = 0
    fc.setpath() # set up directory
    fN = os.path.basename(__file__) # get expName of this file
    expName, extN = os.path.splitext(fN) # get expName and extN
    expDate = datetime.datetime.now().strftime("%Y-%m-%d_T%H_%M_%S") # get stageName
    sessid,p_num,p_net,setiddtb,host_ip,var,dbc = fc.exp_setup(var,doo,dbc,getName,sub_id,expName,expDate) # database setup and data start recording
    setupList = fc.nonverbalSetup(var.nonverbalTotalTrial,var.mag,var.shortmag) # setup the reward of blocks for the whole experiment(same as in nonverbal)
    shuffledSetupList = copy.copy(setupList)# shuffle the reward list
    random.shuffle(shuffledSetupList) # show subjects stage name (short delay)
    for i in range(len(shuffledSetupList)):# apply a reward mag for each block
        var.blockRewMag = shuffledSetupList[i][0] # assign reward mag for this block
        var.blockName = i+1 # assign blockName
        var = fc.instruction(var,doo) # show block instruction to the subject
        while var.blockTrialCounter < shuffledSetupList[i][1]: # run pre-determined number of trials in each block 
            var.rewmag = var.blockRewMag # assign reward mag
            if not var.sameInitPos: # get a new setup if no violation made in the last trial
                fc.getInitPos(var)
                fc.getFixmag(var)
                fc.getBluePos(var)
                var = fc.symmetricYBPair(var)  # gets symmetric yellow position
                fc.getDelayTime(var)
            var,doo,myPoints = fc.draw_initCircle(var,doo,myPoints) # start the first state
            while var.state != 'none': # go through all connected states in one trial
                mouse.clickReset()
                var,doo,myPoints = fc.funcDic[var.state](var,doo,myPoints)
            fc.dataRecord_mixNon(var,dbc,sessid) # record data
            if fc.again_or_next(var) == 'again': # if any violations made
                var.trialCounter+=1 # plus 1 in trialCounter
                var.totalTrialCounter+=1 # not in used here
                var.mergedTrialCounter+=1 # not in used here
                var.sameInitPos = True # next trial will use the same init position
                var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
                var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
                var.delay_clicks=[] # reset delay_clicks(records the clicks during delay waiting time) list
                continue # start over the same trial
            else: # if no violation made
                var.trialCounter+=1 # plus 1 in trialCounter (total trial num)
                var.blockTrialCounter += 1  # plus 1 in blockTrialCounter (trial num in current block)
                var.fixation_clicks = []# reset fixation_clicks record list
                var.reward_clicks=[]# reset reward_clicks record list
                var.delay_clicks=[] # reset delay_clicks(records the clicks during delay waiting time) list
        var.blockTrialCounter = 0 # reset blockTrialCounter to 0 for next block
    fc.show_bigCoins(var,myPoints) # show the total profits to the subjects
    var.dataFile.close() # close the data file
    fc.end_instruction_mixNon(doo) # give the ending instruciton to the subject
    endt = datetime.datetime.now() # record end time

    sql.w_after_mixNonALL(dbc,var,sessid, p_num, expDate, endt, expName, host_ip, setiddtb) # save the data of this session to database
    
if __name__ == "__main__":
    MixNonverbal(var,doo,myPoints,dbc,mouse) # run main function
