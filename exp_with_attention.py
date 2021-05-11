import os
import pickle
import sys
from factory.environment import Env
from factory.vehicles import *

def set_follower(lane_id, model_type, model_name, driver_type):
    config = {
             "model_config": {
                 "learning_rate": 1e-3,
                "batch_size": 50,
                },
                "exp_id": "NA",
                "Note": ""}

    exp_dir = './models/experiments/'+model_name+'/model'

    if  model_type == 'driver_model':
        from models.core.driver_model import  Encoder
        model = Encoder(config, model_use='inference')
        model.load_weights(exp_dir).expect_partial()
        follower = NeurIDM(id='neural', lane_id=lane_id, x=50, v=20,
                        driver_type=driver_type, model=model)

    # follower.scaler = scaler
    return follower


env = Env()

model_type='driver_model'
model_name='driver_model'
leader = LeadVehicle(id='leader', lane_id=1, x=100, v=20)
merger = MergeVehicle(id='merger', lane_id=2, x=70, v=20)

neural_IDM = set_follower(lane_id=1, model_type=model_type, model_name=model_name,\
                                                            driver_type='normal_idm')

# follower_IDM1 = IDMVehicle(id='aggressive_idm', lane_id=3, x=40, v=20, driver_type='aggressive_idm')
follower_IDM = IDMVehicle(id='normal_idm', lane_id=1, x=50, v=20, driver_type='normal_idm')
# follower_IDM = IDMVehicle(id='timid_idm', lane_id=1, x=40, v=20, driver_type='timid_idm')

# follower_IDM.lead_vehicle = leader1

neural_IDM.lead_vehicle = leader
neural_IDM.attend_veh = leader
neural_IDM.merge_vehicle = merger
follower_IDM.lead_vehicle = leader

env.vehicles = [
                neural_IDM,
                follower_IDM,
                leader,
                merger]

env.render(model_type)
for i in range(5000):
    env.step()
    env.render()
    if env.elapsed_time > 0 and  round(env.elapsed_time, 1) % 10 == 0:
        answer = input('Continue?')
        if answer == 'n':
            sys.exit()
