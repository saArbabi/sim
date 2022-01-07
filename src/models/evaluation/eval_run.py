import sys
sys.path.insert(0, './src')
from models.evaluation.eval_obj import MCEVAL
val_run_name = 'test_dense'
def main():
    data_obj = MCEVAL(val_run_name)
    data_obj.run()

if __name__=='__main__':
    main()
# "neural_029": "NeuralVehicle",
# "latent_mlp_02": "LatentMLPVehicle",
# "mlp_01": "MLPVehicle",
# "lstm_01": "LSTMVehicle"
