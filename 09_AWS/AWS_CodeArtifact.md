
# Quy trình deploy package và build package
## 1. Deploy package lên AWS CodeArtifact:

+ Document AWS CodeArtifact: https://docs.aws.amazon.com/codeartifact/latest/ug/welcome.html
  + AWS CodeArtifact là dịch vụ kho lưu trữ hiện vật an toàn, có khả năng mở rộng cao và được quản lý giúp các tổ chức 
lưu trữ và chia sẻ các gói phần mềm để phát triển ứng dụng.

+ Sử dụng make: https://www.gnu.org/software/make/manual/make.html

`make deploy-lib`: Lệnh này sử dụng make để chạy mục tiêu deploy-lib trong Makefile

  + `clear-old-version login-deploy`: Đây là các mục tiêu phụ (dependencies) của deploy-lib

  + `python3 setup.py sdist bdist_wheel`: sử dụng setup.py để **tạo các gói phân phối của thư viện Python.**
    + `sdist`: Tạo gói phân phối nguồn (source distribution).
    + `bdist_wheel`: Tạo gói phân phối nhị phân (binary distribution) dưới dạng .whl.

  + `twine upload --repository codeartifact dist/*`: Lệnh này sử dụng twine để upload các gói phân phối đã tạo lên repository codeartifact.
    + https://packaging.python.org/en/latest/key_projects/#twine
    + `dist/*`: Chỉ định tất cả các file trong thư mục dist (nơi chứa các gói phân phối đã tạo)
  + `python3 -m pip config set global.index-url https://pypi.org/simple/`: Đặt lại URL của chỉ mục gói toàn cầu của pip về mặc định của PyPI.
    + Điều này đảm bảo rằng pip sẽ sử dụng chỉ mục gói mặc định của PyPI cho các lệnh cài đặt gói trong tương lai. 


## 2. Build Docker image:
`make CODEARTIFACT_AUTH_TOKEN=$(aws codeartifact get-authorization-token  --domain itrvn-pypi 
--domain-owner 387601267200 --query authorizationToken --output text) docker-base-build`

+ Sử dụng AWS CLI để lấy mã thông báo ủy quyền từ AWS CodeArtifact.
+ Thiết lập biến môi trường CODEARTIFACT_AUTH_TOKEN với mã thông báo ủy quyền.
+ Chạy mục tiêu `docker-base-build` trong Makefile để build Docker image. Mục tiêu này có thể bao gồm các bước để tạo
Docker image với các phụ thuộc cần thiết, bao gồm TensorFlow.

## 3. Push Docker image lên Docker registry:
`make docker-base_push`

+ Lệnh này sử dụng make để chạy mục tiêu docker-base_push trong Makefile. 
+ Mục tiêu này có thể bao gồm các bước để push Docker image đã build lên một Docker registry (ví dụ: Docker Hub hoặc Amazon ECR).


