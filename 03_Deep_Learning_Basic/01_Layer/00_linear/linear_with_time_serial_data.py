import torch
import torch.nn as nn                    # the basic building blocks for your nets
import torch.nn.functional as F          # some lower-level functions kept here
import torch.optim as optim              # we'll use this for optimization of the net

import matplotlib.pyplot as plt
import numpy as np
import onnxruntime
from sklearn.metrics import mean_squared_error

"""
Example from: https://github.com/nrokh/PyTorch-TimeSeriesPrediction/blob/main/Guide%20to%20time-series%20prediction%20in%20PyTorch.ipynb
"""

def create_dataset():
    t = np.arange(0,100,1)                    # create a time vector of length 100, starting from 0, in steps of 1
    f = 0.25                                  # pick a frequency you like
    A = 5                                     # and an amplitude for your waves

    # make the sine and cosine waves and add some random noise of length 100 in the range of 0 to 0.25
    data_in_train = A * np.sin(f*t) + np.random.normal(0, 0.25, 100) # X data
    data_out_train = A * np.cos(f*t) + np.random.normal(0, 0.25, 100) # Y label

    data_in_test = A * np.sin(f*t) + np.random.normal(0, 0.25, 100)
    data_out_test = A * np.cos(f*t) + np.random.normal(0, 0.25, 100)
    np.save("data/data_in_train.npy", data_in_train)
    np.save("data/data_out_train.npy", data_out_train)
    np.save("data/data_in_test.npy", data_in_test)
    np.save("data/data_out_test.npy", data_out_test)

    # visualize the training data you've created:
    plt.plot(data_in_train[0:100])
    plt.plot(data_out_train[0:100])
    plt.title('Input and output training data')
    plt.xlabel('Time step')
    plt.ylabel('Signal amplitude')
    plt.legend(['input', 'output'], bbox_to_anchor=(1,1), loc="upper left") # put the legend on the right of the plot
    plt.show()

# Step2: Convert the data to tensors
def load_convert_data_to_tensor(show=True):
    data_in_train = np.load("data/data_in_train.npy")
    data_out_train = np.load("data/data_out_train.npy")
    data_in_test = np.load("data/data_in_test.npy")
    data_out_test = np.load("data/data_out_test.npy")

    # so our tensors play nice with our model without us having to cast new variable types, set the default to float64
    torch.set_default_dtype(torch.float64)

    t_data_in_train = torch.tensor(data_in_train)
    t_data_out_train = torch.tensor(data_out_train)
    t_data_in_test = torch.tensor(data_in_test)
    t_data_out_test = torch.tensor(data_out_test)
    print('Tensor size: ', np.shape(t_data_in_train))

    if show:
        # check the shape of our tensors:
        # print('Tensor size: ', np.shape(t_data_in_train))
        # visualize the training data you've created:
        plt.plot(t_data_in_test[0:100])
        plt.plot(t_data_out_test[0:100])
        plt.title('Input and output training data')
        plt.xlabel('Time step')
        plt.ylabel('Signal amplitude')
        plt.legend(['input', 'output'], bbox_to_anchor=(1,1), loc="upper left") # put the legend on the right of the plot
        plt.show()

    return t_data_in_train, t_data_out_train, t_data_in_test, t_data_out_test


# Step3: Build the network
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        # now we play hidden-layer ping-pong: the number of hidden layers OUT needs to equal the number IN to the next layer

        self.fc1 = nn.Linear(100, 5)  # we input the size of our feature (length 100) and decide on 5 hidden layers
        self.fc2 = nn.Linear(5,
                             10)  # the number of hidden layers out from the last step (5) should be the same as input (5)
        # LSTM layer
        # self.lstm = nn.LSTM(10, 10)

        # Conv1d
        self.conv1d = nn.Conv1d(10, 10, 3, stride=1)

        self.fc3 = nn.Linear(10, 100)  # and we set our final output to the length of our output signal (also 100)

    # we have to define the forward method within the nn.Module itself
    def forward(self, x):
        x = F.relu(self.fc1(x))  # we use a ReLU activation for each Linear layer
        x = F.relu(self.fc2(x))


        # # Change shape for LSTM
        # # Reshape x to (seq_len, batch, input_size) for LSTM
        # x = x.view(1, -1, 10)  # (batch, seq_len, input_size) -> (seq_len, batch, input_size)
        # x, _ = self.lstm(x)
        # # Reshape x back to (batch, seq_len)
        # x = x.view(-1, 10)

        # Using CNN
        x = F.relu(self.conv1d(x))

        x = self.fc3(x)  # and return just the output signal
        return x


