import matplotlib.pyplot as plt
from importlib import reload
import sys
import data_generator
reload(data_generator)
from data_generator import DataGenerator
reload(plt)
import matplotlib.pyplot as plt

import numpy as np
np.set_printoptions(suppress=True)

import highway
reload(highway)
from highway import Env

import time

config = {'lanes_n':6,
        'lane_width':3.75, # m
        'lane_length':600 # m
        }
env = Env(config)
# viewer = Viewer(config)
data_config = {
                # 'future_scaeq_length':40,
                'history_scaeq_length':20,
                'env_steps_n':2000,
                'model_type':'belief_net'
                }
data_gen = DataGenerator(env, data_config)
features_origin = data_gen.prep_data()
# features_origin.shape
# features_origin = features_origin[features_origin[:, indxs['m_veh_exists']] == 1]
# features_origin[:, indxs['em_delta_y']].max()
features_origin.shape
features_origin.shape

# %%
indxs = {}
feature_names = [
         'episode_id', 'time_step',
         'e_veh_id', 'f_veh_id', 'm_veh_id',
         'e_veh_decision', 'f_veh_exists', 'm_veh_exists',
         'aggressiveness', 'e_veh_att',
         'e_veh_glob_x', 'f_veh_glob_x', 'm_veh_glob_x',
         'e_veh_speed', 'f_veh_speed', 'm_veh_speed',
         'e_veh_action', 'f_veh_action', 'm_veh_action',
         'ef_delta_v', 'ef_delta_x', 'em_delta_v', 'em_delta_x', 'em_delta_y']

index = 0
for item_name in feature_names:
    indxs[item_name] = index
    index += 1
indxs['e_veh_att']
# %%
np.where((features_origin[:, indxs['m_veh_id']] != -1)
         & (features_origin[:, indxs['m_veh_id']] == features_origin[:, indxs['f_veh_id']]))
# features_origin[2938, :]
# %%

np.where((features_origin[:, indxs['time_step']] == 408) & \
                        (features_origin[:, indxs['e_veh_id']] == 42))
features_origin[324, indxs['e_veh_action']]
# %%
episode_info = []
episs = np.unique(features_origin[:, 0])
for epis in episs:
    episode_info.append([epis, np.where(features_origin[:, 0] == epis)[0].shape[0]])
episode_info
# %%
features_origin[(features_origin[:, indxs['f_veh_id']] != -1) & \
                    (features_origin[:, indxs['e_veh_decision']] == 1)].shape

# %%
features_origin[(features_origin[:, indxs['e_veh_att']] == 1) & \
                    (features_origin[:, indxs['m_veh_exists']] == 0) ].shape
# %%
features_origin[(features_origin[:, indxs['em_delta_y']] == 0) & \
                    (features_origin[:, indxs['e_veh_att']] == 1) ].shape
# %%
features_origin[(features_origin[:, indxs['e_veh_att']] == 0) & \
                    (features_origin[:, indxs['m_veh_exists']] == 1) ].shape

# %%
features_origin[(features_origin[:, indxs['m_veh_id']] == -1) & \
                    (features_origin[:, indxs['f_veh_id']] == -1) ].shape
features_origin[(features_origin[:, indxs['m_veh_exists']] == 0) & \
                    (features_origin[:, indxs['f_veh_exists']] == 0) ].shape
# %%
features_origin[(features_origin[:, indxs['m_veh_id']] == -1) & \
                    (features_origin[:, indxs['e_veh_att']] == 1) ].shape
# %%
features_origin[(features_origin[:, indxs['em_delta_y']] < 1.5) & \
                    (features_origin[:, indxs['e_veh_att']] == 0) ].shape

# %%
features_origin[(features_origin[:, indxs['aggressiveness']] == 1.) & \
                    (features_origin[:, indxs['e_veh_att']] == 1) ].shape
# %%

features_origin[(features_origin[:, indxs['aggressiveness']] < 0.5) & \
                    (features_origin[:, indxs['e_veh_att']] == 1) ].shape
# %%

features_origin[(features_origin[:, indxs['aggressiveness']] > 0.5) & \
                    (features_origin[:, indxs['e_veh_att']] == 1) ].shape
# %%
features_origin[(features_origin[:, indxs['m_veh_exists']] == 1)].shape
features_origin[(features_origin[:, indxs['e_veh_att']] == 1)].shape
features_origin[(features_origin[:, indxs['e_veh_att']] == 1)].shape
features_origin[(features_origin[:, indxs['f_veh_exists']] == 0)].shape
features_origin[(features_origin[:, indxs['f_veh_exists']] == 0)]
features_origin[(features_origin[:, indxs['f_veh_exists']] == 0)]
features_origin[features_origin[:, indxs['e_veh_id']] == 58 %]
# %%
features_origin[(features_origin[:, indxs['e_veh_id']] == 58) & \
                    (features_origin[:, indxs['aggressiveness']] == 0.5)]
# %%
features_origin[:, indxs['m_veh_speed']].mean()
features_origin[:, indxs['e_veh_action']].std()
features_origin[:, indxs['e_veh_action']].std()
features_origin[:, indxs['e_veh_action']].std()
future_e_veh_a[:, :, -1].std()
future_e_veh_a[:, :, -1].mean()
features_origin[:, indxs['e_veh_action']].mean()
# %%

"""
Driver model - neural idm
"""
features = features_origin.copy()
# features = features[features[:, indxs['aggressiveness']] == 0.5]
# features[features[:, indxs['m_veh_exists']] == 1].shape
features, dummy_value_set = data_gen.fill_missing_values(features)
features_scaled, scaler = data_gen.scale_data(features)
history_future_seqs = data_gen.sequence(features, 20, 40)
history_future_seqs_scaled = data_gen.sequence(features_scaled, 20, 40)
data_arrays = data_gen.split_data(history_future_seqs, history_future_seqs_scaled)
# data_arrays = [data_array[:5000, :, :] for data_array in data_arrays]

history_future_usc, history_sca, future_sca, future_idm_s, \
                future_m_veh_a, future_e_veh_a = data_arrays
future_m_veh_a[future_m_veh_a[:, :, 2] == 1]

# data_arrays = [np.nan_to_num(data_array, 0) for data_array in data_arrays]
future_idm_s[0:10, 0, :]
future_m_veh_a.shape
future_m_veh_a.shape
np.squeeze(future_m_veh_a).shape
# %%

