# General imports used throughout the tutorial
# file operations
import json
import os

import numpy as np
import tensorflow as tf
from IPython.display import SVG
from matplotlib import patches
from matplotlib import pyplot as plt
from PIL import Image
from tensorflow.python.eager.context import eager_mode

# import the hailo sdk client relevant classes
from hailo_sdk_client import ClientRunner, InferenceContext

# %matplotlib inline

IMAGES_TO_VISUALIZE = 5

def optimizer_test_model_sin_code():
    # Prepare data
    data_in_train = np.load("data_in_train.npy")
    # data_in_train = data_in_train.view(1, 100)
    data_in_train = np.reshape(data_in_train, (1, 100))
    print(data_in_train.shape)

    model_name = "test_model"
    hailo_model_har_name = f"{model_name}_hailo_model.har"
    assert os.path.isfile(hailo_model_har_name), "Please provide valid path for HAR file"
    runner = ClientRunner(har=hailo_model_har_name)
    runner.optimize(data_in_train)

    # Save the result state to a Quantized HAR file
    quantized_model_har_path = f"{model_name}_quantized_model.har"
    runner.save_har(quantized_model_har_path)




def preproc(image, output_height=224, output_width=224, resize_side=256):
    """imagenet-standard: aspect-preserving resize to 256px smaller-side, then central-crop to 224px"""
    with eager_mode():
        h, w = image.shape[0], image.shape[1]
        scale = tf.cond(tf.less(h, w), lambda: resize_side / h, lambda: resize_side / w)
        resized_image = tf.compat.v1.image.resize_bilinear(tf.expand_dims(image, 0), [int(h * scale), int(w * scale)])
        cropped_image = tf.compat.v1.image.resize_with_crop_or_pad(resized_image, output_height, output_width)

        return tf.squeeze(cropped_image)

def optimizer_with_dataset():
    # First, we will prepare the calibration set. Resize the images to the correct size and crop them.
    images_path = "../data"
    images_list = [img_name for img_name in os.listdir(images_path) if os.path.splitext(img_name)[1] == ".jpg"]

    calib_dataset = np.zeros((len(images_list), 224, 224, 3))
    for idx, img_name in enumerate(sorted(images_list)):
        img = np.array(Image.open(os.path.join(images_path, img_name)))
        img_preproc = preproc(img)
        calib_dataset[idx, :, :, :] = img_preproc.numpy()

    np.save("calib_set.npy", calib_dataset)

    # Second, we will load our parsed HAR from the Parsing Tutorial
    model_name = "test_model"
    hailo_model_har_name = f"{model_name}_hailo_model.har"
    assert os.path.isfile(hailo_model_har_name), "Please provide valid path for HAR file"
    runner = ClientRunner(har=hailo_model_har_name)
    # By default it uses the hw_arch that is saved on the HAR. For overriding, use the hw_arch flag.
    # Now we will create a model script, that tells the compiler to add a normalization on the beginning
    # of the model (that is why we didn't normalize the calibration set;
    # Otherwise we would have to normalize it before using it)

    # Batch size is 8 by default
    alls = "normalization1 = normalization([123.675, 116.28, 103.53], [58.395, 57.12, 57.375])\n"

    # Load the model script to ClientRunner so it will be considered on optimization
    runner.load_model_script(alls)

    # Call Optimize to perform the optimization process
    runner.optimize(calib_dataset)

    # Save the result state to a Quantized HAR file
    quantized_model_har_path = f"{model_name}_quantized_model.har"
    runner.save_har(quantized_model_har_path)


