import matplotlib.pyplot as plt

class Viewer():
    def __init__(self, model_type, env_config):
        self.env_config  = env_config
        self.fig = plt.figure(figsize=(10, 3))
        self.env_ax = self.fig.add_subplot(211)
        self.model_type = model_type

    def draw_road(self, ax, percept_origin, elapsed_time):
        lane_cor = self.env_config['lane_width']*self.env_config['lane_count']
        ax.hlines(0, 0, self.env_config['lane_length'], colors='k', linestyles='solid')
        ax.hlines(lane_cor, 0, self.env_config['lane_length'],
                                                    colors='k', linestyles='solid')

        if self.env_config['lane_count'] > 1:
            lane_cor = self.env_config['lane_width']
            for lane in range(self.env_config['lane_count']-1):
                ax.hlines(lane_cor, 0, self.env_config['lane_length'],
                                                        colors='k', linestyles='--')
                lane_cor += self.env_config['lane_width']

        if percept_origin < self.env_config['percept_range']:
            ax.set_xlim(0, self.env_config['percept_range']*2)
        else:
            ax.set_xlim(percept_origin - self.env_config['percept_range'],
                                percept_origin + self.env_config['percept_range'])

        ax.set_yticks([])
        plt.title('#Elapsed time:'+str(round(elapsed_time, 1))+\
        's  #model: '+self.model_type)

    def draw_vehicles(self, ax, vehicles):
        xs = [veh.x for veh in vehicles if veh.id != 'neural']
        ys = [veh.y for veh in vehicles if veh.id != 'neural']
        for veh in vehicles:
            vehicle_color = 'grey'
            edgecolors = 'black'

            if veh.id == 'neural':
                vehicle_color = 'none'

                if veh.control_type == 'neural':
                    edgecolors = 'green'
                    ax.annotate('e', (veh.x, veh.y+0.3))
    
            if veh.id == 'normal_idm':
                vehicle_color = 'orange'
            if veh.id == 'timid_idm':
                vehicle_color = 'yellow'
            if veh.id == 'aggressive_idm':
                vehicle_color = 'red'

            ax.scatter(veh.x, veh.y, s=100, marker=">", \
                                            facecolors=vehicle_color, edgecolors=edgecolors)

            # ax.annotate(round(veh.v, 1), (veh.x, veh.y+0.1))
            # ax.annotate(round(veh.v, 1), (veh.x, veh.y+0.1))

    def draw_env(self, ax, vehicles, elapsed_time):
        ax.clear()
        self.draw_road(ax, percept_origin = vehicles[0].x, elapsed_time=elapsed_time)
        self.draw_vehicles(ax, vehicles)

    def update_plots(self, vehicles, elapsed_time):
        self.draw_env(self.env_ax, vehicles, elapsed_time)
        plt.pause(0.00000000000000000000001)
        # plt.show()