def train_loop():
    # Define model
    net = Net()

    # visualize what our network looks like: it should have 3 Linear layers in total
    print(net)

    # pick an optimzer (Adam learns the optimal learning rate, so it's a common one to use)

    optimizer = optim.Adam(net.parameters(), lr=0.002)
    # pick a loss function that suits the data (continuous time-series data work well with MSE)
    criterion = nn.MSELoss()

    # initialize the variable we'll use to store overall loss
    model_loss = []

    # let's train the net for 1000 iterations (overkill, considering how simple the function is)
    for epoch in range(1000):
        # reset the running loss that will be printed as we train our model
        running_loss = 0.0

        # reset the gradient values
        optimizer.zero_grad()

        # put the training data into the net
        outputs = net(t_data_in_train)

        # calculate the MSE Loss using the ground-truth training signal output
        loss = criterion(outputs, t_data_out_train)

        # backpropagate weights
        loss.backward()

        # move forward one step in the optimization
        optimizer.step()

        # save the MSE loss value so we can plot later (and we want to detach it with .item() so we don't run out of memory)
        model_loss.append(loss.item())

        # print the current loss:
        running_loss += loss.item()
        if epoch % 100 == 99:  # every 100 steps
            print(running_loss / 100)  # print the running loss
            running_loss = 0.0
    print('Finished Training')

        # # plot the loss over training iterations:
        # plt.plot(model_loss)
        # plt.title('Training loss')
        # plt.xlabel('Iteration')
        # plt.ylabel('MSE Loss')
        # plt.show()

    print("Save model...")
    torch.save(net, "test_model.pt")


# Step5: Test the network on new data
def test_new_data():
    # https://pytorch.org/tutorials/beginner/saving_loading_models.html
    # Model class must be defined somewhere
    net = torch.load("test_model.pt", weights_only=False)
    net.eval()
    # use the trained net to predict an output for the input test data
    model_out = net(t_data_in_test)

    # to plot the data, we first collapse it back to a [100] length tensor
    model_out = model_out.view(-1)
    # then we need to "detach" it from a tensor
    model_out = model_out.detach().numpy()
    plt.plot(model_out)

    # and the same for the ground-truth data:
    test_out = t_data_out_test.view(-1)
    test_out = test_out.detach().numpy()
    plt.plot(test_out)

    # and let's see what the input signal was as well:
    test_in = t_data_in_test.view(-1)
    plt.plot(test_in.detach().numpy())

    # plot:
    plt.title('Example 1: Model prediction vs. Real data')
    plt.xlabel('Time step')
    plt.ylabel('Amplitude')
    plt.legend(['predicted', 'real', 'model input'], bbox_to_anchor=(1, 1), loc="upper left")
    plt.show()

def convert_save_onnx():
    torch_model = Net()
    torch_model.float()  # Ensure the model is in float32 precision
    torch_input = torch.randn(1, 100, dtype=torch.float32, requires_grad=True)
    torch.onnx.export(torch_model, torch_input, "test_model.onnx", export_params=True, input_names=['input'], output_names=['output'], dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}})
    print("Model successfully exported to ONNX format")

def infer_onnxruntime():
    onnx_input = t_data_in_test.view(1, 100).float()  # Ensure the input is in float32 precision
    onnx_input = onnx_input.detach().numpy()

    session = onnxruntime.InferenceSession("test_model.onnx")
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    result = session.run([output_name], {input_name: onnx_input})
    plt.plot(result[0][0])

    # # and the same for the ground-truth data:
    test_out = t_data_out_test.view(-1)
    test_out = test_out.detach().numpy()
    plt.plot(test_out)

    # and let's see what the input signal was as well:
    test_in = t_data_in_test.view(-1)
    plt.plot(test_in.detach().numpy())

    # plot:
    plt.title('Example 1: Model prediction vs. Real data')
    plt.xlabel('Time step')
    plt.ylabel('Amplitude')
    plt.legend(['predicted', 'real', 'model input'], bbox_to_anchor=(1, 1), loc="upper left")
    plt.show()

if __name__ == '__main__':
    # create_dataset()
    t_data_in_train, t_data_out_train, t_data_in_test, t_data_out_test = load_convert_data_to_tensor(show=False)
    train_loop()
    # test_new_data()
    # convert_save_onnx()
    # infer_onnxruntime()