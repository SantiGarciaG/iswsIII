from __future__ import division
from psychopy import visual
from pygaze import libscreen, libtime, libinput, libsound
import pygaze
from constants import *
import numpy as np
import random
import os

# This class implements user interface of AvoidanceExp based on psychopy API (and partly pygaze)
class ISWSExpUI:
    standard_text_heigth = 28

    # (width, height)
    start_button_size = (50, 30)
    # (x offset, y offset)
    start_button_offset = (0, 30)
    start_button_pos = (0, -DISPSIZE[1]/2 + (start_button_size[1]/2 + start_button_offset[1]))

    # (width, height)
    deadzone_size = (DISPSIZE[0], 90)
    deadzone_pos = start_button_pos
    
    # (x, y)
    target_pos = (0, -DISPSIZE[1]/4)
    target_height = 150
       
    
    # (width, height)
    respButton_size = (250, 250)

    # (x offset, y offset)
    respButton_offset = (160, 91)
    
    # (width, height)
    rating_button_size = (120, 60)
    rating_button_pos = (0, -200) # (x, y) of "base button" for offsets 
#    button_x_offsets = [0, -520, -345, -170, 0, 170, 345, 520] # For each button (0...7)
    button_x_offsets = [0, -DISPSIZE[1]/2, -DISPSIZE[1]/3, -DISPSIZE[1]/6, 
                        0, DISPSIZE[1]/6, DISPSIZE[1]/3, DISPSIZE[1]/2] 
    button_y_offsets = [-120, 0, 0, 0, 0, 0, 0, 0] # For each button (0...7)    
    
    expectancy_rating_labels = ['No sensation', 'Tickles', 'Weak', 'Mild', 
                                'Moderate', 'Tolerable', 'Strong', 'Unbearable']    
    sensation_rating_labels = ['Absent', '1', '2', '3', '4', '5', '6', ' 7']  
    
    rating_emoticon_positions = [(button_x_offsets[1], -100), 
                                 (button_x_offsets[4], -100),
                                 (button_x_offsets[7], -100)]    
    
    
    leftButton_pos = (-DISPSIZE[0]/2 + (respButton_size[0]/2 + respButton_offset[0]), 
                     DISPSIZE[1]/2 - (respButton_size[1]/2 + respButton_offset[1]))
    rightButton_pos = (DISPSIZE[0]/2 - (respButton_size[0]/2 + respButton_offset[0]), 
                     DISPSIZE[1]/2 - (respButton_size[1]/2 + respButton_offset[1]))
    

    def __init__(self):
        self.disp = libscreen.Display()
        self.win = pygaze.expdisplay
        self.mouse = libinput.Mouse(visible=True)
        
        instructions_file = 'resources/%s_instructions.txt'
        
        self.experiment_start_screen = self.intialize_message_screen(
                                instructions_file % ('experiment_start'), wrapWidth=1600)
        self.experiment_end_screen = self.initialize_experiment_end_screen(
                                instructions_file % ('experiment_end'))

        self.block_start_screen, self.block_threshold_stim = self.initialize_block_start_screen(
                                instructions_file % ('block_start'))
        self.block_end_screen = self.intialize_message_screen(
                                instructions_file % ('block_end'))
        
        self.trial_start_screen, self.start_button_rect = self.initialize_trial_start_screen()
        self.response_screen = self.initialize_response_screen()

        self.trial_end_screen = self.initialize_trial_end_screen()
        
        self.rating_screen = self.initialize_rating_screen()
        # TODO: change this to PsychoPy's sound.Sound
        self.shocker_tone = libsound.Sound(soundfile = 'resources/trigger_tone.wav')


    def intialize_message_screen(self, message_file, **kwargs):
        message_screen = libscreen.Screen()
        with open(message_file) as f:
            instructions = f.read()
        instructions_stim = visual.TextStim(self.win, text=instructions, units='pix', 
                                                    height=self.standard_text_heigth, **kwargs)
        message_screen.screen.append(instructions_stim)        
        return message_screen    
    
    def show_message_screen(self, screen):
        self.mouse.set_visible(True)
        self.disp.fill(screen)
        self.disp.show()
        self.mouse.get_clicked()
        self.mouse.set_visible(False)
        libtime.pause(500)

    def show_experiment_start_screen(self):
        self.show_message_screen(self.experiment_start_screen)

    def initialize_experiment_end_screen(self, message_file):
        experiment_end_screen = self.intialize_message_screen(message_file)
        return experiment_end_screen
    
    def show_experiment_end_screen(self):
        self.show_message_screen(self.experiment_end_screen)

    def initialize_block_start_screen(self, message_file):
        block_start_screen = self.intialize_message_screen(message_file)
        
        block_threshold_stim = visual.TextStim(self.win, pos=(0,-150), color= '#F5F500',
                                                    height=60, units='pix')
        block_start_screen.screen.append(block_threshold_stim)
    
        numeroDblock = visual.TextStim(self.win, pos=(0,-250), color= 'white',            #BBBBBB
                                                    height=60, units='pix',
                                                    text= 'Blok No: ' + str(self.blockNumero)+'/10')
        
        block_start_screen.screen.append(numeroDblock)                                      #BBBBBB
    
        return block_start_screen, block_threshold_stim, numeroDblock                       #BBBBBB

    def show_block_start_screen(self, threshold):
        self.block_threshold_stim.setText(str(threshold))
        self.show_message_screen(self.block_start_screen)

    
    def show_block_end_screen(self):
        self.show_message_screen(self.block_end_screen)

    def initialize_trial_start_screen(self):
        trial_start_screen = libscreen.Screen()
        
        start_button_rect = visual.Rect(win=self.win, pos=self.start_button_pos,
                                          width=self.start_button_size[0], 
                                            height=self.start_button_size[1],
                                            lineColor=(200,200,200), lineColorSpace='rgb255',
                                            fillColor=None, lineWidth=3)
                                                   
        start_button_text = visual.TextStim(self.win, text='Start', pos=self.start_button_pos) 
        
        trial_start_screen.screen.append(start_button_rect)
        trial_start_screen.screen.append(start_button_text)

        return trial_start_screen, start_button_rect
        
    def show_trial_start_screen(self):
        self.mouse.set_visible(True)
        self.disp.fill(self.trial_start_screen)
        self.disp.show()
        
        while not self.mouse.mouse.isPressedIn(self.start_button_rect):
            continue
        self.mouse.set_visible(False)


    def initialize_response_screen(self):
        response_screen = libscreen.Screen()
        
        self.deadzone_rect = visual.Rect(win=self.win, pos=self.deadzone_pos,
                                            width=self.deadzone_size[0], 
                                            height=self.deadzone_size[1],
                                            lineColor=None, fillColor=None)        
        
        #We're using psychopy object ImageStim  
        self.left_resp_img = visual.ImageStim(self.win, pos=self.leftButton_pos) 
        self.right_resp_img = visual.ImageStim(self.win, pos=self.rightButton_pos)

        self.left_resp_rect = visual.Rect(win=self.win, pos=self.leftButton_pos,
                                          width=self.respButton_size[0], height=self.respButton_size[1],
                                            lineColor=None, fillColor=None)
        self.right_resp_rect = visual.Rect(win=self.win, pos=self.rightButton_pos,
                                          width=self.respButton_size[0], height=self.respButton_size[1],
                                            lineColor=None, fillColor=None)
        self.target = visual.TextStim(self.win, pos=self.target_pos, height=self.target_height, 
                                      units='pix', opacity=0.0)
        
        # Here we specify the screeen onto which the stimuli are to be displayed
        response_screen.screen.append(self.deadzone_rect)        
        response_screen.screen.append(self.left_resp_img)
        response_screen.screen.append(self.right_resp_img)
        response_screen.screen.append(self.left_resp_rect)
        response_screen.screen.append(self.right_resp_rect)        
        response_screen.screen.append(self.target)

        return response_screen
    
    def show_response_screen(self, trial_info, tracker):
