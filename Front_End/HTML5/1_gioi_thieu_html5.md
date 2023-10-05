# Giới thiệu
+ Là phiên bản mới của HTML để trình bày trang web.
## Các phần tử mới
```commandline
<article>, <aside>, <audio>, <canvas>, <datalist>, 
<details>, <embed>, <footer>, <header>, <nav>, 
<output>, <progress>, <section>, <video> ...

```
## Cải tiến FORM
+ HTML5 hỗ trợ Web Form 2.0 tạo ra các form mạnh mẽ hơn
+ Hỗ trợ điều khiển chọn ngày tháng, màu sắc, chọn số
+ Hỗ trợ kiểu input mới như `email`, `search`, `URL`
+ Ngoài phương thức **get**, **post** hỗ trợ thêm phương thức **put** và **delete**

## Tích hợp API
Tích hợp một số API trong giao diện như:
+ `Kéo và thả` trong HTML
+ Phát `Audio, Video`
+ Ứng dụng Web Offline
+ Các hàm `truy cập lịch sử` duyệt web
+ Lưu trữ `dữ liệu nội bộ`
+ Các hàm về `vị trí (địa lý)`
+ Gửi thông điệp Web

## Nội dung được phân chia thành 7 mô hình.
1. Metadata
   + Thiết lập cách hiển thị và ứng xử của trang.
   + Những loại phần tử này ở phần head của trang.
   + Các phần tử như :
   + ```commandline
        <base>, <link>, <meta>, <noscript>, <script>, <style>, <title>
        ```
2. Nhúng dữ liệu
   + Nội dung đa dạng được nhúng vào trang web.
   + Các phần tử thuộc loại nhúng dữ liệu gồm:
   ```commandline
    <audio>, <video>, <canvas>, <iframe>, <img>, <math>, <object>, <svg>
    ```
3. Interactive-phần tử tương tác
   + Các phần tử sử dụng để người dùng tương tác với trang.
   ```commandline
    <a>, <audio>, <video>, <button>, <details>, <embed>, <iframe>, <img>, <input>, <label>, <object>, <select>, <textarea>
    ```
4. Phần tử heading
   + Các phần tử trình bày tiêu đề nội dung.
   ```commandline
    <h1>, <h2>, <h3>, <h4>, <h5>, <h6>, <hgroup>
    ```
5. Pharsing
   + Các phần tử dạng inline.
   ```commandline
    <img>, <span>, <strong>, <label>, <br />, <small>, <sub> ...
    ```
6. Luồng nội dung.
   + Chứa các phần tử HTML5 trình bày theo quy tắc để tạo luồng nội dụng của trang
7. Phần đoạn Section.
   + Trình bày một phạm vi của nội dung như heading, điều hướng, chân trang
   ```commandline
    <article>, <aside>, <nav>, <section>
    ```