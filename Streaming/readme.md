# Khái niệm
+ Stream là một kỹ thuật chuyển dữ liệu theo dòng ổn định và liên tục
+ Streaming video sử dụng cách thức phát lại các đoạn video được lưu trữ trên các máy tính trên mạng tới người dùng đầu cuối muốn xem đoạn video mà không cần tải đoạn video đó về trên máy tính.
+ Streaming hay streaming media là một quá trình mà các định dạng truyền thông (như âm thanh, hình ảnh) được gửi tới người dùng và hiển thị ngay cả khi nó vẫn đang trong quá trình tải


```commandline
"""
docker pull ossrs/srs:4
sudo docker run --rm -it -p 55555:1935 -p 55556:1985 -p 55557:8080     --env CANDIDATE="0.0.0.0" -p 55558:8000/udp     ossrs/srs:4 ./objs/srs -c conf/docker.conf
"""
```

# Ref
+ https://sites.google.com/site/embedded247/npcourse/tim-hieu-ky-thuat-video-streaming
+ https://longvan.net/video-streaming.html
+ https://ruby-forum.org/streaming-video-la-gi/
+ https://cuongquach.com/he-thong-http-live-streaming-video-la-gi.html