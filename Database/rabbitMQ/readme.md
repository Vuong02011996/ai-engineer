# Ref
https://viblo.asia/p/xay-dung-rabbitmq-su-dung-docker-va-nodejs-QpmleR2V5rd

# Concept
+ RabbitMQ là một **message broker** (MOM - Message-Oriented Middleware), sử dụng giao thức **AMQP** (Advanced Message Queue Protocol)
+ RabbitMQ là một phần mềm trung gian được sử dụng như là phương tiện liên lạc giữa các ứng dụng, dịch vụ với nhau.

# Kiến trúc một message queue
+ Producer : là ứng dụng client, tạo message và publish tới broker.
+ Consumer : là ứng dụng client khác, kết nối đến queue, subscribe (đăng ký) và xử lý (consume) message.
+ Broker (RabbitMQ) : nhận message từ Producer, lưu trữ chúng an toàn trước khi được lấy từ Consumer.

# Các thuật ngữ cần nắm trong mô hình message queue
+ Producer: Phía bên đảm nhận việc gửi message. Bạn có thể xem đây là người cần gửi thư cho một ai đó
+ Consumer: Phía bên đảm nhận việc nhận message. Bạn có thể xem đây là người nhận được thư mà ai đó gửi tới.
+ Message: Thông tin dữ liệu truyền từ Producer đến Consumer. Đây chính là thư được gửi đi chứa nội dung gửi, nó có thể là thư tay, hàng hóa, bưu phẩm…
+ Queue: Nơi lưu trữ messages. Bạn có thể xem đây là một hòm lưu trữ thư với cơ chế, ai gửi trước thì được chuyển phát trước (**First in first out**)
+ Exchange: Là nơi nhận message được publish từ Producer và đẩy chúng vào queue dựa vào quy tắc của từng loại Exchange. Để nhận được message, queue phải được nằm (binding) trong ít nhất 1 Exchange
+ ...

# Install 
## RabbitMQ server bằng docker-compose 
+ https://x-team.com/blog/set-up-rabbitmq-with-docker-compose/

```commandline
version: "3.2"
services:
  rabbitmq:
    image: rabbitmq:3-management-alpine
    container_name: 'rabbitmq'
    ports:
        - 5672:5672
        - 15672:15672
    volumes:
        - ~/.docker-conf/rabbitmq/data/:/var/lib/rabbitmq/
        - ~/.docker-conf/rabbitmq/log/:/var/log/rabbitmq
    networks:
        - rabbitmq_go_net

networks:
  rabbitmq_go_net:
    driver: bridge
```
+ We're using an Alpine implementation of RabbitMQ with the management plugin.
+ The Alpine distro is the one you'll want to use if you want to save disk space.

## Tạo ra Publisher và Consumer bằng python
