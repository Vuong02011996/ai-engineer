# Khái niệm.
+ `HyperText Markup Language` (ngôn ngữ đánh dấu siêu văn bản), nó được dùng để tạo ra các tài liệu hiển thị được trên trình duyệt.
+ `Siêu văn bản (HyperText)`: Ám chỉ sự liên kết giữa các trang, một trang HTML có liên kết tham chiếu đến một trang khác trên cùng một Website hay giữa các website.
+ HTML sử dụng cách đánh dấu (markup) để chú thích cho các thành phần (`phần tử HTML`) như văn bản, hình ảnh ... các phần tử HTML tạo thành trang tài liệu hiện thị được trong các trình duyệt.
+ HTML4(1990) -> XHTML(2014-2015) -> HTML5
+ Có rất nhiều `thẻ HTML` như :
    ```html
    <p>, <a>, <img>, <title>, <body> ... 
    ```
+ Một `phần tử HTML` bắt đầu bằng mở thẻ (viết tên thẻ như `p, a, img ... giữa < và >`), đến nội dung phần tử và kết thúc bằng đóng thẻ - viết tên thẻ giữa `</ và >`  
+ Example: 
    ```html
    <p>Hello world!</p>
    ```
+ Có hai loại thẻ phân loại theo hình thức sử dụng:
  + **Thẻ HTML chứa nội dung** (có chứa nội dung, giữa mở thẻ và đóng thẻ, như thẻ `<p>, <title>, <h1> ...`)
  + **Thẻ HTML rỗng** (chỉ mở thẻ, không đóng thẻ, không chứa nội dung như thẻ `<br>, <img> ...`)
# Các thành phần công nghệ có trong trang HTML
  Với một trang HTML hiện đại thường thấy có các thành phần sau:
  + **HTML**: Mô tả cấu trúc của trang (các nội dung xuất hiện trên trang theo một cấu trúc).
  + **CSS**: Trình bày cấu trúc (định dạng, format ... như màu sắc, canh lề, font chữ ...)
  + **JavaScript**: Ứng xử của trang (tương tác với người dùng, thi hành các tác vụ khi trang web đã được tải về ...)

# Cấu trúc trang HTML
```html
Cấu trúc cơ bản cho mọi trang HTML
<!doctype html>
<html>
   <head>
      <meta  charset="utf-8" /> 
      <title>Trang HTML Đầu tiên</title>
   </head>
   <body>
      Chào tất cả mọi người, tôi là HTML 
   </body>
</html>
```
+ Thẻ `<html>`: 
  + Một tài liệu (trang) HTML hoàn chỉnh có một thẻ gốc là `<html>`, mọi thẻ khác trình bày trong thẻ `<html>` này, thông thường nó chứa trực tiếp 2 thẻ là `<head>` và `<body>`.
  + Trước thẻ `<html>` có đoạn text xác định nó là tài liệu HTML và phiên bản HTML. Hiện giờ bản chỉ cần ấn định là HTML5 với đoạn text `<!DOCTYPE html>`
+ Thẻ `<head>`: 
  + Đây là thẻ cần mở ngay sau mở thẻ `<html>`, thẻ `<head>` chứa các thành phần (phần tử HTML) hầu như là không hiện thị tới người dùng, chúng là các điều khiển, thiết lập giúp trang html được hiện thị theo một mục đích cụ thể
  + Ví dụ thiết lập encoding (bảng mã kỹ tự), nạp file CSS, thiết lập các keywords ...
  + Một văn bản HTML chỉ dùng một thẻ `<head>`
  + Một số thẻ tạo phần tử trong thẻ `<head>`
    + Thẻ `<title>` nằm trong thẻ `<head>`, nó thiết lập tiêu đề trang HTML. Mặc dù không bắt buộc nhưng mọi trang web nên có thẻ này.
    + Thẻ `<meta>` đặt trong thẻ `<head>` để thêm metadata(các thông tin mô tả cho trang (siêu dữ liệu), các thông tin này gọi là metadata), nó là thẻ tạo ra phần tử rỗng (chỉ mở thẻ - thiết lập dữ liệu qua các thuộc tính)
      Có rất nhiều loại dữ liệu metadata có thể thêm vào, như một số trường hợp sau:
      + Thiết lập trang encoding là UTF-8 (thiết lập bảng mã cho các ký tự): dùng thẻ meta và thuộc tính charset của nó: `<meta charset="utf-8">`
      + Thiết lập mô mô tả ngắn ngọn về trang (search engine đọc nội dung này): `<meta name="description" content="Mô tả về trang">`
      + Thiết lập Viewport: `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
        + Viewport là phần không gian cửa sổ trình duyệt hiện thị trang, để trang HTML đáp ứng tốt cho nhiều loại màn hình (desktop, điện thoại ...) thì cần thiết lập viewport như trên. Sử dụng cú pháp trên, thì viewport rộng bằng chiều rộng màn hình thiết bị (trình duyệt), khi trang nạp thiết lập độ thu phóng là 1.
+ Thẻ `<body>`:
  + Thẻ `<body>` nằm trong thẻ `<html>`, những thành phần hiện thị tới người dùng (đoạn văn, hình ảnh, liên kết ...) phải nằm trong thẻ này.
  + Một trang HTML chỉ có 1 thẻ `<body>`