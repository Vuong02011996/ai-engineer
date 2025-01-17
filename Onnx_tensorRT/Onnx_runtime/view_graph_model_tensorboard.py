import tensorflow as tf
import numpy as np
import os


class BeatModel:
    def __init__(
            self,
            feature_len,
            num_of_class,
            from_logit=False,
            num_filters=None,
            num_loop=7,
            rate=0.5,
            name='beat_concat_seq_add'
    ):
        if num_filters is None:
            num_filters = [(16, 16), (16, 32), (32, 48), (48, 64)]
        else:
            tmp = []
            for i, f in enumerate(num_filters):
                if len(tmp) == 0:
                    tmp.append((f, f))
                else:
                    tmp.append((tmp[-1][-1], f))

            num_filters = tmp.copy()

        input_layer = tf.keras.Input(shape=(feature_len,))
        resnet_input_layer = tf.keras.layers.Reshape((feature_len, 1))(input_layer)

        # Convolution(stride=2)
        x = self.conv1d_net(
            x=resnet_input_layer,
            num_filters=num_filters[0][0],
            kernel_size=3,
            strides=2,
            pad='SAME',
            act=False,
            bn=False,
            rate=1.0,
            name="input_stage"
        )

        for st, (f1, f2) in enumerate(num_filters):
            st += 1
            name = f'stage_{st}'

            # 1x1 Convolution (stride=2)
            x_skip = self.conv1d_net(
                x=x,
                num_filters=f2,
                kernel_size=1,
                strides=2,
                pad='SAME',
                act=False,
                bn=False,
                rate=1.0,
                name="skip12_" + name
            )

            # Batch norm, Activation, Dropout, Convolution (stride=2)
            x = self.conv1d_net(
                x=x,
                num_filters=f1,
                kernel_size=3,
                strides=2,
                pad='SAME',
                act=True,
                bn=True,
                rate=0.5,
                name="resnet12" + name
            )

            # Batch norm, Activation, Dropout, Convolution (stride=1)
            x = self.conv1d_net(
                x=x,
                num_filters=f2,
                kernel_size=3,
                strides=1,
                pad='SAME',
                act=True,
                bn=True,
                rate=0.5,
                name="resnet11" + name
            )

            x = tf.keras.layers.Add(
                name="add_" + name
            )([x, x_skip])

            ffs = [(f2, f2) for _ in range(num_loop)]
            for sl, ffl in enumerate(ffs):
                x = self.block1d(
                    xx=x,
                    ff=ffl,
                    stage=name,
                    step=sl
                )

        with tf.compat.v1.variable_scope('collected') as scope:
            bxx = x[:, :-2, :]
            bzz = tf.zeros_like(x[:, 0:2, :])
            bxx = tf.concat((bzz, bxx), axis=1)

            xx = x[:, :-1, :]
            zz = tf.zeros_like(x[:, 0:1, :])
            xx = tf.concat((zz, xx), axis=1)

            yy = x[:, 1:, :]
            zz = tf.zeros_like(x[:, 0:1, :])
            yy = tf.concat((yy, zz), axis=1)

            ayy = x[:, 2:, :]
            azz = tf.zeros_like(x[:, 0:2, :])
            ayy = tf.concat((ayy, azz), axis=1)

            x = tf.concat((bxx, xx, x, yy, ayy), axis=2)

        logit_layer1 = tf.keras.layers.Dense(num_of_class)(x)

        lstm_layer = tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate)
        lstm_dec = tf.keras.layers.Bidirectional(lstm_layer)(x)
        lstm_dec = tf.keras.layers.Bidirectional(lstm_layer)(lstm_dec)
        logit_layer2 = tf.keras.layers.Dense(num_of_class)(lstm_dec)

        output_layer = tf.keras.layers.Add()([logit_layer1, logit_layer2])
        if not from_logit:
            output_layer = tf.keras.layers.Softmax(axis=-1)(output_layer)

        self.model = tf.keras.Model(input_layer, output_layer, name=name)

    @staticmethod
    def conv1d_net(
            x,
            num_filters,
            kernel_size,
            strides=1,
            pad='SAME',
            act=True,
            bn=True,
            rate=0.5,
            name=""
    ):

        if bn:
            x = tf.keras.layers.BatchNormalization(axis=-1, name=name + '_bn')(x)

        if act:
            x = tf.keras.layers.ReLU(name=name + '_act')(x)

        if rate < 1.0:
            x = tf.keras.layers.Dropout(rate=rate, name=name + '_drop')(x)

        x = tf.keras.layers.Conv1D(
            filters=num_filters,
            kernel_size=kernel_size,
            strides=strides,
            padding=pad,
            name=name + '_conv1d'
        )(x)

        return x

    def block1d(
            self,
            xx,
            ff,
            stage,
            step
    ):

        xx_skip = xx
        f1, f2 = ff

        # Batch norm, Activation, Dropout, Convolution (stride=1)
        xx = self.conv1d_net(
            x=xx,
            num_filters=f1,
            kernel_size=3,
            strides=1,
            pad='SAME',
            act=True,
            bn=True,
            rate=0.5,
            name='resnet11a_{}_{}'.format(step, stage)
        )

        # Batch norm, Activation, Dropout, Convolution (stride=1)
        xx = self.conv1d_net(
            x=xx,
            num_filters=f2,
            kernel_size=3,
            strides=1,
            pad='SAME',
            act=True,
            bn=True,
            rate=0.5,
            name='resnet11b_{}_{}'.format(step, stage)
        )

        xx = tf.keras.layers.Add(name='skip11_{}_{}'.format(step, stage))([xx, xx_skip])

        return xx


