import numpy as np
from collections import deque
from sklearn import preprocessing
np.random.seed(2020)
import time

class DataGenerator:
    def __init__(self, env, config):
        self.config = config
        self.env_steps_n = 500 # number of data samples. Not all of it is useful.
        self.env = env
        self.initiate()

    def initiate(self):
        self.env.usage = 'data generation'
        self.env.recordings = {}
        self.env.veh_log = ['id', 'lane_decision', 'lane_id',
                             'target_lane', 'glob_x', 'lane_y', 'speed']
        self.indxs = {}
        all_col_names = ['episode_id', 'veh_id', 'time_steps', 'ego_decision', \
                 'leader_speed', 'follower_speed', 'merger_speed', \
                 'leader_action', 'follower_action', 'merger_action', \
                 'fl_delta_v', 'fl_delta_x', 'fm_delta_v', 'fm_delta_x', \
                 'lane_y', 'leader_exists', 'follower_aggress', \
                 'follower_atten', 'follower_id']

        index = 0
        for item_name in all_col_names:
            self.indxs[item_name] = index
            index += 1

    def run_sim(self):
        for step in range(self.env_steps_n):
            self.env.step()

        return self.env.recordings

    def round_scalars(self, data_list):
        rounded_items = []
        for item in data_list:
            try:
                rounded_items.append(round(item, 2))
            except:
                rounded_items.append(item)
        return rounded_items

    def get_step_state(self, follower, leader, merger):
        """
        Note: If a merger is missing, np.nan is assigned to its feature values.
        """
        step_state = []

        if follower_s:
            follower_speed, follower_glob_x, follower_act_long, \
                    follower_aggress, follower_atten, follower_id = follower_s
        else:
            return

        if leader_s:
            leader_speed, leader_glob_x, leader_act_long, _, _, _ = leader_s
            if leader_glob_x-follower_glob_x < 100:
                leader_exists = 1
            else:
                leader_speed, leader_glob_x, leader_act_long = [np.nan]*3
                leader_exists = 0
        else:
            leader_speed, leader_glob_x, leader_act_long = [np.nan]*3
            leader_exists = 0

        merger_speed, merger_glob_x, merger_act_long, \
                                merger_act_lat, ego_lane_y = merger_s


        step_feature = [leader_speed, follower_speed, merger_speed, \
                        leader_act_long, follower_act_long, merger_act_long]

        # as if follower following leader
        step_feature.extend([
                             follower_speed-leader_speed,
                             leader_glob_x-follower_glob_x
                            ])

        # as if follower following merger
        step_feature.extend([
                             follower_speed-merger_speed,
                             merger_glob_x-follower_glob_x
                             ])

        step_feature.extend([ego_lane_y, leader_exists, follower_aggress, \
                                                    follower_atten, follower_id])
        # return self.round_scalars(step_feature)
        return step_feature


    def extract_features(self, raw_recordings):
        """
        Extrtacts features from follower's perspective.
        """
        def trace_back(time_step):
            """
            When a merger is found, trace back its state while it is being observed
            by follower.
            """
            pointer = -1
            while True:
                merger_glob_x = merger_ts[time_step]['glob_x']
                merger_decision = merger_ts[time_step]['lane_decision']
                follower_glob_x = follower_ts[time_step]['glob_x']
                leader_glob_x = leader_ts[time_step]['glob_x']

                if merger_glob_x >= follower_glob_x and \
                                        merger_glob_x <= leader_glob_x:
                    try:
                        epis_states[pointer][-1] = merger_id
                    except:
                        break
                else:
                    break

                time_step -= 1
                pointer -= 1

        def is_epis_end():
            """
            To tell if an episode should end. Reasons for ending an episode:
            - follower changes lane.
            - leader leaves lane.
            - merger completes its manoeuvre.
            """
            if leader['lane_decision'] != 'keep_lane' or \
                                follower['lane_decision'] != 'keep_lane':
                return True

            elif merger:
                if merger['lane_decision'] == 'keep_lane':
                    return True
            return False

        def reset_episode():
            nonlocal epis_states, leader_id, merger_id, episode_id
            if len(epis_states) > 10:
                feature_data.extend(epis_states)
                episode_id += 1
            epis_states = []
            leader_id = None
            merger_id = None

        feature_data = [] # episode_id ...
        episode_id = 0
        epis_states = []
        leader_id = None
        merger_id = None

        for follower_id in raw_recordings.keys():
            # if follower_id != 14:
            #     continue
            follower_ts = raw_recordings[follower_id]
            follower_time_steps = list(follower_ts.keys())
            reset_episode()

            for time_step, follower in follower_ts.items():
                if follower['att_veh_id']:
                    att_veh = raw_recordings[follower['att_veh_id']][time_step]
                else:
                    # no point if follower is not attending to anyone
                    reset_episode()
                    continue

                if not leader_id:
                    if att_veh['lane_decision'] == 'keep_lane' and \
                                    att_veh['lane_id'] == follower['lane_id']:
                        # confirm this is the leader
                        leader_id = att_veh['id']
                        leader_ts = raw_recordings[leader_id]
                        leader_time_steps = list(leader_ts.keys())
                        leader = leader_ts[time_step]
                    else:
                        reset_episode()
                        continue
                else:
                    leader = leader_ts[time_step]

                if not merger_id:
                    if att_veh['lane_decision'] != 'keep_lane' and \
                                    att_veh['target_lane'] == follower['lane_id']:
                        # confirm this is the leader
                        merger_id = att_veh['id']
                        merger_ts = raw_recordings[merger_id]
                        trace_back(time_step)
                        merger_time_steps = list(merger_ts.keys())
                        merger = merger_ts[time_step]
                    else:
                        merger = None
                else:
                    merger = merger_ts[time_step]

                if is_epis_end():
                    reset_episode()
                    continue
                # step_state =
                epis_states.append([episode_id,
                                             time_step,
                                            follower_id,
                                            leader_id,
                                            -1 if not merger_id else merger_id
                                             ])

        return np.array(feature_data)









    def extract_features_edddddddd(self, raw_recordings):
        """
        - remove redundancies: only keeping states for merger, leader and follower car.
        Extract
        """
        feature_data = []
        episode_id = 0
        for veh_id in raw_recordings['info'].keys():
            time_stepss = np.array(raw_recordings['time_steps'][veh_id])
            ego_decisions = np.array(raw_recordings['decisions'][veh_id])
            veh_states = raw_recordings['states'][veh_id]
            split_indxs = self.get_split_indxs(ego_decisions)
            if not split_indxs:
                # not a single lane change
                continue

            for split_indx in split_indxs:
                # each split forms an episode
                start_snip, end_snip = split_indx
                ego_end_decision = ego_decisions[end_snip]
                epis_states = []

                for _step in range(start_snip, end_snip+1):
                    ego_decision = ego_decisions[_step]
                    time_steps = time_stepss[_step]
                    veh_state = veh_states[_step]

                    if ego_end_decision == 1:
                        # an episode ending with a lane change left
                        if ego_decision == 0:
                            step_feature = self.get_step_feature(
                                                                veh_state['ego'],
                                                                veh_state['fl'],
                                                                veh_state['rl'])

                        elif ego_decision == 1:
                            step_feature = self.get_step_feature(
                                                                veh_state['ego'],
                                                                veh_state['f'],
                                                                veh_state['r'])

                    elif ego_end_decision == -1:
                        # an episode ending with a lane change right
                        if ego_decision == 0:
                            # print(ego_decision)
                            step_feature = self.get_step_feature(
                                                                veh_state['ego'],
                                                                veh_state['fr'],
                                                                veh_state['rr'])

                        elif ego_decision == -1:
                            # print(ego_decision)
                            step_feature = self.get_step_feature(
                                                                veh_state['ego'],
                                                                veh_state['f'],
                                                                veh_state['r'])
                    elif ego_end_decision == 0:
                        # an episode ending with lane keep
                        step_feature = self.get_step_feature(
                                                            veh_state['ego'],
                                                            veh_state['f'],
                                                            veh_state['r'])

                    if step_feature:
                        step_feature[0:0] = episode_id, veh_id, time_steps, ego_decision
                        epis_states.append(step_feature)
                    else:
                        break
                else:
                    # runs if no breaks in loop
                    if len(epis_states) > 50:
                        # ensure enough steps are present within a given episode
                        episode_id += 1
                        feature_data.extend(epis_states)

        # return feature_data
        return np.array(feature_data)

    def fill_missing_values(self, feature_data):
        """
        Fill dummy values for the missing lead vehicle.
        Note:
        Different dummy values need to be fed to the IDM action function. Here goal
        is to assign values to maintain close to gaussian data distributions. Later,
        to ensure an IDM follower is not perturbed by the leader, different dummy values
        will be assigned.
        """
        def fill_with_dummy(arr, indx):
            dummy_value = arr[~np.isnan(arr).any(axis=1)][:, indx].mean()
            nan_mask = np.isnan(arr[:, indx])
            nan_indx = np.where(nan_mask)
            arr[nan_indx, indx] = dummy_value
            return arr

        feature_data = fill_with_dummy(feature_data, self.indxs['leader_speed'])
        feature_data = fill_with_dummy(feature_data, self.indxs['leader_action'])
        feature_data = fill_with_dummy(feature_data, self.indxs['fl_delta_v'])
        feature_data = fill_with_dummy(feature_data, self.indxs['fl_delta_x'])

        return feature_data

    def sequence(self, feature_data, history_length, future_length):
        """
        Sequence the data into history/future sequences.
        """
        episode_ids = list(np.unique(feature_data[:, 0]))
        history_seqs, future_seqs = [], []
        for episode_id in episode_ids:
            epis_data = feature_data[feature_data[:, 0] == episode_id]
            history_seq = deque(maxlen=history_length)
            for step in range(len(epis_data)):
                history_seq.append(epis_data[step])
                if len(history_seq) == history_length:
                    future_indx = step + future_length
                    if future_indx + 1 > len(epis_data):
                        break

                    history_seqs.append(list(history_seq))
                    future_seqs.append(epis_data[step+1:future_indx+1])
        return [np.array(history_seqs), np.array(future_seqs)]

    def names_to_index(self, col_names):
        return [self.indxs[item] for item in col_names]

    def split_data(self, history_future_seqs_seqs, history_future_seqs_scaled):
        history_seqs, future_seqs = history_future_seqs_seqs
        history_seqs_scaled, future_seqs_scaled = history_future_seqs_scaled
        # future and histroy states - fed to LSTMs
        col_names = ['episode_id', 'leader_speed', 'follower_speed', 'merger_speed', \
                 'leader_action', 'follower_action', 'merger_action', \
                 'fl_delta_v', 'fl_delta_x', 'fm_delta_v', 'fm_delta_x', \
                 'lane_y', 'leader_exists']
        history_sca = history_seqs_scaled[:, :, self.names_to_index(col_names)]
        future_sca = future_seqs_scaled[:, :, self.names_to_index(col_names)]

        #  history+future info for debugging/ visualisation
        col_names = ['episode_id', 'time_steps', 'ego_decision', \
                'leader_action', 'follower_action', 'merger_action', \
                'lane_y', 'follower_aggress', \
                'follower_atten', 'veh_id', 'follower_id']

        history_usc = history_seqs[:, :, self.names_to_index(col_names)]
        future_usc = future_seqs[:, :, self.names_to_index(col_names)]
        history_future_usc = np.append(history_usc, future_usc, axis=1)

        # future states - fed to idm_layer
        col_names = ['episode_id', 'follower_speed',
                        'fl_delta_v', 'fl_delta_x',
                        'fm_delta_v', 'fm_delta_x']
        future_idm_s = future_seqs[:, :, self.names_to_index(col_names)]

        # future action of merger - fed to LSTMs
        col_names = ['episode_id', 'merger_action', 'lane_y']
        future_merger_a = future_seqs[:, :, self.names_to_index(col_names)]

        # future action of follower - used as target
        col_names = ['episode_id', 'follower_action']
        future_follower_a = future_seqs[:, :, self.names_to_index(col_names)]

        data_arrays = [history_future_usc, history_sca, future_sca, future_idm_s, \
                        future_merger_a, future_follower_a]

        return data_arrays

    def scale_data(self, feature_data):
        col_names = ['leader_speed', 'follower_speed', 'merger_speed', \
                 'fl_delta_v', 'fl_delta_x', 'fm_delta_v', 'fm_delta_x']

        scalar_indexs = self.names_to_index(col_names)
        scaler = preprocessing.StandardScaler().fit(feature_data[:, scalar_indexs])
        feature_data_scaled = feature_data.copy()
        feature_data_scaled[:, scalar_indexs] = scaler.transform(feature_data[:, scalar_indexs])
        return feature_data_scaled

    def mask_steps(self, history_future_seqss):
        """
        This is needed for cases where the merger passes
        several cars (i.e., a sequence has states from more than one vehicle
        """
        history_seqs, future_seqs = history_future_seqss
        follower_id_index = self.indxs['follower_id']

        axis_0, axis_1 = np.where(history_seqs[:, 1:, follower_id_index] != \
                                    history_seqs[:, :-1, follower_id_index])
        for sample, step in zip(axis_0, axis_1):
            history_seqs[sample, :step+1, 1:] = 0

        axis_0, axis_1 = np.where(future_seqs[:, 1:, follower_id_index] != \
                                    future_seqs[:, :-1, follower_id_index])
        for sample, step in zip(axis_0, axis_1):
            future_seqs[sample, step+1:, 1:] = 0
        return [history_seqs, future_seqs]

    def prep_data(self):
        time_1 = time.time()
        raw_recordings = self.run_sim()
        print(time.time()-time_1)
        time_1 = time.time()
        feature_data = self.extract_features(raw_recordings)
        print(time.time()-time_1)

        # feature_data = self.fill_missing_values(feature_data)
        # feature_data_scaled = self.scale_data(feature_data)
        # history_future_seqs_seqs = self.sequence(feature_data, 20, 20)
        # history_future_seqs_seqs = self.mask_steps(history_future_seqs_seqs)
        # history_future_seqs_scaled = self.sequence(feature_data_scaled, 20, 20)
        # history_future_seqs_scaled = self.mask_steps(history_future_seqs_scaled)
        # data_arrays = self.split_data(history_future_seqs_seqs, history_future_seqs_scaled)
        return feature_data
        # return data_arrays, raw_recordings['info']

    # def save(self):
    #     pass
