from constants import *
import random, csv
import numpy as np
from datetime import datetime
import os

# This class implements data access layer of AvoidanceExp (primarily, logging).
# All data outputs are stored in tab-delimited format in txt files in 'data' folder
class ISWSExpDA:                                     
    # stubs for experiment-level variables
    exp_info = {}
    
    def __init__(self, subj_id=None, exp_type='lose'):
        self.exp_info['exp_type'] = exp_type
        
        if subj_id is None:
            self.exp_info['subj_id'] = self.generate_subj_id()        
        self.exp_info['start_time'] = datetime.strftime(datetime.now(), '%b_%d_%Y_%H_%M_%S')
        self.initialize_log()
    
    def initialize_log(self):
        log_path = 'data/%s'
        log_name = log_path + '/' + self.exp_info['subj_id'] + '_' + \
                self.exp_info['start_time'] + '_%s_%s.txt'

        self.response_dynamics_log_file = log_name % ('dynamics', 'dynamics', 
                                                      self.exp_info['exp_type'])        
        self.choices_log_file = log_name % ('choices', 'choices', 
                                            self.exp_info['exp_type'])
        self.blocks_log_file = log_name % ('blocks', 'blocks', 
                                            self.exp_info['exp_type'])
        
        if not os.path.exists(log_path % 'dynamics'):
            os.makedirs(log_path % 'dynamics')
        if not os.path.exists(log_path % 'choices'):
            os.makedirs(log_path % 'choices')
        if not os.path.exists(log_path % 'blocks'):
            os.makedirs(log_path % 'blocks')            
            
        with open(self.response_dynamics_log_file, 'ab+') as fp:
            writer = csv.writer(fp, delimiter = '\t')
            writer.writerow(['subj_id', 'block_no', 'trial_no', 'timestamp', 
                             'mouse_x', 'mouse_y', 'pupil_size', 'eye_x', 'eye_y'])
        
        with open(self.choices_log_file, 'ab+') as fp:
            writer = csv.writer(fp, delimiter = '\t')
            writer.writerow(['subj_id', 'block_no', 'trial_no', 'is_take_left', 'target', 
                             'is_threat', 'option_chosen', 'points_earned', 'shock_delivered',
                             'response_time', 'idle_time', 'shock_prob'])
                             
        with open(self.blocks_log_file, 'ab+') as fp:
            writer = csv.writer(fp, delimiter = '\t')
            writer.writerow(['subj_id', 'block_no', 'expectancy_rating', 'accumulated_points']) #'sensation_rating'
                             
                             
    def write_trial_log(self, response_dynamics_log, choice_info): 
        with open(self.response_dynamics_log_file, 'ab+') as fp:
            writer = csv.writer(fp, delimiter = '\t')
            writer.writerows(response_dynamics_log)
            
        with open(self.choices_log_file, 'ab+') as fp:
            writer = csv.writer(fp, delimiter = '\t')
            writer.writerow(choice_info)
    
    def write_block_log(self, block_info):
        with open(self.blocks_log_file, 'ab+') as fp:
            writer = csv.writer(fp, delimiter = '\t')
            writer.writerow(block_info)
            
    # this function generates new random subject id if one is not provided in constants.py
    # (which is only the case for experiments requiring multiple sessions with each subject)
    def generate_subj_id(self):
        file_name = 'existing_subj_ids.txt'
        try:
            f = open(file_name, 'r')
        except IOError:
            with open(file_name, 'w') as f:
                f.write('666\n')
    
        if SUBJ_ID is None:
            existing_subj_ids = np.loadtxt(file_name)
            subj_id = int(random.uniform(ID_RANGE[0], ID_RANGE[1]))
            while subj_id in existing_subj_ids:
                subj_id = int(random.uniform(ID_RANGE[0], ID_RANGE[1]))
    
            with open(file_name, 'ab+') as fp:
#                fp.write(str(subj_id)+'\n')
                writer = csv.writer(fp, delimiter = '\t')
                writer.writerow([str(subj_id)])
        else:
            subj_id = SUBJ_ID
        return str(subj_id)