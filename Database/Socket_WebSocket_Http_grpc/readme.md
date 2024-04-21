
# Socket vs Websocket
+ https://topdev.vn/blog/socket-la-gi-websocket-la-gi/
+ https://teky.edu.vn/blog/socket-la-gi/
## Socket 
+ Nghĩa là một socket được sử dụng để cho phép 1 process nói chuyện với 1 process khác.
+ Socket giúp lập trình viên kết nối các ứng dụng để truyền và nhận dữ liệu trong môi trường có kết nối Internet bằng cách sử dụng phương thức TCPIP và UDP.
+ Khi cần trao đổi dữ liệu cho nhau thì 2 ứng dụng cần phải biết thông tin IP và port bao nhiêu của ứng dụng kia.
+ Có rất nhiều dạng socket khác nhau phụ thuộc vào sự khác biệt giữa cách truyền dữ liệu (protocol). Dạng phổ biến nhất là TCP và UDP.
## Phân loại socket :
+ Hiện nay, có tổng cộng 4 loại module socket đang hiện hành bao gồm: 
  + Stream Socket, 
  + Datagram Socket, 
  + Websocket 
  + Unix socket. 
+ Stream Socket và Websocket thường được sử dụng phổ biến nhất. Hai loại còn lại thì ít được dùng hơn.
  + **Stream Socket**:
    + Dựa trên giao thức TCP( Tranmission Control Protocol), 
    + Stream socket thiết lập giao tiếp 2 chiều theo mô hình client và server. 
    + Được gọi là socket hướng kết nối.
    + Các bản ghi dữ liệu cũng không hề có giới hạn nào, bạn có thể thoải mái truyền bao nhiêu thông tin tùy thích. 
    + Song song với đó, Stream Socket còn sở hữu 2 cơ chế bao gồm quản lý luồng lưu thông trên mạng và chống tắc nghẽn nhằm tối ưu hóa thời gian truyền dữ liệu.
    + Mỗi thông điệp được thực hiện phải có thông báo trả về mới tính là hoàn thành. 
    + Ngoài ra, Stream Socket hoạt động dựa trên mô hình lắng nghe và chấp nhận. Có nghĩa rằng giữa 2 process phải có 1 bên yêu cầu kết nối trước.
  + **Datagram Socket**:
    + Dựa trên giao thức UDP( User Datagram Protocol) 
    + Việc truyền dữ liệu không yêu cầu có sự thiết lập kết nối giữa 2 process.
    + Gọi là socket không hướng kết nối.
    + Do không yêu cầu thiết lập kết nối, không phải có những cơ chế phức tạp. Nên tốc độ giao thức khá nhanh, thuận tiện cho các ứng dụng truyền dữ liệu nhanh như chat, game online…
    + Datagram Socket không đảm bảo tuyệt đối kết quả của tiến trình. Một số trường hợp ghi nhận thông điệp không thể đến tay của bên nhận.
  + **Unix socket**:
    + Unix socket được biết đến như một điểm chuyển giao giữa các ứng dụng ở trong một máy tính. 
    + Vì không phải qua bước kiểm tra và routing nên quá trình truyền tin diễn ra vô cùng nhẹ nhàng và nhanh chóng.
    + Unix socket vẫn còn một số nhược điểm tồn đọng như: không thể dịch chuyển giữa 2 máy khác nhau, đôi khi xảy ra delay do vấn đề phân quyền giữa các tệp tin.
  + **Websocket**:
    + Websocket là giao thức hỗ trợ giao tiếp hai chiều giữa client và server để tạo một kết nối trao đổi dữ liệu.
    + Giao thức này không sử dụng HTTP mà thực hiện nó qua TCP. 
    + Mặc dù được thiết kế để chuyên sử dụng cho các ứng dụng web, lập trình viên vẫn có thể đưa chúng vào bất kì loại ứng dụng nào.
    + Websocket sở hữu gần như hầu hết những ưu điểm của các loại socket khác như: tỷ lệ xảy ra delay thấp, dễ xử lý lỗi, khả năng dịch chuyển thông tin nhanh chóng và mạnh mẽ,
    + Phù hợp cho những hoạt động cần đến tính tức thời như chat realtime, chat online, biểu đồ chứng khoán…
    + Giao thức chuẩn phổ biến nhất của WebSocket là ws:// . Còn giao thức secure là wss:// . WebSocket có chuẩn giao tiếp là String và hỗ trợ buffered arrays cùng blobs.
    + Tuy ưu việt là thế nhưng Web socket vẫn có một số nhược điểm. Một số trình duyên chưa có khả năng tương thích với Websocket. 
    + Bên cạnh đó, Websocket cũng sẽ dễ bị hạn chế với các dịch vụ có phạm vi yêu cầu.

# Compare http(fastAPI), socket(tcp), grpc(http2):
+ Socket - web socket chậm nhất.
+ FastAPI - (32FPS)
+ grpc - (36FPS)