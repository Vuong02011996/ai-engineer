from neuron_layer_mlp import MLP
import torch
"""Creating a tiny dataset, writing the loss function"""

# Simple binary classifier example. Ví dụ về một bài toán phân loại đơn giản.
# Ta có 4 input đi vào neuron và 4 output mong muốn sau khi qua neuron.
xs = torch.Tensor([[2.0, 3.0, -1.0],
      [3.0, -1.0, 0.5],
      [0.5, 1.0, 1.0],
      [1.0, 1.0, -1.0],])
ys = torch.Tensor([1.0, -1.0, -1.0, 1.0]) # desired targets

# Ta có thể cho 4 input qua neuron net và xem output trả về cho mỗi input như thế nào.
# ypred = [n(x) for x in xs]
# ypred

# [Value(data = 0.5275235824211477),
#  Value(data = 0.5010104111433705),
#  Value(data = -0.21245683856279649),
#  Value(data = 0.6877916273558004)]

# Ta thấy kết quả hoàn toàn không giống với output chúng ta yêu cầu ở trên
# Nhưng không sao ta có thể thay đổi trọng số của network để ra được gần như chính xác
# output ta mong muốn ở trên.



def train_step_by_step_by_hand():
    "Training by hand"
    "Step Loop: forward pass -> backward pass -> update , change weights"

    # Define model
    n = MLP(3, [4, 4, 1])
    # 3 input, 3 layer (layer 1, 2 có 4 neuron, layer 3 có 1 neuron)

    # Step 1: forward pass
    ypred = [n(x) for x in xs]

    """Loss funtion"""
    loss = sum((yout - ygt) ** 2 for ygt, yout in zip(ys, ypred))
    print("Loss: ", loss)

    # Step 2: backward pass
    loss.backward()

    # Step 3: Change weights
    for p in n.parameters():
        p.data += -0.005 * p.grad


class MLPTORCH:
  def __init__(self, nin, nouts):
    # nouts: list of nout - list chứa đựng số lượng neuron trong mỗi layer.
    # size = [nin] + nouts # list + list
    # print('size:', size) # [3, 4, 4, 1]
    # size[i]: số lượng neuron input của layer trước đó, không phải input ban đầu => 3 4 4
    # số lượng neuron output của layer hiện tại là input của layer tiếp theo.
    # self.layers = [Layer(size[i], size[i + 1]) for i in range(len(nouts))]
    n_hidden = 10
    vocab_size = nouts
    self.layers = [
        torch.nn.Linear(nin, n_hidden), torch.nn.Tanh(),
        torch.nn.Linear(n_hidden, n_hidden), torch.nn.Tanh(),
        torch.nn.Linear(n_hidden, n_hidden), torch.nn.Tanh(),
        torch.nn.Linear(n_hidden, n_hidden), torch.nn.Tanh(),
        torch.nn.Linear(n_hidden, n_hidden), torch.nn.Tanh(),
        torch.nn.Linear(n_hidden, vocab_size),
    ]
  def __call__(self, x):
    for layer in self.layers:
      x = layer(x)
    return x

  def parameters(self):
    return [p for layer in self.layers for p in layer.parameters()]



def train_loop():
    # Define model
    n = MLPTORCH(3, 1)

    for k in range(20):
        # forward pass
        ypred = [n(x) for x in xs]
        print(ypred)
        loss = sum((yout - ygt) ** 2 for ygt, yout in zip(ys, ypred))

        # Misstakes three: We forgot to .zero_grad() before .backward()
        for p in n.parameters():
            torch.optim.Optimizer.zero_grad(p)
        # backward pass
        loss.backward()

        # update
        for p in n.parameters():
            p.data += -0.1 * p.grad

        print(k, loss.data)

if __name__ == '__main__':
    train_loop()
