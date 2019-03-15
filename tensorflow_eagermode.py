"""
This is exactly like the other neural net, but it is in Tensorflow's Eager mode
So it should actually work lol


Initial loss= 4.640756607
Step: 0001  loss= 4.640756607  accuracy= 0.1719
Step: 0100  loss= 1.294759512  accuracy= 0.6077
Step: 0200  loss= 0.572107673  accuracy= 0.7556
Step: 0300  loss= 0.468368530  accuracy= 0.7945
Step: 0400  loss= 0.431688845  accuracy= 0.8109
Step: 0500  loss= 0.357956439  accuracy= 0.8453
Step: 0600  loss= 0.281263858  accuracy= 0.8885
Step: 0700  loss= 0.227537379  accuracy= 0.9144
Step: 0800  loss= 0.243623480  accuracy= 0.9063
Step: 0900  loss= 0.151595414  accuracy= 0.9508
Step: 1000  loss= 0.132566571  accuracy= 0.9531
Testset Accuracy: 0.9531


"""

import tensorflow as tf
import pandas as pd
# Set Eager API
tf.enable_eager_execution()
tfe = tf.contrib.eager

features = pd.read_csv("data-generation/jobs_features.csv")
labels = pd.read_csv("data-generation/job_labels.csv")

all_data = features.merge(labels, left_on="name", right_on="file")
all_data['class'] = pd.factorize(all_data['class'])[0]

features = ["loops", "fdefs", "fcalls", "loads", "asmts"]

# Parameters
learning_rate = 0.001
num_steps = 1000
batch_size = 128
display_step = 100

# Network Parameters
n_hidden_1 = 256 # 1st layer number of neurons
n_hidden_2 = 256 # 2nd layer number of neurons
n_hidden_3 = 256 # 3rd layer number of neurons
num_input = 5
num_classes = 5 

# Using TF Dataset to split data into batches
training_dataset = (
    tf.data.Dataset.from_tensor_slices(
        (
            tf.cast(all_data[features].values, tf.float32),
            tf.cast(all_data['class'].values, tf.int32)
        )
    )
)

dataset = training_dataset
dataset = dataset.repeat().batch(batch_size).prefetch(batch_size)
dataset_iter = tfe.Iterator(dataset)


# Define the neural network. To use eager API and tf.layers API together,
# we must instantiate a tfe.Network class as follow:
class NeuralNet(tfe.Network):
    def __init__(self):
        # Define each layer
        super(NeuralNet, self).__init__()
        # Hidden fully connected layer with 256 neurons
        self.layer1 = self.track_layer(
            tf.layers.Dense(n_hidden_1, activation=tf.nn.relu))
        # Hidden fully connected layer with 256 neurons
        self.layer2 = self.track_layer(
            tf.layers.Dense(n_hidden_2, activation=tf.nn.relu))
        # Hidden fully connected layer with 256 neurons
        self.layer3 = self.track_layer(
            tf.layers.Dense(n_hidden_3, activation=tf.nn.relu))
        # Output fully connected layer with a neuron for each class
        self.out_layer = self.track_layer(tf.layers.Dense(num_classes))

    def call(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        return self.out_layer(x)


neural_net = NeuralNet()


# Cross-Entropy loss function
def loss_fn(inference_fn, inputs, labels):
    # Using sparse_softmax cross entropy
    return tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(
        logits=inference_fn(inputs), labels=labels))


# Calculate accuracy
def accuracy_fn(inference_fn, inputs, labels):
    prediction = tf.nn.softmax(inference_fn(inputs))
    correct_pred = tf.equal(tf.argmax(prediction, 1), labels)
    return tf.reduce_mean(tf.cast(correct_pred, tf.float32))


# SGD Optimizer
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
# Compute gradients
grad = tfe.implicit_gradients(loss_fn)

# Training
average_loss = 0.
average_acc = 0.
for step in range(num_steps):

    # Iterate through the dataset
    d = dataset_iter.next()

    x_batch = d[0]
    # Labels
    y_batch = tf.cast(d[1], dtype=tf.int64)

    # Compute the batch loss
    batch_loss = loss_fn(neural_net, x_batch, y_batch)
    average_loss += batch_loss
    # Compute the batch accuracy
    batch_accuracy = accuracy_fn(neural_net, x_batch, y_batch)
    average_acc += batch_accuracy

    if step == 0:
        # Display the initial cost, before optimizing
        print("Initial loss= {:.9f}".format(average_loss))

    # Update the variables following gradients info
    optimizer.apply_gradients(grad(neural_net, x_batch, y_batch))

    # Display info
    if (step + 1) % display_step == 0 or step == 0:
        if step > 0:
            average_loss /= display_step
            average_acc /= display_step
        print("Step:", '%04d' % (step + 1), " loss=",
              "{:.9f}".format(average_loss), " accuracy=",
              "{:.4f}".format(average_acc))
        average_loss = 0.
        average_acc = 0.

training_dataset = (
    tf.data.Dataset.from_tensor_slices(
        (
            tf.cast(all_data[features].values, tf.float32),
            tf.cast(all_data['class'].values, tf.int32)
        )
    )
)

dataset = training_dataset
dataset = dataset.repeat().batch(batch_size).prefetch(batch_size)
dataset_iter = tfe.Iterator(dataset)


d = dataset_iter.next()

x_test = d[0]

y_test = tf.cast(d[1], dtype=tf.int64)
# Evaluate model on the test set


test_acc = accuracy_fn(neural_net, x_test, y_test)
print("Testset Accuracy: {:.4f}".format(test_acc))