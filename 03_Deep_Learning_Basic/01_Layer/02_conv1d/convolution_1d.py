import tensorflow.compat.v1 as tf1
tf1.disable_v2_behavior()
import tensorflow as tf
import numpy as np
"""
Tensorflow
+ https://riptutorial.com/tensorflow/example/30750/math-behind-1d-convolution-with-advanced-examples-in-tf
So if your input = [1, 0, 2, 3, 0, 1, 1] and kernel = [2, 1, 3] the result of the convolution is [8, 11, 7, 9, 4], 
which is calculated in the following way:

8 = 1 * 2 + 0 * 1 + 2 * 3
11 = 0 * 2 + 2 * 1 + 3 * 3
7 = 2 * 2 + 3 * 1 + 0 * 3
9 = 3 * 2 + 0 * 1 + 1 * 3
4 = 0 * 2 + 1 * 1 + 1 * 3
"""
def tf1_conv_1d():
    i = tf1.constant([1, 0, 2, 3, 0, 1, 1], dtype=tf1.float32, name='i')
    k = tf1.constant([2, 1, 3], dtype=tf1.float32, name='k')

    print(i, '\n', k, '\n')
    data   = tf1.reshape(i, [1, int(i.shape[0]), 1], name='data')
    kernel = tf1.reshape(k, [int(k.shape[0]), 1, 1], name='kernel')


    print(data, '\n', kernel, '\n')

    res = tf1.squeeze(tf1.nn.conv1d(data, kernel, 1, 'VALID'))
    with tf1.Session() as sess:
        print(sess.run(res))


def tf2_conv_1d():
    # The inputs are 128-length vectors with 10 timesteps, and the
    # batch size is 4.
    x = np.random.rand(1, 10, 128)
    y = tf.keras.layers.Conv1D(32, 3, strides=1, padding="SAME")(x)
    print(y.shape)
'''
Pytorch
Onnx
'''

if __name__ == '__main__':
    tf2_conv_1d()