'''
A logistic regression learning algorithm example using TensorFlow library.
'''

from __future__ import print_function
import tensorflow as tf 

#import
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot = True)

#parameters
learning_rate = 0.01
training_epochs = 25
batch_size = 100
display_step = 1

#tf graph input

x = tf.placeholder(tf.float32, [None, 784]) #mnist data image of shape 784
y = tf.placeholder(tf.float32, [None, 10]) # 0-9 digits recognition->10 classes

#Set model weights

W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))

#Construct model
pred = tf.nn.softmax(tf.matmul( x, W ) + b) #softmax

#Minimize error using cross entropy
cost = tf.reduce_mean( - tf.reduce_sum(y * tf.log(pred), reduction_indices = 1))

#Gradient descent
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

#initializing the variables
init = tf.global_variables_initializer()

#launch the grap
with tf.Session() as sess:
	sess.run(init)

	#Training cycle
	for epoch in range(training_epochs):
		avg_cost = 0
		#print(mnist.train.num_examples)
		total_batch = int(mnist.train.num_examples / batch_size)
		#lopp over all batchs
		for i in range(total_batch):
			batch_xs, batch_ys = mnist.train.next_batch(batch_size)
			#run optimization op (backprop) and cost op(to get the loss value)
			_, c = sess.run([optimizer, cost], feed_dict={x: batch_xs, y: batch_ys})
			#compute average loss
			avg_cost += c/total_batch
		#Display logs per epoch step
		if (epoch +1 ) % display_step ==0:
			print("Epoch:", '%04d' % (epoch +1), "cost:", "{:.9f}".format(avg_cost))

	print("optimization finished")

	#test model

	correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y,1))

	#calculate accuracy
	accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
	print("Accuracy:", accuracy.eval({x: mnist.test.images, y: mnist.test.labels}))