from pygaze import libtime
from constants import *
import numpy as np
import random
from ui.isws_exp_ui import ISWSExpUI
from da.isws_exp_da import ISWSExpDA
from et.isws_exp_et import ISWSExpET

# ISWSExp class provides high-level functions controlling the flow 
# of the experiment. To run the experiment, just create the instance of the class and call run_exp()
class ISWSExp:    
    def __init__(self, subj_id=None, exp_type='high'):
        self.user_interface = ISWSExpUI()  
        self.data_access = ISWSExpDA(subj_id, exp_type)
        self.eye_tracker = ISWSExpET(user_interface=self.user_interface, 
                                 subj_id=self.data_access.exp_info['subj_id'], exp_type=exp_type)
        self.exp_info = self.data_access.exp_info
           
    def run_exp(self, test_mode=False):
        libtime.expstart()
        self.user_interface.show_experiment_start_screen()
#        self.user_interface.show_practice_start_screen()

        self.blockNumero = 0                                                                    # BBBBBBBBB 
        
        # counterbalance first block response area location across participants        
        is_take_left = random.choice([False,True])  
            
        for i in range(1, N_BLOCKS+1):
            # Taking club-deck as reference, 
            # REMEMBER: rewards[0] is reward for T; rewards[1] is L         
            block_info = self.run_block(i, is_take_left=is_take_left)
            
            self.data_access.write_block_log(block_info)
                    
            # Here the value is changed in every block / iteration of 'for' loop
            # So it starts with e.g. is_take_left = True and changed after the next iteration to = False, 
            # and after the second iteration the False is Not more (i.e., True)
            # TODO: implement different ways of counterbalancing (alternating vs. random)
            if COUNTERBALANCE == 'alternate':
                is_take_left = not is_take_left
            else:
                is_take_left = not is_take_left
        self.eye_tracker.close()    
        libtime.pause(500)
        
        self.user_interface.show_experiment_end_screen()
        
        # With this function ALL of the screens are ended
        self.user_interface.close()
        
    #------ WE CREATE A FUNCTION THAT WILL RUN THE CONTENTS OF A BLOCK ----------             
    def run_block(self, block_no, is_take_left=True):
        expectancy_rating = self.user_interface.show_rating_screen(rating_type='expectancy')
        
        threshold = (MIN_N_CHUNKS*(NUMBER_RANGE[1]+NUMBER_RANGE[0])* \
                        (NUMBER_RANGE[1]-NUMBER_RANGE[0]+1)/2)
        
        # TODO: generate numbers (incl threat/no_threat mark) for all trials in the block
        target_numbers = self.prepare_target_numbers()
        
        self.eye_tracker.calibrate()
        
        # The threshold is set by taking the minimum rewards and multiplying it by the value 
        # in the constant MAX_N_TRIALS
        self.user_interface.show_block_start_screen(threshold=threshold)
        
        # We create the variable that will contain the points
        accumulated_points = 0
        
        trial_no = 1
        # This is the loop for proceeding to the next block
        while (accumulated_points < threshold) & (len(target_numbers)>0):
            target_num, is_threat = target_numbers.pop(0)
            points_earned, response_dynamics_log, choice_info = \
                    self.run_trial(target_num, is_threat, accumulated_points, threshold, 
                                   block_no, trial_no, is_take_left)
                                   
            self.data_access.write_trial_log(response_dynamics_log, choice_info)
                
            accumulated_points += points_earned
            # We update the variable adding 1 per trial iteration            
            trial_no += 1

        self.blockNumero += 1                                                                 # BBBBBBBBB
        
        # uncomment this to get sensation rating
#        sensation_rating = self.user_interface.show_rating_screen(rating_type='sensation')
        
        block_info = [self.exp_info['subj_id'], block_no, expectancy_rating, accumulated_points]#sensation_rating
        # We show the interblock message after each block except for the last one
        if block_no < N_BLOCKS:
            self.user_interface.show_block_end_screen()
        return block_info
    
    def prepare_target_numbers(self):
        is_threat_values = np.concatenate([np.repeat(True, THREAT_CHUNKS), 
                                           np.repeat(False, MIN_N_CHUNKS-THREAT_CHUNKS)])
        numbers = np.arange(NUMBER_RANGE[0], NUMBER_RANGE[1]+1)
        
        targets_base = [(n, is_threat) for n in numbers for is_threat in is_threat_values]
        random.shuffle(targets_base)
        
        targets_extra = [(n, is_threat) for n in numbers for is_threat in is_threat_values]
        random.shuffle(targets_extra)
        
        targets = targets_base + targets_extra
                         
        # if there are three consecutive repetitions of same number...
        shuffled_numbers = [number for (number, is_threat) in targets]
        is_three_consecutive = np.any(np.diff(np.where(np.diff(shuffled_numbers) == 0)[0])==1)
        # ... do the whole thing again recursively
        if(is_three_consecutive):
            targets = self.prepare_target_numbers()           
                
        return targets
        
    def run_trial(self, target_num, is_threat, accumulated_points, threshold, 
                                   block_no, trial_no, is_take_left=True):
        trial_info = {'exp_type': self.exp_info['exp_type'],
                      'subj_id': self.exp_info['subj_id'],                      
                      'block_no': block_no,
                      'trial_no': trial_no,
                      'target_num': target_num,
                      'is_threat': is_threat,
                      'is_take_left': is_take_left,
                      'threshold': threshold}
      
        self.user_interface.show_trial_start_screen()
        self.eye_tracker.start_recording(start_message = 'subject %s block %d trial %d' % 
                                            (self.exp_info['subj_id'], block_no, trial_no))

        response_dynamics_log, option_chosen, response_time = self.user_interface.show_response_screen(                                                                    
                                                                    trial_info=trial_info,
                                                                    tracker=self.eye_tracker)
        self.eye_tracker.stop_recording()

        trial_info['option_chosen'] = option_chosen
        points_earned = 0
        # this if is for the experimental blocks
        if option_chosen == 'T':
            points_earned = target_num
        elif option_chosen == 'L':
            if trial_info['exp_type']=='lose':
                points_earned = -target_num
            elif trial_info['exp_type']=='leave':
                points_earned = 0
        
        shock_delivered = self.user_interface.show_trial_end_screen(points_earned, 
                                                accumulated_points+points_earned, trial_info)

        choice_info = [self.exp_info['subj_id'], block_no, trial_no, is_take_left, 
                           target_num, is_threat, option_chosen, points_earned, 
                           shock_delivered, response_time, SHOCK_PROB]

#        # drift correction after every fifth trial
        if trial_no % 10 == 0:
            self.eye_tracker.correct_drift()        
        
        return points_earned, response_dynamics_log, choice_info


isws_exp = ISWSExp(exp_type=EXP_TYPE)
isws_exp.run_exp()