import tensorflow as tf

class BeatModel:
    @staticmethod
    def conv1d_net(x,
                   num_filters,
                   kernel_size,
                   strides=1,
                   pad='SAME',
                   act=True,
                   bn=True,
                   rate=0.5,
                   name=""):
        if bn:
            x = tf.keras.layers.BatchNormalization(axis=-1, name=name + '_bn')(x)

        if act:
            x = tf.keras.layers.ReLU(name=name + '_act')(x)

        if rate < 1.0:
            x = tf.keras.layers.Dropout(rate=rate, name=name + '_drop')(x)

        x = tf.keras.layers.Conv1D(filters=num_filters,
                                   kernel_size=kernel_size,
                                   strides=strides,
                                   padding=pad,
                                   name=name + '_conv1d')(x)

        return x

    def block1d_loop(self, xx, ff, stage, step):
        xx_skip = xx
        f1, f2 = ff
        # Batch norm, Activation, Dropout, Convolution (stride=1)
        xx = self.conv1d_net(x=xx,
                             num_filters=f1,
                             kernel_size=3,
                             strides=1,
                             pad='SAME',
                             act=True,
                             bn=True,
                             rate=0.5,
                             name='resnet11a_{}_{}'.format(step, stage))
        # Batch norm, Activation, Dropout, Convolution (stride=1)
        xx = self.conv1d_net(x=xx,
                             num_filters=f2,
                             kernel_size=3,
                             strides=1,
                             pad='SAME',
                             act=True,
                             bn=True,
                             rate=0.5,
                             name='resnet11b_{}_{}'.format(step, stage))

        xx = tf.keras.layers.Add(name='skip11_{}_{}'.format(step, stage))([xx, xx_skip])
        return xx

    def selection_net(self,
                      feature_len,
                      num_of_class=2,
                      from_logits=False,
                      filters_rhythm_net=None,
                      num_loop=9,
                      rate=0.5,
                      name='selection_net'):
        if filters_rhythm_net is None:
            filters_rhythm_net = [(16, 16),
                                  (16, 32),
                                  (32, 48),
                                  (48, 64),
                                  (64, 80),
                                  (80, 96),
                                  (96, 112)]
        else:
            tmp = []
            for i, f in enumerate(filters_rhythm_net):
                tmp.append((max(f - filters_rhythm_net[0], filters_rhythm_net[0]), f))

            filters_rhythm_net = tmp.copy()

        input_layer = tf.keras.layers.Input(shape=(feature_len * 3,))
        resnet_input_layer = tf.keras.layers.Reshape((feature_len, 3))(input_layer)
        # Convolution(stride=2)
        x = self.conv1d_net(x=resnet_input_layer,
                            num_filters=16,
                            kernel_size=3,
                            strides=2,
                            pad='SAME',
                            act=False,
                            bn=False,
                            rate=1.0,
                            name='input_stage')

        for st, ff in enumerate(filters_rhythm_net):
            st += 1
            f1, f2 = ff
            name = 'stage_{}'.format(st)
            # 1x1 Convolution (stride=2)
            x_skip = self.conv1d_net(x=x,
                                     num_filters=f2,
                                     kernel_size=1,
                                     strides=2,
                                     pad='SAME',
                                     act=False,
                                     bn=False,
                                     rate=1.0,
                                     name='skip12_' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=2)
            x = self.conv1d_net(x=x,
                                num_filters=f1,
                                kernel_size=3,
                                strides=2,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=rate,
                                name='resnet12' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=1)
            x = self.conv1d_net(x=x,
                                num_filters=f2,
                                kernel_size=3,
                                strides=1,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=rate,
                                name='resnet11' + name)

            x = tf.keras.layers.Add(name='add_' + name)([x, x_skip])
            ffs = [(f2, f2) for _ in range(num_loop)]
            for sl, ffl in enumerate(ffs):
                x = self.block1d_loop(x, ffl, name, sl)

        logits_layer = tf.keras.layers.Dense(num_of_class)(x)
        softmax_layer = tf.keras.layers.Softmax(axis=-1)(logits_layer)
        if not from_logits:
            return tf.keras.Model(input_layer, softmax_layer, name=name)
        else:
            return tf.keras.Model(input_layer, logits_layer, name=name)

    def rhythm_net(self,
                   feature_len,
                   num_of_class=2,
                   from_logits=False,
                   filters_rhythm_net=None,
                   num_loop=9,
                   rate=0.5,
                   name='rhythm_net'):

        if filters_rhythm_net is None:
            filters_rhythm_net = [(16, 16),
                                  (16, 32),
                                  (32, 48),
                                  (48, 64),
                                  (64, 80),
                                  (80, 96),
                                  (96, 112)]
        else:
            tmp = []
            for i, f in enumerate(filters_rhythm_net):
                tmp.append((max(f - filters_rhythm_net[0], filters_rhythm_net[0]), f))

            filters_rhythm_net = tmp.copy()

        input_layer = tf.keras.layers.Input(shape=(feature_len,))
        resnet_input_layer = tf.keras.layers.Reshape((feature_len, 1))(input_layer)
        # Convolution(stride=2)
        x = self.conv1d_net(x=resnet_input_layer,
                            num_filters=16,
                            kernel_size=3,
                            strides=2,
                            pad='SAME',
                            act=False,
                            bn=False,
                            rate=1.0,
                            name='input_stage')

        for st, ff in enumerate(filters_rhythm_net):
            st += 1
            f1, f2 = ff
            name = 'stage_{}'.format(st)
            # 1x1 Convolution (stride=2)
            x_skip = self.conv1d_net(x=x,
                                     num_filters=f2,
                                     kernel_size=1,
                                     strides=2,
                                     pad='SAME',
                                     act=False,
                                     bn=False,
                                     rate=1.0,
                                     name='skip12_' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=2)
            x = self.conv1d_net(x=x,
                                num_filters=f1,
                                kernel_size=3,
                                strides=2,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=rate,
                                name='resnet12' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=1)
            x = self.conv1d_net(x=x,
                                num_filters=f2,
                                kernel_size=3,
                                strides=1,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=rate,
                                name='resnet11' + name)

            x = tf.keras.layers.Add(name='add_' + name)([x, x_skip])
            ffs = [(f2, f2) for _ in range(num_loop)]
            for sl, ffl in enumerate(ffs):
                x = self.block1d_loop(x, ffl, name, sl)

        logits_layer = tf.keras.layers.Dense(num_of_class)(x)
        softmax_layer = tf.keras.layers.Softmax(axis=-1)(logits_layer)
        if not from_logits:
            return tf.keras.Model(input_layer, softmax_layer, name=name)
        else:
            return tf.keras.Model(input_layer, logits_layer, name=name)

    def rhythm_seq(self,
                   feature_len,
                   num_of_class=2,
                   from_logits=False,
                   filters_rhythm_net=None,
                   num_loop=9,
                   rate=0.5,
                   name='rhythm_seq'):

        if filters_rhythm_net is None:
            filters_rhythm_net = [(16, 16),
                                  (16, 32),
                                  (32, 48),
                                  (48, 64),
                                  (64, 80),
                                  (80, 96),
                                  (96, 112)]
        else:
            tmp = []
            for i, f in enumerate(filters_rhythm_net):
                tmp.append((max(f - filters_rhythm_net[0], filters_rhythm_net[0]), f))

            filters_rhythm_net = tmp.copy()

        input_layer = tf.keras.layers.Input(shape=(feature_len,))
        resnet_input_layer = tf.keras.layers.Reshape((feature_len, 1))(input_layer)
        # Convolution(stride=2)
        x = self.conv1d_net(x=resnet_input_layer,
                            num_filters=16,
                            kernel_size=3,
                            strides=2,
                            pad='SAME',
                            act=False,
                            bn=False,
                            rate=1.0,
                            name='input_stage')

        for st, ff in enumerate(filters_rhythm_net):
            st += 1
            f1, f2 = ff
            name = 'stage_{}'.format(st)
            # 1x1 Convolution (stride=2)
            x_skip = self.conv1d_net(x=x,
                                     num_filters=f2,
                                     kernel_size=1,
                                     strides=2,
                                     pad='SAME',
                                     act=False,
                                     bn=False,
                                     rate=1.0,
                                     name='skip12_' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=2)
            x = self.conv1d_net(x=x,
                                num_filters=f1,
                                kernel_size=3,
                                strides=2,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=rate,
                                name='resnet12' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=1)
            x = self.conv1d_net(x=x,
                                num_filters=f2,
                                kernel_size=3,
                                strides=1,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=rate,
                                name='resnet11' + name)

            x = tf.keras.layers.Add(name='add_' + name)([x, x_skip])
            ffs = [(f2, f2) for _ in range(num_loop)]
            for sl, ffl in enumerate(ffs):
                x = self.block1d_loop(x, ffl, name, sl)

        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(x)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer)

        logits_layer = tf.keras.layers.Dense(num_of_class)(lstm_layer)
        softmax_layer = tf.keras.layers.Softmax(axis=-1)(logits_layer)
        if not from_logits:
            return tf.keras.Model(input_layer, softmax_layer, name=name)
        else:
            return tf.keras.Model(input_layer, logits_layer, name=name)

    def rhythm_seq_add(self,
                       feature_len,
                       num_of_class=2,
                       from_logits=False,
                       filters_rhythm_net=None,
                       num_loop=9,
                       rate=0.5,
                       name='rhythm_seq_add'):
        if filters_rhythm_net is None:
            filters_rhythm_net = [(16, 16),
                                  (16, 32),
                                  (32, 48),
                                  (48, 64),
                                  (64, 80),
                                  (80, 96),
                                  (96, 112)]
        else:
            tmp = []
            for i, f in enumerate(filters_rhythm_net):
                tmp.append((max(f - filters_rhythm_net[0], filters_rhythm_net[0]), f))

            filters_rhythm_net = tmp.copy()

        input_layer = tf.keras.layers.Input(shape=(feature_len,))
        resnet_input_layer = tf.keras.layers.Reshape((feature_len, 1))(input_layer)
        # Convolution(stride=2)
        x = self.conv1d_net(x=resnet_input_layer,
                            num_filters=16,
                            kernel_size=3,
                            strides=2,
                            pad='SAME',
                            act=False,
                            bn=False,
                            rate=1.0,
                            name='input_stage')

        for st, ff in enumerate(filters_rhythm_net):
            st += 1
            f1, f2 = ff
            name = 'stage_{}'.format(st)
            # 1x1 Convolution (stride=2)
            x_skip = self.conv1d_net(x=x,
                                     num_filters=f2,
                                     kernel_size=1,
                                     strides=2,
                                     pad='SAME',
                                     act=False,
                                     bn=False,
                                     rate=1.0,
                                     name='skip12_' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=2)
            x = self.conv1d_net(x=x,
                                num_filters=f1,
                                kernel_size=3,
                                strides=2,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=rate,
                                name='resnet12' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=1)
            x = self.conv1d_net(x=x,
                                num_filters=f2,
                                kernel_size=3,
                                strides=1,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=rate,
                                name='resnet11' + name)

            x = tf.keras.layers.Add(name='add_' + name)([x, x_skip])
            ffs = [(f2, f2) for _ in range(num_loop)]
            for sl, ffl in enumerate(ffs):
                x = self.block1d_loop(x, ffl, name, sl)

        logits_layer1 = tf.keras.layers.Dense(num_of_class)(x)

        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(x)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer)
        logits_layer2 = tf.keras.layers.Dense(num_of_class)(lstm_layer)

        logits_layer = tf.keras.layers.Add()([logits_layer1, logits_layer2])
        softmax_layer = tf.keras.layers.Softmax(axis=-1)(logits_layer)
        if not from_logits:
            return tf.keras.Model(input_layer, softmax_layer, name=name)
        else:
            return tf.keras.Model(input_layer, logits_layer, name=name)

    def beat_net(self,
                 feature_len,
                 num_of_class=2,
                 from_logits=False,
                 filters_rhythm_net=None,
                 num_loop=7,
                 rate=0.5,
                 name='beat_net'):

        if filters_rhythm_net is None:
            filters_rhythm_net = [(16, 16),
                                  (16, 32),
                                  (32, 48),
                                  (48, 64)]
        else:
            tmp = []
            for i, f in enumerate(filters_rhythm_net):
                if len(tmp) == 0:
                    tmp.append((f, f))
                else:
                    tmp.append((tmp[-1][-1], f))

            filters_rhythm_net = tmp.copy()

        input_layer = tf.keras.layers.Input(shape=(feature_len,))
        resnet_input_layer = tf.keras.layers.Reshape((feature_len, 1))(input_layer)
        # Convolution(stride=2)
        x = self.conv1d_net(x=resnet_input_layer,
                            num_filters=filters_rhythm_net[0][0],
                            kernel_size=3,
                            strides=2,
                            pad='SAME',
                            act=False,
                            bn=False,
                            rate=1.0,
                            name='input_stage')

        for st, ff in enumerate(filters_rhythm_net):
            st += 1
            f1, f2 = ff
            name = 'stage_{}'.format(st)
            # 1x1 Convolution (stride=2)
            x_skip = self.conv1d_net(x=x,
                                     num_filters=f2,
                                     kernel_size=1,
                                     strides=2,
                                     pad='SAME',
                                     act=False,
                                     bn=False,
                                     rate=1.0,
                                     name='skip12_' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=2)
            x = self.conv1d_net(x=x,
                                num_filters=f1,
                                kernel_size=3,
                                strides=2,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=rate,
                                name='resnet12' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=1)
            x = self.conv1d_net(x=x,
                                num_filters=f2,
                                kernel_size=3,
                                strides=1,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=rate,
                                name='resnet11' + name)

            x = tf.keras.layers.Add(name='add_' + name)([x, x_skip])
            ffs = [(f2, f2) for _ in range(num_loop)]
            for sl, ffl in enumerate(ffs):
                x = self.block1d_loop(x, ffl, name, sl)

        logits_layer = tf.keras.layers.Dense(num_of_class)(x)
        softmax_layer = tf.keras.layers.Softmax(axis=-1)(logits_layer)
        if not from_logits:
            return tf.keras.Model(input_layer, softmax_layer, name=name)
        else:
            return tf.keras.Model(input_layer, logits_layer, name=name)

    def beat_seq(self,
                 feature_len,
                 num_of_class=2,
                 from_logits=False,
                 filters_rhythm_net=None,
                 num_loop=7,
                 rate=0.5,
                 name='beat_seq'):
        if filters_rhythm_net is None:
            filters_rhythm_net = [(16, 16),
                                  (16, 32),
                                  (32, 48),
                                  (48, 64)]
        else:
            tmp = []
            for i, f in enumerate(filters_rhythm_net):
                if len(tmp) == 0:
                    tmp.append((f, f))
                else:
                    tmp.append((tmp[-1][-1], f))

            filters_rhythm_net = tmp.copy()

        input_layer = tf.keras.layers.Input(shape=(feature_len,))
        resnet_input_layer = tf.keras.layers.Reshape((feature_len, 1))(input_layer)
        # Convolution(stride=2)
        x = self.conv1d_net(x=resnet_input_layer,
                            num_filters=filters_rhythm_net[0][0],
                            kernel_size=3,
                            strides=2,
                            pad='SAME',
                            act=False,
                            bn=False,
                            rate=1.0,
                            name='input_stage')

        for st, ff in enumerate(filters_rhythm_net):
            st += 1
            f1, f2 = ff
            name = 'stage_{}'.format(st)
            # 1x1 Convolution (stride=2)
            x_skip = self.conv1d_net(x=x,
                                     num_filters=f2,
                                     kernel_size=1,
                                     strides=2,
                                     pad='SAME',
                                     act=False,
                                     bn=False,
                                     rate=1.0,
                                     name='skip12_' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=2)
            x = self.conv1d_net(x=x,
                                num_filters=f1,
                                kernel_size=3,
                                strides=2,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet12' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=1)
            x = self.conv1d_net(x=x,
                                num_filters=f2,
                                kernel_size=3,
                                strides=1,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet11' + name)

            x = tf.keras.layers.Add(name='add_' + name)([x, x_skip])
            ffs = [(f2, f2) for _ in range(num_loop)]
            for sl, ffl in enumerate(ffs):
                x = self.block1d_loop(x, ffl, name, sl)

        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(x)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer)

        logits_layer = tf.keras.layers.Dense(num_of_class)(lstm_layer)
        softmax_layer = tf.keras.layers.Softmax(axis=-1)(logits_layer)
        if not from_logits:
            return tf.keras.Model(input_layer, softmax_layer, name=name)
        else:
            return tf.keras.Model(input_layer, logits_layer, name=name)

    def beat_seq_add(self,
                     feature_len,
                     num_of_class=2,
                     from_logits=False,
                     filters_rhythm_net=None,
                     num_loop=7,
                     rate=0.5,
                     name='beat_seq_add'):

        if filters_rhythm_net is None:
            filters_rhythm_net = [(16, 16),
                                  (16, 32),
                                  (32, 48),
                                  (48, 64)]
        else:
            tmp = []
            for i, f in enumerate(filters_rhythm_net):
                if len(tmp) == 0:
                    tmp.append((f, f))
                else:
                    tmp.append((tmp[-1][-1], f))

            filters_rhythm_net = tmp.copy()

        input_layer = tf.keras.layers.Input(shape=(feature_len,))
        resnet_input_layer = tf.keras.layers.Reshape((feature_len, 1))(input_layer)
        # Convolution(stride=2)
        x = self.conv1d_net(x=resnet_input_layer,
                            num_filters=filters_rhythm_net[0][0],
                            kernel_size=3,
                            strides=2,
                            pad='SAME',
                            act=False,
                            bn=False,
                            rate=1.0,
                            name='input_stage')

        for st, ff in enumerate(filters_rhythm_net):
            st += 1
            f1, f2 = ff
            name = 'stage_{}'.format(st)
            # 1x1 Convolution (stride=2)
            x_skip = self.conv1d_net(x=x,
                                     num_filters=f2,
                                     kernel_size=1,
                                     strides=2,
                                     pad='SAME',
                                     act=False,
                                     bn=False,
                                     rate=1.0,
                                     name='skip12_' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=2)
            x = self.conv1d_net(x=x,
                                num_filters=f1,
                                kernel_size=3,
                                strides=2,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet12' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=1)
            x = self.conv1d_net(x=x,
                                num_filters=f2,
                                kernel_size=3,
                                strides=1,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet11' + name)

            x = tf.keras.layers.Add(name='add_' + name)([x, x_skip])
            ffs = [(f2, f2) for _ in range(num_loop)]
            for sl, ffl in enumerate(ffs):
                x = self.block1d_loop(x, ffl, name, sl)

        logits_layer1 = tf.keras.layers.Dense(num_of_class)(x)

        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(x)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer)

        logits_layer2 = tf.keras.layers.Dense(num_of_class)(lstm_layer)

        logits_layer = tf.keras.layers.Add()([logits_layer1, logits_layer2])
        softmax_layer = tf.keras.layers.Softmax(axis=-1)(logits_layer)
        if not from_logits:
            return tf.keras.Model(input_layer, softmax_layer, name=name)
        else:
            return tf.keras.Model(input_layer, logits_layer, name=name)

    def beat_concat_seq(self,
                        feature_len,
                        num_of_class=2,
                        from_logits=False,
                        filters_rhythm_net=None,
                        num_loop=7,
                        rate=0.5,
                        name='beat_concat_seq'):

        if filters_rhythm_net is None:
            filters_rhythm_net = [(16, 16),
                                  (16, 32),
                                  (32, 48),
                                  (48, 64)]
        else:
            tmp = []
            for i, f in enumerate(filters_rhythm_net):
                if len(tmp) == 0:
                    tmp.append((f, f))
                else:
                    tmp.append((tmp[-1][-1], f))

            filters_rhythm_net = tmp.copy()

        input_layer = tf.keras.layers.Input(shape=(feature_len,))
        resnet_input_layer = tf.keras.layers.Reshape((feature_len, 1))(input_layer)
        # Convolution(stride=2)
        x = self.conv1d_net(x=resnet_input_layer,
                            num_filters=filters_rhythm_net[0][0],
                            kernel_size=3,
                            strides=2,
                            pad='SAME',
                            act=False,
                            bn=False,
                            rate=1.0,
                            name='input_stage')

        for st, ff in enumerate(filters_rhythm_net):
            st += 1
            f1, f2 = ff
            name = 'stage_{}'.format(st)
            # 1x1 Convolution (stride=2)
            x_skip = self.conv1d_net(x=x,
                                     num_filters=f2,
                                     kernel_size=1,
                                     strides=2,
                                     pad='SAME',
                                     act=False,
                                     bn=False,
                                     rate=1.0,
                                     name='skip12_' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=2)
            x = self.conv1d_net(x=x,
                                num_filters=f1,
                                kernel_size=3,
                                strides=2,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet12' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=1)
            x = self.conv1d_net(x=x,
                                num_filters=f2,
                                kernel_size=3,
                                strides=1,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet11' + name)

            x = tf.keras.layers.Add(name='add_' + name)([x, x_skip])
            ffs = [(f2, f2) for _ in range(num_loop)]
            for sl, ffl in enumerate(ffs):
                x = self.block1d_loop(x, ffl, name, sl)

        with tf.compat.v1.variable_scope('collected') as scope:
            xx = x[:, 1:, :]
            zz = tf.zeros_like(x[:, 0:1, :])
            xx = tf.concat((xx, zz), axis=1)

            yy = x[:, 2:, :]
            zz = tf.zeros_like(x[:, 0:2, :])
            yy = tf.concat((yy, zz), axis=1)

            xy = x[:, 3:, :]
            zz = tf.zeros_like(x[:, 0:3, :])
            xy = tf.concat((xy, zz), axis=1)

            x = tf.concat((x, xx, yy, xy), axis=2)

        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(x)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer)

        logits_layer = tf.keras.layers.Dense(num_of_class)(lstm_layer)
        softmax_layer = tf.keras.layers.Softmax(axis=-1)(logits_layer)
        if not from_logits:
            return tf.keras.Model(input_layer, softmax_layer, name=name)
        else:
            return tf.keras.Model(input_layer, logits_layer, name=name)

    def beat_concat_seq_other(self,
                              feature_len,
                              num_of_class=2,
                              from_logits=False,
                              filters_rhythm_net=None,
                              num_loop=7,
                              rate=0.5,
                              name='beat_concat_seq'):
        if filters_rhythm_net is None:
            filters_rhythm_net = [(16, 16),
                                  (16, 32),
                                  (32, 48),
                                  (48, 64)]
        else:
            tmp = []
            for i, f in enumerate(filters_rhythm_net):
                if len(tmp) == 0:
                    tmp.append((f, f))
                else:
                    tmp.append((tmp[-1][-1], f))

            filters_rhythm_net = tmp.copy()

        input_layer = tf.keras.layers.Input(shape=(feature_len,))
        resnet_input_layer = tf.keras.layers.Reshape((feature_len, 1))(input_layer)
        # Convolution(stride=2)
        x = self.conv1d_net(x=resnet_input_layer,
                            num_filters=filters_rhythm_net[0][0],
                            kernel_size=3,
                            strides=2,
                            pad='SAME',
                            act=False,
                            bn=False,
                            rate=1.0,
                            name='input_stage')

        for st, ff in enumerate(filters_rhythm_net):
            st += 1
            f1, f2 = ff
            name = 'stage_{}'.format(st)
            # 1x1 Convolution (stride=2)
            x_skip = self.conv1d_net(x=x,
                                     num_filters=f2,
                                     kernel_size=1,
                                     strides=2,
                                     pad='SAME',
                                     act=False,
                                     bn=False,
                                     rate=1.0,
                                     name='skip12_' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=2)
            x = self.conv1d_net(x=x,
                                num_filters=f1,
                                kernel_size=3,
                                strides=2,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet12' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=1)
            x = self.conv1d_net(x=x,
                                num_filters=f2,
                                kernel_size=3,
                                strides=1,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet11' + name)

            x = tf.keras.layers.Add(name='add_' + name)([x, x_skip])
            ffs = [(f2, f2) for _ in range(num_loop)]
            for sl, ffl in enumerate(ffs):
                x = self.block1d_loop(x, ffl, name, sl)

        with tf.compat.v1.variable_scope('collected') as scope:
            xx = x[:, :-1, :]
            zz = tf.zeros_like(x[:, 0:1, :])
            xx = tf.concat((zz, xx), axis=1)

            yy = x[:, 1:, :]
            zz = tf.zeros_like(x[:, 0:1, :])
            yy = tf.concat((yy, zz), axis=1)

            x = tf.concat((xx, x, yy), axis=2)

        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(x)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer)

        logits_layer = tf.keras.layers.Dense(num_of_class)(lstm_layer)
        softmax_layer = tf.keras.layers.Softmax(axis=-1)(logits_layer)
        if not from_logits:
            return tf.keras.Model(input_layer, softmax_layer, name=name)
        else:
            return tf.keras.Model(input_layer, logits_layer, name=name)

    def beat_concat_seq_other2(self,
                               feature_len,
                               num_of_class=2,
                               from_logits=False,
                               filters_rhythm_net=None,
                               num_loop=7,
                               rate=0.5,
                               name='beat_concat_seq'):
        if filters_rhythm_net is None:
            filters_rhythm_net = [(16, 16),
                                  (16, 32),
                                  (32, 48),
                                  (48, 64)]
        else:
            tmp = []
            for i, f in enumerate(filters_rhythm_net):
                if len(tmp) == 0:
                    tmp.append((f, f))
                else:
                    tmp.append((tmp[-1][-1], f))

            filters_rhythm_net = tmp.copy()

        input_layer = tf.keras.layers.Input(shape=(feature_len,))
        resnet_input_layer = tf.keras.layers.Reshape((feature_len, 1))(input_layer)
        # Convolution(stride=2)
        x = self.conv1d_net(x=resnet_input_layer,
                            num_filters=filters_rhythm_net[0][0],
                            kernel_size=3,
                            strides=2,
                            pad='SAME',
                            act=False,
                            bn=False,
                            rate=1.0,
                            name='input_stage')

        for st, ff in enumerate(filters_rhythm_net):
            st += 1
            f1, f2 = ff
            name = 'stage_{}'.format(st)
            # 1x1 Convolution (stride=2)
            x_skip = self.conv1d_net(x=x,
                                     num_filters=f2,
                                     kernel_size=1,
                                     strides=2,
                                     pad='SAME',
                                     act=False,
                                     bn=False,
                                     rate=1.0,
                                     name='skip12_' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=2)
            x = self.conv1d_net(x=x,
                                num_filters=f1,
                                kernel_size=3,
                                strides=2,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet12' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=1)
            x = self.conv1d_net(x=x,
                                num_filters=f2,
                                kernel_size=3,
                                strides=1,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet11' + name)

            x = tf.keras.layers.Add(name='add_' + name)([x, x_skip])
            ffs = [(f2, f2) for _ in range(num_loop)]
            for sl, ffl in enumerate(ffs):
                x = self.block1d_loop(x, ffl, name, sl)

        with tf.compat.v1.variable_scope('collected') as scope:
            xx = x[:, :-1, :]
            zz = tf.zeros_like(x[:, 0:1, :])
            xx = tf.concat((zz, xx), axis=1)

            yy = x[:, 1:, :]
            zz = tf.zeros_like(x[:, 0:1, :])
            yy = tf.concat((yy, zz), axis=1)

        lstm_layer_x = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(x)
        lstm_layer_x = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer_x)

        lstm_layer_xx = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(xx)
        lstm_layer_xx = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer_xx)

        lstm_layer_yy = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(yy)
        lstm_layer_yy = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer_yy)

        lstm_layer = tf.concat((lstm_layer_xx, lstm_layer_x, lstm_layer_yy), axis=2)

        logits_layer = tf.keras.layers.Dense(num_of_class)(lstm_layer)
        softmax_layer = tf.keras.layers.Softmax(axis=-1)(logits_layer)
        if not from_logits:
            return tf.keras.Model(input_layer, softmax_layer, name=name)
        else:
            return tf.keras.Model(input_layer, logits_layer, name=name)

    def beat_concat_seq_add(self,
                            feature_len,
                            num_of_class=2,
                            from_logits=False,
                            filters_rhythm_net=None,
                            num_loop=7,
                            rate=0.5,
                            name='beat_concat_seq_add'):
        if filters_rhythm_net is None:
            filters_rhythm_net = [(16, 16),
                                  (16, 32),
                                  (32, 48),
                                  (48, 64)]
        else:
            tmp = []
            for i, f in enumerate(filters_rhythm_net):
                if len(tmp) == 0:
                    tmp.append((f, f))
                else:
                    tmp.append((tmp[-1][-1], f))

            filters_rhythm_net = tmp.copy()

        input_layer = tf.keras.layers.Input(shape=(feature_len,))
        resnet_input_layer = tf.keras.layers.Reshape((feature_len, 1))(input_layer)
        # Convolution(stride=2)
        x = self.conv1d_net(x=resnet_input_layer,
                            num_filters=filters_rhythm_net[0][0],
                            kernel_size=3,
                            strides=2,
                            pad='SAME',
                            act=False,
                            bn=False,
                            rate=1.0,
                            name='input_stage')

        for st, ff in enumerate(filters_rhythm_net):
            st += 1
            f1, f2 = ff
            name = 'stage_{}'.format(st)
            # 1x1 Convolution (stride=2)
            x_skip = self.conv1d_net(x=x,
                                     num_filters=f2,
                                     kernel_size=1,
                                     strides=2,
                                     pad='SAME',
                                     act=False,
                                     bn=False,
                                     rate=1.0,
                                     name='skip12_' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=2)
            x = self.conv1d_net(x=x,
                                num_filters=f1,
                                kernel_size=3,
                                strides=2,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet12' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=1)
            x = self.conv1d_net(x=x,
                                num_filters=f2,
                                kernel_size=3,
                                strides=1,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet11' + name)

            x = tf.keras.layers.Add(name='add_' + name)([x, x_skip])
            ffs = [(f2, f2) for _ in range(num_loop)]
            for sl, ffl in enumerate(ffs):
                x = self.block1d_loop(x, ffl, name, sl)

        with tf.compat.v1.variable_scope('collected') as scope:
            xx = x[:, 1:, :]
            zz = tf.zeros_like(x[:, 0:1, :])
            xx = tf.concat((xx, zz), axis=1)

            yy = x[:, 2:, :]
            zz = tf.zeros_like(x[:, 0:2, :])
            yy = tf.concat((yy, zz), axis=1)

            xy = x[:, 3:, :]
            zz = tf.zeros_like(x[:, 0:3, :])
            xy = tf.concat((xy, zz), axis=1)

            x = tf.concat((x, xx, yy, xy), axis=2)

        logits_layer1 = tf.keras.layers.Dense(num_of_class)(x)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(x)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer)

        logits_layer2 = tf.keras.layers.Dense(num_of_class)(lstm_layer)

        logits_layer = tf.keras.layers.Add()([logits_layer1, logits_layer2])
        softmax_layer = tf.keras.layers.Softmax(axis=-1)(logits_layer)
        if not from_logits:
            return tf.keras.Model(input_layer, softmax_layer, name=name)
        else:
            return tf.keras.Model(input_layer, logits_layer, name=name)

    def beat_concat_seq_add_other(self,
                                  feature_len,
                                  num_of_class=2,
                                  from_logits=False,
                                  filters_rhythm_net=None,
                                  num_loop=7,
                                  rate=0.5,
                                  name='beat_concat_seq_add'):
        if filters_rhythm_net is None:
            filters_rhythm_net = [(16, 16),
                                  (16, 32),
                                  (32, 48),
                                  (48, 64)]
        else:
            tmp = []
            for i, f in enumerate(filters_rhythm_net):
                if len(tmp) == 0:
                    tmp.append((f, f))
                else:
                    tmp.append((tmp[-1][-1], f))

            filters_rhythm_net = tmp.copy()

        input_layer = tf.keras.layers.Input(shape=(feature_len,))
        resnet_input_layer = tf.keras.layers.Reshape((feature_len, 1))(input_layer)
        # Convolution(stride=2)
        x = self.conv1d_net(x=resnet_input_layer,
                            num_filters=filters_rhythm_net[0][0],
                            kernel_size=3,
                            strides=2,
                            pad='SAME',
                            act=False,
                            bn=False,
                            rate=1.0,
                            name='input_stage')

        for st, ff in enumerate(filters_rhythm_net):
            st += 1
            f1, f2 = ff
            name = 'stage_{}'.format(st)
            # 1x1 Convolution (stride=2)
            x_skip = self.conv1d_net(x=x,
                                     num_filters=f2,
                                     kernel_size=1,
                                     strides=2,
                                     pad='SAME',
                                     act=False,
                                     bn=False,
                                     rate=1.0,
                                     name='skip12_' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=2)
            x = self.conv1d_net(x=x,
                                num_filters=f1,
                                kernel_size=3,
                                strides=2,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet12' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=1)
            x = self.conv1d_net(x=x,
                                num_filters=f2,
                                kernel_size=3,
                                strides=1,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet11' + name)

            x = tf.keras.layers.Add(name='add_' + name)([x, x_skip])
            ffs = [(f2, f2) for _ in range(num_loop)]
            for sl, ffl in enumerate(ffs):
                x = self.block1d_loop(x, ffl, name, sl)

        with tf.compat.v1.variable_scope('collected') as scope:
            xx = x[:, :-1, :]
            zz = tf.zeros_like(x[:, 0:1, :])
            xx = tf.concat((zz, xx), axis=1)

            yy = x[:, 1:, :]
            zz = tf.zeros_like(x[:, 0:1, :])
            yy = tf.concat((yy, zz), axis=1)

            x = tf.concat((xx, x, yy), axis=2)

        logits_layer1 = tf.keras.layers.Dense(num_of_class)(x)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(x)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer)

        logits_layer2 = tf.keras.layers.Dense(num_of_class)(lstm_layer)

        logits_layer = tf.keras.layers.Add()([logits_layer1, logits_layer2])
        softmax_layer = tf.keras.layers.Softmax(axis=-1)(logits_layer)
        if not from_logits:
            return tf.keras.Model(input_layer, softmax_layer, name=name)
        else:
            return tf.keras.Model(input_layer, logits_layer, name=name)

    def beat_concat_seq_add_other1(self,
                                   feature_len,
                                   num_of_class=2,
                                   from_logits=False,
                                   filters_rhythm_net=None,
                                   num_loop=7,
                                   rate=0.5,
                                   name='beat_concat_seq_add'):
        if filters_rhythm_net is None:
            filters_rhythm_net = [(16, 16),
                                  (16, 32),
                                  (32, 48),
                                  (48, 64)]
        else:
            tmp = []
            for i, f in enumerate(filters_rhythm_net):
                if len(tmp) == 0:
                    tmp.append((f, f))
                else:
                    tmp.append((tmp[-1][-1], f))

            filters_rhythm_net = tmp.copy()

        input_layer = tf.keras.layers.Input(shape=(feature_len,))
        resnet_input_layer = tf.keras.layers.Reshape((feature_len, 1))(input_layer)
        # Convolution(stride=2)
        x = self.conv1d_net(x=resnet_input_layer,
                            num_filters=filters_rhythm_net[0][0],
                            kernel_size=3,
                            strides=2,
                            pad='SAME',
                            act=False,
                            bn=False,
                            rate=1.0,
                            name='input_stage')

        for st, ff in enumerate(filters_rhythm_net):
            st += 1
            f1, f2 = ff
            name = 'stage_{}'.format(st)
            # 1x1 Convolution (stride=2)
            x_skip = self.conv1d_net(x=x,
                                     num_filters=f2,
                                     kernel_size=1,
                                     strides=2,
                                     pad='SAME',
                                     act=False,
                                     bn=False,
                                     rate=1.0,
                                     name='skip12_' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=2)
            x = self.conv1d_net(x=x,
                                num_filters=f1,
                                kernel_size=3,
                                strides=2,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet12' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=1)
            x = self.conv1d_net(x=x,
                                num_filters=f2,
                                kernel_size=3,
                                strides=1,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet11' + name)

            x = tf.keras.layers.Add(name='add_' + name)([x, x_skip])
            ffs = [(f2, f2) for _ in range(num_loop)]
            for sl, ffl in enumerate(ffs):
                x = self.block1d_loop(x, ffl, name, sl)

        with tf.compat.v1.variable_scope('collected') as scope:
            aa = x[:, :-2, :]
            zz = tf.zeros_like(x[:, 0:2, :])
            aa = tf.concat((zz, aa), axis=1)

            xx = x[:, :-1, :]
            zz = tf.zeros_like(x[:, 0:1, :])
            xx = tf.concat((zz, xx), axis=1)

            yy = x[:, 1:, :]
            zz = tf.zeros_like(x[:, 0:1, :])
            yy = tf.concat((yy, zz), axis=1)

            bb = x[:, 2:, :]
            zz = tf.zeros_like(x[:, 0:2, :])
            bb = tf.concat((bb, zz), axis=1)

            x = tf.concat((aa, xx, x, yy, bb), axis=2)

        logits_layer1 = tf.keras.layers.Dense(num_of_class)(x)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(x)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer)

        logits_layer2 = tf.keras.layers.Dense(num_of_class)(lstm_layer)

        logits_layer = tf.keras.layers.Add()([logits_layer1, logits_layer2])
        softmax_layer = tf.keras.layers.Softmax(axis=-1)(logits_layer)
        if not from_logits:
            return tf.keras.Model(input_layer, softmax_layer, name=name)
        else:
            return tf.keras.Model(input_layer, logits_layer, name=name)

    def beat_concat_seq_add_other2(self,
                                   feature_len,
                                   num_of_class=2,
                                   from_logits=False,
                                   filters_rhythm_net=None,
                                   num_loop=7,
                                   rate=0.5,
                                   name='beat_concat_seq'):
        if filters_rhythm_net is None:
            filters_rhythm_net = [(16, 16),
                                  (16, 32),
                                  (32, 48),
                                  (48, 64)]
        else:
            tmp = []
            for i, f in enumerate(filters_rhythm_net):
                if len(tmp) == 0:
                    tmp.append((f, f))
                else:
                    tmp.append((tmp[-1][-1], f))

            filters_rhythm_net = tmp.copy()

        input_layer = tf.keras.layers.Input(shape=(feature_len,))
        resnet_input_layer = tf.keras.layers.Reshape((feature_len, 1))(input_layer)
        # Convolution(stride=2)
        x = self.conv1d_net(x=resnet_input_layer,
                            num_filters=filters_rhythm_net[0][0],
                            kernel_size=3,
                            strides=2,
                            pad='SAME',
                            act=False,
                            bn=False,
                            rate=1.0,
                            name='input_stage')

        for st, ff in enumerate(filters_rhythm_net):
            st += 1
            f1, f2 = ff
            name = 'stage_{}'.format(st)
            # 1x1 Convolution (stride=2)
            x_skip = self.conv1d_net(x=x,
                                     num_filters=f2,
                                     kernel_size=1,
                                     strides=2,
                                     pad='SAME',
                                     act=False,
                                     bn=False,
                                     rate=1.0,
                                     name='skip12_' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=2)
            x = self.conv1d_net(x=x,
                                num_filters=f1,
                                kernel_size=3,
                                strides=2,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet12' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=1)
            x = self.conv1d_net(x=x,
                                num_filters=f2,
                                kernel_size=3,
                                strides=1,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet11' + name)

            x = tf.keras.layers.Add(name='add_' + name)([x, x_skip])
            ffs = [(f2, f2) for _ in range(num_loop)]
            for sl, ffl in enumerate(ffs):
                x = self.block1d_loop(x, ffl, name, sl)

        with tf.compat.v1.variable_scope('collected') as scope:
            xx = x[:, :-1, :]
            zz = tf.zeros_like(x[:, 0:1, :])
            xx = tf.concat((zz, xx), axis=1)

            yy = x[:, 1:, :]
            zz = tf.zeros_like(x[:, 0:1, :])
            yy = tf.concat((yy, zz), axis=1)

        lstm_layer_x = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(x)
        lstm_layer_x = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer_x)

        lstm_layer_xx = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(xx)
        lstm_layer_xx = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer_xx)

        lstm_layer_yy = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(yy)
        lstm_layer_yy = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer_yy)

        lstm_layer = tf.keras.layers.Add()([lstm_layer_xx, lstm_layer_x, lstm_layer_yy])

        logits_layer = tf.keras.layers.Dense(num_of_class)(lstm_layer)
        softmax_layer = tf.keras.layers.Softmax(axis=-1)(logits_layer)
        if not from_logits:
            return tf.keras.Model(input_layer, softmax_layer, name=name)
        else:
            return tf.keras.Model(input_layer, logits_layer, name=name)

    def beat_concat_seqn_add(self,
                             feature_len,
                             num_of_class=2,
                             from_logits=False,
                             filters_rhythm_net=None,
                             num_loop=7,
                             rate=0.5,
                             name='beat_concat_seqn_add'):
        if filters_rhythm_net is None:
            filters_rhythm_net = [(16, 16),
                                  (16, 32),
                                  (32, 48),
                                  (48, 64)]
        else:
            tmp = []
            for i, f in enumerate(filters_rhythm_net):
                if len(tmp) == 0:
                    tmp.append((f, f))
                else:
                    tmp.append((tmp[-1][-1], f))

            filters_rhythm_net = tmp.copy()

        input_layer = tf.keras.layers.Input(shape=(feature_len,))
        resnet_input_layer = tf.keras.layers.Reshape((feature_len, 1))(input_layer)
        # Convolution(stride=2)
        x = self.conv1d_net(x=resnet_input_layer,
                            num_filters=filters_rhythm_net[0][0],
                            kernel_size=3,
                            strides=2,
                            pad='SAME',
                            act=False,
                            bn=False,
                            rate=1.0,
                            name='input_stage')

        for st, ff in enumerate(filters_rhythm_net):
            st += 1
            f1, f2 = ff
            name = 'stage_{}'.format(st)
            # 1x1 Convolution (stride=2)
            x_skip = self.conv1d_net(x=x,
                                     num_filters=f2,
                                     kernel_size=1,
                                     strides=2,
                                     pad='SAME',
                                     act=False,
                                     bn=False,
                                     rate=1.0,
                                     name='skip12_' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=2)
            x = self.conv1d_net(x=x,
                                num_filters=f1,
                                kernel_size=3,
                                strides=2,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet12' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=1)
            x = self.conv1d_net(x=x,
                                num_filters=f2,
                                kernel_size=3,
                                strides=1,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet11' + name)

            x = tf.keras.layers.Add(name='add_' + name)([x, x_skip])
            ffs = [(f2, f2) for _ in range(num_loop)]
            for sl, ffl in enumerate(ffs):
                x = self.block1d_loop(x, ffl, name, sl)

        with tf.compat.v1.variable_scope('collected') as scope:
            xx = x[:, 1:, :]
            zz = tf.zeros_like(x[:, 0:1, :])
            xx = tf.concat((xx, zz), axis=1)

            yy = x[:, 2:, :]
            zz = tf.zeros_like(x[:, 0:2, :])
            yy = tf.concat((yy, zz), axis=1)

            xy = x[:, 3:, :]
            zz = tf.zeros_like(x[:, 0:3, :])
            xy = tf.concat((xy, zz), axis=1)

            x = tf.concat((x, xx, yy, xy), axis=2)

        logits_layer1 = tf.keras.layers.Dense(num_of_class)(x)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True))(x)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True))(lstm_layer)

        logits_layer2 = tf.keras.layers.Dense(num_of_class)(lstm_layer)

        logits_layer = tf.keras.layers.Add()([logits_layer1, logits_layer2])
        softmax_layer = tf.keras.layers.Softmax(axis=-1)(logits_layer)
        if not from_logits:
            return tf.keras.Model(input_layer, softmax_layer, name=name)
        else:
            return tf.keras.Model(input_layer, logits_layer, name=name)

    def beat_concat_seq2_add(self,
                             feature_len,
                             num_of_class=2,
                             from_logits=False,
                             filters_rhythm_net=None,
                             num_loop=7,
                             rate=0.5,
                             name='beat_concat_seq2_add'):
        if filters_rhythm_net is None:
            filters_rhythm_net = [(16, 16),
                                  (16, 32),
                                  (32, 48),
                                  (48, 64)]
        else:
            tmp = []
            for i, f in enumerate(filters_rhythm_net):
                if len(tmp) == 0:
                    tmp.append((f, f))
                else:
                    tmp.append((tmp[-1][-1], f))

            filters_rhythm_net = tmp.copy()

        input_layer = tf.keras.layers.Input(shape=(feature_len,))
        resnet_input_layer = tf.keras.layers.Reshape((feature_len, 1))(input_layer)
        # Convolution(stride=2)
        x = self.conv1d_net(x=resnet_input_layer,
                            num_filters=filters_rhythm_net[0][0],
                            kernel_size=3,
                            strides=2,
                            pad='SAME',
                            act=False,
                            bn=False,
                            rate=1.0,
                            name='input_stage')

        for st, ff in enumerate(filters_rhythm_net):
            st += 1
            f1, f2 = ff
            name = 'stage_{}'.format(st)
            # 1x1 Convolution (stride=2)
            x_skip = self.conv1d_net(x=x,
                                     num_filters=f2,
                                     kernel_size=1,
                                     strides=2,
                                     pad='SAME',
                                     act=False,
                                     bn=False,
                                     rate=1.0,
                                     name='skip12_' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=2)
            x = self.conv1d_net(x=x,
                                num_filters=f1,
                                kernel_size=3,
                                strides=2,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet12' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=1)
            x = self.conv1d_net(x=x,
                                num_filters=f2,
                                kernel_size=3,
                                strides=1,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet11' + name)

            x = tf.keras.layers.Add(name='add_' + name)([x, x_skip])
            ffs = [(f2, f2) for _ in range(num_loop)]
            for sl, ffl in enumerate(ffs):
                x = self.block1d_loop(x, ffl, name, sl)

        with tf.compat.v1.variable_scope('collected') as scope:
            xx = x[:, 1:, :]
            zz = tf.zeros_like(x[:, 0:1, :])
            xx = tf.concat((xx, zz), axis=1)

            yy = x[:, 2:, :]
            zz = tf.zeros_like(x[:, 0:2, :])
            yy = tf.concat((yy, zz), axis=1)

            xy = x[:, 3:, :]
            zz = tf.zeros_like(x[:, 0:3, :])
            xy = tf.concat((xy, zz), axis=1)

            x = tf.concat((x, xx, yy, xy), axis=2)

        logits_layer1 = tf.keras.layers.Dense(num_of_class)(x)

        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(x)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer)

        logits_layer2 = tf.keras.layers.Dense(num_of_class)(lstm_layer)

        logits_layer = tf.keras.layers.Add()([logits_layer1, logits_layer2])
        softmax_layer = tf.keras.layers.Softmax(axis=-1)(logits_layer)
        if not from_logits:
            return tf.keras.Model(input_layer, softmax_layer, name=name)
        else:
            return tf.keras.Model(input_layer, logits_layer, name=name)

    def beat_concat_seq3_add(self,
                             feature_len,
                             num_of_class=2,
                             from_logits=False,
                             filters_rhythm_net=None,
                             num_loop=7,
                             rate=0.5,
                             name='beat_concat_seq3_add'):
        if filters_rhythm_net is None:
            filters_rhythm_net = [(16, 16),
                                  (16, 32),
                                  (32, 48),
                                  (48, 64)]
        else:
            tmp = []
            for i, f in enumerate(filters_rhythm_net):
                if len(tmp) == 0:
                    tmp.append((f, f))
                else:
                    tmp.append((tmp[-1][-1], f))

            filters_rhythm_net = tmp.copy()

        input_layer = tf.keras.layers.Input(shape=(feature_len,))
        resnet_input_layer = tf.keras.layers.Reshape((feature_len, 1))(input_layer)
        # Convolution(stride=2)
        x = self.conv1d_net(x=resnet_input_layer,
                            num_filters=filters_rhythm_net[0][0],
                            kernel_size=3,
                            strides=2,
                            pad='SAME',
                            act=False,
                            bn=False,
                            rate=1.0,
                            name='input_stage')

        for st, ff in enumerate(filters_rhythm_net):
            st += 1
            f1, f2 = ff
            name = 'stage_{}'.format(st)
            # 1x1 Convolution (stride=2)
            x_skip = self.conv1d_net(x=x,
                                     num_filters=f2,
                                     kernel_size=1,
                                     strides=2,
                                     pad='SAME',
                                     act=False,
                                     bn=False,
                                     rate=1.0,
                                     name='skip12_' + name)
            # Batch norm, Activa         tion, Dropout, Convolution (stride=2)
            x = self.conv1d_net(x=x,
                                num_filters=f1,
                                kernel_size=3,
                                strides=2,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet12' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=1)
            x = self.conv1d_net(x=x,
                                num_filters=f2,
                                kernel_size=3,
                                strides=1,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet11' + name)

            x = tf.keras.layers.Add(name='add_' + name)([x, x_skip])
            ffs = [(f2, f2) for _ in range(num_loop)]
            for sl, ffl in enumerate(ffs):
                x = self.block1d_loop(x, ffl, name, sl)

        with tf.compat.v1.variable_scope('collected') as scope:
            xx = x[:, 1:, :]
            zz = tf.zeros_like(x[:, 0:1, :])
            xx = tf.concat((xx, zz), axis=1)

            yy = x[:, 2:, :]
            zz = tf.zeros_like(x[:, 0:2, :])
            yy = tf.concat((yy, zz), axis=1)

            xy = x[:, 3:, :]
            zz = tf.zeros_like(x[:, 0:3, :])
            xy = tf.concat((xy, zz), axis=1)

            x = tf.concat((x, xx, yy, xy), axis=2)

        logits_layer1 = tf.keras.layers.Dense(num_of_class)(x)

        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(x)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer)

        logits_layer2 = tf.keras.layers.Dense(num_of_class)(lstm_layer)

        logits_layer = tf.keras.layers.Add()([logits_layer1, logits_layer2])
        softmax_layer = tf.keras.layers.Softmax(axis=-1)(logits_layer)
        if not from_logits:
            return tf.keras.Model(input_layer, softmax_layer, name=name)
        else:
            return tf.keras.Model(input_layer, logits_layer, name=name)

    def beat_concat_seq_add_more_other(self,
                                       feature_len,
                                       num_of_class=2,
                                       from_logits=False,
                                       filters_rhythm_net=None,
                                       num_loop=7,
                                       rate=0.5,
                                       name='beat_concat_seq_add_more_other'):

        if filters_rhythm_net is None:
            filters_rhythm_net = [(16, 16),
                                  (16, 32),
                                  (32, 48),
                                  (48, 64)]
        else:
            tmp = []
            for i, f in enumerate(filters_rhythm_net):
                if len(tmp) == 0:
                    tmp.append((f, f))
                else:
                    tmp.append((tmp[-1][-1], f))

            filters_rhythm_net = tmp.copy()

        input_layer = tf.keras.layers.Input(shape=(feature_len,))
        resnet_input_layer = tf.keras.layers.Reshape((feature_len, 1))(input_layer)
        # Convolution(stride=2)
        x = self.conv1d_net(x=resnet_input_layer,
                            num_filters=filters_rhythm_net[0][0],
                            kernel_size=3,
                            strides=2,
                            pad='SAME',
                            act=False,
                            bn=False,
                            rate=1.0,
                            name='input_stage')

        for st, ff in enumerate(filters_rhythm_net):
            st += 1
            f1, f2 = ff
            name = 'stage_{}'.format(st)
            # 1x1 Convolution (stride=2)
            x_skip = self.conv1d_net(x=x,
                                     num_filters=f2,
                                     kernel_size=1,
                                     strides=2,
                                     pad='SAME',
                                     act=False,
                                     bn=False,
                                     rate=1.0,
                                     name='skip12_' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=2)
            x = self.conv1d_net(x=x,
                                num_filters=f1,
                                kernel_size=3,
                                strides=2,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet12' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=1)
            x = self.conv1d_net(x=x,
                                num_filters=f2,
                                kernel_size=3,
                                strides=1,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet11' + name)

            x = tf.keras.layers.Add(name='add_' + name)([x, x_skip])
            ffs = [(f2, f2) for _ in range(num_loop)]
            for sl, ffl in enumerate(ffs):
                x = self.block1d_loop(x, ffl, name, sl)

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

        logits_layer1 = tf.keras.layers.Dense(num_of_class)(x)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(x)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer)

        logits_layer2 = tf.keras.layers.Dense(num_of_class)(lstm_layer)

        logits_layer = tf.keras.layers.Add()([logits_layer1, logits_layer2])
        softmax_layer = tf.keras.layers.Softmax(axis=-1)(logits_layer)
        if not from_logits:
            return tf.keras.Model(input_layer, softmax_layer, name=name)
        else:
            return tf.keras.Model(input_layer, logits_layer, name=name)

    def beat_concat_seq_add_more2_other(self,
                                        feature_len,
                                        num_of_class=2,
                                        from_logits=False,
                                        filters_rhythm_net=None,
                                        num_loop=7,
                                        rate=0.5,
                                        name='beat_concat_seq_add_more2_other'):
        if filters_rhythm_net is None:
            filters_rhythm_net = [(16, 16),
                                  (16, 32),
                                  (32, 48),
                                  (48, 64)]
        else:
            tmp = []
            for i, f in enumerate(filters_rhythm_net):
                if len(tmp) == 0:
                    tmp.append((f, f))
                else:
                    tmp.append((tmp[-1][-1], f))

            filters_rhythm_net = tmp.copy()

        input_layer = tf.keras.layers.Input(shape=(feature_len,))
        resnet_input_layer = tf.keras.layers.Reshape((feature_len, 1))(input_layer)
        # Convolution(stride=2)
        x = self.conv1d_net(x=resnet_input_layer,
                            num_filters=filters_rhythm_net[0][0],
                            kernel_size=3,
                            strides=2,
                            pad='SAME',
                            act=False,
                            bn=False,
                            rate=1.0,
                            name='input_stage')

        for st, ff in enumerate(filters_rhythm_net):
            st += 1
            f1, f2 = ff
            name = 'stage_{}'.format(st)
            # 1x1 Convolution (stride=2)
            x_skip = self.conv1d_net(x=x,
                                     num_filters=f2,
                                     kernel_size=1,
                                     strides=2,
                                     pad='SAME',
                                     act=False,
                                     bn=False,
                                     rate=1.0,
                                     name='skip12_' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=2)
            x = self.conv1d_net(x=x,
                                num_filters=f1,
                                kernel_size=3,
                                strides=2,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet12' + name)
            # Batch norm, Activation, Dropout, Convolution (stride=1)
            x = self.conv1d_net(x=x,
                                num_filters=f2,
                                kernel_size=3,
                                strides=1,
                                pad='SAME',
                                act=True,
                                bn=True,
                                rate=0.5,
                                name='resnet11' + name)

            x = tf.keras.layers.Add(name='add_' + name)([x, x_skip])
            ffs = [(f2, f2) for _ in range(num_loop)]
            for sl, ffl in enumerate(ffs):
                x = self.block1d_loop(x, ffl, name, sl)

        with tf.compat.v1.variable_scope('collected') as scope:
            bbxx = x[:, :-3, :]
            bbzz = tf.zeros_like(x[:, 0:3, :])
            bbxx = tf.concat((bbzz, bbxx), axis=1)

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

            aayy = x[:, 3:, :]
            aazz = tf.zeros_like(x[:, 0:3, :])
            aayy = tf.concat((aayy, aazz), axis=1)

            x = tf.concat((bbxx, bxx, xx, x, yy, ayy, aayy), axis=2)

        logits_layer1 = tf.keras.layers.Dense(num_of_class)(x)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(x)
        lstm_layer = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(x.shape[-1], return_sequences=True, dropout=rate))(lstm_layer)

        logits_layer2 = tf.keras.layers.Dense(num_of_class)(lstm_layer)

        logits_layer = tf.keras.layers.Add()([logits_layer1, logits_layer2])
        softmax_layer = tf.keras.layers.Softmax(axis=-1)(logits_layer)
        if not from_logits:
            return tf.keras.Model(input_layer, softmax_layer, name=name)
        else:
            return tf.keras.Model(input_layer, logits_layer, name=name)