"""
Driver model - lstm
"""
history_future_seqs = data_gen.sequence(features, 20, 1)
history_future_seqs_scaled = data_gen.sequence(features_scaled, 20, 1)
data_arrays = data_gen.split_data(history_future_seqs, history_future_seqs_scaled)
# data_arrays = [data_array[:5000, :, :] for data_array in data_arrays]

history_future_usc, history_sca, future_sca, future_idm_s, \
                future_m_veh_a, future_e_veh_a = data_arrays

future_e_veh_a.shape
# %%
"""
Driver model - mlp
"""
history_future_seqs = data_gen.sequence(features, 1, 1)
history_future_seqs_scaled = data_gen.sequence(features_scaled, 1, 1)
data_arrays = data_gen.split_data(history_future_seqs, history_future_seqs_scaled)
# data_arrays = [data_array[:5000, :, :] for data_array in data_arrays]

history_future_usc, history_sca, future_sca, future_idm_s, \
                future_m_veh_a, future_e_veh_a = data_arrays

future_e_veh_a.shape

history_sca.flatten().shape
future_e_veh_a[0]
history_future_usc[0]


# %%
# """
# BALANCE DATA
# """
# history_future_usc, history_sca, future_sca, future_idm_s, future_m_veh_a, future_e_veh_a = data_arrays
# cond = (history_sca[:, :, -1] == 1).any(axis=1)
# data_arrays = [np.append(data_array, data_array[cond], axis=0) for data_array in data_arrays]
# # _ = plt.hist(history_sca[:, :, -1].flatten(), bins=150)
# balance_value = np.count_nonzero((history_sca[:, :, -1] == 1).any(axis=1))/\
# np.count_nonzero((history_sca[:, :, -1] != 1).any(axis=1))
# print(balance_value)

# %%
np.count_nonzero((history_future_usc[:, :, -3] == 1).any(axis=1))/history_future_usc.shape[0]

a = np.zeros([100, 20, 3])
a[34:36, 3:5, 1] = 1
(a[:, :, 1] == 1).any(axis=1).shape

# %%
"""
For debugging - all samples
"""

for i in range(10000000):
# for i in range(1000):
    aggressiveness = history_future_usc[i, 0, -1]
    if aggressiveness == 0:
        desired_v = 19.4
        desired_tgap = 2
        min_jamx = 4
        max_act = 0.8
        min_act = 1
    elif aggressiveness == 0.5:
        desired_v = 24.7
        desired_tgap = 1.5
        min_jamx = 2
        max_act = 1.4
        min_act = 2
    elif aggressiveness == 1:
        desired_v = 30
        desired_tgap = 1
        min_jamx = 0
        max_act = 2
        min_act = 3

    vel = future_idm_s[i, :, 2]
    f_veh_v = future_idm_s[i, :, 3]
    m_veh_v = future_idm_s[i, :, 4]
    e_veh_glob_x = future_idm_s[i, :, 5]
    f_veh_glob_x = future_idm_s[i, :, 6]
    m_veh_glob_x = future_idm_s[i, :, 7]
    f_veh_exists = future_idm_s[i, :, -2]
    m_veh_exists = future_idm_s[i, :, -1]

    dv = (vel - f_veh_v)*f_veh_exists
    dx = (f_veh_glob_x - e_veh_glob_x)*f_veh_exists + 1000*(1-f_veh_exists)

    desired_gap = min_jamx + \
    np.clip(desired_tgap*vel+(vel*dv)/(2*np.sqrt(max_act*min_act)), a_min=0,a_max=None)

    ef_act = max_act*(1-(vel/desired_v)**4-(desired_gap/dx)**2)
    ef_act = np.clip(ef_act, -3, 3)

    dv = (vel - m_veh_v)*m_veh_exists
    dx = (m_veh_glob_x - e_veh_glob_x)*m_veh_exists + 1000*(1-m_veh_exists)
    desired_gap = min_jamx + \
    np.clip(desired_tgap*vel+(vel*dv)/(2*np.sqrt(max_act*min_act)), a_min=0,a_max=None)

    em_act = max_act*(1-(vel/desired_v)**4-(desired_gap/dx)**2)
    em_act = np.clip(em_act, -3, 3)
    att_scores = future_idm_s[i, :, -3]
    act = (1-att_scores)*ef_act + att_scores*em_act
    # features = features[features[:, 6]==0] # merger exists
    loss = abs(act-future_e_veh_a[i, :, -1])
    if not loss.max() < 0.001:
        print('index:  ', i)
        print(loss.max())
#
# plt.plot(future_e_veh_a[i, :, -1])
# plt.plot(act)
# %%

"""
For debugging - single sample
"""
# (array([ 2938,  3806,  5163,  7907,  9053,  9428, 10068, 11380, 21039,
#         23600, 24103, 27184, 33040, 34718, 36181, 39556, 41057, 43373,
#         44243, 45802, 46875, 47244, 51806, 53337, 53914, 60293, 60831,
#         63801, 64256, 64347, 66563, 67068, 68246, 72719, 75622, 78407,
#         80217, 80345, 81882, 82192, 86496], dtype=int64),)

i = 26075
history_future_usc[i, 0, :]
aggressiveness = history_future_usc[i, 0, -1]
if aggressiveness == 0:
    desired_v = 19.4
    desired_tgap = 2
    min_jamx = 4
    max_act = 0.8
    min_act = 1
elif aggressiveness == 0.5:
    desired_v = 24.7
    desired_tgap = 1.5
    min_jamx = 2
    max_act = 1.4
    min_act = 2
elif aggressiveness == 1:
    desired_v = 30
    desired_tgap = 1
    min_jamx = 0
    max_act = 2
    min_act = 3
#
# desired_v = 20.81
# desired_tgap = 2
# min_jamx = 3.1
# max_act = 0.8
# min_act = 1.3
vel = future_idm_s[i, :, 2]
f_veh_v = future_idm_s[i, :, 3]
m_veh_v = future_idm_s[i, :, 4]
e_veh_glob_x = future_idm_s[i, :, 5]
f_veh_glob_x = future_idm_s[i, :, 6]
m_veh_glob_x = future_idm_s[i, :, 7]
f_veh_exists = future_idm_s[i, :, -2]
m_veh_exists = future_idm_s[i, :, -1]

