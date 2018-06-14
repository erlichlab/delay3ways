# this file contains all the SQL request calls
# functions starting with 'w' are executing/writing data into dtb
# functions starting with 'r' are query/reading data from dtb
import json

# select username in the database
def select_user(dbc,name):
    dbc.use(name)

# get subject id (p_num) given netid 
def r_subjid(dbc,p_net):
    return int(dbc.query("select subjid from subjinfo where netid = '%s'" %p_net)[0][0])

# record data of one trial after the trial for learning stages
def w_after_LearningStages(dbc,var,sd):
    if var.stg <= 2:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, points) values (%s, %s, %s, %s, %s)',vals=(var.sessid, var.trialCounter+1, sd, var.stg, var.points))
    elif var.stg == 3:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, points, smag, sdelay) values (%s, %s, %s, %s, %s, %s, %s)',vals=(var.sessid, var.trialCounter+1, sd, var.stg, var.points, var.shortmag, var.shortdelay))
    elif var.stg == 4:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, points, sdelay) values (%s, %s, %s, %s, %s, %s, %s)',vals=(var.sessid, var.totalTrialCounter+1, sd, var.stg, var.rewmag, var.points, var.shortdelay))
    else:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, delay, points) values (%s, %s, %s, %s, %s, %s, %s)',vals=(var.sessid, var.totalTrialCounter+1, sd, var.stg, var.rewmag, var.delaymag, var.points))

# record data of one trial after the trial for mixNonverbal session
def w_after_Mixnon(dbc,var,sessid,sd):
    if var.initWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, points) values (%s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter+1, sd, var.blockName, var.points))
    elif var.fixWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, points) values (%s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter+1, sd, var.blockName, var.points))
    elif var.yellowWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, delay, points) values (%s, %s, %s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter+1, sd, var.blockName, var.blockRewMag, var.delaymag, var.points))
    elif var.blueWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, points, smag, sdelay) values (%s, %s, %s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter+1, sd, var.blockName, var.points, var.shortmag, var.shortdelay))
    elif var.choiceWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, delay, points, smag, sdelay) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter+1, sd, var.blockName, var.blockRewMag, var.delaymag, var.points, var.shortmag, var.shortdelay))
    elif var.rewWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, delay, points, smag, sdelay) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter+1, sd, var.blockName, var.blockRewMag, var.delaymag, var.points, var.shortmag, var.shortdelay))
    else:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, delay, choice, points, smag, sdelay) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter+1, sd, var.blockName, var.blockRewMag, var.delaymag, var.ychoice, var.points, var.shortmag, var.shortdelay))

# record data of one trial after the trial for short delay verbal sessions
def w_after_shortVerbal(dbc,var,sessid,sd):
    if var.initWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, points) values (%s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter, sd, var.blockName, var.points))
    elif var.yellowWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, delay, points) values (%s, %s, %s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter, sd, var.blockName, var.blockRewMag, var.delaymag, var.points))
    elif var.blueWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, points, smag, sdelay) values (%s, %s, %s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter, sd, var.blockName, var.points, var.shortmag, var.shortdelay))
    elif var.choiceWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, delay, points, smag, sdelay) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter, sd, var.blockName, var.blockRewMag, var.delaymag, var.points, var.shortmag, var.shortdelay))
    elif var.rewWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, delay, points, smag, sdelay) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter, sd, var.blockName, var.blockRewMag, var.delaymag, var.points, var.shortmag, var.shortdelay))
    else:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, delay, choice, points, smag, sdelay) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter, sd, var.blockName, var.blockRewMag, var.delaymag, var.ychoice, var.points, var.shortmag, var.shortdelay))

# record data of one trial after the trial for long delay verbal sessions
def w_after_longVerbal(dbc,var,sessid,sd):
    if var.initWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, points) values (%s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter, sd, var.blockName, var.points))
    elif var.choiceWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, delay, points, smag, sdelay) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter, sd, var.blockName, var.blockRewMag, var.delaymag, var.points, var.shortmag, var.shortdelay))
    elif var.rewWrong:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, delay, points, smag, sdelay) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter, sd, var.blockName, var.blockRewMag, var.delaymag, var.points, var.shortmag, var.shortdelay))
    else:
        dbc.execute('insert into trials (sessid, trialnum, trialdata, stage, rewmag, delay, choice, points, smag, sdelay) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', vals=(sessid, var.trialCounter, sd, var.blockName, var.blockRewMag, var.delaymag, var.ychoice, var.points, var.shortmag, var.shortdelay))

