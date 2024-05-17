
# Meaning
+ Theo dõi lỗi tương ứng thời gian thực
+ Phân tích sự cố chi tiết: Sentry cung cấp thông tin chi tiết về các lỗi và sự cố, bao gồm cả nguồn gốc của lỗi, stack trace
+ Ghi log và thông tin môi trường: Sentry cũng ghi lại các thông tin liên quan như log của ứng dụng, thông tin môi trường (environment) và người dùng để giúp xác định nguyên nhân của lỗi.
+ Stack trace chi tiết: Sentry tự động ghi lại stack trace của lỗi, cung cấp thông tin chi tiết về nguyên nhân và nguồn gốc của lỗi, giúp nhà phát triển dễ dàng định vị và sửa chữa lỗi.
+ Cảnh báo và thông báo qua email: Bạn có thể ứng dụng cấu hình Sentry để gửi cảnh báo qua email khi có lỗi quan trọng xảy ra.
+ Liên kết với các dịch vụ issue tracker như: GitHub, Bitbucket, Trello... để tạo nhanh task

# Cài đặt Sentry lên website , sử dụng server sentry of sentry.io 
+ Tạo tài khoản Sentry: https://sentry.io/welcome/
+ Tạo một project mới
+ Cài đặt Sentry vào ứng dụng của bạn
+ Lập trình để tự gửi event theo ý muốn
  + Ngoài việc những error/exception được tự gửi đi thì bạn cũng có thể tự lập trình để gửi event đi.

# Install server sentry
## Concept
+ https://github.com/Ramhm/sentry-setup
+ **sentry-cron**: Chạy các công việc định kỳ cần thiết để duy trì và bảo trì hệ thống Sentry.
+ **sentry-worker**: Xử lý các công việc nền, bao gồm xử lý sự kiện và gửi thông báo, để đảm bảo Sentry hoạt động hiệu quả.
+ **Sentry-base** là thành phần cốt lõi của hệ thống Sentry, chạy ứng dụng web và cung cấp các API cần thiết để người dùng có thể tương tác với hệ thống. 
Nó chịu trách nhiệm chính trong việc xử lý các yêu cầu từ người dùng, hiển thị thông tin về lỗi và sự kiện, và cho phép người dùng cấu hình và quản lý các dự án và cảnh báo.
+ **Sentry Redis (sentry-redis)**:
  + Sử dụng cho caching, quản lý hàng đợi công việc, và giới hạn tốc độ.
  + Giúp cải thiện hiệu suất và xử lý công việc nhanh chóng.
+ Sentry PostgreSQL (sentry-postgres):
  + Lưu trữ dữ liệu chính và bền vững như sự kiện lỗi, thông tin dự án, người dùng, và cấu hình.
  + Đảm bảo tính nhất quán và an toàn của dữ liệu quan trọng.
# Setup sentry server 
+ Download file docker-compose from: https://github.com/Ramhm/sentry-setup
+ Tạo các folder to connect volumes container
+ Generate secret key - Run: `docker-compose run --rm sentry-base config generate-secret-key` to get SENTRY_SECRET_KEY, copy SENTRY_SECRET_KEY and pass to file .env'
+ Initialize database - Run: `docker-compose run --rm sentry-base upgrade` and create user account for sentry : vanvuong0440@gmail.com.vn, 02011996
+ Service Start - Run: `docker-compose up -d`

+ `pip install --upgrade sentry-sdk==0.10.2`

# Send noti in try exception
+ https://docs.sentry.io/platforms/python/usage/#capturing-errors

# Shutdown 
+ https://docs.sentry.io/platforms/python/configuration/draining/
+ 

# Sent info to email
+ https://develop.sentry.dev/services/email/
+ SMTP mail: SMTP (Simple Mail Transfer Protocol) là một giao thức tiêu chuẩn được sử dụng để gửi email qua mạng Internet
+ SMTP hoạt động :
  + Khi bạn gửi một email, máy khách email của bạn (ví dụ: Outlook, Gmail) sẽ kết nối với máy chủ SMTP của bạn. 
  + Máy chủ này sẽ kiểm tra và xử lý email, sau đó chuyển tiếp nó qua các máy chủ khác nhau cho đến khi đến được máy chủ email của người nhận.
  + Add to file .env:
    ```commandline
    # Cấu hình trong tập tin .env cho Sentry
    SENTRY_EMAIL_HOST=smtp.gmail.com
    SENTRY_EMAIL_PORT=587
    SENTRY_EMAIL_USER=your-email@gmail.com
    SENTRY_EMAIL_PASSWORD=your-email-password
    SENTRY_EMAIL_USE_TLS=True
    SENTRY_SERVER_EMAIL=your-email@gmail.com
    ```
  + `docker-compose down`
  + `docker-compose up -d`
# Ref:
+ https://develop.sentry.dev/ - docs for dev
+ https://docs.sentry.io/product/sentry-basics/integrate-frontend/create-new-project/#create-a-project - create project and setup for python