dv = (vel - f_veh_v)*f_veh_exists
dx = (f_veh_glob_x - e_veh_glob_x)*f_veh_exists + 1000*(1-f_veh_exists)
desired_gap = min_jamx + \
np.clip(desired_tgap*vel+(vel*dv)/(2*np.sqrt(max_act*min_act)), a_min=0,a_max=None)
ef_act = max_act*(1-(vel/desired_v)**4-(desired_gap/dx)**2)
ef_act = np.clip(ef_act, -3, 3)


dv = (vel - m_veh_v)*m_veh_exists
dx = (m_veh_glob_x - e_veh_glob_x)*m_veh_exists + 1000*(1-m_veh_exists)
desired_gap = min_jamx + \
np.clip(desired_tgap*vel+(vel*dv)/(2*np.sqrt(max_act*min_act)), a_min=0,a_max=None)
em_act = max_act*(1-(vel/desired_v)**4-(desired_gap/dx)**2)
em_act = np.clip(em_act, -3, 3)

att_scores = future_idm_s[i, :, -3].copy()
future_idm_s[i, :, :]


# att_scores+=1
# att_scores[0] = 1
history_future_usc[i, :, :]
act = (1-att_scores)*ef_act + att_scores*em_act
future_e_veh_a[i, :, -1].shape
plt.plot(future_e_veh_a[i, :, -1], color='red')
plt.plot(act)

# %%

"""
EPISODE EVALUATION
"""
# %%
np.unique(features[features[:, 2] == 19][:, 0])
# features[features[:, 2] == 34]
veh_arr[:, -1]
veh_arr[:, indxs['time_step']]
plt.scatter(veh_arr[:, indxs['time_step']], veh_arr[:, indxs['time_step']])
np.where(veh_arr[:, indxs['e_veh_att']] == 1)
veh_arr[:, indxs['f_veh_id']]
veh_arr[:, indxs['em_delta_y']][13]
veh_arr[:, indxs['em_delta_y']][85+39]
future_m_veh_a[37964, :, -1]
history_future_usc, history_sca, future_sca, future_idm_s, \
                future_m_veh_a, future_e_veh_a = data_arrays
history_future_usc[37964, :, -6]

veh_arr[:, indxs['e_veh_decision']]
veh_arr[:, indxs['m_veh_id']]
veh_arr[:, indxs['f_veh_id']]
veh_arr[:, indxs['e_veh_id']]
veh_arr[:, indxs['m_veh_action']]
# veh_arr[:, indxs['e_veh_att']][25]
# %%
veh_arr = features[features[:, 0] == 39]
time_snap_start = veh_arr[0, 1]
time_snap_1 = 971
time_snap_2 = time_snap_1+40
for i in range(veh_arr.shape[-1]):
    plt.figure(figsize=(4, 4))
    plt.plot(veh_arr[:, 1], veh_arr[:, i])
    # plt.plot([time_snap_1, time_snap_1],[veh_arr[:, i].min(), veh_arr[:, i].max()])
    # plt.plot([time_snap_2, time_snap_2],[veh_arr[:, i].min(), veh_arr[:, i].max()])
    plt.plot([time_snap_start, time_snap_start],[veh_arr[:, i].min(), veh_arr[:, i].max()])
    plt.title(feature_names[i])
    plt.grid()



# %%
a = []
def add_to_list(this_list):
    this_list.append(5)
add_to_list(a)
a
# %%
round(0.111, 1)
"""
RAW FEATURE ANAL
"""
for i in range(features.shape[-1]):
    plt.figure(figsize=(4, 4))
    _ = plt.hist(features[:, i], bins=150)
    plt.title(feature_names[i])
    plt.grid()

# %%


col_names = ['episode_id', 'time_step',
        'e_veh_speed', 'f_veh_speed', 'm_veh_speed',
        'ef_delta_v', 'ef_delta_x', 'em_delta_v', 'em_delta_x',
        'em_delta_y', 'f_veh_exists', 'm_veh_exists']

for i in range(future_sca.shape[-1]):
    plt.figure(figsize=(3, 3))
    to_plot = history_sca[:, :, i].flatten()
    _ = plt.hist(to_plot, bins=150)
    plt.title(col_names[i])
    # plt.grid()
# %%
col_names = ['episode_id', 'time_step', 'em_delta_y', 'm_veh_action',\
                                            'f_veh_exists', 'm_veh_exists']
for i in range(future_m_veh_a.shape[-1]):
    plt.figure(figsize=(3, 3))
    to_plot = future_m_veh_a[:, :, i].flatten()
    _ = plt.hist(to_plot, bins=150)
    plt.title(col_names[i])
# %%

col_names = ['episode_id', 'time_step', 'e_veh_id',
        'e_veh_speed', 'f_veh_speed', 'm_veh_speed',
        'e_veh_action', 'f_veh_action', 'm_veh_action',
        'ef_delta_v', 'ef_delta_x', 'em_delta_v', 'em_delta_x',
        'em_delta_y', 'e_veh_att', 'f_veh_exists', 'm_veh_exists',
        'e_veh_decision', 'aggressiveness']
# np.count_nonzero(history_future_usc[:, :, 6] == 0)

for i in range(history_future_usc.shape[-1]):
    plt.figure(figsize=(3, 3))
    to_plot = history_future_usc[:, :, i].flatten()
    _ = plt.hist(to_plot, bins=150)
    plt.title(col_names[i])
    # plt.grid()
# %%


# %%

col_names = ['episode_id', 'time_step',
                'e_veh_speed', 'f_veh_speed', 'm_veh_speed',
                'e_veh_glob_x', 'f_veh_glob_x', 'm_veh_glob_x']
# type(future_idm_s[i, 0, -3])

for i in range(future_idm_s.shape[-1]):
    plt.figure(figsize=(3, 3))
    _ = plt.hist(future_idm_s[:, -1, i], bins=150)
    plt.title(col_names[i])
    plt.grid()
# %%

# %%
config = {
 "model_config": {
     "learning_rate": 1e-3,
    "batch_size": 256,
    },
    "exp_id": "NA",
    "Note": ""
}

