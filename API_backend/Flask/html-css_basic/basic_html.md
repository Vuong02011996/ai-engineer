## HTML
[xuanthulab](https://xuanthulab.net/html/)
##1. Thẻ `<p>` , `<br>` va khoảng trắng trong đoạn văn HTML
+ Thẻ `<p>`:
  + Để tạo ra một đoạn văn bản (paragraph), đơn giản là sử dụng `<p>` với nội dung văn bản (text) nằm giữa mở thẻ `<p>` và đóng thẻ `</p>`.
    ```html
    <p>Nội dung trong thẻ ... </p>
    ```
  + Với thẻ `<p>`, trình duyệt tạo ra một khối (chữ nhật) để hiện thị nội dung văn bản, khối này phân cách bởi các dòng trống.

+ Thẻ `<br>`:
  + Thẻ `<br>` dùng để ngắt dòng, thẻ `<br>` là thẻ rỗng, nó không cần đóng. Có thể viết bằng `<br>` hoặc `<br />`
    ```html
    <p>Những đêm hè<br>
    Khi ve ve<br>
    Đã ngủ<br>
    Tôi lắng nghe<br>
    Trên đường Trần Phú<br>
    Tiếng chổi tre</p>
    ```
+ Khoảng trắng:
  + Các khoảng trắng (whitespace) khi biên tập HTML đó là các: ký tự xuống dòng, ký tự tab, ký tự spacebar.
  + HTML bỏ qua hầu hết các khoảng trắng:
    + Nhiều khoảng trắng giữa các từ (word) thì chỉ giữ lại một
    + Các khoảng trắng ở vị trí bắt đầu hoặc ở cuối phần tử sẽ bị bỏ qua
    + Các khoảng trắng bên ngoài phần tử bị bỏ qua.
  + Chèn nhiều khoảng trắng vào HTML: các ký tự khoảng trắng chèn vào HTML cần sử dụng mã ký tự (HTML Entity) để chèn, ví dụ ký tự spacebar thì viết là &nbsp

##2. Các thẻ định dạng văn bản HTML:
+ Các thẻ để định dạng HTML gồm có:
  + Thẻ `<b>` cho biết nội dung cần nhấn mạnh,
  + Thẻ `<strong>` cho biết nội dung cần nhấn mạnh, trình duyệt hiện thị với chữ đậm
  + Thẻ `<big>` hiện thị với cỡ chữ lớn hơn một cấp (thẻ này đánh dấu lạc hậu không nên dùng nữa)
  + Thẻ `<small>` hiện thị chữ nhỏ hơn một cấp
  + Thẻ `<i>` hiện thị chữ in nghiêng
  + Thẻ `<em>` đánh dấu nhấn mạnh (hiện thị in nghiêng)
  + Thẻ `<ins>` đánh dấu đoạn text được chèn vào
  + Thẻ `<del>` đánh dấu đoạn text xóa đi
  + Thẻ `<sub>` tạo chỉ số dưới
  + Thẻ `<sup>` tạo chỉ số trên
    ```html
    <html lang="en">
       <head>
          <title>Ví dụ Định dạng HTML</title>
       </head>
       <body>
          <p>Một văn bản bình thường </p>
          <p><b> văn bản in đâm </b></p>
          <p><big> văn bản cỡ chữ lớn hơn</big></p>
          <p><i> in nghiêng văn bản </i></p>
          <p><em>nhấn mạnh (in nghiêng)</em></p>
          <p><small> văn bản chữ nhỏ hơn</small></p>
          <p><strong>nhấn mạn văn bản (hiện thị in đậm)</strong></p>
          <p>Text <sub>chỉ số dưới</sub></p>
          <p>Text <sup>chỉ số trên</sup></p>
          <p><ins> đánh dấu văn bản chèn vào </ins></p>
          <p><del> đánh dấu là văn bản được xóa </del></p>
       </body>
    </html>
    ```
##3. Các thẻ heading `<h1> - <h6>` của HTML
  + Trong một trang HTML (tài liệu) có thể phân chia ra thành nhiều đề mục với cấp độ khác nhau.
  + Có sáu cấp độ tương ứng với thẻ `<h1>` đến thẻ `<h6>`, với thẻ `<h1>` có cấp độ cao nhất (đề mục lớn nhất) và `<h6>` là cấp độ thấp nhất
  + Khi sử dụng cần sử dụng theo dúng cấp độ của đề mục - không bỏ qua đề mục (ví dụ có dùng `<h3>` mà không có `<h2>`). 
  + Trong một trang chỉ dùng một thẻ `<h1>`
    ```html
    <html>
       <head>
          <title>Kiểm tra thẻ Heading</title>
          <meta charset="UTF-8">
       </head>
       <body>
          <h1>This is heading 1</h1>
          <h2>This is heading 2</h2>
          <h3>This is heading 3</h3>
          <h4>This is heading 4</h4>
          <h5>This is heading 5</h5>
          <h6>This is heading 6</h6>
       </body>
    </html>
    ```
##4. Kẻ đường ngang với `<hr/>`
+ Thẻ `<hr>` được dùng để tạo đường kẻ ngang trong trang HTML, nó thường dùng để phân tách giữa các đoạn văn, các phân đoạn nội dung để dễ đọc, dễ theo dõi.
+ Phần tử `<hr>` có một số thuộc tính riêng gồm:
  + **width** - thiết lập độ rộng
  + **size** - thiết lập chiều cao (đơn vị px, pixel)
  + **color** - thiết lập màu đường (red, green, blue ...)
  + **align** - căn lề (left, right, center)
    ```html
    <hr width="50%">
    <p>
        XUANTHULAB.NET là blog cá nhân,
        chia sẻ những kiến thức
        công nghệ thông tin từ sử dụng
        các ứng dụng đến lập trình.
    </p>
    <hr>
    <p>
        Nội dung của blog
        là kiến thức tôi học được,
        xuất bản tại đây
        như là cách ghi chú
        để đọc lại khi cần.
    </p>
    <hr width="50%"
        color="red"
        align="right"
        size="5px">
    ```
    
##5 Chú thích(comment) trong HTML
+ Viết chú thích `<!-- ghi chú -->` trong văn bản HTML, các comment không hiện thị mà là các ghi chú giúp đọc lại code HTML dễ dàng hơn.
    ```html
    <!-- Chú thích của bạn ở đây -->
    ```
  
##6 Cấu trúc phần tử HTML và các thuộc tính HTML
1. Cấu trúc phần tử HTML
   + Một văn bản HTML được tạo ra từ các phần tử HTML. 
   + Một phần tử HTML nói chung nó được viết bởi các thẻ, bắt đầu bởi `mở thẻ <tên-thẻ>` kết thúc bởi `đóng thẻ </tên-thẻ>` và ở giữa là **nội dung phần tử**.
   + Các phần tử HTML có thể lồng vào nhau, nghĩa là phần tử này chứa phần tử khác
       ```html
       <html>
           <head>
               <title>Phần tử HTML</title>
               <meta charset="UTF-8">
           </head>
           <body>
               <p>Đây là một đoạn văn <br /></p>
           </body>
       </html>
       ```
     
2. Các thuộc tính HTML
   + Các thuộc tính nhằm thiết lập thêm thông tin cho các thẻ (phần tử HTML).
   + Hầu hết thuộc tính phần tử HTML thiết lập bằng `tên` thuộc tính và `giá trị` đi cùng với nó.
   + Các thuộc tính của phần tử HTML viết tại tại vị trí `mở thẻ`, giữa ký hiệu `<tên-thẻ` và ký hiệu `>`
   + Thuộc tính viết theo cặp : `tên-thuộc-tính="giá trị"`
   + Các thuộc tính thông dụng:
     + Thuộc tính kích thước **width**:
       + Thuộc tính này thiết lập độ rộng phần tử, nó có tác động trên các phần tử như:` <hr>, <canvas>, <embed>, <iframe>, <img>, <input>, <object>, <video>`
       + Ngoài đơn vị px như trên, bạn có thể xác định theo tỷ lệ phần trăm:
       ```html
        Tạo đường ngang với kích thước ấn định có độ rộng là 50 pixel
        <hr width="50px" />
        <hr width="50%" />
        ```
     + Thuộc tính canh lề **align**:
       + align là thuộc tính xác định cách căn lề của phần tử `( <caption>, <col>, <colgroup>, <hr>, <iframe>, <img>, <table>, <tbody>, <td>, <tfoot> , <th>, <thead>, <tr>)` theo chiều ngang nó có thể nhận các giá trị:
         + align = "left" canh trái
         + align = "right" canh phải
         + align = "center" canh giữa
         + align = "justify" canh đều
       ```html
        <html>
           <head>
              <title>Attributes</title>
           </head>
           <body>
              <p align="center">This is a text <br />
                 <hr width="10%" align="right" /> This is also a text.
              </p>
           </body>
        </html>
        ```
     + Thuộc tính toàn cục:
       + Các phần tử HTML khác nhau có thể có các thuộc tính khác nhau (thuộc tính này dùng được cho phần tử này nhưng chưa chắc đã dùng được cho phần tử khác). 
       + Do vậy, mỗi phần tử cần xem xét các thuộc tính riêng của nó
       + Tuy nhiên có một số thuộc tính mà mọi phần tử HTML đều có thể có gọi là các thuộc tính toàn cục:
         + **accesskey**: Chỉ ra một phím tắt kích hoạt phần tử. 
         ```html
         <a href="https://xuanthulab.net" accesskey="x">HTML</a>
         ```
         + **class**: Chỉ ra một hoặc nhiều tên lớp áp dụng cho phần tử (lớp liên quan CSS) 
         ```html
         <a href="https://xuanthulab.net" class="link1 link2">HTML</a>
         ```
         + **contenteditable**:Cho biết nội dung trong phần tử có thể soạn thảo biên tập lại hay không. Nếu true thì sẽ xuất hiện box soạn thảo cho phần tử
          ```html
          <p contenteditable="true">Nội dung này soạn thảo được</p>
         ```
         + **data-***: Thuộc tính thiết lập dữ liệu riêng cho phần tử, ký hiệu * là một tên tự đặt. data-* là chuẩn đặt tên thuộc tính dữ liệu dùng cho HTML5
         ```html
         <p data-dulieu="Đây là dữ liệu riêng">Ví dụ</p>
         ``` 
         + **draggable**: Chỉ ra phần tử có thể kéo thả (true,false, auto)
         ```html
          <p draggable="true">Ví dụ</p>
         ```
         + **hidden**: Khi có thuộc tính này phần tử sẽ ẩn
         ```html
         <p hidden>Ví dụ</p>
         ```
         + **id**: Thiết lập một định danh duy nhất cho phần tử HTML. Định danh này để tìm kiếm trong DOM
         ```html
          <p id="idphantup">Ví dụ</p>
         ```
         + **spellcheck**: Cho trình duyệt biết có kiểm tra ngữ pháp phần tử này hay không
         ```html
          <p spellcheck="true">Có kiểm tra ngữ pháp</p>
         ```
         + **style**: Định nghĩa CSS cho phần tử.
         ```html
          <p style="font-size: 18px">Inline style sheet</p>
         ```
         + **title**: Thông tin thêm về phần tử
         ```html
         <p title="Thông tin thêm">Đây là đoạn văn</p>
         ```
##7 Chèn ảnh vơi thẻ `<img>`
+ Thẻ <img> được dùng để nhúng một hình ảnh vào trang HTML.
+ Thẻ này có vài thuộc tính và nó không có phần đóng thẻ.
+ Địa chỉ URL dẫn đến vị trí của ảnh được xác định thông qua thuộc tính `src`.
+ Vị trí URL ảnh phải nằm giữa dấu nháy kép "url"
+ Trong trường hợp ảnh không hiện thị được (ví dụ ảnh bị xóa ...) thì thuộc tính `alt` là một văn bản thay thế sẽ hiện thị thay cho ảnh. 
+ Nói chung bất kỳ ảnh nào trong HTML thì thuộc tính alt yêu cầu nên có.
+ Điều chỉnh cỡ ảnh hiện thị bạn có thể chỉ ra chiều rộng và chiều cao của ảnh thông qua thuộc tính `width` và `height`. Đơn vị sử dụng là pixel `px` hoặc phần trăm `%`
+ Mặc định, anh không có đường viền bao quanh. Để tạo đường viền bao quanh ảnh sử dụng thuộc tính `border` và chỉ ra kích cỡ của đường viền theo đơn vị `px`
```html
<html>
   <head>
      <title>Ví dụ về ảnh</title>
   </head>
   <body> 
      <img 
            border="4px"
            width="700px"
            src="https://raw.githubusercontent.com/xuanthulabnet/learn-php/master/imgs/php-004.png" 
            alt="vi du" />
   </body>
</html>
```

## Tạo liên kết với thẻ `<a>` anchor(mỏ neo)
1. Phần tử liên kết - mỏ neo `<a>`
+ Các liên kết - link là một phần không thể thiếu cho mọi trang web. 
+ Bạn có thể thêm link dạng text(văn bản) hay dạng ảnh mà người dùng bấm chuột vào nó để chuyển hướng đến một trang web khác, một file khác
+ Thẻ `<a>` (anchor - mỏ neo) được dùng để tạo ra các liên kết, với thuộc tính `href` được thiết lập là siêu liên kết (hyperlink) trỏ tới các trang, các file, địa chỉ email, bất kỳ loại địa chỉ URL nào ... 
+ Nội dung trong thẻ `<a>` có thể là text, hình ảnh ... cho biết trang được liên kết đến
```html
<p>Liên hệ với xuanthulab:</p>
<p>
- Website: <a href="https://xuanthulab.net">xuanthulab.net</a> <br>
- Email: <a href="mailto:xuanthulab.net@gmail.com">xuanthulab.net@gmail.com</a> <br>
- Phone: <a href="tel:+84977xxxx">0977.xxx.xxx</a>
</p>
```

















