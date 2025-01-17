import os
import time

import numpy as np

import warnings
warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

import logging
logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
# os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
tf.get_logger().setLevel(logging.ERROR)
tf.autograph.set_verbosity(1)
import json
from scipy import signal
from scipy.signal import butter, filtfilt, lfilter, iirnotch, sosfiltfilt, iirfilter
from scipy.ndimage.filters import maximum_filter1d
from collections import Counter
import matplotlib.pyplot as plt
from os.path import basename, dirname
import onnxruntime as ort

print("ONNX on device: ", ort.get_device())



class BeatModel:
    def __init__(
            self,
            feature_len,
            num_of_class,
            from_logit = False,
            num_filters = None,
            num_loop    = 7,
            rate        = 0.5,
            name        = 'beat_concat_seq_add'
    ) :
        if num_filters is None:
            num_filters = [(16, 16), (16, 32), (32, 48), (48, 64)]
        else:
            tmp = []
            for i, f in enumerate(num_filters):
                if len(tmp) == 0: tmp.append((f, f))
                else: tmp.append((tmp[-1][-1], f))

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


# SYS
NUM_NORMALIZATION = 0.6
MIN_RR_INTERVAL = 0.15
HES_SAMPLING_RATE = 200
# CONFIG
NEW_MODE = 0
OLD_MODE = 1
MODE = NEW_MODE
OFFSET_FRAME_BEAT = [0, 3, 6, 9, 11]
MAX_CHANNEL = 3
ADD_ARTIFACT = True
BAND_PASS_FILTER = [1.0, 30.0]
RHYTHM_BAND_PASS_FILTER = [1.0, 30.0]
CLIP_RANGE = [-5.0, 5.0]
RHYTHM_CLIP_RANGE = [-5.0, 5.0]
MAX_NUM_IMG_SAVE = 100
MAX_LEN_PLOT = 15
EVENT_LEN_STANDARD = 60


