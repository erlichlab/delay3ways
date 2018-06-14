# a class that draws everything about the coins shown in the experiments
from psychopy import visual, core
import setup

class NewPoints:
    def __init__(self):
        self.__pileOrigin = [0,-230] 
        self.__rad = 100
        self.__cPos = [0,0]
        self.__OneStack = 50
        self.__OneBigStack = 50
        self.black = "#000000"
        self.coin = visual.Polygon(setup.mywin, edges=32, units='pix', radius= self.__rad/20, size=(5, 2.5))
        self.bigcoin = visual.Polygon(setup.mywin, edges=32, units='pix', radius= self.__rad/20, size=(10, 5))
        self.dollarSign = visual.TextStim(setup.mywin, text='$',color=self.black, italic=True)
        self.dollarSign3 = visual.TextStim(setup.mywin, text='$$$',color=self.black, italic=True)        
    
    # draw stack of coins given number of coins
    def stackCoins(self, denomination, stack_xpos, ypos, fill):
        for x in range(0, int(denomination)):
            self.__cPos[0] = stack_xpos
            self.__cPos[1] = ypos
            ypos += 5
            self.coin.setPos(self.__cPos)
            self.dollarSign.setPos(self.__cPos)
            self.coin.fillColor = fill
            self.coin.draw()
            self.dollarSign.draw()
    
    # draw stack of big coins given number of coins (shown at the end of session/block)
    def stackBigCoins(self,denomination, stack_xpos, ypos, fill):
        for x in range(0, int(denomination)):
            cPos = [0,0]
            cPos[0] = stack_xpos
            cPos[1] = ypos
            ypos += 8
            self.bigcoin.setPos(cPos)
            self.dollarSign3.setPos(cPos)
            self.bigcoin.fillColor = fill
            self.bigcoin.draw()
            self.dollarSign3.draw()
    
    # make a full stack of  big coins (at the end of a session/block)
    def stackAllbigStackFull(self,Xpos):
        myXpos = Xpos
        myYpos = -150
        self.stackBigCoins(self.__OneBigStack, myXpos, myYpos, '#EE9900')
    
    # make a full stack of  small coins (during the experiment on the right side)
    def totalUpdateStackFull(self,move):
        t_xpos = self.__pileOrigin[0]+450-move
        t_ypos = self.__pileOrigin[1]
        self.stackCoins(self.__OneStack, t_xpos, t_ypos, '#EE9900f')
    
    # draw the coins earned in this trial
    def nowtotalUpdate(self, rewmag):
        n_xpos = self.__pileOrigin[0]
        n_ypos = self.__pileOrigin[1]
        self.stackCoins(rewmag, n_xpos, n_ypos, '#EE9900')
    
    # update the small coin stack during the experiment on the right side
    def totalUpdate(self,points):
        t_xpos = self.__pileOrigin[0]+450
        t_ypos = self.__pileOrigin[1]
        if points <= self.__OneStack:
            self.stackCoins(points, t_xpos, t_ypos, '#EE9900')
        elif points >self.__OneStack and points<=self.__OneStack*2:
            self.totalUpdateStackFull(10)
            self.stackCoins(points-self.__OneStack,t_xpos, t_ypos, '#EE9900')
        elif points> self.__OneStack*2 and points <= self.__OneStack*3:
            self.totalUpdateStackFull(20)
            self.totalUpdateStackFull(10)
            self.stackCoins(points-self.__OneStack*2,t_xpos, t_ypos, '#EE9900')
        elif points> self.__OneStack*3 and points <= self.__OneStack*4:
            self.totalUpdateStackFull(30)
            self.totalUpdateStackFull(20)
            self.totalUpdateStackFull(10)
            self.stackCoins(points-self.__OneStack*3,t_xpos, t_ypos, '#EE9900')
        elif points> self.__OneStack*4 and points <= self.__OneStack*5:
            self.totalUpdateStackFull(40)
            self.totalUpdateStackFull(30)
            self.totalUpdateStackFull(20)
            self.totalUpdateStackFull(10)
            self.stackCoins(points-self.__OneStack*4,t_xpos, t_ypos, '#EE9900')
        elif points> self.__OneStack*5 and points <= self.__OneStack*6:
            self.totalUpdateStackFull(50)
            self.totalUpdateStackFull(40)
            self.totalUpdateStackFull(30)
            self.totalUpdateStackFull(20)
            self.totalUpdateStackFull(10)
            self.stackCoins(points-self.__OneStack*5,t_xpos, t_ypos, '#EE9900')
        elif points> self.__OneStack*6 and points <= self.__OneStack*7:
            self.totalUpdateStackFull(60)
            self.totalUpdateStackFull(50)
            self.totalUpdateStackFull(40)
            self.totalUpdateStackFull(30)
            self.totalUpdateStackFull(20)
            self.totalUpdateStackFull(10)
            self.stackCoins(points-self.__OneStack*6,t_xpos, t_ypos, '#EE9900')
        elif points> self.__OneStack*7 and points <= self.__OneStack*8:
            self.totalUpdateStackFull(70)
            self.totalUpdateStackFull(60)
            self.totalUpdateStackFull(50)
            self.totalUpdateStackFull(40)
            self.totalUpdateStackFull(30)
            self.totalUpdateStackFull(20)
            self.totalUpdateStackFull(10)
            self.stackCoins(points-self.__OneStack*7,t_xpos, t_ypos, '#EE9900')
        elif points> self.__OneStack*8 and points <= self.__OneStack*9:
            self.totalUpdateStackFull(80)
            self.totalUpdateStackFull(70)
            self.totalUpdateStackFull(60)
            self.totalUpdateStackFull(50)
            self.totalUpdateStackFull(40)
            self.totalUpdateStackFull(30)
            self.totalUpdateStackFull(20)
            self.totalUpdateStackFull(10)
            self.stackCoins(points-self.__OneStack*8,t_xpos, t_ypos, '#EE9900')
        elif points> self.__OneStack*9 and points <= self.__OneStack*10:
            self.totalUpdateStackFull(90)
            self.totalUpdateStackFull(80)
            self.totalUpdateStackFull(70)
            self.totalUpdateStackFull(60)
            self.totalUpdateStackFull(50)
            self.totalUpdateStackFull(40)
            self.totalUpdateStackFull(30)
            self.totalUpdateStackFull(20)
            self.totalUpdateStackFull(10)
            self.stackCoins(points-self.__OneStack*9,t_xpos, t_ypos, '#EE9900')
        elif points> self.__OneStack*10 and points <= self.__OneStack*11:
            self.totalUpdateStackFull(100)
            self.totalUpdateStackFull(90)
            self.totalUpdateStackFull(80)
            self.totalUpdateStackFull(70)
            self.totalUpdateStackFull(60)
            self.totalUpdateStackFull(50)
            self.totalUpdateStackFull(40)
            self.totalUpdateStackFull(30)
            self.totalUpdateStackFull(20)
            self.totalUpdateStackFull(10)
            self.stackCoins(points-self.__OneStack*10,t_xpos, t_ypos, '#EE9900')
        elif points> self.__OneStack*11 and points <= self.__OneStack*12:
            self.totalUpdateStackFull(110)
            self.totalUpdateStackFull(100)
            self.totalUpdateStackFull(90)
            self.totalUpdateStackFull(80)
            self.totalUpdateStackFull(70)
            self.totalUpdateStackFull(60)
            self.totalUpdateStackFull(50)
            self.totalUpdateStackFull(40)
            self.totalUpdateStackFull(30)
            self.totalUpdateStackFull(20)
            self.totalUpdateStackFull(10)
            self.stackCoins(points-self.__OneStack*11,t_xpos, t_ypos, '#EE9900')
        elif points> self.__OneStack*12 and points <= self.__OneStack*13:
            self.totalUpdateStackFull(120)
            self.totalUpdateStackFull(110)
            self.totalUpdateStackFull(100)
            self.totalUpdateStackFull(90)
            self.totalUpdateStackFull(80)
            self.totalUpdateStackFull(70)
            self.totalUpdateStackFull(60)
            self.totalUpdateStackFull(50)
            self.totalUpdateStackFull(40)
            self.totalUpdateStackFull(30)
            self.totalUpdateStackFull(20)
            self.totalUpdateStackFull(10)
            self.stackCoins(points-self.__OneStack*12,t_xpos, t_ypos, '#EE9900')
        elif points> self.__OneStack*13 and points <= self.__OneStack*14:
            self.totalUpdateStackFull(130)
            self.totalUpdateStackFull(120)
            self.totalUpdateStackFull(110)
            self.totalUpdateStackFull(100)
            self.totalUpdateStackFull(90)
            self.totalUpdateStackFull(80)
            self.totalUpdateStackFull(70)
            self.totalUpdateStackFull(60)
            self.totalUpdateStackFull(50)
            self.totalUpdateStackFull(40)
            self.totalUpdateStackFull(30)
            self.totalUpdateStackFull(20)
            self.totalUpdateStackFull(10)
            self.stackCoins(points-self.__OneStack*13,t_xpos, t_ypos, '#EE9900')
        elif points> self.__OneStack*14:
            self.totalUpdateStackFull(140)
            self.totalUpdateStackFull(130)
            self.totalUpdateStackFull(120)
            self.totalUpdateStackFull(110)
            self.totalUpdateStackFull(100)
            self.totalUpdateStackFull(90)
            self.totalUpdateStackFull(80)
            self.totalUpdateStackFull(70)
            self.totalUpdateStackFull(60)
            self.totalUpdateStackFull(50)
            self.totalUpdateStackFull(40)
            self.totalUpdateStackFull(30)
            self.totalUpdateStackFull(20)
            self.totalUpdateStackFull(10)
            self.stackCoins(points-self.__OneStack*14,t_xpos, t_ypos, '#EE9900')

