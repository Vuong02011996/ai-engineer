# Basic command
+ `FROM`: Chỉ định image gốc (base image) từ đó xây dựng image mới.
     -  `FROM ubuntu:20.04`
+ `RUN`: Thực thi các lệnh trong quá trình build image (thường dùng để cài đặt các phần mềm, công cụ cần thiết).
     - `RUN apt-get update && apt-get install -y nginx`
+ `COPY`: Sao chép các tệp từ máy chủ build (host) vào container. 
     - `COPY ./app /usr/src/app`
+ `ADD`: Tương tự COPY nhưng có thể xử lý thêm một số định dạng như file nén hoặc tải tệp từ URL. 
     - `ADD https://example.com/file.tar.gz /tmp/`
+ `CMD`: Xác định câu lệnh mặc định sẽ chạy khi container khởi động. Chỉ có một lệnh CMD trong mỗi Dockerfile. 
     - `CMD ["nginx", "-g", "daemon off;"]`
+ `ENTRYPOINT`: Giống CMD nhưng không thể bị ghi đè bởi lệnh khi chạy container. Dùng để định nghĩa câu lệnh chính bắt buộc phải chạy
     - `ENTRYPOINT ["python", "app.py"]`
+ `WORKDIR`: Đặt thư mục làm việc cho các lệnh tiếp theo. - `WORKDIR /usr/src/app`
+ `ENV`: Thiết lập biến môi trường. - `ENV NODE_ENV=production`
+ `EXPOSE`: Chỉ định các cổng mà container sẽ lắng nghe. - `EXPOSE 80`
+ `VOLUME`: Khai báo một thư mục làm volume để chia sẻ dữ liệu giữa container và máy chủ hoặc giữa các container. - `VOLUME ["/data"]`
+ `ARG`: Khai báo biến được truyền vào trong quá trình build image (build-time variable). - `ARG VERSION=1.0`
+ `USER`: Xác định người dùng nào sẽ được sử dụng để chạy các lệnh tiếp theo. - `USER nginx`

# Conflict
+ ARG vs ENV
+ ADD vs COPY
+ ENTRYPOINT vs CMD

