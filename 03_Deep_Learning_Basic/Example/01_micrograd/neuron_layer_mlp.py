import math
import numpy as np
import matplotlib.pyplot as plt
import random
from helper import draw_dot


class Value:
  # A common example of a dunder method is the __init__ method.
  # This method is automatically called when an object is created.
  def __init__(self, data, _children = (), _op = '', label = ''):
    self.data = data
    self._prev = set(_children) # dùng để xem dữ liệu trước khi thực hiện tính toán
    self._op = _op # what is the operation
    self.label = label

    # lambda arguments: expression(biểu thức được gọi khi gọi hàm)
    # Hàm lambda trong Python là một hàm vô danh (anonymous function), có thể được định nghĩa mà không cần sử dụng từ khóa def.
    # Hàm này thường được sử dụng khi bạn cần một hàm ngắn gọn và chỉ sử dụng ở một nơi duy nhất trong code.

    # _backward hàm này sẽ thực hiện việc : lấy grad từ output và tính toán grad cho input.(backward) dựa vào chain rule, ...
    self._backward = lambda:None

    # the gradient is zero that means that changing this variable is not changing the loss function
    self.grad = 0.0

  # __repr__ is a special method used to represent a class's objects as a string.
  # https://www.educative.io/answers/what-is-the-repr-method-in-python
  def __repr__(self):
    return f"Value(data = {self.data})"

  # https://www.codingem.com/python-__add__-method/
  def __add__(self, other):
    # self chính là object gọi tới phương thức __add__  ,ở đây là a

    # can't not : a = Value(2.0); a + 1 ; because 1 is other 1.data is error. =>
    other = other if isinstance(other, Value) else Value(other)

    out = Value(self.data + other.data, (self, other), '+')

    # lấy grad từ output và tính toán grad cho input.(backward) dựa vào chain rule, ...
    def _backward():
      self.grad += 1.0 * out.grad
      other.grad += 1.0 * out.grad
    out._backward = _backward
    return out

  def __radd__(self, other):
    return self + other

  # https://blog.finxter.com/python-__mul__/
  def __mul__(self, other):
    # self chính là object gọi tới phương thức __mul__  ,ở đây là a
    other = other if isinstance(other, Value) else Value(other)
    out = Value(self.data * other.data, (self, other), '*')

    def _backward():
      self.grad += other.data * out.grad
      other.grad += self.data  * out.grad
    out._backward = _backward
    return out

  # 2 * a : TypeError: unsupported operand type(s) for *: 'int' and 'Value'
  # Giống như một hàm dự phòng , nếu 2*a bị lỗi nó sẽ  check nếu có __rmul__ sẽ
  # hoán đổi thành a * 2
  # other * self => self * other, https://www.geeksforgeeks.org/__rmul__-in-python/
  def __rmul__(self, other):
    return self * other

  # https://en.wikipedia.org/wiki/Hyperbolic_functions
  def tanh(self):
    x = self.data
    t = (math.exp(2*x) - 1) / (math.exp(2*x) + 1)
    out = Value(t, (self,), 'tanh')

    def _backward():
      self.grad += (1 - t**2) * out.grad
    out._backward = _backward
    print(out._backward)
    return out

   # Breaking up a tanh, exercising with more operations
  def exp(self):
    x = self.data
    out = Value(math.exp(x), (self, ), 'exp')
    def _backward():
      # f(x) = e^x => f'(x) = e^x = out.data;  ddx(ex)=ex.
      self.grad += out.data * out.grad
    out._backward = _backward
    return out

  def __pow__(self, other):
    assert isinstance(other, (int, float)), "only supporting in/float for now"
    out = Value(self.data ** other, (self, ), f'**{other}')
    def _backward():
      # https://en.wikipedia.org/wiki/Power_rule (x^n)' = n * x^(n-1)
      self.grad += other * (self.data ** (other - 1)) * out.grad
    out._backward = _backward
    return out

  def __truediv__(self, other): # self/other
    # a / b = a * 1/b = a * (b ** -1)
    # TypeError: unsupported operand type(s) for *: 'float' and 'NoneType'
    # Do hàm __pow__ không return out => other**-1 is NoneType
    return self * other**-1

  def __neg__(self): # -self
    return self * -1

  def __sub__(self, other): #self - other
    return self + (-other)

  # Implementing the backward function for a whole expression graph
  def backward(self):
    # sử dụng topological sort để lưu tất cả các node của neuro net vào topo
    topo = []
    visited = set()
    def build_topo(v):
      if v not in visited:
        visited.add(v)
        for child in v._prev:
          build_topo(child)
        topo.append(v)
    build_topo(self)
    # tính grad cho toàn bộ neuro net.
    self.grad = 1.0
    for node in reversed(topo):
      node._backward()


