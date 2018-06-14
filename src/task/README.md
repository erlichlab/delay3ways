**Necessary setups before experiment:**

[email *el2509@nyu.edu* or *yw1384@nyu.edu* for further explanations]

    1. Python 2.7 needs to be installed in your computer
    2. Download and install PsychoPy 1.83.04
    3. Download and install any MySQL user interface
    4. git clone repos/ folder (with helpers/ folder and code/ folder in it)
    'helpers' is custom module needed to access dtb
    5. Setup working path
        - In repos/code/functions.py, find setpath() function
        - sys.path.append('directory where you git cloned repos folder')
        - sys.path.append('directory where your /Python/2.7/site-packages is')
    6. Setup MySQL database
        6.1. Setup all tables(and column names) needed in our code
            -sessions: sessid/subjid/sessiondate/starttime/treatment/hostip/settingsid/startts
            -sessions_end: sessid/subjid/sessiondate/endtime/treatment/hostip/num_trials/total_profit/settingsid/sessionpay/trialpay/payrew/paydelay/endts/moneyscarcity/timescarcity/hurry/questionnaire
            -settings: settingid/expgroupid/data/description
            -subjinfo: subjid/netid/firstname/fullname
            -trials: trialid/sessid/trialtime/trialnum/trialdata/stage/rewmag/delay/choice/points/smag/sdelay/short_delay/long_delay
        6.2. Set database user name
            - In repos/code/functions, find dbconnect() function
            - Input your database user name in sql.select_user(dbc,'your user name')
        6.3. Setup a subjects pool in your database
            - In 'subjinfo' table, input information of all subjects
            - There needs to be an ID(netid) for each subject to input at the beginning of each program that will lead a unique subjid saved in the 'subjinfo' table
        6.4. Create two necessary settings
            - You can input whatever fits your need in the n/a's 
            - In 'settings' table, create two rows of necessary settings for our experiment:
| settingsid | expgroupid | data                                                                                                                             | description |
|-----------:|------------|----------------------------------------------------------------------------------------------------------------------------------|-------------|
| n/a        | n/a        | {"delay": [3, 6.5, 14 , 30, 64], "forcedTrialNum": 6, "passThreshold": 4, "ddiscounter": 1.2}                                    | learn3      |
| n/a        | n/a        | {"delay": [ 3 , 6.5, 14, 30, 64], "refresherNum": 10, "blockTrial": 2, "passThreshold": 2, "rewdelpair": 10, "ddiscounter": 1.2} | seconds3    |            

    


**Necessary notes for subjects before experiments:**
    
    1. Ask for subject's consent and ask him to read through and fill out all necessary forms in 'Forms' folder.
    2. Once the person gave his consent, add his data to subjinfo table and he will be given a subjid (manual entry in the dtb).
    3. Adjust sound stimuli volume by running WhiteNoise1.py
    3. Participant will be instructed to insert his netID. If netID is not in the database psychopy will display an error message.



**run the code from the 'cleaned_code' folder:**

    1.For [first time subjects]nonverbal learning + decision stages -> run learn+nonverbal.py
    2.For [returning subjects]nonverbal learning + decision stages -> run learn_r+nonverbal.py
    3.For [subjects with odd subid] verbal blocks -> run verbal_combined_odd.py
    4.For [subjects with even subid] verbal blocks -> run verbal_combined_even.py


**Auxiliary files catalog**
    
    1.functions.py: file which contains all functions needed for other scripts
    2.SQL_call.py: all database related commands(read and write) needed for other scripts
    3.stage0/1/2/3/4/5.py: learning stage 0-5 for first time subjects in nonverbal experiment(imported by learningStages.py)
    4.stage4/5_r.py: learning stage 4/5 for returning subjects in nonverbal experiment(imported by learningStages_r.py)
    5.learningStages.py: compiled learning stages for first time subjects in nonverbal experiment(imported by learn_nonverbal.py)
    6.learningStages_r.py: compiled learning stages for returning subjects in nonverbal experiment(imported by learn_r+nonverbal.py)
    7.MixNonverbal.py: decision stage for first time subjects in nonverbal experiment(imported by learn_nonverbal.py)
    8.MixNonverbal_r.py: decision stage for returning subjects in nonverbal experiment(imported by learn_r+nonverbal.py)
    9.Short_Verbal.py: short-delay session in verbal experiment(imported by verbal_combined_odd/even.py)
    10.Long_verbal.py: long-delay session in verbal experiment(imported by verbal_combined_odd/even.py)
    11.doodle.py: defines class Doodle which creates circle/text/sound objects and modifies their properties(important file that decreases memory use)
    12.newPoints.py: defines class NewPoins which creates coin objects and modifies their properties(imported by all files that need to draw coins)
    13.setup.py: defines the window that displays stimuli and other setups(imported by all files for experiments)
    14.variables.py: defines class Variables which defines all the variables needed(imported by all files for experiments)
    15.whitenoise_2sec.wav: the whitenoise stimuli when testing the headphones
    16.coin_echo5.wav: the sound stimuli when getting a coin