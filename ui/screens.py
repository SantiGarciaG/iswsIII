from psychopy import visual
from pygaze import libscreen, libtime
from constants import *

class BaseScreen(object):
    def __init__(self, win, disp, mouse):
        self.disp = disp
        self.mouse = mouse
        self.screen = libscreen.Screen()
    
    def show(self):
        self.disp.fill(self.screen)
        self.disp.show()
        
class TrialEndScreen(BaseScreen):
    def __init__(self, win, disp, mouse):
        
        super(TrialEndScreen, self).__init__(win, disp, mouse)
    
    def show(self):
        super(TrialEndScreen, self).show()
    