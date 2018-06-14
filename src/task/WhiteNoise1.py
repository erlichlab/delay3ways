from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import locale_setup, visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import random, datetime, time
# This Python file uses the following encoding: utf-8
#!/usr/bin/env python
# -*- coding: utf8 -*- 
import os  # handy system and path functions
import platform, sys # to get file system encoding
#Load White Noise 
white_noise_file = 'whitenoise_2sec.wav'
white_noise = sound.Sound(value=white_noise_file)
vc = 1
instr = True
adjust = False

#Window Setup
win = visual.Window((900.0,600.0),allowGUI=False,
            monitor='testMonitor', units ='cm')

#Please adjust volume
while instr:
    instructions = visual.TextStim(win, units='pix', ori=0, name='Instructions',
        text="You will hear different sound stimuli throughout the experiment.\n"+ " \n"
        "To prevent any DISCOMFORT or HEARING LOSS,"+ " please adjust the volume of the sound.\n"+ " \n"+
        "If you are ready to hear the white noise press enter.",
        pos=[0, 0], height = 30, wrapWidth=0.9*900, bold=True, font=u'Arial',
        color=u'black', colorSpace='rgb', opacity=1)
    instructions.draw()
#    textbox=visual.TextBox(win,
#                         text=u'\n You will hear different sound stimuli throughout the experiment.\n To prevent any DISCOMFORT or HEARING LOSS,\n please adjust the volume of the sound.\n If you are ready to hear the white noise press enter.', 
#                         font_name='Courier New',
#                         font_size=22,
#                         font_color=[-1,-1,-1], 
#                         units='norm',
#                         size=(1.0,6.0),
#                         pos=(0.5,0.5), 
#                         grid_horz_justification='center',
#                         grid_vert_justification='center'
#                         )
#    textbox.draw()
    win.flip()
    
    presses = event.waitKeys(keyList="return")
    if not presses:
        # no keypress
        print "none"
    elif presses[0]=="return":
        print "yes"
        adjust = True
        instr = False
        # White Noise
        while adjust:
            instructions2 = visual.TextStim(win, units='pix', ori=0, name='Instructions',
                text= "This is the loudest sound you will hear throughout the experiment.\n"+ " \n"+
                "To adjust the volume press on audio icon,"+ " located in the bottom right corner of the Windows screen.\n"+ " \n"+
                "Press Enter to finish volume adjustment.",
                pos=[0, 0], height=30, alignHoriz='center', font=u'Arial',
                color=u'black', colorSpace='rgb', opacity=1, bold=True, wrapWidth=0.9*900
                )
            instructions2.draw()
            win.flip()
            white_noise.setVolume(vc)
            white_noise.play(loops = -1)
            presses = event.waitKeys(10)
            if not presses:
                # no keypress
                print "none"
                p = 0
            elif presses[0]=="esc":
                break
#            elif presses[0]=="up":
#                white_noise.stop()
#                vc+=0.05
#                print 'upvc:',vc
#                white_noise.setVolume(vc)
#                white_noise.play(loops = -1)
#            elif presses[0]=="down":
#                white_noise.stop()
#                vc+=-0.05
#                print 'downvc:',vc
#                white_noise.setVolume(vc)
#                white_noise.play(loops = -1)
            elif presses[0]=="return":
                volume = white_noise.getVolume()
                print 'volume:',volume
                adjust=False
                white_noise.stop()
        


win.close()
core.quit()

