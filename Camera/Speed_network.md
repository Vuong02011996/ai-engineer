# Độ phân giải các loại camera 
+ 1MP Megapixel (1280*720): bitrate 2048 Kbps(2Mbps), chuẩn nén H264
+ 2MP Megapixel (1920*1080): bitrate 4096 Kbps(4Mbps), chuẩn nén H264
+ 4MP Megapixel (2560*2440): bitrate 8192Kbps = 1024KBps = 8Mbps, chuẩn nén H264

# 4 Yếu tố liên quan đến tốc độ camera
+ Độ phân giải của Camera IP nào cao hơn sẽ yêu cầu nhiều băng thông Internet hơn.
+ FPS (Tốc độ khung hình trên giây). FPS càng cao thì càng cần sử dụng nhiều băng thông internet hơn
+ Codec nén video. Nó xác định cách video được đóng gói và nén trước khi được gửi qua Internet. Có 2 loại định dạng nén video phổ biến: H.264 và MJPEG(Camera IP H.264 HD với khả năng nén tốt hơn nó chiếm ít băng thông internet hơn so với Camera IP MJPEG)
+ Số lượng camera an ninh IP của bạn. Càng sử dụng nhiều camera IP thì bạn cần phải cung cấp tốc độ Internet càng cao cho camera an ninh của bạn.

# Cách tính băng thông mạng cần thiết cho camera IP
+ Giá trị mặc định của camera IP 1080P là 4096Kbps, do đó băng thông cần thiết là: 4096Kbps ÷ 8 (1 byte = 8 bit) = 512 KBps = 4 Mbps.
+ Vì thế:  một camera IP 4.0 Megapixel sẽ đòi hỏi băng thông là: 8192Kbps = 1024KBps = 8Mbps.
+ [ref](https://congnghehoangnguyen.com/cach-tinh-dung-luong-luu-tru-camera-an-ninh-chinh-xac.html#:~:text=C%C3%B4ng%20th%E1%BB%A9c%20t%C3%ADnh%20dung%20l%C6%B0%E1%BB%A3ng%20%E1%BB%95%20c%E1%BB%A9ng%20camera%20%C4%91%C6%B0%E1%BB%A3c%20t%C3%ADnh,v%E1%BB%9Bi%20camera%20IP%20720P%3A%202048Kbps.)

# Ref
+ [camera mau](https://shopee.vn/Camera-Speed-Dome-4MP-IP-HIKVISION-DS-2DE3A404IW-DE---H%C3%A0ng-ch%C3%ADnh-h%C3%A3ng-i.156178331.4076307999?gclid=CjwKCAiA9tyQBhAIEiwA6tdCrCfQNiDLOsjGDMA14C13mYAqpTfDYqsMgt-CCFRI8fp3IS9O5W8fDBoCZ6MQAvD_BwE)
+ [fpt camera](https://fptcamera.com.vn/bang-thong-internet-danh-cho-camera-ip/)
+ [tinh dung luong o cung cho camera](https://annhien.vn/tinh-dung-luong-o-cung-cho-camera/)