class Trainer():
    def __init__(self, training_data, model_type):
        self.model = None
        self.model_type = model_type

        self.train_mseloss = []
        self.train_att_klloss = []
        self.train_idm_klloss = []

        self.test_mseloss = []
        self.test_att_klloss = []
        self.test_idm_klloss = []
        self.epoch_count = 0
        self.initiate_model()
        self.prep_data(training_data)

    def initiate_model(self, model_type=None):
        if self.model_type == 'driver_model':
            from models.core import driver_model
            reload(driver_model)
            from models.core.driver_model import  NeurIDMModel
            self.model = NeurIDMModel(config)

        elif self.model_type == 'lstm_model':
            from models.core import lstm
            reload(lstm)
            from models.core.lstm import  Encoder
            self.model = Encoder(config)

        elif self.model_type == 'mlp_model':
            from models.core import mlp
            reload(mlp)
            from models.core.mlp import  MLP
            self.model = MLP(config)

    def prep_data(self, training_data):
        all_epis = np.unique(training_data[0][:, 0, 0])
        np.random.seed(2021)
        np.random.shuffle(all_epis)
        train_epis = all_epis[:int(len(all_epis)*0.8)]
        val_epis = np.setdiff1d(all_epis, train_epis)
        train_indxs = np.where(training_data[0][:, 0:1, 0] == train_epis)[0]
        val_indxs = np.where(training_data[0][:, 0:1, 0] == val_epis)[0]

        _, history_sca, future_sca, future_idm_s,\
                    future_m_veh_a, future_e_veh_a = training_data

        if self.model_type == 'driver_model':

            self.train_input = [history_sca[train_indxs, :, 2:],
                        future_sca[train_indxs, :, 2:],
                        future_idm_s[train_indxs, :, 2:],
                        future_m_veh_a[train_indxs, :, 2:],
                        future_e_veh_a[train_indxs, :, 2:]]

            self.val_input = [history_sca[val_indxs, :, 2:],
                        future_sca[val_indxs, :, 2:],
                        future_idm_s[val_indxs, :, 2:],
                        future_m_veh_a[val_indxs, :, 2:],
                        future_e_veh_a[val_indxs, :, 2:]]

        elif self.model_type == 'lstm_model':
            self.train_input = [history_sca[train_indxs, :, 2:],
                                        future_e_veh_a[train_indxs, 0, -1]]

            self.val_input = [history_sca[val_indxs, :, 2:],
                                        future_e_veh_a[val_indxs, 0, -1]]

        elif self.model_type == 'mlp_model':
            history_sca = np.squeeze(history_sca)
            future_e_veh_a = np.squeeze(future_e_veh_a)

            self.train_input = [history_sca[train_indxs, 2:],
                                        future_e_veh_a[train_indxs, -1]]

            self.val_input = [history_sca[val_indxs, 2:],
                                        future_e_veh_a[val_indxs, -1]]

    def train(self, epochs):
        # self.model.epochs_n = epochs
        avg_training_time = (45+epochs*15)/60
        print('it will take about ' , round(avg_training_time), ' mins to complete')
        for epoch in range(epochs):
            t0 = time.time()
            self.model.train_loop(self.train_input)
            self.model.test_loop(self.val_input, epoch)
            if self.model_type == 'vae_idm' or self.model_type == 'driver_model':
                self.train_mseloss.append(round(self.model.train_mseloss.result().numpy().item(), 2))
                self.train_att_klloss.append(round(self.model.train_att_klloss.result().numpy().item(), 2))
                self.train_idm_klloss.append(round(self.model.train_idm_klloss.result().numpy().item(), 2))
                self.test_mseloss.append(round(self.model.test_mseloss.result().numpy().item(), 2))
                self.test_att_klloss.append(round(self.model.test_att_klloss.result().numpy().item(), 2))
                self.test_idm_klloss.append(round(self.model.test_idm_klloss.result().numpy().item(), 2))
            else:
                self.train_mseloss.append(round(self.model.train_loss.result().numpy().item(), 2))
                self.test_mseloss.append(round(self.model.test_loss.result().numpy().item(), 2))
            t1 = time.time()
            print(self.epoch_count, 'epochs completed')
            print('Epoch took: ', round(t1-t0), ' seconds')
            self.epoch_count += 1

    def save_model(self, model_name):
        exp_dir = './models/experiments/'+model_name+'/model'
        self.model.save_weights(exp_dir)

# model_trainer = Trainer(data_arrays, model_type='driver_model')
# model_trainer.train(data_arrays, epochs=2)
# exp_dir = './models/experiments/'+'driver_model'+'/model'
# model_trainer.model.load_weights(exp_dir).expect_partial()
# model_trainer = Trainer(data_arrays, model_type='lstm_model')
model_trainer = Trainer(data_arrays, model_type='mlp_model')
# %%
#
model_trainer.train(epochs=5)

fig = plt.figure(figsize=(15, 5))
plt.style.use('default')

mse_axis = fig.add_subplot(131)
att_kl_axis = fig.add_subplot(132)
idm_kl_axis = fig.add_subplot(133)
mse_axis.plot(model_trainer.test_mseloss)
mse_axis.plot(model_trainer.train_mseloss)


# %%
x = np.linspace(-5, 5, 1000)
minval = 15
maxval = 20
for i in [0.25, 0.5, 1, 1.5]:
    y = minval + maxval/(1+np.exp(-i*x))
    plt.plot(x, y)
plt.plot(x, x + 25)
plt.grid()
# %%
all_epis = np.unique(history_sca[:, 0, 0])
np.random.seed(2021)
np.random.shuffle(all_epis)
train_epis = all_epis[:int(len(all_epis)*0.8)]
val_epis = np.setdiff1d(all_epis, train_epis)
train_indxs = np.where(history_future_usc[:, 0:1, 0] == train_epis)[0]
val_examples = np.where(history_future_usc[:, 0:1, 0] == val_epis)[0]
history_sca.shape
train_indxs.shape
val_examples.shape
history_sca = np.float32(history_sca)
future_idm_s = np.float32(future_idm_s)
future_m_veh_a = np.float32(future_m_veh_a)
# %%
model_trainer.model.vae_loss_weight = 1.
model_trainer.train(epochs=5)
################## MSE LOSS ##################
fig = plt.figure(figsize=(15, 5))
# plt.style.use('default')

