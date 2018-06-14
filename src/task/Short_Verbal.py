# Verbal tasks with shorter delays (in seconds)

#--------------import stuff----------------------------------------
import  os, datetime, copy, random
import newPoints,setup,variables,doodle
from psychopy import event
import functions as fc
import SQL_call as sql
#------------make objects----------------------
# these objects won't be made if the file is called from another file
myPoints = newPoints.NewPoints()
var = variables.Variables()
doo = doodle.Doodle()
dbc = fc.dbconnect()
mouse = event.Mouse(setup.mywin)
#--------------------------Main Code--------------------------------
def ShortVerbal(var,doo,myPoints,dbc,mouse,getName=True,sub_id=None,pre_points=0,pre_trials=0,pre_trialsCorrect=0):
    var.rewardGot = pre_trialsCorrect# if it's the second short verbal session in the experiment, rewardGot is accumulated from the first short verbal session
    var.trialCounter = pre_trials# if it's the second short verbal session in the experiment, trialCounter is accumulated from the first short verbal session
    var.points = pre_points # if it's the second short verbal session in the experiment, points are accumulated from the first short verbal session
    var.shortVerbal = True # specify short verbal for specific functions
    fc.setpath() # set up directory
    fN = os.path.basename(__file__) # get expName of this file
    expName, extN = os.path.splitext(fN) # get expName and extN
    stageName = expName[:-7] # get stageName
    expDate = datetime.datetime.now().strftime("%Y-%m-%d_T%H_%M_%S") # get expDate
    sessid,p_num,p_net,setiddtb,host_ip, var,dbc = fc.exp_setup(var,doo,dbc,getName,sub_id,expName,expDate) # database setup and data start recording
    setupList = fc.verbalSetup(var.verbalTotalTrial,var.mag,var.shortmag) # setup the reward of blocks for the whole experiment(same as in nonverbal)
    shuffledSetupList = copy.copy(setupList)# shuffle the reward list
    random.shuffle(shuffledSetupList)
    fc.stage_instruction(stageName,var,doo) # show subjects stage name (short delay)
    for i in range(len(shuffledSetupList)): # apply a reward mag for each block
        var.blockRewMag = shuffledSetupList[i][0] # assign reward mag for this block
        var.blockName = i+1 # assign blockName
        fc.block_instruction(var,doo) # show block instruction to the subject
        while var.blockTrialCounter < shuffledSetupList[i][1]: # run pre-determined number of trials in each block 
            var.rewmag = var.blockRewMag # assign reward mag
            if not var.sameInitPos: # get a new setup if no violation made in the last trial
                fc.getInitPos(var)
                fc.getFixmag(var)
                fc.getBluePos(var)
                var = fc.symmetricYBPair(var) 
                fc.getDelayTime(var)
            var,doo,myPoints = fc.draw_initCircle(var,doo,myPoints) # start the first state
            while var.state != 'none': # go through all connected states in one trial
                mouse.clickReset()
                var,doo,myPoints = fc.funcDic[var.state](var,doo,myPoints)
            if fc.again_or_next(var) == 'again': # if any violations made
                var.trialCounter+=1 # plus 1 in trialCounter
                var.sameInitPos = True # next trial will use the same init position
                var.fixation_clicks=[] # reset fixation_clicks(records the clicks during fixation) list
                var.reward_clicks=[] # reset reward_clicks(records the clicks during reward) list
                var.delay_clicks=[] # reset delay_clicks(records the clicks during delay waiting time) list
                again = True
            else: # if no violation made
                var.trialCounter+=1 # plus 1 in trialCounter (total trial num)
                var.blockTrialCounter += 1  # plus 1 in blockTrialCounter (trial num in current block)
                var.fixation_clicks = []# reset fixation_clicks record list
                var.reward_clicks=[]# reset reward_clicks record list
                var.delay_clicks=[] # reset delay_clicks(records the clicks during delay waiting time) list
                again = False
            fc.dataRecord_shortVerbal(var,dbc,sessid) # record the data for this trial
            fc.resetVar(var,again)
        var.blockTrialCounter = 0 # reset blockTrialCounter
    fc.show_bigCoins(var,myPoints) # show the total profits to the subjects
    var.dataFile.close() # close the data file
    var.shortVerbal = False # reset shortVerbal boolean to be False
    endt = datetime.datetime.now() # record end time
    sql.w_after_Verbal(dbc,var,sessid, p_num, expDate, endt, expName, host_ip, setiddtb) # save data of this session in database
    return p_net,var.points, var.trialCounter, var.rewardGot
    
if __name__ == "__main__":
    ShortVerbal(var,doo,myPoints,dbc,mouse) # run main function
