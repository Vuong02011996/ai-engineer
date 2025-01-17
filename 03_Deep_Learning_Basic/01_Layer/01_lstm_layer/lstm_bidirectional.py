import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# 1. Tạo dữ liệu giả lập
def generate_data(seq_length, num_samples):
    """
    Tạo dữ liệu chuỗi đơn giản:
    Đầu vào là dãy số, đầu ra là tổng của dãy.
    """
    x = np.random.randint(1, 10, size=(num_samples, seq_length, 1))  # (batch_size, seq_length, input_size)
    y = np.sum(x, axis=1, keepdims=True)  # Tổng dãy số, shape: (batch_size, 1, 1)
    return torch.tensor(x, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)


# 2. Định nghĩa mô hình LSTM hai chiều
class BiLSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(BiLSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size, bidirectional=True, batch_first=True)
        self.fc = nn.Linear(hidden_size * 2, output_size)  # 2 * hidden_size vì bidirectional=True

    def forward(self, x):
        lstm_out, _ = self.lstm(x)  # lstm_out shape: (batch_size, seq_length, hidden_size * 2)
        # Chỉ lấy đầu ra của bước cuối cùng
        final_output = lstm_out[:, -1, :]  # (batch_size, hidden_size * 2)
        output = self.fc(final_output)  # (batch_size, output_size)
        return output



def train_model(model, x_train, y_train, criterion, optimizer, num_epochs, batch_size):
    model.train()
    for epoch in range(num_epochs):
        epoch_loss = 0
        for i in range(0, len(x_train), batch_size):
            x_batch = x_train[i:i + batch_size]
            y_batch = y_train[i:i + batch_size]

            optimizer.zero_grad()
            outputs = model(x_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()

        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss/len(x_train):.4f}")




def evaluate_model(model, x_test, y_test):
    model.eval()
    with torch.no_grad():
        predictions = model(x_test)
        mse = criterion(predictions, y_test)
        print(f"Test MSE: {mse.item():.4f}")



# 6. Lưu mô hình sang ONNX
# Kiểm tra mô hình với một số cụ thể
def test_model_with_specific_input(model, input_value):
    model.eval()
    with torch.no_grad():
        # Tạo đầu vào từ số cụ thể
        specific_input = torch.tensor(input_value, dtype=torch.float32).view(1, len(input_value),
                                                                             1)  # Shape: (batch_size=1, seq_length, input_size=1)
        print(f"Testing input: {specific_input}")

        # Chạy mô hình
        prediction = model(specific_input)
        print(f"Model prediction: {prediction}")
        return specific_input, prediction





def save_model_to_onnx_with_test_input(model, file_name, specific_input):
    model.eval()
    torch.onnx.export(
        model,  # Mô hình PyTorch
        specific_input,  # Đầu vào cụ thể
        file_name,  # Tên tệp ONNX
        export_params=True,  # Lưu trọng số mô hình
        opset_version=11,  # Phiên bản ONNX
        do_constant_folding=True,  # Bật tối ưu hóa hằng số
        input_names=['input'],  # Tên đầu vào
        output_names=['output'],  # Tên đầu ra
        # dynamic_axes={  # Định nghĩa các trục động
        #     'input': {0: 'batch_size'},
        #     'output': {0: 'batch_size'}
        # }
    )
    print(f'Model saved to {file_name} with specific input.')




if __name__ == '__main__':
    seq_length = 5
    num_samples = 1000
    x_data, y_data = generate_data(seq_length, num_samples)

    # Chia thành tập huấn luyện và kiểm tra
    train_size = int(0.8 * num_samples)
    x_train, x_test = x_data[:train_size], x_data[train_size:]
    y_train, y_test = y_data[:train_size], y_data[train_size:]

    # 3. Khởi tạo mô hình, hàm mất mát và tối ưu hóa
    input_size = 1
    hidden_size = 32
    output_size = 1
    model = BiLSTMModel(input_size, hidden_size, output_size)

    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # 4. Huấn luyện mô hình
    num_epochs = 50
    batch_size = 32

    train_model(model, x_train, y_train, criterion, optimizer, num_epochs, batch_size)

    # 5. Kiểm tra mô hình
    evaluate_model(model, x_test, y_test)

    # Đầu vào cụ thể để kiểm tra (ví dụ: chuỗi [3, 6, 9, 2, 5])
    specific_input_value = [3, 6, 9, 2, 5]
    specific_input, specific_output = test_model_with_specific_input(model, specific_input_value)

    # Lưu mô hình ONNX với đầu vào cụ thể
    save_model_to_onnx_with_test_input(model, "bilstm_model.onnx", specific_input)
