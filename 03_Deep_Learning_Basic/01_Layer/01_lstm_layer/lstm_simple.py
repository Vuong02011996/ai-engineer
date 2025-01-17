import torch
import torch.nn as nn
import torch.optim as optim

# Dữ liệu chuỗi
data = [1, 2, 3, 4, 5]  # Chuỗi mẫu
seq_length = 1  # Chiều dài của mỗi đầu vào
X = torch.tensor(data[:-1], dtype=torch.float32).view(-1, seq_length, 1)  # Đầu vào
Y = torch.tensor(data[1:], dtype=torch.float32).view(-1, 1)  # Đầu ra


# Mô hình LSTM
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True, bidirectional=False)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # Khởi tạo hidden state và cell state
        h0 = torch.zeros(1, x.size(0), self.hidden_size)
        c0 = torch.zeros(1, x.size(0), self.hidden_size)

        # LSTM output
        out, _ = self.lstm(x, (h0, c0))  # out: (batch_size, seq_length, hidden_size)
        out = self.fc(out[:, -1, :])  # Chỉ lấy đầu ra cuối cùng
        return out


# Khởi tạo mô hình, hàm mất mát và bộ tối ưu
input_size = 1
hidden_size = 10
output_size = 1
model = LSTMModel(input_size, hidden_size, output_size)
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# Huấn luyện mô hình
num_epochs = 200
for epoch in range(num_epochs):
    model.train()
    outputs = model(X)
    loss = criterion(outputs, Y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 20 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

# Dự đoán
model.eval()
test_input = torch.tensor([[5]], dtype=torch.float32).view(-1, seq_length, 1)
predicted = model(test_input).item()
print(f'Giá trị dự đoán tiếp theo sau 5 là: {predicted:.4f}')

import torch.onnx

# Chuyển đổi mô hình sang ONNX và lưu lại
def save_model_to_onnx(model, file_name, input_size):
    model.eval()  # Chuyển mô hình sang chế độ đánh giá
    dummy_input = torch.randn(1, 1, input_size)  # Tạo đầu vào giả để xuất ONNX
    torch.onnx.export(
        model,                     # Mô hình PyTorch
        dummy_input,               # Đầu vào giả
        file_name,                 # Tên tệp ONNX
        export_params=True,        # Lưu trọng số mô hình
        opset_version=11,          # Phiên bản ONNX (ONNX opset)
        do_constant_folding=True,  # Bật tối ưu hóa hằng số nếu có thể
        input_names=['input'],     # Tên đầu vào
        output_names=['output'],   # Tên đầu ra
        dynamic_axes={             # Định nghĩa các trục có kích thước động
            'input': {0: 'batch_size'},
            'output': {0: 'batch_size'}
        }
    )
    print(f'Mô hình đã được lưu dưới dạng {file_name}')

# Gọi hàm để lưu mô hình
save_model_to_onnx(model, "lstm_model.onnx", input_size)
