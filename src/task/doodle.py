# a class that does most of the drawing in the experiment
from psychopy import visual,sound
import setup, variables
import numpy as np  # whole numpy lib is available, prepend 'np.'
var = variables.Variables()
class Doodle:
    def __init__(self):
        self.circle = visual.Circle(setup.mywin, units='pix', size = var.circle_fullSize, 
            ori=0, pos=np.array([var.elX[0],var.elY[0]]), fillColor=var.gray2, fillColorSpace='rgb',
            opacity =1, interpolate=True)
        self.scale = visual.Line(setup.mywin, start=(0,0), end=(0,0))
        self.clock = visual.RadialStim(setup.mywin,tex='sqrXsqr', mask='none', units='pix', 
                    pos=(0, 240), size=(148, 148), radialCycles=1, angularCycles=1, 
                    radialPhase=0, angularPhase=0, ori=0.0, texRes=64, angularRes=100, 
                    visibleWedge=(0, 0), rgb=None, color=(1.0, 1.0, 1.0), colorSpace='rgb', 
                    dkl=None, lms=None, contrast=0.0, opacity=1.0, depth=10, rgbPedestal=(1.0, 1.0, 1.0), 
                    interpolate=False, name=None, autoLog=None, maskParams=None)
        self.pressCircle = visual.Circle(setup.mywin, units='pix', size = 150, 
            ori=0, pos=(0, 240), fillColor=None, fillColorSpace='rgb',opacity =1, interpolate=True)
        self.instruction = visual.TextStim(setup.mywin, units='pix', ori=0, name='Instructions',text=u'Block Name',    font=u'Arial',
            pos=[0, 0], height=30, wrapWidth=None,color=u'black', colorSpace='rgb', opacity=1,depth=-12.0,alignVert='center',alignHoriz='center')
        self.survey_instr = visual.TextStim(setup.mywin, units='pix', ori=0, name='Instructions',text=u'Block Name',    font=u'Arial',
            pos=[0, 0], height=20, wrapWidth=None,color=u'black', colorSpace='rgb', opacity=1,depth=-12.0,alignVert='center',alignHoriz='center')

    #this function creates the delayed big reward sound
    def createToneMag(self,magA, magB, r):
        min_freq=600
        max_freq=3000
        dur=var.DBRSoundDur
        freq=44100
        per = 1.0/freq
        tuning = 1
        time = np.arange(0, dur, per)
        sinefreqMagA = min_freq + (magA * (max_freq-min_freq)/var.magScale)
        waveA = np.sin(tuning*time*sinefreqMagA*2*np.pi)/4
        sinefreqMagB = min_freq + (magB * (max_freq-min_freq)/var.magScale)
        waveB = np.sin(tuning*time*sinefreqMagB*2*np.pi)/4
        # Depending on coinflip at runtine, set the tones in the proper channel
        if r == 0:
            waveLR = np.array([waveB, waveA]).transpose()
        elif r == 1:
            waveLR = np.array([waveA, waveB]).transpose()
        waveLR=waveLR.copy(order='C')
        #print waveLR, waveLR.flags
        return waveLR
    
    # get the magnitude of stimulus tone
    def toneMag(self,rewmag):
        toneMag = sound.Sound(value=self.createToneMag(10*rewmag,10*rewmag,0))
        return toneMag
    
    #this function creates the the sound of the delay
    def createToneProb(self,mag, prob, dur, min_freq=600, max_freq=3000, freq=44100):
        per = 1.0/freq
        time = np.arange(0, dur, per)
        # Lottery tone
        sinefreqMag = min_freq + (mag * (max_freq-min_freq)/var.magScale)
        halftime = np.arange(0, dur/2, per)
        waveB1 = np.sin(halftime*sinefreqMag*2*np.pi)
        AM = np.sin(halftime*2*np.pi*(2**(4*prob)))
        AM[AM<0.9]=0
        waveB2 = np.sin(halftime*sinefreqMag*2*np.pi) * AM
        waveB = np.concatenate((waveB2, waveB2))
        # Click rate tones in both channels
        waveLR = np.array([waveB, waveB]).transpose()
        waveLR = waveLR.copy(order='C')
        return waveLR
    
    # get the delay tone
    def toneDelay(self,rewmag,delaymag, disc):
            toneDelay = sound.Sound(value=self.createToneProb(10*rewmag,1.0-delaymag/(10.0*disc), 1.6))
            return toneDelay
    
    # get the violation sound
    def violationSound(self):
        dt = 1.0/var.SF
        t = np.arange (0, var.vioSoundDur, dt) # want to change duration from 0.5 to 2, so that violation sound stays with the black dots.
        k=var.SF*var.vioSoundDur
        tr = np.random.random((k,))
        miss1=np.sin(np.array(t)*8*2*np.pi) 
        miss=miss1*((tr*2)-1)
        toneOut2 = sound.Sound(value=miss,secs=var.vioSoundDur)
        return toneOut2
    
    # create all 8 circle stimuli
    def circle0(self):
        self.circle.pos = ([var.elX[0],var.elY[0]])
        return self.circle
    def circle1(self):
        self.circle.pos = ([var.elX[1],var.elY[1]])
        return self.circle
    def circle2(self):
        self.circle.pos = ([var.elX[2],var.elY[2]])
        return self.circle
    def circle3(self):
        self.circle.pos = ([var.elX[3],var.elY[3]])
        return self.circle
    def circle4(self):
        self.circle.pos = ([var.elX[4],var.elY[4]])
        return self.circle
    def circle5(self):
        self.circle.pos = ([var.elX[5],var.elY[5]])
        return self.circle
    def circle6(self):
        self.circle.pos = ([var.elX[6],var.elY[6]])
        return self.circle
    def circle7(self):
        self.circle.pos = ([var.elX[7],var.elY[7]])
        return self.circle
    def circle8(self):
        self.circle.pos = ([var.elX[8],var.elY[8]])
        return self.circle
    