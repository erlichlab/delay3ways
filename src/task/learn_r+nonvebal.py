# leaning stages + Mixnonverbal tasks for returning subjects
#-------------------imports--------------------------------------------------------------------
import learningStages_r, MixNonverbal_r, doodle, setup, datetime, time, os, newPoints, variables
from psychopy import core,event, visual
import json
import functions as fc
import SQL_call as sql
#-------------make necessary objects------------------------------
myPoints = newPoints.NewPoints()
var = variables.Variables()
doo = doodle.Doodle()
dbc = fc.dbconnect()
mouse = event.Mouse(setup.mywin)
#--------------------------Main Code--------------------------------
def main(var,doo,myPoints,dbc,mouse):
    [rate_ans, dt_ans, chhist_ans]=fc.survey(doo)
    d = {'answer': rate_ans, 'decisionTime': dt_ans, 'choiceHistory': chhist_ans}
    quest = json.dumps(d)
    fc.about_to_start(doo)
    p_net = learningStages_r.learn_r(var,doo,myPoints,dbc,mouse)
    fc.break_instruction(doo)
    MixNonverbal_r.MixNonverbal_r(var,doo,myPoints,dbc,mouse,getName=False,sub_id=p_net)
    expName = os.path.basename(__file__)[:-3]
    expDate = datetime.datetime.now().strftime("%Y-%m-%d_T%H_%M_%S")
    endt = datetime.datetime.now()
    p_num = sql.r_subjid(dbc,p_net)
    id = sql.r_sessid(dbc,p_num)
    sql.w_after_learnNon(dbc,id,p_num, expDate, endt, expName, rate_ans, quest)

if __name__ == '__main__':
    main(var,doo,myPoints,dbc,mouse) # call main function of learning stages for returning subjects