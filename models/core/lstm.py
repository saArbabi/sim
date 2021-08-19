from tensorflow.keras.layers import Dense, LSTM
from keras import backend as K
from importlib import reload
from models.core import abstract_model
reload(abstract_model)
from models.core.abstract_model import  AbstractModel
import tensorflow as tf
import tensorflow_probability as tfp
tfd = tfp.distributions

class Encoder(AbstractModel):
    def __init__(self, config=None):
        super(Encoder, self).__init__(config)
        self.enc_units = 50
        self.architecture_def()

    @tf.function(experimental_relax_shapes=True)
    def train_step(self, states, targets):
        with tf.GradientTape() as tape:
            pred_dis = self(states)
            loss = self.log_loss(targets, pred_dis)

        gradients = tape.gradient(loss, self.trainable_variables)
        self.optimizer.apply_gradients(zip(gradients, self.trainable_variables))
        self.train_loss.reset_states()
        self.train_loss(loss)

    @tf.function(experimental_relax_shapes=True)
    def test_step(self, states, targets):
        pred_dis = self(states)
        loss = self.log_loss(targets, pred_dis)
        self.test_loss.reset_states()
        self.test_loss(loss)

    def log_loss(self, act_true, pred_dis):
        likelihood = pred_dis.log_prob(act_true)
        return -tf.reduce_mean(likelihood)

    def architecture_def(self):
        self.lstm_layer = LSTM(self.enc_units, return_state=True)
        self.neu_mean = Dense(1)
        self.neu_var = Dense(1, activation=K.exp)

    def train_loop(self, data_objs):
        train_ds = self.batch_data(data_objs)
        for s, t in train_ds:
            self.train_step(s, t)

    def test_loop(self, data_objs, epoch):
        train_ds = self.batch_data(data_objs)
        for s, t in train_ds:
            self.test_step(s, t)

    def call(self, inputs):
        _, h_t, c_t = self.lstm_layer(inputs)
        neu_mean = self.neu_mean(h_t)
        neu_var = self.neu_var(h_t)
        pred_dis = tfp.distributions.Normal(neu_mean, neu_var, name='Normal')

        return pred_dis