mse_axis = fig.add_subplot(131)
att_kl_axis = fig.add_subplot(132)
idm_kl_axis = fig.add_subplot(133)
mse_axis.plot(model_trainer.test_mseloss)
mse_axis.plot(model_trainer.train_mseloss)

mse_axis.grid()
mse_axis.set_xlabel('epochs')
mse_axis.set_ylabel('loss (MSE)')
mse_axis.set_title('MSE')
mse_axis.legend(['test', 'train'])

################## att_kl LOSS ##################
att_kl_axis.plot(model_trainer.test_att_klloss)
att_kl_axis.plot(model_trainer.train_att_klloss)

att_kl_axis.grid()
att_kl_axis.set_xlabel('epochs')
att_kl_axis.set_ylabel('loss (att_kl)')
att_kl_axis.set_title('att_kl')
att_kl_axis.legend(['test', 'trai n'])

################## idm_kl LOSS ##################
idm_kl_axis.plot(model_trainer.test_idm_klloss)
idm_kl_axis.plot(model_trainer.train_idm_klloss)
idm_kl_axis.grid()
idm_kl_axis.set_xlabel('epochs')
idm_kl_axis.set_ylabel('loss (idm_kl)')
idm_kl_axis.set_title('idm_kl')
idm_kl_axis.legend(['test', 'train'])
att_axis, idm_axis = latent_vis()

# %%
from scipy.stats import beta, gamma, norm
x = np.linspace(0, 1, 100)
p = beta.pdf(x, 3, 10)
plt.plot(x*35, p, color='green')
p = beta.pdf(x,  11, 11)
plt.plot(x*35, p, color='orange')
p = beta.pdf(x, 10, 3)
plt.plot(x*35, p, color='red')
mean, var, skew, kurt = beta.stats(2, 10, moments='mvsk')
mean
driver_types = ['Timid', 'Normal', 'Aggressive']
plt.legend(driver_types)
plt.xlabel('Lateral displacement (%)')
plt.ylabel('Attention pdf')
plt.grid()
# %%
x = np.linspace(0, 1, 100)
prec = 5
mean = 0.9
alpha = mean*prec
beta_param = prec*(1-mean)
p = beta.pdf(x, alpha, beta_param)
plt.plot(x*35, p)

np.random.beta(alpha, beta_param)*35
# %%

prec = 10
mean = 0.9
alpha = mean*prec
beta_param = prec*(1-mean)
p = beta.pdf(x, alpha, beta_param)
plt.plot(x*35, p)

mean = 0.1
alpha = mean*prec
beta_param = prec*(1-mean)
p = beta.pdf(x, alpha, beta_param)
plt.plot(x*35, p)
# %%
prec = 15
mean = 0.9
alpha = mean*prec
beta_param = prec*(1-mean)
p = beta.pdf(x, alpha, beta_param)
plt.plot(x*35, p)

# %%
# %%
import tensorflow as tf
examples_to_vis = val_examples[:]

val_input = [history_sca[examples_to_vis , :, 2:],
            future_sca[examples_to_vis, :, 2:],
            future_idm_s[examples_to_vis, :, 2:],
            future_m_veh_a[examples_to_vis, :, 2:]]
act_pred, pri_params, pos_params = model_trainer.model(val_input)
loss = (tf.abs(tf.subtract(act_pred, future_e_veh_a[examples_to_vis, :, 2:])))
loss = tf.reduce_mean(loss, axis=1).numpy()


_ = plt.hist(loss, bins=150)
bad_examples = np.where(loss > 0.1)

# %%
future_m_veh_a[3508, 0, 0]
np.where(future_m_veh_a[:, 0, 0] == 33)
# %%


np.where(loss < 0.01)
np.where(loss == loss.max())
loss[5157]
val_examples[5157]
np.where(val_examples == 24896)
np.where(loss == loss.min())

# %%

x = np.linspace(-4, 4, 100)
y = 15+ 2000*(1/(1+tf.exp(-2*x)))
plt.plot(x, y)
# %%
import pickle

# model_trainer.save_model('driver_model')
# model_trainer.save_model('lstm_model')
model_trainer.save_model('mlp_model')
with open('./models/experiments/scaler.pickle', 'wb') as handle:
    pickle.dump(scaler, handle)
with open('./models/experiments/dummy_value_set.pickle', 'wb') as handle:
    pickle.dump(dummy_value_set, handle)
# %%

# %%
def latent_samples(model_trainer, sample_index):
    h_seq = history_sca[sample_index, :, 2:]
    sdv_actions = future_m_veh_a[sample_index, :, 2:]
    enc_h = model_trainer.model.h_seq_encoder(h_seq)
    prior_param = model_trainer.model.belief_net(enc_h, dis_type='prior')
    sampled_att_z, sampled_idm_z = model_trainer.model.belief_net.sample_z(prior_param)
    return sampled_att_z, sampled_idm_z

def latent_vis():
    fig = plt.figure(figsize=(6, 11))
    # plt.style.use('ggplot')
    # plt.style.use('default')
    att_axis = fig.add_subplot(211)
    idm_axis = fig.add_subplot(212)
    examples_to_vis = np.random.choice(val_examples, 7000, replace=False)
    sampled_att_z, sampled_idm_z = latent_samples(model_trainer, examples_to_vis)
    aggressiveness = history_future_usc[examples_to_vis, 0, -1]
    color_shade = aggressiveness
    att_axis.scatter(sampled_att_z[:, 0], sampled_att_z[:, 1], s=15, alpha=0.2, \
                                                c=color_shade, cmap='rainbow')
    idm_axis.scatter(sampled_idm_z[:, 0], sampled_idm_z[:, 1], s=15, alpha=0.2, \
                                    c=color_shade, cmap='rainbow')

    att_axis.set_ylabel('$z_{1}$')
    att_axis.set_xlabel('$z_{2}$')
    idm_axis.set_ylabel('$z_{1}$')
    idm_axis.set_xlabel('$z_{2}$')
    att_axis.set_title('Driver attention')
    idm_axis.set_title('Driver disposition')

    return att_axis, idm_axis
att_axis, idm_axis = latent_vis()
# plt.savefig("latent.png", dpi=500)

# %%
plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
#Options
params = {'text.usetex' : True,
          'font.size' : 11,
          'font.family' : 'lmodern',
          'text.latex.unicode': True,
          }
