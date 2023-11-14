import os
import time
import pandas as pd
import tensorflow as tf

def benchmark(device: str, size):
    tf.compat.v1.reset_default_graph()
    start = time.time()
    with tf.device(device):
        v1 = tf.Variable(tf.random.normal((size, size)))
        v2 = tf.Variable(tf.random.normal((size, size)))
        op = tf.matmul(v1, v2)

    with tf.compat.v1.Session() as sess:
        sess.run(tf.compat.v1.global_variables_initializer())
        sess.run(op)
    return time.time() - start

if __name__ == '__main__':
    tf.compat.v1.disable_eager_execution()
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    num_trials = 5
    sizes = [2, 16, 32, 64, 128, 256, 512, 768, 1024, 2048, 3000, 4096, 5000, 8000, 10000]
    # sizes = [2, 16, 32, 64, 128, 256, 512, 1024, 2048]
    # sizes = [2, 10, 30, 60, 130, 250, 500, 800, 1000, 2000]
    df = pd.DataFrame(columns=['device', 'size', 'time'])

    for device in ['cpu:0', 'gpu:0']:
        benchmark(device, sizes[0])
        for size in sizes:
            print(device, size)
            for _ in range(num_trials):
                df.loc[len(df)] = device, size, benchmark(device, size)
    # df = df.groupby(['device', 'size', 'time']).mean()

    import seaborn as sns
    import matplotlib.pyplot as plt

    sns.lineplot(
        data=df,
        x='size',
        y='time',
        hue='device'
    )
    plt.xscale('log')
    plt.yscale('log')
    plt.show()

    df = df.groupby(['device', 'size']).mean().reset_index()
    ratio = df.loc[df.device == 'gpu:0', 'time'].values / df.loc[df.device == 'cpu:0', 'time'].values
    sns.lineplot(
        y=ratio,
        x=sizes
    )
    plt.xscale('log')
    # plt.yscale('log')
    plt.show()