def optimizer_bilstm_model():
    # Prepare data
    input_value = [3, 6, 9, 2, 5]
    input_value = np.reshape(input_value, (-1, len(input_value),1))
    # specific_input = torch.tensor(input_value, dtype=torch.float32).view(1, len(input_value),
    #                                                                      1)  # Shape: (batch_size=1, seq_length, input_size=1)

    model_name = "bilstm_model"
    hailo_model_har_name = f"../models/{model_name}.har"

    assert os.path.isfile(hailo_model_har_name), "Please provide valid path for HAR file"
    runner = ClientRunner(har=hailo_model_har_name)
    runner.optimize(input_value)

    # Save the result state to a Quantized HAR file
    quantized_model_har_path = f"../models/{model_name}_quantized_model.har"
    runner.save_har(quantized_model_har_path)


def optimizer_model_mexh():
    # First, we will prepare the calibration set. Resize the images to the correct size and crop them.
    # images_path = "../data"
    # images_list = [img_name for img_name in os.listdir(images_path) if os.path.splitext(img_name)[1] == ".jpg"]
    #
    # calib_dataset = np.zeros((len(images_list), 224, 224, 3))
    # for idx, img_name in enumerate(sorted(images_list)):
    #     img = np.array(Image.open(os.path.join(images_path, img_name)))
    #     img_preproc = preproc(img)
    #     calib_dataset[idx, :, :, :] = img_preproc.numpy()
    #
    # np.save("calib_set.npy", calib_dataset)

    # Second, we will load our parsed HAR from the Parsing Tutorial
    model_name = "model_mexh"
    hailo_model_har_name = f"../models/{model_name}.har"
    assert os.path.isfile(hailo_model_har_name), "Please provide valid path for HAR file"
    runner = ClientRunner(har=hailo_model_har_name)

    # For calling Optimize, use the short version: runner.optimize(calib_dataset)
    # A more general approach is being used here that works also with multiple input nodes.
    # The calibration dataset could also be a dictionary with the format:
    # {input_layer_name_1_from_hn: layer_1_calib_dataset, input_layer_name_2_from_hn: layer_2_calib_dataset}
    hn_layers = runner.get_hn_dict()["layers"]
    print("Input layers are: ")
    print([layer for layer in hn_layers if hn_layers[layer]["type"] == "input_layer"])

    # By default it uses the hw_arch that is saved on the HAR. For overriding, use the hw_arch flag.
    # Now we will create a model script, that tells the compiler to add a normalization on the beginning
    # of the model (that is why we didn't normalize the calibration set;
    # Otherwise we would have to normalize it before using it)

    # Batch size is 8 by default
    # alls = "normalization1 = normalization([123.675, 116.28, 103.53], [58.395, 57.12, 57.375])\n"

    # Load the model script to ClientRunner so it will be considered on optimization
    # runner.load_model_script(alls)

    # Call Optimize to perform the optimization process
    x1_test = np.load("x1_test.npy")
    x2_test = np.load("x2_test.npy")
    # x1_test = np.squeeze(x1_test)
    # x2_test = np.squeeze(x2_test)
    print(x1_test.shape)
    # x1_test = x1_test.reshape(100, 100, 1, -1)
    x1_test = x1_test.transpose(0, 2, 3, 1)
    # x2_test = x2_test.reshape(4, -1)
    # x2_test = x2_test.reshape(1, 1, 4)
    x2_test = x2_test.reshape(2271, 1, 1, 4)
    # calib_dataset = {"x1": torch.tensor(x1_test, dtype=torch.float32).to(device), "x2": torch.tensor(x2_test, dtype=torch.float32).to(device)}
    # calib_dataset = {"x1": x1_test, "x2": x2_test}
    calib_dataset_dict = {'model_mexh/input_layer1': x1_test,  'model_mexh/input_layer2': x2_test}
    runner.optimize(calib_dataset_dict)

    # Save the result state to a Quantized HAR file
    quantized_model_har_path = f"../models/{model_name}_quantized_model.har"
    runner.save_har(quantized_model_har_path)



if __name__ == '__main__':
   # optimizer_bilstm_model()
   optimizer_model_mexh()
   """
   # Compiler with CLI, no dataset
   hailo optimize ../models/bilstm_model.har --hw-arch hailo8l --use-random-calib-set
   """