plt.rcParams.update(params)
# %%

import matplotlib.pyplot as plt

#Direct input
plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
#Options
params = {
          'font.size' : 20,
          'font.family' : 'EB Garamond',
          }
plt.rcParams.update(params)
plt.style.use(['science','ieee'])
# %%

fig = plt.figure()
    att_axis.title('$Driver attention$')
EB Garamond
#You must select the correct size of the plot in advance
fig.set_size_inches(3.54,3.54)

plt.plot([1,2,3,4])
plt.xlabel("Excitation-Energy")
plt.ylabel("Intensität")
plt.savefig("graph.pdf",
            #This is simple recomendation for publication plots
            dpi=1000,
            # Plot will be occupy a maximum of available space
            bbox_inches='tight',
            )
# %%
"""
Choose cars based on the latent for debugging
"""
sampled_att_z, sampled_idm_z = latent_samples(model_trainer, val_examples)
sampled_att_z, sampled_idm_z = sampled_att_z.numpy(), sampled_idm_z.numpy()

sampled_att_z
# %%
bad_episodes = []
bad_504 = []
bad_498 = []
# bad_zs = np.where((sampled_idm_z[:, 0] < -2) & (sampled_idm_z[:, 0] > -5))[0]
bad_zs = np.where((sampled_att_z[:, 1] > 5))[0]
for bad_z in bad_zs:
    exmp_indx = val_examples[bad_z]
    epis = history_future_usc[exmp_indx, 0, 0]
    bad_episodes.append([epis, exmp_indx])
    if epis == 504:
        bad_504.append(exmp_indx)
    if epis == 498:
        bad_498.append(exmp_indx)
min(bad_504)
min(bad_498)
# val_examples[2910]
_ = plt.hist(np.array(bad_episodes)[:, 0], bins=150)

bad_episodes
history_future_usc[71538, :, 1]
history_future_usc[55293, 0, :]
plt.plot(bad_504)
plt.scatter(bad_504,bad_504)
# %%
plt.plot(history_future_usc[55300, :, -6])
71538
for bad_indx in bad_504:
    plt.figure()
    plt.plot(history_future_usc[bad_indx, :, -6])
    plt.title(bad_indx)
    plt.grid()

# %%

# %%
"""Anticipation visualisation
"""
def vectorise(step_row, traces_n):
    return np.repeat(step_row, traces_n, axis=0)

def get_e_veh_att(e_veh_id, e_veh_decision, e_veh_att):
    atten_on_ego = np.where(e_veh_att == e_veh_id)
    e_veh_changing_lane = np.where(e_veh_decision != 0)
    atten_on_e_veh_changing_lane = np.intersect1d(atten_on_ego, e_veh_changing_lane)
    e_veh_att = np.ones(40)
    e_veh_att[atten_on_e_veh_changing_lane] = 0
    return e_veh_att

hf_usc_indexs = {}
col_names = ['episode_id', 'time_step', 'e_veh_id',
        'e_veh_speed', 'f_veh_speed', 'm_veh_speed',
        'e_veh_action', 'f_veh_action', 'm_veh_action',
        'ef_delta_v', 'ef_delta_x', 'em_delta_v', 'em_delta_x',
        'em_delta_y', 'e_veh_att', 'f_veh_exists', 'm_veh_exists',
        'e_veh_decision', 'aggressiveness']

index = 0
for item_name in col_names:
    hf_usc_indexs[item_name] = index
    index += 1
