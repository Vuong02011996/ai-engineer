# Backpropagation 
+ Chúng ta sẽ bắt đầu ở node cuối cùng, tức là output mong muôn, chúng ta đã có một biểu thức toán học biểu diễn 
neuro nets để ra được output này. Chng ta sẽ tìm mối liên hệ của output này với node trước đó gần nhất 
bằng cách đạo hàm biểu thức toán học này với sự thay đổi nhỏ của trọng số ở node này, 
Khi đạo hàm ta sẽ thấy output của biểu thức toán học sẽ tăng hoặc giảm, từ đó ta điều chỉnh trọng số của node này 
để tăng hoặc giảm đầu ra như chúng ta mong muốn.

# Neural networks
+ Just a mathematical expression they take the input data as an input and they take the weights of a
neural network as an input and it's a mathematical expression and the output are your predictions of your neural net
or the loss function.

## A Neuron
+ Mỗi neuron trong layer không phải là n = xw + b mà là n = x1w1 + x2w2 +... + b. Lúc trước nghĩ mỗi vòng tròn là một xw là sai.
+ Mỗi neuron sẽ connect tới tất cả các input đầu vào(dù là input data hay hidden layer)
## Layer of Neuron
+ layer has actually a number of neurons 
+ một list các Neuron.
+ Các neuron trong list này không kết nối với nhau nhưng mỗi neuron sẽ connect tới tất cả các input đầu vào.

```
x = [2.0, 3.0]
n = Layer(2, 4) # Layer có 4 neuron mỗi neuron có 2 input (x1, x2)
    Layer(nin, nout)
    # nin: số lượng input của layer trước đó.(không phải số lượng input ban đầu)
    # nout: How many neuron trong layer, number of output in this layer
```
## MLP - Multi Layer of Neuron
+ MLP chỉ là các layer được kết nối tuần tự với nhau.
```
x = [2.0, 3.0, -1.0]
n = MLP(3, [4, 4, 1]) 
# 3 input(batch size = 3, mỗi input có thể là một vector chứa nhiều sample(hoặc một ảnh là ma trận))
# 3 layer (layer 1, 2 có 4 neuron, layer 3 có 1 neuron)
n(x)
```

# Activation function hay squashing function
+ có chức năng đè nén, giới hạn output ở một mức cụ thể .
+ VD: Tanh: tới một điểm sẽ không cho output vượt qua 1 -1 dù input là bao nhiêu. 
        + Ta thấy ở node n, output có thể là lớn hơn 1 rất nhiều nhưng qua tanh output luôn <= 1.

# Loss function and optimization loss function by gradient descent 
+ The trick used in deep learning to achieve this is to `calculate a single number that somehow measures the
total performance of your neural net` and we call this single number the loss.

+ Giải thích chỗ thay đổi trọng số theo hướng nào to optimization loss.
  + w[0] đang dương
    + Ví dụ ở trên. grad tại w[0] đang dương, tức là tăng một thay đổi nhỏ giá trị của trọng số ở đây thì sẽ làm loss go up, tức là làm loss tăng lên.
    + Do đó ta muốn loss giảm thì ra phải làm giá trị của trọng số ở đây nhỏ lại.(hạn chế sự ảnh của trọng số tại đây).
    + Bằng cách cộng trọng số ở đây một lượng âm bằng -0.01 * w.grad (< 0 vì w.grad đang dương)
  + Ngược lại: w[0] đang âm
    + Nếu grad tại w[0] đang âm, tức là nếu ta tăng một lượng nhỏ giá trị của trọng số ở đây thì sẽ làm hàm loss go down, tức làm loss giảm xuống.
    + Do đó ta muốn loss giảm thì ta phải làm giá trị của trọng số ở đây tăng lên.
    + Bằng cách cộng trọng số ở đây thêm một lượng dương bằng -0.01 * w.grad(> 0 vì w.grad đang âm)
  
    => DO đó dấu của step luôn là âm.(-0.01)
  `Cách giải thích khác: Gradient là một vector có hướng luôn làm tăng loss function do đó ,
  ta phải nhân gradient với một số âm để làm loss function go down .`

# Training model
+ Prepare data
+ Define model
+ Step train: forward pass -> backward pass(from loss function) -> update , change weights