def main():
    _qrs_model_path = MODEL_NAME.split('_')
    func = ''
    m = 0
    for m in range(len(_qrs_model_path)):
        if _qrs_model_path[m].isnumeric():
            break
        else:
            func += _qrs_model_path[m] + '_'
    
    num_loop = int(_qrs_model_path[m])
    num_filters = np.asarray([int(i) for i in _qrs_model_path[m + 1].split('.')], dtype=int)
    try:
        from_logit = bool(int(_qrs_model_path[m + 2]))
    except (Exception,):
        from_logit = False
    
    function = BeatModel(
            feature_len=FEATURE_LENGTH,
            num_of_class=len(BEAT_CLASSES.keys()),
            from_logit=from_logit,
            num_filters=num_filters,
            num_loop=num_loop,
            rate=float(_qrs_model_path[-1]),
    )
    function.model.load_weights(tf.train.latest_checkpoint(CKPT_DIR)).expect_partial()
    
    # # Save the model to a .pb file
    # tf.saved_model.save(function.model, "model_beat")
    # print("Model saved successfully")

    # Load the model and create a TensorBoard log directory
    log_dir = "logs/beat_model"
    os.makedirs(log_dir, exist_ok=True)

    # Create a summary writer
    writer = tf.summary.create_file_writer(log_dir)

    # Use the writer to log the model graph
    tf.summary.trace_on(graph=True, profiler=True)
    # Run a dummy input through the model to log the graph
    dummy_input = np.zeros((1, FEATURE_LENGTH), dtype=np.float32)
    function.model(dummy_input)
    with writer.as_default():
        tf.summary.trace_export(name="BeatModel", step=0, profiler_outdir=log_dir)

    print(f"TensorBoard logs saved in {log_dir}")
    
    print(f"TensorBoard logs saved in {log_dir}")
if __name__ == '__main__':
    # MODEL_NAME = 'beat_concat_seq_add_more_other_7_16.32.48.64_0_0.5'
    MODEL_NAME = 'beat_concat_seq_add_more_other_7_16.32.48.64_0_0.5'
    FEATURE_LENGTH  = 15360
    BEAT_CLASSES    = {
        "NOTABEAT": [],
        "ARTIFACT": [],
        "N": [],
        "A": [],
        "V": [],
        "R": [],
        "Q": []
    }
    
    CKPT_DIR = '/home/server2/Desktop/Vuong/models/210929/256_60.0_480_0_0_0_2_0_0.8/output-3.780749/model/beat_concat_seq_add_more_other_7_16.32.48.64_0_0.5/best_squared_error_metric'
    main()