# %%
Example_pred = 0
i = 0
covered_episodes = []
model_trainer.model.idm_sim.attention_temp = 20
# model_trainer.model.arbiter.attention_temp = 20
traces_n = 20
sepcific_examples = [100000]
# for i in bad_examples[0]:
# for i in sepcific_examples:
# for i in bad_zs:
# for i in bad_examples[0][0:10]:
while Example_pred < 5:
    "ENSURE ONLY VAL SAMPLES CONSIDERED"

    sample_index = [val_examples[i]]
    # sample_index = [i]
    i += 1
    e_veh_decision = history_future_usc[sample_index, :, hf_usc_indexs['e_veh_decision']][0]
    e_veh_att = history_future_usc[sample_index, :, hf_usc_indexs['e_veh_att']][0]
    m_veh_exists = history_future_usc[sample_index, :, hf_usc_indexs['m_veh_exists']][0]
    aggressiveness = history_future_usc[sample_index, 0, hf_usc_indexs['aggressiveness']][0]
    # if e_veh_att.mean() != 0:
    # plt.figure(figsize=(4, 4))
    # plt.plot(e_veh_decision)
    # plt.plot(e_veh_att)
    # plt.plot(e_veh_decision)
    em_delta_y = history_future_usc[sample_index, :, hf_usc_indexs['em_delta_y']][0]
    episode = future_idm_s[sample_index, 0, 0][0]
    # if episode not in covered_episodes and aggressiveness > 0.9:
    # if episode not in covered_episodes:
    # if 4 == 4:
    # if  e_veh_att.mean() > 0:
    # #
    #
    act_20 = history_future_usc[sample_index, 10, hf_usc_indexs['e_veh_action']][0]
    if episode not in covered_episodes and act_20 < -0.5 and aggressiveness < 0.5:
    # if episode not in covered_episodes and e_veh_att[:25].mean() == 0 and \
    #                 e_veh_att[20:55].mean() > 0:
    # if episode not in covered_episodes and e_veh_att[:50].mean() > 0 and \
    #                 e_veh_att[50:].mean() == 0:

    # if sample_index[0] == 14841:
    # if  aggressiveness == 0.5:
    # if episode not in covered_episodes and aggressiveness == 0.5:
        covered_episodes.append(episode)
        sdv_actions = vectorise(future_m_veh_a[sample_index, :, 2:], traces_n)
        h_seq = vectorise(history_sca[sample_index, :, 2:], traces_n)
        future_idm_ss = vectorise(future_idm_s[sample_index, :, 2:], traces_n)
        enc_h = model_trainer.model.h_seq_encoder(h_seq)
        prior_param = model_trainer.model.belief_net(enc_h, dis_type='prior')
        sampled_att_z, sampled_idm_z = model_trainer.model.belief_net.sample_z(prior_param)
        idm_params = model_trainer.model.idm_layer(sampled_idm_z)
        act_seq, att_scores = model_trainer.model.idm_sim.rollout([sampled_att_z, \
                                                    idm_params, future_idm_ss, sdv_actions])
        act_seq, att_scores = act_seq.numpy(), att_scores.numpy()

        plt.figure(figsize=(4, 4))
        episode_id = history_future_usc[sample_index, 0, hf_usc_indexs['episode_id']][0]
        e_veh_id = history_future_usc[sample_index, 0, hf_usc_indexs['e_veh_id']][0]
        time_0 = history_future_usc[sample_index, 0, hf_usc_indexs['time_step']][0]
        info = [str(item)+' '+'\n' for item in [episode_id, time_0, e_veh_id, aggressiveness]]
        plt.text(0.5, 0.5,
                        'episode_id: '+ info[0] +
                        'time_0: '+ info[1] +
                        'e_veh_id: '+ info[2] +
                        'aggressiveness: '+ info[3]
                            , fontsize=10)
        plt.text(0.1, 0.1, str(idm_params.numpy()[:, :].mean(axis=0)))


        plt.figure(figsize=(4, 4))
        plt.plot(history_future_usc[sample_index, :, hf_usc_indexs['f_veh_action']][0], color='purple')
        plt.plot(history_future_usc[sample_index, :, hf_usc_indexs['e_veh_action']][0], color='black')
        plt.plot(history_future_usc[sample_index, :, hf_usc_indexs['m_veh_action']][0], color='red')
        plt.legend(['f_veh_action', 'e_veh_action', 'm_veh_action'])

        for sample_trace_i in range(traces_n):
           plt.plot(range(20, 60), act_seq[sample_trace_i, :, :].flatten(),
                                        color='grey', alpha=0.5)
           # plt.plot(range(19, 39), act_seq[sample_trace_i, :, :].flatten(), color='grey')

        # plt.ylim(-3, 3)
        plt.title(str(sample_index[0]) + ' -- Action')
        plt.grid()

        plt.figure(figsize=(4, 4))
        # plt.plot(e_veh_att[:40] , color='black')
        plt.plot(range(0, 60), e_veh_att, color='red')
        for sample_trace_i in range(traces_n):
           plt.plot(range(20, 60), att_scores[sample_trace_i, :].flatten(), color='grey')
        # plt.ylim(-0.1, 1.1)
        plt.title(str(sample_index[0]) + ' -- Attention')
        plt.grid()

        ##########
        # lATENT
        att_axis, idm_axis = latent_vis()
        att_axis.scatter(sampled_att_z[:, 0], sampled_att_z[:, 1], s=15, color='black')
        idm_axis.scatter(sampled_idm_z[:, 0], sampled_idm_z[:, 1], s=15, color='black')

        att_axis.set_ylabel('$z_1$')
        att_axis.set_xlabel('$z_2$')
        ##########

        # plt.plot(desired_vs)
        # plt.grid()
        # plt.plot(desired_tgaps)
        # plt.grid()
        plt.figure(figsize=(4, 4))
        desired_vs = idm_params.numpy()[:, 0]
        desired_tgaps = idm_params.numpy()[:, 1]
        plt.scatter(desired_vs, desired_tgaps, color='grey')

        plt.scatter(24.7, 1.5, color='red')
        plt.xlim(15, 40)
        plt.ylim(0, 3)
        #
        # plt.scatter(30, 1, color='red')
        # plt.xlim(25, 35)
        # plt.ylim(0, 2)

        plt.title(str(sample_index[0]) + ' -- Param')
        plt.grid()

        ##########
        plt.figure(figsize=(4, 4))
        plt.plot(m_veh_exists, color='black')
        plt.title(str(sample_index[0]) + ' -- m_veh_exists')
        plt.grid()
        ######\######
        plt.figure(figsize=(4, 4))
        plt.plot(em_delta_y[:20], color='black')
        plt.plot(range(0, 60), em_delta_y, color='red')
        # plt.plot([0, 40], [-0.37, -0.37], color='green')
        # plt.plot([0, 40], [-1, -1], color='red')
        # plt.plot([0, 40], [-1.5, -1.5], color='red')
        plt.title(str(sample_index[0]) + ' -- em_delta_y')
        plt.grid()
        ############

        Example_pred += 1
# %%




# %%
"""Single sample Anticipation visualisation
"""
# model_trainer.model.arbiter.attention_temp = 5
traces_n = 100
model_trainer.model.idm_sim.attention_temp = 5
sample_index = [8526]
e_veh_decision = history_future_usc[sample_index, :, hf_usc_indexs['e_veh_decision']][0]
e_veh_att = history_future_usc[sample_index, :, hf_usc_indexs['e_veh_att']][0]
m_veh_exists = history_future_usc[sample_index, :, hf_usc_indexs['m_veh_exists']][0]

em_delta_y = history_future_usc[sample_index, :, hf_usc_indexs['em_delta_y']][0]
episode = future_idm_s[sample_index, 0, 0][0]

episode = future_idm_s[sample_index, 0, 0][0]
sdv_actions = vectorise(future_m_veh_a[sample_index, :, 2:], traces_n)
sdv_actions.shape
# sdv_actions[:, :, 0] = 0
h_seq = vectorise(history_sca[sample_index, :, 2:], traces_n)
future_idm_ss = vectorise(future_idm_s[sample_index, :, 2:], traces_n)
enc_h = model_trainer.model.h_seq_encoder(h_seq)
prior_param = model_trainer.model.belief_net(enc_h, dis_type='prior')
sampled_att_z, sampled_idm_z = model_trainer.model.belief_net.sample_z(prior_param)
idm_params = model_trainer.model.idm_layer(sampled_idm_z)
act_seq, att_scores = model_trainer.model.idm_sim.rollout([sampled_att_z, \
                                            idm_params, future_idm_ss, sdv_actions])
act_seq, att_scores = act_seq.numpy(), att_scores.numpy()

