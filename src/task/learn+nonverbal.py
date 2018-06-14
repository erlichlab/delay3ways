# leaning stages + Mixnonverbal tasks for new subjects
#-------------------imports--------------------------------------------------------------------
import learningStages, MixNonverbal, doodle, setup, datetime, time, os, newPoints, variables
from psychopy import core,event, visual
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
    p_net = learningStages.learn(var,doo,myPoints,dbc,mouse)
    fc.break_instruction(doo)
    MixNonverbal.MixNonverbal(var,doo,myPoints,dbc,mouse,getName=False,sub_id=p_net)
    
if __name__ == '__main__':
    main(var,doo,myPoints,dbc,mouse) # call main function of learning stages for returning subjects



