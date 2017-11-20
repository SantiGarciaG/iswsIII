from pygaze import eyetracker
from constants import *
import os

# This class wraps eye-tracking functions of PyGaze
class ISWSExpET:   
    def __init__(self, user_interface, subj_id, exp_type):
        self.user_interface = user_interface
 
        #So before we index and 'a' or and 'b' to the .edf (see commented code below) -perhaps we could shoce this based on exp_type   
        # a is 'lose' and b is 'leave'
        data_file_suffix = 'a' if exp_type=='lose' else 'b'
        data_file = str(subj_id)+data_file_suffix
        if os.path.isfile(data_file+'.edf'):
            data_file = data_file + '_'

        self.tracker = eyetracker.EyeTracker(self.user_interface.disp, data_file=data_file+'.edf')

    def calibrate(self):
        # TODO: instead of calling pygaze.calibrate, try using pylink.getEYELINK().doTrackerSetup()
        # look also at pylink.getEYELINK().enableAutoCalibration()
        self.user_interface.mouse.set_visible(False)
        self.tracker.calibrate()
        self.user_interface.mouse.set_visible(True)
    
    def sample(self):
        return self.tracker.sample()
    
    def pupil_size(self):
        return 0 if DUMMYMODE else self.tracker.pupil_size()
    
    def close(self):
        self.tracker.close()
                   
    def start_recording(self, start_message):                        
        self.tracker.start_recording()
        self.tracker.status_msg(start_message)
        self.tracker.log(start_message)
        
    def stop_recording(self):
        self.tracker.stop_recording()
        
    def correct_drift(self):
        if not DUMMYMODE:
            self.user_interface.mouse.set_visible(False)
            checked = False
            while not checked:
                checked = self.tracker.drift_correction(fix_triggered=True)