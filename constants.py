##Experiment-specific variables
#
N_BLOCKS = 10   # (Ten) 
NUMBER_RANGE = [1, 9]  # 1-9 digits i.e., [1, 9]
MIN_N_CHUNKS = 5    # (including "threat" chunks) 5 would gives us a 4:1 ratio of threat-free and threat-loaded 
THREAT_CHUNKS = 1   # sets of 1-9 digits to which the threat prob is applied (from MIN_N_CHUNKS)
SHOCK_PROB = .20

# counterbalancing of the response buttons across blocks: 'alternate' (systematically); 
# 'random' (referring to the order, but still a minimum of 50 on the left / 50 on the right)
COUNTERBALANCE = 'alternate' # TODO: 'random' option still to be coded!!! 

TARGET_COLOR = '#2EAA06' #'green'   # 'white' for CB individuals
THREAT_TARGET_COLOR = '#E34D0B' #'red'

#EXP_TYPE = 'leave'  # uncomment this to run version with without loses # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
EXP_TYPE = 'lose'  # uncomment this to run version with loses

SUBJ_ID = None # If an id number is given instead, this is used and no id number is automatically generated # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


##MAX_N_TRIALS = 20 # TAKING AS POINT OF REFERENCE THE LOWER PAY OPTION (IF CHOSEN EXCLUSIVELY) (for "Exp. Group A" condition)
EYELINKCALBEEP = False

#-------values for testing------------------
#N_BLOCKS = 3   
#NUMBER_RANGE = [1, 3]  
#MIN_N_CHUNKS = 3    
#-------------------------


FEEDBACK_VIEWING_TIME = 2000 #for img version, 2500 for video version  # This is the time (in miliseconds) participants have to look at the contingent image   
FEEDBACK_VIEWING_THRESHOLD = 20000  # This is the max time (in miliseconds) the feedback is presented

PRACTICE_REWARDS = [[20, 22], [18, 20]]

INITIAL_REWARDS = [16, 8]
REWARD_DIFFERENCE = [4, 2, 1]
P_THRESHOLD = 0.5
THRESHOLD_TYPE = "fixed"    # "fixed" for 50/50%, or "matching" for matching-law



#HIGH_CLUB_THREAT_PROB = 0.7
#LOW_CLUB_THREAT_PROB = 0.3

SPADE_THREAT_PROB = 0
#CLUB_THREAT_PROB = 1  # where 1 is 100%, 0.5 50% and 0.9 90% etc
#CLUB_THREAT_PROB = 0.7
#CLUB_THREAT_PROB = 0.3


ID_RANGE = (1000, 9999)
BEEP_THRESHOLD = 500  # Response time under which the tone is played


#SBP = 400 # "Start Button Position" simply moves the decks on the y axis (sometimes necessary to fit other screens)

#DPX = 235  # "Deck Position on Screen" simply moves the decks on the x axis 
#DPY = 50   # "Deck Position on Screen" simply moves the decks on the y axis 

SBP = 435   # Eye-lab values ("Start Button X Position")

DPX = 100   # Eye-lab values ("Deck X Position on Screen")
DPY = 0   # Eye-lab values  ("Deck Y Position on Screen")


TIMESTEP = 10 #mouse coordinate samplin rate in ms

# MAIN
DUMMYMODE = True         # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#DUMMYMODE = False # False for gaze contingent display, True for dummy mode (using mouse or joystick)
LOGFILENAME = 'eyedata' # logfilename, without path
LOGFILE = LOGFILENAME[:] # .txt; adding path before logfilename is optional; logs responses (NOT eye movements, these are stored in an EDF file!)

# DISPLAY
# used in libscreen, for the *_display functions. The values may be adjusted,
# but not the constant's names
SCREENNR = 0 # number of the screen used for displaying experiment
DISPTYPE = 'psychopy' # either 'psychopy' or 'pygame'
DISPSIZE = (1920,1080) # canvas size
#DISPSIZE = (1366,768) # canvas size
#SCREENSIZE = (53., 30.) # physical display size in cm
BGC = (0,0,0,255) # backgroundcolour
FGC = (255,255,255,255) # foregroundcolour

# EYETRACKER
# general
#TRACKERTYPE = 'dummy'      
TRACKERTYPE = 'eyelink' # either 'smi', 'eyelink' or 'dummy' (NB: if DUMMYMODE is True, trackertype will be set to dummy automatically)
EVENTDETECTION = 'native'
# EyeLink only
# FRL
# Used in libgazecon.FRL. The values may be adjusted, but not the constant names.
FRLSIZE = 200 # pixles, FRL-size
FRLDIST = 125 # distance between fixation point and FRL
FRLTYPE = 'gauss' # 'circle', 'gauss', 'ramp' or 'raisedCosine'
FRLPOS = 'center' # 'center', 'top', 'topright', 'right', 'bottomright', 'bottom', 'bottomleft', 'left', or 'topleft'
# SOUND
# defaults used in libsound. The values may be adjusted, but not the constants'
# names
SOUNDOSCILLATOR = 'sine' # 'sine', 'saw', 'square' or 'whitenoise'
SOUNDFREQUENCY = 440 # Herz
SOUNDLENGTH = 100 # milliseconds (duration)
SOUNDATTACK = 0 # milliseconds (fade-in)
SOUNDDECAY = 5 # milliseconds (fade-out)
SOUNDBUFFERSIZE = 1024 # increase if playback is choppy
SOUNDSAMPLINGFREQUENCY = 48000 # samples per second
SOUNDSAMPLESIZE = -16 # determines bit depth (negative is signed
SOUNDCHANNELS = 2 # 1 = mono, 2 = stereo

# INPUT
# used in libinput. The values may be adjusted, but not the constant names.
MOUSEBUTTONLIST = None # None for all mouse buttons; list of numbers for buttons of choice (e.g. [1,3] for buttons 1 and 3)
MOUSETIMEOUT = None # None for no timeout, or a value in milliseconds
KEYLIST = None # None for all keys; list of keynames for keys of choice (e.g. ['space','9',':'] for space, 9 and ; keys)
KEYTIMEOUT = 1 # None for no timeout, or a value in milliseconds
JOYBUTTONLIST = None # None for all joystick buttons; list of button numbers (start counting at 0) for buttons of choice (e.g. [0,3] for buttons 0 and 3 - may be reffered to as 1 and 4 in other programs)
JOYTIMEOUT = None # None for no timeout, or a value in milliseconds

# CURSOR
# Used in libgazecon.Cursor. The values may be adjusted, but not the constants' names
CURSORTYPE = 'cross' # 'rectangle', 'ellipse', 'plus' (+), 'cross' (X), 'arrow'
CURSORSIZE = 20 # pixels, either an integer value or a tuple for width and height (w,h)
CURSORCOLOUR = 'red' # colour name (e.g. 'red'), a tuple RGB-triplet (e.g. (255, 255, 255) for white or (0,0,0) for black), or a RGBA-value (e.g. (255,0,0,255) for red)
CURSORFILL = True # True for filled cursor, False for non filled cursor
CURSORPENWIDTH = 3 # cursor edge width in pixels (only if cursor is not filled)