#        self.mouse.set_pos((DISPSIZE[0]/2, DISPSIZE[1]-(self.start_button_size[1]/2 + self.start_button_offset)))
        self.mouse.set_visible(visible=True)
        
        # This (re)sets the deck images every trial, so it doesn't show the flipped images 
        # after reading code below
        # Note that what changes is the image drawn (not the variable)
        if trial_info['is_take_left']:         
            self.left_resp_img.setImage('resources/T_button.png')        
            self.right_resp_img.setImage('resources/L_button.png')                
        else:
            self.left_resp_img.setImage('resources/L_button.png')        
            self.right_resp_img.setImage('resources/T_button.png')
                    

#        self.disp.show()
        
        while self.deadzone_rect.contains(self.mouse.mouse):
            self.disp.fill(self.response_screen)
            self.disp.show()

        self.target.setOpacity(1.0)            
        self.target.setText(text=trial_info['target_num'])
        if(trial_info['is_threat']):
            self.target.setColor(THREAT_TARGET_COLOR)
        else:
            self.target.setColor(TARGET_COLOR)            
        
            
        self.disp.fill(self.response_screen)
        self.disp.show()
        
        option_chosen = None
        response_dynamics_log = []

        trial_start_time = libtime.get_time()
        
        while option_chosen is None:
            mouse_position = self.mouse.get_pos()
            t = libtime.get_time() - trial_start_time
                
            eye_position = tracker.sample()
            pupil_size = tracker.pupil_size()
 
            response_dynamics_log.append([trial_info['subj_id'], trial_info['block_no'], 
                                          trial_info['trial_no'], str(t), 
                                            mouse_position[0], mouse_position[1], 
                                            pupil_size, eye_position[0], eye_position[1]])
            
            if self.mouse.mouse.isPressedIn(self.left_resp_rect):
                if trial_info['is_take_left']:
                    option_chosen = 'T'
                    self.left_resp_img.setImage('resources/selectedT.png') # CREATE THE STIM!!!
                else:
                    option_chosen = 'L'
                    self.left_resp_img.setImage('resources/selectedL.png')
            elif self.mouse.mouse.isPressedIn(self.right_resp_rect):
                if trial_info['is_take_left']:
                    option_chosen = 'L'
                    self.right_resp_img.setImage('resources/selectedL.png')
                else:
                    option_chosen = 'T'
                    self.right_resp_img.setImage('resources/selectedT.png')
            
            libtime.pause(TIMESTEP)        
        response_time = libtime.get_time()-trial_start_time
            
        self.target.setOpacity(0.0) 
        self.target.setText(text='')

        self.disp.fill(self.response_screen)
        self.disp.show()
        libtime.pause(300)
        
        return response_dynamics_log, option_chosen, response_time    
        
    def initialize_trial_end_screen(self):
        trial_end_screen = libscreen.Screen()
        
        self.points_earned_stim = visual.TextStim(pygaze.expdisplay, 
                                                  color='#F5F500', pos=(0,DISPSIZE[1]/2-200), 
                                             height=40)  #fontsize=height
        trial_end_screen.screen.append(self.points_earned_stim)
      
        self.accumulated_points_stim = visual.TextStim(pygaze.expdisplay, 
                                                       color='#F5F500', #pos=(0,DISPSIZE[1]/2-400), 
                                           height=30)
        trial_end_screen.screen.append(self.accumulated_points_stim)

        trial_end_instructions = visual.TextStim(pygaze.expdisplay, 
                                                 pos=(0,-DISPSIZE[1]/2+100), color='#80FF40', 
                                          text='CLICK TO CONTINUE', height=28)
        trial_end_screen.screen.append(trial_end_instructions)

        
        return trial_end_screen
                
    def show_trial_end_screen(self, points_earned, accumulated_points, trial_info):
        self.mouse.set_visible(True)

        shock_delivered = False
        rnd = random.uniform(0,1)
        if ((trial_info['is_threat'] == True) and \
            (trial_info['option_chosen'] == 'T') and \
            (rnd < SHOCK_PROB)):
            self.shocker_tone.play()                    
            shock_delivered = True
        
        outcome = 'earned'
        if points_earned < 0:
            outcome = 'lost'
        elif points_earned == 0:
            outcome = 'foregone'
            
        self.points_earned_stim.setText(text='You have %s %i points' % (outcome, trial_info['target_num']))
        self.accumulated_points_stim.setText(text='Accumulated points: %i out of %i' % \
                                            (accumulated_points, trial_info['threshold']))
        
        self.disp.fill(self.trial_end_screen)
        self.disp.show()
        
        self.mouse.get_clicked()

        libtime.pause(500)
        
        return shock_delivered
    
    def initialize_rating_screen(self, rating_type='expectancy'):
        rating_screen = libscreen.Screen()

        instruction_text_file = 'resources/%s_instruct.txt' % (rating_type)
        with open(instruction_text_file) as f:
                instructions = f.read()

        labels = []
        label_size = 18        
        
        if rating_type == 'expectancy':
            labels = self.expectancy_rating_labels
            label_size = 18
        elif rating_type == 'sensation':
            labels = self.sensation_rating_labels
            label_size = 35
            
        instructions_stim = visual.TextStim(self.win, text=instructions, units='pix', 
                                            wrapWidth=1200,#pos=(0,DISPSIZE[1]/2-300), 
                                            color='white', height=30)
        rating_screen.screen.append(instructions_stim)

        self.rating_buttons = []        
        
        for i, label in enumerate(labels):
            button = visual.Rect(win=pygaze.expdisplay, 
                    pos=(self.rating_button_pos[0]+self.button_x_offsets[i], 
                         self.rating_button_pos[1]+self.button_y_offsets[i]),
                    width=self.rating_button_size[0], height=self.rating_button_size[1],
                    lineColor=(200,200,200), lineWidth=3, 
                    lineColorSpace='rgb255', fillColor=None)
            button_text = visual.TextStim(win=pygaze.expdisplay, text=labels[i], height=18,
                      pos=(self.rating_button_pos[0]+self.button_x_offsets[i], 
                           self.rating_button_pos[1]+self.button_y_offsets[i]))
            self.rating_buttons.append(button)
            
            rating_screen.screen.append(button)
            rating_screen.screen.append(button_text)

        happyFace_img = visual.ImageStim(pygaze.expdisplay, 
                                         image='resources/happyFace.png', 
                                         pos=self.rating_emoticon_positions[0])
        rating_screen.screen.append(happyFace_img)                                          
        
        neutralFace_img = visual.ImageStim(pygaze.expdisplay, 
                                           image='resources/neutralFace.png', 
                                           pos=self.rating_emoticon_positions[1])
        rating_screen.screen.append(neutralFace_img)  

        scaredFace_img = visual.ImageStim(pygaze.expdisplay, 
                                          image='resources/scaredFace.png', 
                                          pos=self.rating_emoticon_positions[2])
        rating_screen.screen.append(scaredFace_img)   

        return rating_screen

    def show_rating_screen(self, rating_type='expectancy'):
        self.mouse.set_visible(True)
        
        self.disp.fill(self.rating_screen)
        self.disp.show()        
        
        while(True):
            for i, button in enumerate(self.rating_buttons):
                if self.mouse.mouse.isPressedIn(button):
                    return i
            self.disp.fill(self.rating_screen)
            self.disp.show()
            

    def close(self):
        self.disp.close()
           