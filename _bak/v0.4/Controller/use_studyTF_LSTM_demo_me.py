""" Recurrent Neural Network.
A Recurrent Neural Network (LSTM) implementation example using TensorFlow library.
This example is using the MNIST database of handwritten digits (http://yann.lecun.com/exdb/mnist/)
Links:
    [Long Short Term Memory](http://deeplearning.cs.cmu.edu/pdfs/Hochreiter97_lstm.pdf)
    [MNIST Dataset](http://yann.lecun.com/exdb/mnist/).
Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
"""

from __future__ import print_function

import tensorflow as tf
from tensorflow.contrib import rnn

# Import MNIST data
from tensorflow.examples.tutorials.mnist import input_data


def RNN(x, weights, biases):
    timesteps = 28 # timesteps
    num_hidden = 128 # hidden layer num of features


    # Prepare data shape to match `rnn` function requirements
    # Current data input shape: (batch_size, timesteps, n_input)
    # Required shape: 'timesteps' tensors list of shape (batch_size, n_input)

    # Unstack to get a list of 'timesteps' tensors of shape (batch_size, n_input)
    x = tf.unstack(x, timesteps, 1)

    # Define a lstm cell with tensorflow
    lstm_cell = rnn.BasicLSTMCell(num_hidden, forget_bias=1.0)

    # Get lstm cell output
    outputs, states = rnn.static_rnn(lstm_cell, x, dtype=tf.float32)

    # Linear activation, using rnn inner loop last output
    return tf.matmul(outputs[-1], weights['out']) + biases['out']

def main(): 

    '''
    To classify images using a recurrent neural network, we consider every image
    row as a sequence of pixels. Because MNIST image shape is 28*28px, we will then
    handle 28 sequences of 28 steps for every sample.
    '''

    # Training Parameters
    learning_rate = 0.001
    # training_steps = 10000
    training_steps = 10
    batch_size = 128
    display_step = 200

    # Network Parameters
    num_input = 28 # MNIST data input (img shape: 28*28)
    timesteps = 28 # timesteps
    num_hidden = 128 # hidden layer num of features
    num_classes = 10 # MNIST total classes (0-9 digits)

    # tf Graph input
    X = tf.placeholder("float", [None, timesteps, num_input])
    Y = tf.placeholder("float", [None, num_classes])

    # Define weights
    weights = {
        'out': tf.Variable(tf.random_normal([num_hidden, num_classes]))
    }
    biases = {
        'out': tf.Variable(tf.random_normal([num_classes]))
    }


    logits = RNN(X, weights, biases)
    prediction = tf.nn.softmax(logits) # prediction-预测

    # Define loss and optimizer
    # 定义 损失函数 和 优化器
    loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
        logits=logits, labels=Y))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
    train_op = optimizer.minimize(loss_op)

    # Evaluate model (with test logits, for dropout to be disabled)
    # 评估模型（使用测试日志，禁用dropout）
    correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    '''
    # Initialize the variables (i.e. assign their default value)
    # 初始化变量（即分配它们的默认值）
    init = tf.global_variables_initializer()
    '''

    # 声明tf.train.Saver类用于保存/加载模型
    saver = tf.train.Saver() 

    ''' ********************************************************************************** '''

    mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

    with tf.Session() as sess:

        #  即将固化到硬盘中的Session从保存路径再读取出来
        saver.restore(sess, "save/model.ckpt")

        # Calculate accuracy for 128 mnist test images
        # 计算128个mnist测试图像的准确性
        test_len = 128
        test_data = mnist.test.images[:test_len].reshape((-1, timesteps, num_input))
        test_label = mnist.test.labels[:test_len]
        print("Testing Accuracy(测试精度):", \
            sess.run(accuracy, feed_dict={X: test_data, Y: test_label}))

        # 分类
        test_len = 1
        test_data = mnist.test.images[:test_len].reshape((-1, timesteps, num_input))
        test_label = mnist.test.labels[:test_len]
        print(test_data.shape, test_label)
        print("分类:", \
            sess.run(prediction, feed_dict={X: test_data}))


if __name__=='__main__':
    main()