# record session info before a learning stages session in the session table
def w_before_learning(dbc,p_num, expD, st, expN, host_ip, setiddtb):
    dbc.execute('insert into sessions (subjid, sessiondate, starttime, treatment, hostip, settingsid) values (%s, %s, %s, %s, %s, %s)',(p_num, expD, st, expN, host_ip, setiddtb))

# get the last inserted sessid
def r_lastID(dbc):
    return dbc.query('select last_insert_id()')[0][0]# added [0][0] here

# record session info after a learning stages session in the sessions_end table
def w_after_learningALL(dbc,var,p_num, expD, et, expN, host_ip, ttrials, LearningStageTotalPoints, setiddtb):
    dbc.execute('insert into sessions_end (sessid, subjid, sessiondate, endtime, treatment, hostip, num_trials, total_profit, settingsid) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',(var.sessid, p_num, expD, et, expN, host_ip, ttrials, LearningStageTotalPoints, setiddtb))

# get settingsid with given info
def r_settingsid(dbc,settingsdtb):
    return int(dbc.query("select settingsid from settings where description = '%s'" %settingsdtb)[0][0])

# get variables from given setting
def r_varset(dbc,settingsdtb):
    return json.loads(dbc.query("select data from settings where description = '%s'" %settingsdtb)[0][0])

# record session info after a mixNonverbal session in the sessions_end table
def w_after_mixNonALL(dbc,var,sessid, p_num, expDate, endt, expName, host_ip, setiddtb):
    dbc.execute('insert into sessions_end (sessid, subjid, sessiondate, endtime, treatment, hostip, num_trials, total_profit, settingsid) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',\
            (sessid, p_num, expDate, endt, expName, host_ip, var.trialCounter, var.points, setiddtb))
# record session info before a learning stages session in the session table
def w_before_mixnon(dbc,p_num, expDate, stt, expName, host_ip, setiddtb):
    dbc.execute('insert into sessions (subjid, sessiondate, starttime, treatment, hostip, settingsid) values (%s, %s, %s, %s, %s, %s)',(p_num, expDate, stt, expName, host_ip, setiddtb))

# get max sessid(id) from sessions_end table giv given subjid
def r_sessid(dbc,p_num):
    return int(dbc.query("select max(sessid) from sessions_end where subjid = '%s'" %p_num)[0][0])

# record session info after a learning+mixNon session in the sessions_end table
def w_after_learnNon(dbc,id,p_num, expDate, endt, expName, rate_ans, quest):
    dbc.execute('insert into sessions_end (sessid, subjid, sessiondate, endtime, treatment, moneyscarcity, timescarcity, hurry, questionnaire) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',\
                (id+1,p_num, expDate, endt, expName, rate_ans[0], rate_ans[1], rate_ans[2], quest))

#record session info after a (short/long)verbal session in the sessions_end table
def w_after_Verbal(dbc,var,sessid, p_num, expDate, endt, expName, host_ip, setiddtb):
    dbc.execute('insert into sessions_end (sessid, subjid, sessiondate, endtime, treatment, hostip, num_trials, total_profit, settingsid) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)',\
                (sessid, p_num, expDate, endt, expName, host_ip, var.trialCounter, var.points, setiddtb))

# verbal_combined_even/odd
# count the number of trials in the first long verbal session
def r_countChoice(dbc,ses1id):
    return int(dbc.query("select count(choice) from trials where sessid = '%s' and choice is not NULL" %ses1id)[0][0]) 

# record the final info of this whole experiment in sessions_end table in database
def w_after_verbalCombined(dbc,var,id,p_num, expDate, endt, expName, session_pay, trial_pay,pay_num,pay_delay,rate_ans, quest):
    dbc.execute('insert into sessions_end (sessid, subjid, sessiondate, endtime, treatment, sessionpay, trialpay,payrew,paydelay,moneyscarcity, timescarcity, hurry, questionnaire) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',\
                (id+1,p_num, expDate, endt, expName, session_pay, trial_pay,pay_num,pay_delay,rate_ans[0], rate_ans[1], rate_ans[2], quest)) 