time_axis = np.linspace(0., 6., 60)
plt.figure(figsize=(4, 4))
episode_id = history_future_usc[sample_index, 0, hf_usc_indexs['episode_id']][0]
e_veh_id = history_future_usc[sample_index, 0, hf_usc_indexs['e_veh_id']][0]
time_0 = history_future_usc[sample_index, 0, hf_usc_indexs['time_step']][0]
aggressiveness = history_future_usc[sample_index, 0, hf_usc_indexs['aggressiveness']][0]
info = [str(item)+' '+'\n' for item in [episode_id, time_0, e_veh_id, aggressiveness]]
plt.text(0.5, 0.5,
                'episode_id: '+ info[0] +\
                'time_0: '+ info[1] +\
                'e_veh_id: '+ info[2] +\
                'aggressiveness: '+ info[3]
                    , fontsize = 15)
plt.text(0.1, 0.1, str(idm_params.numpy()[:, :].mean(axis=0)))

##########
#5 %%
plt.figure(figsize=(4, 4))
plt.plot(time_axis, history_future_usc[sample_index, :, hf_usc_indexs['f_veh_action']][0], color='purple')
plt.plot(time_axis, history_future_usc[sample_index, :, hf_usc_indexs['e_veh_action']][0], color='red')
plt.plot(time_axis, history_future_usc[sample_index, :, hf_usc_indexs['m_veh_action']][0], color='black')
plt.legend(['Leader', 'Follower', 'Merger'])

for sample_trace_i in range(traces_n):
   plt.plot(time_axis[20:], act_seq[sample_trace_i, :, :].flatten(), \
                                color='grey', alpha=0.5)
plt.title('Vehicle actions')
plt.fill_between([0,2],[-3,-3], [3,3], color='lightgrey')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration ($ms^{-2}$)')
plt.ylim(-3, 1)
plt.grid()
##########
# s%%
plt.figure(figsize=(4, 4))
plt.plot(time_axis, e_veh_att, color='red', linewidth=3)
for sample_trace_i in range(traces_n):
   plt.plot(time_axis[20:], att_scores[sample_trace_i, :].flatten(), color='grey', alpha=0.5)
plt.ylim(-0.1, 1.1)
plt.fill_between([0,2],[-3,-3], [3,3], color='lightgrey')
plt.xlabel('Time (s)')
plt.ylabel('Attentiveness (%)')
plt.title('Driver attentiveness')
plt.legend(['True', 'Predicted'])
plt.grid()
# %%

##########
# lATENT
att_axis, idm_axis = latent_vis()
att_axis.scatter(sampled_att_z[:, 0], sampled_att_z[:, 1], s=15, color='black')
idm_axis.scatter(sampled_idm_z[:, 0], sampled_idm_z[:, 1], s=15, color='black')

att_axis.set_ylabel('$z_1$')
att_axis.set_xlabel('$z_2$')

# %%
##########
desired_vs = idm_params.numpy()[:, 0]
desired_tgaps = idm_params.numpy()[:, 1]
min_jamx = idm_params.numpy()[:, 2]
fig = pyplot.figure()
ax = Axes3D(fig)

ax.scatter(24.7,  1.5, 2, color='red')
# ax.scatter(19.4,  2, 4, color='red')
ax.scatter(desired_vs, desired_tgaps, min_jamx, color='grey')
ax.set_xlim(18, 30)
ax.set_ylim(1, 2)
ax.set_zlim(0, 4)
ax.set_title('Driver disposition')

ax.set_xlabel('Desired speed')
ax.set_ylabel('Desired time gap')
ax.set_zlabel('Minimum jam distance')
plt.legend(['True', 'Predicted'])


# %%
a = 7
b = a
id(a)
id(b)
##########
plt.figure(figsize=(4, 4))
plt.plot(m_veh_exists, color='black')
plt.title(str(sample_index[0]) + ' -- m_veh_exists')
plt.grid()
############
plt.figure(figsize=(4, 4))
plt.plot(em_delta_y[:20], color='black')
plt.plot(range(0, 60), em_delta_y, color='red')
# plt.plot([0, 40], [-0.37, -0.37], color='green')
# plt.plot([0, 40], [-1, -1], color='red')
# plt.plot([0, 40], [-1.5, -1.5], color='red')
plt.title(str(sample_index[0]) + ' -- em_delta_y')
plt.grid()
############
# %%
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import random

"""
LATENT ANIMATION
"""
def get_animation():
    plt.rcParams['animation.ffmpeg_path'] = 'C:/Users/sa00443/ffmpeg_programs/ffmpeg.exe'
    from matplotlib.animation import FuncAnimation, writers

    def latent_samples(model_trainer, sample_index):
        sdv_actions = future_m_veh_a[sample_index, :, 2:]
        h_seq = history_sca[sample_index, :, 2:]
        enc_h = model_trainer.model.h_seq_encoder(h_seq)
        prior_param = model_trainer.model.belief_net(enc_h, dis_type='prior')
        sampled_att_z, sampled_idm_z = model_trainer.model.belief_net.sample_z(prior_param)
        return sampled_att_z, sampled_idm_z

    fig = plt.figure(figsize=(7, 7))
    plt.style.use('ggplot')
    att_axis = fig.add_subplot(211)
    idm_axis = fig.add_subplot(212)


    def animation_frame(i):
        model_trainer.model.vae_loss_weight = 0.1
        model_trainer.train(data_arrays, epochs=1)
        sampled_att_z, sampled_idm_z = latent_samples(model_trainer, val_examples)
        aggressiveness = history_future_usc[val_examples, 0, -1]
        color_shade = aggressiveness
        att_axis.scatter(sampled_att_z[:, 0], sampled_att_z[:, 1], s=15, alpha=0.3, \
                                                    c=color_shade, cmap='rainbow')
        idm_axis.scatter(sampled_idm_z[:, 0], sampled_idm_z[:, 1], s=15, alpha=0.3, \
                                                    c=color_shade, cmap='rainbow')

        att_axis.set_title('Iteration ' + str(i))
        att_axis.set_ylabel('$z_{att_1}$')
        att_axis.set_xlabel('$z_{att_2}$')
        idm_axis.set_ylabel('$z_{idm_1}$')
        idm_axis.set_xlabel('$z_{idm_1}$')

    animation = FuncAnimation(fig, func=animation_frame, \
                              frames=range(1, 81), interval=1)

    # setting up wrtiers object
    Writer = writers['ffmpeg']
    writer = Writer(fps=4, metadata={'artist': 'Me'}, bitrate=3000)
    animation.save('latent_evolution.mp4', writer, dpi=250)


# get_animation()