def resample_sig(x, fs, fs_target):
    """
    Resample a signal to a different frequency.

    Parameters
    ----------
    x : numpy array
        Array containing the signal
    fs : int, or float
        The original sampling frequency
    fs_target : int, or float
        The target frequency

    Returns
    -------
    resampled_x : numpy array
        Array of the resampled signal values
    resampled_t : numpy array
        Array of the resampled signal locations

    """

    t = np.arange(x.shape[0]).astype('float64')

    if fs == fs_target:
        return x, t

    new_length = int(x.shape[0]*fs_target/fs)
    resampled_x, resampled_t = signal.resample(x, num=new_length, t=t)
    assert resampled_x.shape == resampled_t.shape and resampled_x.shape[0] == new_length
    assert np.all(np.diff(resampled_t) > 0)

    return resampled_x, resampled_t

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y
def smooth(x, window_len=11, window='hanning'):
    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise (ValueError, "smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise (ValueError, "Input vector needs to be bigger than window size.")

    if window_len < 3:
        return x

    if window_len % 2 == 0:
        window_len += 1

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise (ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s = np.r_[x[window_len - 1:0:-1], x, x[-2:-window_len - 1:-1]]
    # print(len(s))
    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.' + window + '(window_len)')

    y = np.convolve(w / w.sum(), s, mode='valid')
    # output = np.argwhere(np.isnan(y))
    # if len(output) > 0:
    #     print(output)
    return y[int(window_len / 2):-int(window_len / 2)]
def bwr(raw, fs, l1=0.2, l2=0.6):
    flen1 = int(l1 * fs / 2)
    flen2 = int(l2 * fs / 2)

    if flen1 % 2 == 0:
        flen1 += 1

    if flen2 % 2 == 0:
        flen2 += 1

    out1 = smooth(raw, flen1)
    out2 = smooth(out1, flen2)
    return raw - out2

def norm(raw, window_len, samp_from=-1, samp_to=-1):
    # The window size is the number of samples that corresponds to the time analogue of 2e = 0.5s
    if window_len % 2 == 0:
        window_len += 1

    abs_raw = abs(raw)
    # Remove outlier
    while True:
        g = maximum_filter1d(abs_raw, size=window_len)
        if np.max(abs_raw) <= 5.0:
            break

        abs_raw[g > 5.0] = 0

    g_smooth = smooth(g, window_len, window='hamming')
    g_mean = max(np.mean(g_smooth) / 3.0, 0.1)
    g_smooth = np.clip(g_smooth, g_mean, None)
    # Avoid cases where the value is )
    g_smooth[g_smooth < 0.01] = 1
    normalized = np.divide(raw, g_smooth)

    # if samp_from < 18986081 < samp_to:
    #     print(samp_from)
    #     from matplotlib import pyplot as plt
    #     plt.plot(raw, label="raw")
    #     plt.plot(g_smooth, label="g_smooth")
    #     plt.legend(loc=4)
    #     plt.show()
    #     plt.close()

    return normalized


def beat_cluster(beats, symbols, amps, min_rr):
    _beats = []
    _symbols = []
    _amps = []
    _lens = []
    if len(beats) > 0:
        groups_beat = [beats[0]]
        groups_syms = [symbols[0]]
        groups_amps = [amps[0]]
        for index in range(1, len(beats)):
            if (beats[index] - groups_beat[-1]) > min_rr:
                _beats.append(groups_beat.copy())
                _symbols.append(groups_syms.copy())
                _amps.append(groups_amps.copy())
                _lens.append(len(groups_beat))

                groups_beat.clear()
                groups_syms.clear()
                groups_amps.clear()

            groups_beat.append(beats[index])
            groups_syms.append(symbols[index])
            groups_amps.append(amps[index])

        if len(groups_beat) > 0:
            _beats.append(groups_beat.copy())
            _symbols.append(groups_syms.copy())
            _amps.append(groups_amps.copy())
            _lens.append(len(groups_beat))

    return _beats, _symbols, _amps, _lens

def is_t_wave(ecg, peak, repeak, fs, qrs_radius=0.05):
    segment_slope = np.rad2deg(np.arctan2((ecg[peak] - ecg[peak - int(qrs_radius * fs)]), int(qrs_radius * fs)))
    last_qrs_slope = np.rad2deg(np.arctan2((ecg[repeak] - ecg[repeak - int(qrs_radius * fs)]), int(qrs_radius * fs)))

    # Should we be using absolute values?
    if abs(segment_slope) <= 0.5 * abs(last_qrs_slope):
        return True
    else:
        return False
def beat_select(ibeats, isymbols, iamps, buf_bwr_ecg, fs, thr_min=0.5, thr_max=2.5, pre_peak=3):
    """

    """
    selected_beats = []
    selected_amps = []
    selected_symbols = []
    st = 0

    selected_beats.append(ibeats[st])
    selected_symbols.append(isymbols[st])
    selected_amps.append(iamps[st])
    for i in range(st + 1, len(ibeats)):
        peak = ibeats[i]
        amp = iamps[i]
        if abs(peak - selected_beats[-1]) < 0.36 * fs and is_t_wave(buf_bwr_ecg, peak, selected_beats[-1], fs):
            continue

        cnt = 0
        mean_amp = 0
        for st in reversed(range(i)):
            if isymbols[st] not in ["Q", "V"]:
                mean_amp += iamps[st]
                cnt += 1
                if cnt > pre_peak:
                    break
            else:
                break

        if cnt > 0:
            mean_amp = (mean_amp / cnt)
            if amp < mean_amp * thr_min and isymbols[i] not in ["Q", "V"]:
                isymbols[i] = "Q"
                continue

            if amp >= mean_amp * thr_max and isymbols[i] not in ["Q", "V"]:
                isymbols[i] = "Q"

        symbol = isymbols[i]
        selected_beats.append(peak)
        selected_symbols.append(symbol)
        selected_amps.append(amp)

    return np.asarray(selected_beats), np.asarray(selected_symbols), np.asarray(selected_amps)

def beat_classification(model,
                        input_data,
                        beat_datastore,
                        img_directory=None):
    """

    """
    sampling_rate = beat_datastore["sampling_rate"]
    beat_class = beat_datastore["beat_class"]
    beat_num_block = beat_datastore["num_block"]
    beat_feature_len = beat_datastore["feature_len"]
    beat_ebwr = beat_datastore["bwr"]
    beat_enorm = beat_datastore["norm"]
    if "BAND_PASS_FILTER" in beat_datastore.keys():
        beat_filter = beat_datastore["BAND_PASS_FILTER"]
        beat_clip = beat_datastore["CLIP_RANGE"]
    else:
        beat_filter = [1.0, 30.0]
        beat_clip = None

    # header = wf.rdheader(file_name)
    fs_origin = 250
    samp_to = 0
    samp_from = 0
    total_peak = []
    total_label = []
    event_len = (EVENT_LEN_STANDARD * fs_origin)
    beat_inv = {i: k for i, k in enumerate(beat_class.keys())}
    beat_ind = {k: i for i, k in enumerate(beat_class.keys())}
    if 1:
        try:
            # if header.sig_len - samp_from <= 0:
            #     break

            # region Process
            # samp_len = min(event_len, (header.sig_len - samp_from))
            # samp_to = samp_from + samp_len
            # record = wf.rdsamp(file_name, sampfrom=samp_from, sampto=samp_to, channels=[channel_ecg])
            # Avoid cases where the value is NaN
            buf_record = np.nan_to_num(input_data)
            print(buf_record.shape)
            # fs_origin = record[1].get('fs')

            if fs_origin != sampling_rate:
                buf_ecg_org, _ = resample_sig(buf_record, fs_origin, sampling_rate)
                print(buf_ecg_org.shape)
            else:
                buf_ecg_org = buf_record.copy()

            len_of_standard = int(EVENT_LEN_STANDARD * sampling_rate)
            len_of_buf = len(buf_ecg_org)
            if len_of_buf < len_of_standard:
                buf_ecg_org = np.concatenate((buf_ecg_org, np.full(len_of_standard - len_of_buf, buf_ecg_org[-1])))

            buf_ecg = butter_bandpass_filter(buf_ecg_org,
                                             beat_filter[0],
                                             beat_filter[1],
                                             sampling_rate)
            if beat_clip is not None:
                buf_ecg = np.clip(buf_ecg,
                                  beat_clip[0],
                                  beat_clip[1])

            buf_bwr_ecg = bwr(buf_ecg, sampling_rate)
            if beat_ebwr:
                buf_ecg = bwr(buf_ecg, sampling_rate)

            if beat_enorm:
                buf_ecg = norm(buf_ecg, int(NUM_NORMALIZATION * sampling_rate))
                
            print(buf_ecg.shape)

            data_len = len(buf_ecg)
            beat_label_len = beat_feature_len // beat_num_block
            data_index = np.arange(beat_feature_len)[None, :] + \
                         np.arange(0, data_len, beat_feature_len)[:, None]
            _samp_from = (samp_from * sampling_rate) // fs_origin
            _samp_to = (samp_to * sampling_rate) // fs_origin
            buf_frame = []
            for fr in OFFSET_FRAME_BEAT:
                if len(buf_frame) == 0:
                    buf_frame = np.concatenate((buf_ecg[fr:], np.full(fr, 0)))[data_index]
                else:
                    buf_frame = np.concatenate(
                        (buf_frame, np.concatenate((buf_ecg[fr:], np.full(fr, 0)))[data_index]))

            buf_frame = np.asarray(buf_frame)
            print(buf_frame.shape)
            start_time = time.time()
            # group_beat_prob = model.predict(buf_frame)
            # print("Model tf result:", group_beat_prob)


            # Model onnx
            output_path = "model_beat.onnx"
            session = ort.InferenceSession(output_path)
            input_name = session.get_inputs()[0].name
            output_name = session.get_outputs()[0].name
            result = session.run([output_name], {input_name: buf_frame})
            print("Inference onnx result:", result)
            group_beat_prob = result

            print("Time for model predict: ", time.time() - start_time)
            group_beat_candidate = np.argmax(group_beat_prob, axis=-1)

            label_index = np.arange(beat_label_len)[None, :] + \
                          np.arange(0, beat_feature_len, beat_label_len)[:, None]

            group_bwr_frame = buf_bwr_ecg[data_index]
            beats = []
            symbols = []
            amps = []

            for beat_candidate in group_beat_candidate:
                beat_candidate = np.asarray(beat_candidate).reshape((-1, beat_num_block))
                for group_beat, group_bwr_buff, group_offset in zip(beat_candidate,
                                                                    group_bwr_frame,
                                                                    data_index):
                    _group_offset = group_offset[label_index]
                    _index = np.where(abs(np.diff(group_beat)) > 0)[0] + 1
                    _group_beat = np.split(group_beat, _index)
                    _group_offset = np.split(_group_offset, _index)
                    for gbeat, goffset in zip(_group_beat, _group_offset):
                        if np.max(gbeat) > beat_ind["NOTABEAT"]:
                            goffset = np.asarray(goffset).flatten()
                            index_ext = goffset.copy()
                            if (goffset[0] - beat_label_len) >= 0:
                                index_ext = np.concatenate((np.arange((goffset[0] - beat_label_len),
                                                                      goffset[0]), index_ext))

                            if (goffset[-1] + beat_label_len) < beat_feature_len:
                                index_ext = np.concatenate((index_ext,
                                                            np.arange(goffset[-1], (goffset[-1] + beat_label_len))))

                            gbuff = np.asarray(group_bwr_buff[index_ext]).flatten()
                            flip_g = gbuff * -1.0
                            peaks_up = np.argmax(gbuff)
                            peaks_down = np.argmax(flip_g)
                            if abs(gbuff[peaks_up]) > abs(flip_g[peaks_down]):
                                ma = abs(gbuff[peaks_up])
                                peaks = peaks_up
                            else:
                                ma = abs(flip_g[peaks_down])
                                peaks = peaks_down

                            amps.append(ma)
                            beats.append(peaks + index_ext[0])
                            qr_count = Counter(gbeat)
                            qr = qr_count.most_common(1)[0][0]
                            symbols.append(beat_inv[qr])

            if len(beats) > 0:
                symbols = [x for _, x in sorted(zip(beats, symbols))]
                amps = [x for _, x in sorted(zip(beats, amps))]
                beats = sorted(beats)

                beats = np.asarray(beats, dtype=int)
                symbols = np.asarray(symbols)
                amps = np.asarray(amps)
                index_artifact = symbols == 'ARTIFACT'
                sample_artifact = []
                if np.count_nonzero(index_artifact) > 0:
                    sample_artifact = np.zeros(data_len, dtype=int)
                    sample_artifact[beats[index_artifact]] = 1
                    label_index_artifact = np.arange(sampling_rate)[None, :] + \
                                           np.arange(0, data_len, sampling_rate)[:, None]
                    sample_artifact = sample_artifact[label_index_artifact]
                    sample_artifact = np.asarray([np.max(lbl) for lbl in sample_artifact], dtype=int)

                    index_del = np.where(symbols == 'ARTIFACT')[0]
                    symbols = np.delete(symbols, index_del)
                    beats = np.delete(beats, index_del)
                    amps = np.delete(amps, index_del)

                if len(beats) > 0:
                    min_rr = MIN_RR_INTERVAL * sampling_rate
                    try:
                        group_beats, group_symbols, group_amps, group_len = beat_cluster(beats,
                                                                                         symbols,
                                                                                         amps,
                                                                                         min_rr)
                    except Exception as err:
                        print(err)

                    beats = []
                    symbols = []
                    amps = []
                    for _beat, _symbol, _amp in zip(group_beats, group_symbols, group_amps):
                        qr_count = Counter(_symbol)
                        qr = qr_count.most_common(1)[0][0]
                        symbols.append(qr)

                        p = np.argmax(_amp)
                        amps.append(max(_amp))
                        beats.append(_beat[p])

                    beats = np.asarray(beats)
                    symbols = np.asarray(symbols)
                    amps = np.asarray(amps)
                    try:
                        beats, symbols, amps = beat_select(beats, symbols, amps, buf_bwr_ecg, sampling_rate)
                    except Exception as err:
                        print(err)

                    # # region debug
                    t = np.arange(_samp_from, _samp_from + len(buf_ecg), 1) / sampling_rate
                    plt.plot(t, buf_ecg)
                    # plt.plot(t, lbl_draw)
                    for b, s in zip(beats, symbols):
                        plt.annotate(s, xy=(t[b], buf_ecg[b]))

                    plt.show()
                    # # endregion debug

            if img_directory is not None:
                fig, axx = plt.subplots(nrows=EVENT_LEN_STANDARD // MAX_LEN_PLOT, ncols=1,
                                        figsize=(19.20, 10.80))
                plt.subplots_adjust(
                    hspace=0,
                    wspace=0.04,
                    left=0.04,  # the left side of the subplots of the figure
                    right=0.98,  # the right side of the subplots of the figure
                    bottom=0.2,  # the bottom of the subplots of the figure
                    top=0.88
                )
                rhythm_main = basename(dirname(file_name))
                sub_save_image = img_directory + "/" + rhythm_main

                file_count = 0
                if not os.path.exists(sub_save_image):
                    os.makedirs(sub_save_image)
                else:
                    for root, dirs, files in os.walk(sub_save_image):
                        file_count += len(files)

                sub_save_image = img_directory + "/" + rhythm_main + "/{}".format(file_count // 500)
                if not os.path.exists(sub_save_image):
                    os.makedirs(sub_save_image)

                fig.suptitle('Channel: {}; Sub Rhythm: {}; Id: {}'.format(
                    channel_ecg,
                    rhythm_main,
                    basename(file_name)), fontsize=11)

                if len(beats) > 0:
                    draw_index = np.arange(beat_label_len)[None, None, :] + \
                                 np.arange(0, beat_feature_len, beat_label_len)[None, :, None] + \
                                 np.arange(0, data_len, beat_feature_len)[:, None, None]
                    draw_beat_label = []
                    for beat_candidate in group_beat_candidate:
                        beat_candidate = np.asarray(beat_candidate).reshape((-1, beat_num_block))
                        _draw_beat_label = np.zeros(data_len)[draw_index]
                        for s in range(len(beat_candidate)):
                            for l in range(len(beat_candidate[s])):
                                _draw_beat_label[s][l] = np.full(len(_draw_beat_label[s][l]), beat_candidate[s][l])

                        draw_beat_label.append(_draw_beat_label.flatten())

                for i, ax in enumerate(axx):
                    start_buf = i * MAX_LEN_PLOT * sampling_rate
                    stop_buf = min((i + 1) * MAX_LEN_PLOT * sampling_rate, data_len)

                    plot_len = (MAX_LEN_PLOT * sampling_rate)
                    t = np.arange(start_buf, start_buf + plot_len, 1) / sampling_rate
                    buf_ecg_draw = buf_ecg_org.copy()
                    buf_ecg_draw = butter_bandpass_filter(buf_ecg_draw, 0.5, 40.0, sampling_rate)
                    buf_ecg_draw = np.clip(buf_ecg_draw, -5.0, 5.0)
                    # buf_ecg_draw = bwr(buf_ecg_draw, sampling_rate)
                    buf_frame = buf_ecg_draw[start_buf: stop_buf]
                    plot_len = len(buf_frame)

                    ax.plot(t, buf_frame, linestyle='-', linewidth=2.0)
                    if len(beats) > 0:
                        for d, _draw_beat_label in enumerate(draw_beat_label):
                            ax.plot(t, (_draw_beat_label[start_buf: stop_buf]) + 0.1 * d, label="BEAT-{}".format(d))

                        total_beat_draw = beats.copy()
                        index_draw = (total_beat_draw >= start_buf) == (total_beat_draw < stop_buf)
                        beats_draw = total_beat_draw[index_draw] - start_buf
                        symbols_draw = symbols[index_draw]
                        amps_draw = amps[index_draw]
                        for b, s, a in zip(beats_draw, symbols_draw, amps_draw):
                            if s == "V":
                                ax.annotate('{}\n{:.3f}'.format(s, a), xy=(t[b], buf_frame[b]), color='red',
                                            fontsize=8, fontweight='bold')
                            elif s == "A":
                                ax.annotate('{}\n{:.3f}'.format(s, a), xy=(t[b], buf_frame[b]), color='blue',
                                            fontsize=8, fontweight='bold')
                            elif s == "R":
                                ax.annotate('{}\n{:.3f}'.format(s, a), xy=(t[b], buf_frame[b]), color='green',
                                            fontsize=8, fontweight='bold')
                            else:
                                ax.annotate('{}\n{:.3f}'.format(s, a), xy=(t[b], buf_frame[b]), color='black',
                                            fontsize=8, fontweight='bold')

                    major_ticks = np.arange(start_buf, start_buf + plot_len,
                                            sampling_rate) / sampling_rate
                    minor_ticks = np.arange(start_buf, start_buf + plot_len,
                                            sampling_rate // 4) / sampling_rate
                    ax.set_xticks(major_ticks)
                    ax.set_xticks(minor_ticks, minor=True)
                    ax.grid(which='major', color='#CCCCCC', linestyle='--')
                    ax.grid(which='minor', color='#CCCCCC', linestyle=':')
                    ax.legend(loc="lower right", prop={'size': 6})

                    if stop_buf == data_len:
                        break

                DEBUG_IMG = True
                if not DEBUG_IMG:
                    img_name = sub_save_image + "/{}".format(basename(file_name))

                    fig.savefig(img_name + ".svg", format='svg', dpi=1200)
                    plt.close(fig)
                else:
                    plt.show()

            if len(beats) > 0:
                beats = (beats * fs_origin) // sampling_rate
                beats += samp_from

                if len(total_label) == 0:
                    total_label = symbols
                    total_peak = beats
                else:
                    total_label = np.concatenate((total_label, symbols[beats > total_peak[-1]]), axis=0)
                    total_peak = np.concatenate((total_peak, beats[beats > total_peak[-1]]), axis=0)

            samp_from = samp_to

        except Exception as e:
            print("process_sample {}".format(e))
            # break
    print(total_peak)
    print(total_label)
    print(fs_origin)
    dictionary =[{ 
    "input" : input_data.tolist(), 
    "output" : 
        {
            "beats": np.asarray(total_peak, dtype=int).tolist(), 
            "symbols": np.asarray(total_label).tolist()
        }
        }]
    with open("data-beat-classification-1-sample.json", "w", encoding='utf-8') as outfile: 
        json.dump(dictionary, outfile,sort_keys=True, indent=4) 
    return np.asarray(total_peak, dtype=int), np.asarray(total_label), fs_origin
        
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
    pass
    
    # input_data = np.ones((15000), dtype=np.float32)
    # input_data = np.expand_dims(input_data, axis=0)
    
    with open(datastore_file, 'r') as json_file:
        datastore_dict = json.load(json_file)
    print(datastore_dict)
    
    with open(datainput_file, 'r') as json_file:
        datainput_dict = json.load(json_file)
    print(np.array(datainput_dict[0]["input"]).shape)
    
    beat_classification(function.model,
                        np.array(datainput_dict[0]["input"]),
                        datastore_dict,
                        img_directory=None)
        
    # predict_output = function.model.predict(input_data)
    # print(predict_output.shape)
    
    
if __name__ == '__main__':
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
    
    # CKPT_DIR = '/media/bangau/DATA_500G/BangAu-ITR/HeartBeat-Rhythm/Soft/models/beat_concat_seq_add_more_other_7_16.32.48.64_0_0.5-best_squared_error_metric/best_squared_error_metric'
    CKPT_DIR = '/home/server2/Desktop/Vuong/models/210929/256_60.0_480_0_0_0_2_0_0.8/output-3.780749/model/beat_concat_seq_add_more_other_7_16.32.48.64_0_0.5/best_squared_error_metric'
    datastore_file = "datastore.txt"
    datainput_file = "/home/server2/Downloads/data-beat-classification-3.json"
    main()