class Neuron:
  def __init__(self, nin):
    # nin: number of input, How many inputs come to a neuron
    """
    What different if input is number, vector(time data), matrix(image data)
    What is nin ? And how to initial weight
    :param nin:
    """
    # x1w1, x2w2 => nin = 2
    self.w = [Value(random.uniform(-1, 1)) for _ in range(nin)]

    # bias of neuron , one neuron have one bias.
    self.b = Value(random.uniform(-1, 1))

  def __call__(self, x):
    # x : input x

    # x = [1.0, 2.0]
    # n = Neuron(2)
    # n(x) hàm _call_: khi bạn sử dụng ký hiệu này n(x) python sẽ sử dụng lệnh call
    # và nhận giá trị hàm call trả về.

    # print(list(zip(self.w, x))) # zip takes two iterators
    # [(Value(data = -0.024398776603539618), 1.0), (Value(data = 0.1370132199167322), 2.0)]

    # multiply all of the elements of w with all of the elements of x pairwise
    # activation = sum(wi * xi for wi, xi in zip(self.w, x)) + self.b

    # in python sum have param start = 0.0 you can replace with self.b
    activation = sum((wi * xi for wi, xi in zip(self.w, x)), self.b)
    out = activation.tanh()
    return out
  # collecting all of the parameters of the neural net can operate on all of them simultaneously
  def parameters(self):
    return self.w + [self.b]

def test_neuron():
    x = [1.0, 2.0, 3.0]
    """
    Neuron(1)
    1 <=> len list w = 1, [random_weight1, ]
    Neuron(2)
    2 <=> len list w = 2, [random_weight1, random_weight2]
    ...
    len x and w cannot identical, will take with minimum length
    """
    n = Neuron(1)
    print(n(x))


class Layer:
  def __init__(self, nin: int, nout: int):
    # nin: số lượng input của layer trước đó.(kxhông phải số lượng input ban đầu)
    # nout: How many neuron trong layer, number of output in this layer
    """
    Note: nout also call: num filters, num of neuron of layer,...
    :param nin:
    :param nout:
    """
    self.neurons = [Neuron(nin) for _ in range(nout)]

  def __call__(self, x):
    outs = [n(x) for n in self.neurons]
    return outs[0] if len(outs) == 1 else outs

  def parameters(self):
    # Duyệt qua list các neuron, tại mỗi neuron lại duyệt qua tham số p(w) của
    # mỗi neuron và đưa vào danh sách mới.
    params = [p for neuron in self.neurons for p in neuron.parameters()]
    return params

def test_layer():
    x = [2.0, 3.0]
    n = Layer(2, 4) # Layer có 4 neuron khác nhau mỗi neuron có 2 input.
    print(n(x))


class MLP:
  def __init__(self, nin, nouts):
    # nouts: list of nout - list chứa đựng số lượng neuron trong mỗi layer.
    size = [nin] + nouts # list + list
    print('size:', size) # [3, 4, 4, 1]
    # size[i]: số lượng neuron input của layer trước đó, không phải input ban đầu => 3 4 4
    # số lượng neuron output của layer hiện tại là input của layer tiếp theo.
    self.layers = [Layer(size[i], size[i + 1]) for i in range(len(nouts))]
  def __call__(self, x):
    for layer in self.layers:
      x = layer(x)
    return x

  def parameters(self):
    return [p for layer in self.layers for p in layer.parameters()]


def test_mlp():
    x = [2.0, 3.0, -1.0]
    n = MLP(3, [4, 4, 1]) # 3 input, 3 layer (layer 1, 2 có 4 neuron, layer 3 có 1 neuron)
    print(n(x))
    print(len(n.parameters()))

    # x.backward() AttributeError: 'list' object has no attribute 'backward'
    # n.backward() AttributeError: 'MLP' object has no attribute 'backward'
    # n(x).backward()
    # Oke vì n(x) trả về x mà x = layer(x), layer(x) trả về neuron mà neuron có w thuộc class Value,
    # class Value mới có hàm backward, tương tự như biến tạo bởi torch đều là tensor và có thể gọi backward.

    # draw_dot(n(x))
if __name__ == '__main__':
    # test_neuron()
    # test_layer()
    test_mlp()