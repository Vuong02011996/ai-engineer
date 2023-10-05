# LAN
+ Local Area Network 

# WAN - Internet 

# Tunnel (vd: ngrok)
+ Đường hầm 
+ ngrok Tạo một đường hầm thông đến IP port đến máy khác mạng LAN mà không cần `Forwarding port`, thông qua web socket.

# PORT FORWARDING - NAT PORT -  MỞ PORT 
+ NAT Port, Port Forwarding là quá trình chuyển tiếp một port cụ thể từ mạng này đến mạng khác.
+ Port forwarding là quá trình chuyển một port cụ thể trong hệ thống mạng cục bộ LAN từ một client/terminal/node qua một client/terminal/node của một network khác, điều này sẽ cho phép các clients/terminals/nodes bên ngoài có thể truy cập vào clients/terminals/nodes trong mạng LAN bằng cách sử dụng cái port đó từ bên ngoài thông qua cái Router/Modem/Firewall `đã mở chức năng NAT`.
+ Network Address Translation - NAT là công việc liên quan tới việc ghi lại các địa chỉ nguồn gốc/điểm tới của các gói dữ liệu vận chuyển qua Router/Firewall ta gọi là NAT.
+ Nhà mạng thường sẽ cung cấp một ip public trên router nếu NAT port đúng và dịch vụ server bên trong chạy thì bên ngoài sẽ sử dụng được thông qua IP public và Port nat đó nhưng một số trường hợp nhà mạng sẽ không public IP đó mà phải NAT thêm một lần ISP2(NAT port 2 lần). Ta kiểm tra bằng cách truy cập vào router và tab WAN xem IP và check IP public của máy server xem giống nhau không. Nếu giống thì chỉ cần mở port là được.