#    
    # show of all the coins(big) earned at the end of a session/block
    def stackAllbig(self,points):
        if points <= self.__OneBigStack:
            myXpos = 0
            myYpos = -150
            self.stackBigCoins(points, myXpos, myYpos, '#EE9900')
        elif points > self.__OneBigStack and points<=self.__OneBigStack*2:
            self.stackAllbigStackFull(-20)
            myXpos = 20
            myYpos = -150
            self.stackBigCoins(points-self.__OneBigStack, myXpos, myYpos, '#EE9900')
        elif points > self.__OneBigStack*2 and points<=self.__OneBigStack*3:
            self.stackAllbigStackFull(-40)
            self.stackAllbigStackFull(0)
            myXpos = 40
            myYpos = -150
            self.stackBigCoins(points-self.__OneBigStack*2, myXpos, myYpos, '#EE9900')
        elif points > self.__OneBigStack*3 and points<=self.__OneBigStack*4:
            self.stackAllbigStackFull(-60)
            self.stackAllbigStackFull(-20)
            self.stackAllbigStackFull(20)
            myXpos = 60
            myYpos = -150
            self.stackBigCoins(points-self.__OneBigStack*3, myXpos, myYpos, '#EE9900')
        elif points > self.__OneBigStack*4 and points<=self.__OneBigStack*5:
            self.stackAllbigStackFull(-80)
            self.stackAllbigStackFull(-40)
            self.stackAllbigStackFull(0)
            self.stackAllbigStackFull(40)
            myXpos = 80
            myYpos = -150
            self.stackBigCoins(points-self.__OneBigStack*4, myXpos, myYpos, '#EE9900')
        elif points > self.__OneBigStack*5 and points<=self.__OneBigStack*6:
            self.stackAllbigStackFull(-100)
            self.stackAllbigStackFull(-60)
            self.stackAllbigStackFull(-20)
            self.stackAllbigStackFull(20)
            self.stackAllbigStackFull(60)
            myXpos = 100
            myYpos = -150
            self.stackBigCoins(points-self.__OneBigStack*5, myXpos, myYpos, '#EE9900')
        elif points > self.__OneBigStack*6 and points<=self.__OneBigStack*7:
            self.stackAllbigStackFull(-120)
            self.stackAllbigStackFull(-80)
            self.stackAllbigStackFull(-40)
            self.stackAllbigStackFull(0)
            self.stackAllbigStackFull(40)
            self.stackAllbigStackFull(80)
            myXpos = 120
            myYpos = -150
            self.stackBigCoins(points-self.__OneBigStack*6, myXpos, myYpos, '#EE9900')
        elif points > self.__OneBigStack*7 and points<=self.__OneBigStack*8:
            self.stackAllbigStackFull(-140)
            self.stackAllbigStackFull(-100)
            self.stackAllbigStackFull(-60)
            self.stackAllbigStackFull(-20)
            self.stackAllbigStackFull(20)
            self.stackAllbigStackFull(60)
            self.stackAllbigStackFull(100)
            myXpos = 140
            myYpos = -150
            self.stackBigCoins(points-self.__OneBigStack*7, myXpos, myYpos, '#EE9900')
        elif points > self.__OneBigStack*8 and points<=self.__OneBigStack*9:
            self.stackAllbigStackFull(-160)
            self.stackAllbigStackFull(-120)
            self.stackAllbigStackFull(-80)
            self.stackAllbigStackFull(-40)
            self.stackAllbigStackFull(0)
            self.stackAllbigStackFull(40)
            self.stackAllbigStackFull(80)
            self.stackAllbigStackFull(120)
            myXpos = 160
            myYpos = -150
            self.stackBigCoins(points-self.__OneBigStack*8, myXpos, myYpos, '#EE9900')
        elif points > self.__OneBigStack*9 and points<=self.__OneBigStack*10:
            self.stackAllbigStackFull(-180)
            self.stackAllbigStackFull(-140)
            self.stackAllbigStackFull(-100)
            self.stackAllbigStackFull(-60)
            self.stackAllbigStackFull(-20)
            self.stackAllbigStackFull(20)
            self.stackAllbigStackFull(60)
            self.stackAllbigStackFull(100)
            self.stackAllbigStackFull(140)
            myXpos = 180
            myYpos = -150
            self.stackBigCoins(points-self.__OneBigStack*9, myXpos, myYpos, '#EE9900')
        elif points > self.__OneBigStack*10 and points<=self.__OneBigStack*11:
            self.stackAllbigStackFull(-200)
            self.stackAllbigStackFull(-160)
            self.stackAllbigStackFull(-120)
            self.stackAllbigStackFull(-80)
            self.stackAllbigStackFull(-40)
            self.stackAllbigStackFull(0)
            self.stackAllbigStackFull(40)
            self.stackAllbigStackFull(80)
            self.stackAllbigStackFull(120)
            self.stackAllbigStackFull(160)
            myXpos = 200
            myYpos = -150
            self.stackBigCoins(points-self.__OneBigStack*10, myXpos, myYpos, '#EE9900')
        elif points > self.__OneBigStack*11 and points<=self.__OneBigStack*12:
            self.stackAllbigStackFull(-220)
            self.stackAllbigStackFull(-180)
            self.stackAllbigStackFull(-140)
            self.stackAllbigStackFull(-100)
            self.stackAllbigStackFull(-60)
            self.stackAllbigStackFull(-20)
            self.stackAllbigStackFull(20)
            self.stackAllbigStackFull(60)
            self.stackAllbigStackFull(100)
            self.stackAllbigStackFull(140)
            self.stackAllbigStackFull(180)
            myXpos = 220
            myYpos = -150
            self.stackBigCoins(points-self.__OneBigStack*11, myXpos, myYpos, '#EE9900')
        elif points > self.__OneBigStack*12 and points<=self.__OneBigStack*13:
            self.stackAllbigStackFull(-240)
            self.stackAllbigStackFull(-200)
            self.stackAllbigStackFull(-160)
            self.stackAllbigStackFull(-120)
            self.stackAllbigStackFull(-80)
            self.stackAllbigStackFull(-40)
            self.stackAllbigStackFull(0)
            self.stackAllbigStackFull(40)
            self.stackAllbigStackFull(80)
            self.stackAllbigStackFull(120)
            self.stackAllbigStackFull(160)
            self.stackAllbigStackFull(200)
            myXpos = 240
            myYpos = -150
            self.stackBigCoins(points-self.__OneBigStack*12, myXpos, myYpos, '#EE9900')
        elif points > self.__OneBigStack*13 and points<=self.__OneBigStack*14:
            self.stackAllbigStackFull(-260)
            self.stackAllbigStackFull(-220)
            self.stackAllbigStackFull(-180)
            self.stackAllbigStackFull(-140)
            self.stackAllbigStackFull(-100)
            self.stackAllbigStackFull(-60)
            self.stackAllbigStackFull(-20)
            self.stackAllbigStackFull(20)
            self.stackAllbigStackFull(60)
            self.stackAllbigStackFull(100)
            self.stackAllbigStackFull(140)
            self.stackAllbigStackFull(180)
            self.stackAllbigStackFull(220)
            myXpos = 260
            myYpos = -150
            self.stackBigCoins(points-self.__OneBigStack*13, myXpos, myYpos, '#EE9900')
        elif points > self.__OneBigStack*14:
            self.stackAllbigStackFull(-280)
            self.stackAllbigStackFull(-240)
            self.stackAllbigStackFull(-200)
            self.stackAllbigStackFull(-160)
            self.stackAllbigStackFull(-120)
            self.stackAllbigStackFull(-80)
            self.stackAllbigStackFull(-40)
            self.stackAllbigStackFull(0)
            self.stackAllbigStackFull(40)
            self.stackAllbigStackFull(80)
            self.stackAllbigStackFull(120)
            self.stackAllbigStackFull(160)
            self.stackAllbigStackFull(200)
            self.stackAllbigStackFull(240)
            myXpos = 280
            myYpos = -150
            self.stackBigCoins(points-self.__OneBigStack*14, myXpos, myYpos, '#EE9900')
