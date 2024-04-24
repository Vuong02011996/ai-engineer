# MakeFile 
+ Là một file chứa các chỉ thị để tự động hóa quá trình biên dịch và xây dựng phần mềm.
+ Các lệnh thường dùng trong Makefile:
    + all: biên dịch và xây dựng toàn bộ dự án.
    + clean: xóa file và thư mục, làm sạch dự án và chuẩn bị cho quá trình biên dịch mới sạch sẽ.
    + install: cài đặt phần mềm đã biên dịch vào hệ thống, bao gồm sao chép các file thực thi và các tài nguyên khác vào vị trí chỉ định.
    + uninstall: gỡ cài đặt phần mềm đã cài đặt trước đó.
    + test: thực hiện các bước kiểm thử tự động.
# Cmake 
+ Là một công cụ tạo Makefile tự động dựa trên các cấu hình dự án.
+ cmake ..
# Make
+ Là một công cụ dòng lệnh thực thi các chỉ thị trong Makefile để biên dịch và xây dựng dự án.
+ make -j8
# Makefile vs DockerFile 

# Meson, ninja 
```Build and install gst-python:
cd 3rdparty/gstreamer/subprojects/gst-python/
meson build
meson configure
cd build
ninja
ninja install
```
+ meson build: Lệnh này sử dụng Meson để tạo một thư mục con mới có tên là build để chứa các tệp cấu hình và tệp tạm thời cho quá trình biên dịch. Meson là một công cụ tạo hệ thống tự động cho việc cấu hình, biên dịch và triển khai dự án.
+ meson configure:  lệnh này sẽ cấu hình các tùy chọn cần thiết cho quá trình biên dịch như đường dẫn thư viện, cấu hình bật/tắt tính năng cụ thể, và các tùy chọn biên dịch khác.
+ ninja: Lệnh này sử dụng công cụ build Meson để thực hiện quá trình biên dịch dự án từ mã nguồn đã được cấu hình. ninja là công cụ build được Meson sử dụng để tạo ra các tệp thực thi từ mã nguồn.
+ ninja install: Lệnh này sử dụng công cụ build Meson để cài đặt các tệp thực thi và các tài nguyên khác được tạo ra từ quá trình biên dịch vào hệ thống.

