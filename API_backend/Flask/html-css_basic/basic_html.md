## HTML
+ [xuanthulab](https://xuanthulab.net/html/)

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
**1. Cấu trúc phần tử HTML**
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
     
**2. Các thuộc tính HTML**
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

##8 Tạo liên kết với thẻ `<a>` anchor(mỏ neo)
**1. Phần tử liên kết - mỏ neo `<a>`**
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
**2. Thuộc tính href của `<a>`**
+ Sử dụng thuộc tính `href` (hyperlink reference) để chỉ ra địa chỉ đích mà `link` mở ra.
  ```html
  <a href="https://xuanthulab.net/html/">Học HTML</a>
  ```
+ Với code HTML như trên, nó sẽ hiện thị dạng link text là: Học HTML
+ `href` nếu là email thì viết "mailto:youremail"
+ `href` là số điện thoại thì viết: "tel:phonenumber"

**3. Thuộc tính target của `<a>`**
+ Liên kết mở ra trong cửa sổ hiện tại hay cửa sổ mới của trình duyệt
+ `_self` giá trị mặc định (target của `<a>` không cần thiết lập đã nhận giá trị này). Liên kết mở ra trong cửa sổ hiện tại của trình duyệt.
+ `_blank` mở liên kết ở một Tab mới (cửa sổ mới)
  ```html
  <a href="https://xuanthulab.net">xuanthulab.net</a>
  <a href="https://xuanthulab.net" target="_blank">Mở tab xuanthulab.net</a>
  ```
##9 Tạo danh sách với `<ol>, <ul>, <li>`
+ Thẻ `<ol>` tạo danh sách có thứ tự, mỗi phần tử khi xuất hiện có chỉ số ở đầu (1,2, 3 ... A, B, C ...)
+ Thẻ `<ul>` tạo danh sách không có thứ tự, mỗi phần tử khi xuất hiện có ký hiệu như dấu chấm, gạch ngang ... ở đầu.
+ Mỗi phần tử trong danh sách là `<li>`. Mỗi phần tử trong <ul> hay <ol> được tạo ra bằng bằng thẻ <li> ở bên trong
```html
<ol type="i" start="3">
    <li>HTML</li>
    <li>CSS</li>
    <li>Javascript</li>
    <li>C#</li>
</ol>
<ul type="circle">
    <li>HTML</li>
    <li>CSS</li>
    <li>Javascript</li>
    <li>C#</li>
</ul>
```
+ Thuộc tính type của <ol> gán bằng 1, a, A, i để thiết lập một số kiểu đánh số.

##10 Tạo bảng biểu với  `<table>, <td>, <tr>, <th>`
+ Sử dụng thẻ `<table>` để tạo bảng biểu.
+ Trình bày nội dung `<table>` với các thẻ `<td>, <tr>, <th>`
+ Thiết lập tiêu đề bảng với <caption>
+ Nhóm tiêu đề cột với `<thead>` và `<tfoot>`
+ Bảng là cấu trúc phức tạp, toàn bộ nội dung của bảng được đặt vào thẻ `<table>`.
+ Trong thẻ `<table>` có thuộc tính border để thiết lập độ rộng của các dòng kẻ của bảng (hiện giờ nên dùng CSS)
+ **Thẻ `<td>`:** Trong nội dung bảng, phần tử nhỏ nhất để chứa dữ liệu là `<td>` (table data)
+ **Thẻ `<tr>`**: Để nhóm các phần tử <td> thuộc về một dòng, thì dùng thẻ `<tr>`(row)
+ **Thuộc tính colspan, rowspan của `<td>`**:
  + `rowspan` trong `<td>` có thể gán một giá trị số nguyên dương (mặc định là 1), cho biết cell (ô bảng) đó tương đương bao nhiêu dòng.
  + `colspan` trong `<td>` có thể gán một giá trị số nguyên dương (mặc định là 1), cho biết cell (ô bảng) đó tương đương bao nhiêu cột.
+ **Thẻ `<th>`**: Thẻ `<th>` tương tự như thẻ `<td>` (nằm trong thẻ `<tr>`) được dùng để đánh dấu tiêu đề của một nhóm ô bảng (cell)
+ Thẻ `<caption>`: Thẻ `<caption>` thường tạo ngay sau khi mở thẻ `<table>` để thiết lập tiêu đề của bảng
  ```html
  <table border="1">
      <caption style="caption-side: top">ĐƠN HÀNG</caption>
      <thead>
          <tr>
              <th>STT</th>
              <th>Mặt hàng</th>
              <th>Đơn giá</th>
              <th>Số lượng</th>
              <th>Thành tiền</th>
              <th>Ghi chú</th>
          </tr>
      </thead>
      <tr>
          <td>1</td>
          <td>Mặt hàng A</td>
          <td>1000</td>
          <td>1</td>
          <td>1000</td>
          <td></td>
      </tr>
      <tr>
          <td>2</td>
          <td>Mặt hàng B</td>
          <td>2000</td>
          <td>2</td>
          <td>4000</td>
          <td></td>
      </tr>
      <tfoot>
          <tr>
              <th colspan="4">Thành tiền đơn hàng</th>
              <th colspan="2">4000</th>
  
          </tr>
      </tfoot>
  </table>
  ```

##10 Phần tử dạng block và inline
+ Thẻ `<div>` dùng để định nghĩa khối block chung trong HTML
+ Thẻ `<span>` định nghĩa các inline, phần văn bản dạng inline không ngắt dòng.
+ Phần tử loại block thì có thể chứa các phần tử inline, phần tử inline thì không được chứa phần tử block
```html
<div style="background-color:green; color:white; padding:20px;">
    <p style="border:1px solid red">Một đoạn văn bản.</p>
    <p style="border: 1px solid red">Đoạn văn bản khác.</p>
</div>
```

##11 Màu sắc trong HTML
+ Màu sắc sử dụng trong HTML cũng như CSS là sự kết hợp ba màu (trộn ba màu đỏ RED, xanh lá GREEN, xanh BLUE với cường độ màu khác nhau của các màu thành phần này)
+ Cường độ màu là số nguyên có giá trị từ 0 đến 255.
+ Dùng phổ biến trong HTML, CSS là cách màu sắc được biểu diễn bằng giá trị thập lục phân hexadecimal.
+ Tức là dùng 16 chữ số: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F để biểu diễn những thành phần màu được pha trộn RGB
+ Giá trị màu Hex biểu diễn bằng cách viết ký tự hashtag (#) và theo sau là sáu ký tự HEX gồm 
  + 2 ký tự đầu là giá trị HEX là cường độ màu đỏ RED
  + 2 ký tự giữa là số hex cường độ màu xanh lá GREEN, 
  + 2 ký tự cuối là số hex cường độ màu xanh BLUE
  + Bạn thấy màu hex #8064c8 tương đương trộn màu RGB rgb(128, 100, 200) - hệ thập phân
+ Với cách biểu diễn mỗi màu đơn sắc bằng giá trị HEX với 2 ký tự thì nó biểu diễn được 256 giá trị(#FF0000). Ba màu RGB kết hợp lại sẽ biểu diễn được 16 triệu màu
+ Thuộc tính `bgcolor` dùng để thay đổi màu nền trang web
+ Khi cần thay đổi màu văn bản, bạn có thể dùng thẻ `font` kết hợp với thuộc tính color, các trường hợp khác về màu sắc trên trang ngày nay người ta dùng CSS chứ không sử dụng trực tiếp các thuộc tính thẻ HTML chuyên biệt.
```html
<html>
   <head> 
      <title>Color</title>  
   </head>
   <body bgcolor="#000099">
       <h1>
        <font color="#FFFFFF"> Chữ trắng nền đen </font>
       </h1> 
   </body>
</html>
```
##12 Tạo form trong HTML với thẻ `<form>`,các thẻ tạo phần tử điều khiển trong form như thẻ `<input>`, thẻ `<textarea>`, `<button>` ...
**1. Khái niệm web form**
+ Biểu mẫu - **web form** - được tạo ra trong HTML là khu vực hình thành nên sự tương tác giữa người dùng và ứng dụng web
+ Các form cho phép người dùng nhập dữ liệu vào, sau đó gửi dữ liệu đó cho web server, hoặc nhập dữ liệu vào xử lý dữ liệu ngay tại client side.
+ Các **form** được tạo ra bằng thẻ `<form>`, trong đó nó chứa các phần tử để nhập liệu gọi là các điều khiển (**control**), có nhiều loại điều khiển như:
  + Điều khiển nhập một dòng text
  + Điều khiển cho nhập nhiều dòng text
  + Điều khiển là các nút bấm
  + Các phần tử checkbox (hộp chọn)
  + Các phần tử radio (chọn một)
+ Hầu hết các control được tạo ra bằng phần tử là `<input>` đi cùng phần tử `<lable>` để tạo ra nhãn (tiêu đề) cho control
```html
<form action="http://xuanthulab.net" method="get">
    <label>Tên đăng nhập:</label><br>
    <input name="name" type="text" value=""><br>

    <label>Mật khẩu:</label><br>
    <input name="pass" type="password" value=""><br>

    <input type="submit" name="submit" value="Đăng Nhập" />
</form>
```
+ Để tạo ra HTML Form thì dùng đến thẻ `<form>`, sau đó nội dung trong thẻ trình bày các HTML và các phần tử là điều khiển (control) có trong form
+ Thẻ `<form>` cơ bản có hai thuộc tính cần lưu tâm là action và method:
  + **action** thuộc tính để thiết lập URL, là địa chỉ mà dữ liệu của form gửi đến (submit đến, post đến). Thiếu tham số này thì action bằng URL đang truy cập
  + **method** thuộc tính để thiết lập HTTP Method, xem thêm HTTP Request Message thường có giá trị bằng get hoặc post
  + Sử dụng `method="get"` thì khi submit dữ liệu được biểu diễn thông qua URL. Sử dụng `method="post"` thì khi submit biểu diễn trong nội dung của Request gửi đến Server và là ẩn với người dùng, sử dụng post an toàn hơn.
  + Khi thông tin gửi tới địa chỉ máy chủ (tham số action), thì dữ liệu nhận được xử lý thế nào là việc của server, bạn sẽ thực hiện việc sử lý này khi lập trình backend với một ngôn ngữ lập trình nào đó như php, c# ...
+ Để submit (gửi) form, thường tạo ra một nút bấm từ phần tử `<input>` và chỉ ra `type="submit"`, thì nó sẽ tạo ra nút bấm, khi bấm vào đó dữ liệu form sẽ gửi đi. Ví dụ:
  ```html
  <input type="submit" name="submit" value="Gửi" />
  ```
  
+ Giả sử bạn nhập vào tên là test, mật khẩu là abc thì với form sử dụng phương thức `get`, nên bấm vào đăng nhập thì thông tin sẽ mô tả bởi URL và nhìn vào thanh địa chỉ trình duyệt sẽ có dạng:
`https://xuanthulab.net/?name=test&pass=abc&submit=Đăng+Nhập`
+ Bạn thấy các dữ liệu trong thẻ input đã được biểu diễn bằng URL với tên dữ liệu tương ứng với tên của input là: name, pass, submit.
+ Trong trường hợp bạn chọn method là `post` thì sẽ không nhìn thấy dữ liệu biểu diễn qua URL như thế này mà `dữ liệu được tích hợp vào dữ liệu Request`.

**2. Các phần tử trong FORM**
+ Các phần tử trong FORM là nơi mà người dụng nhập dữ liệu, lựa chọn dữ liệu, các phần tử dữ liệu hay dùng trong form có thể kể đến là: `<input> <textarea> <select> <button> <datalist> <label> <fieldset> <datalist>`
  + Thẻ `<input>`:
    + Thẻ **input** là thẻ cơ bản trong form, thẻ này tạo ra các loại điều khiển tùy vào thuộc tính **type**
    + Thẻ **input** chỉ có phần mở thẻ.
    + Trong **form** người ta cũng thường dùng thẻ **label** để cho biết tiêu đề của một thẻ **input**
    + Sau đây là một số **type** hay dùng:
      + **type="text"**: Hộp nhập liệu một dòng
      + **type="password"**: Hộp nhập password
      + **type="submit"**: Tạo nút bấm gửi form
      + **type="reset"**: Tạo nút bấm - đưa dữ liệu đang nhập trên form về mặc định
      + **type="radio"**: Tạo lựa chọn
      + **type="checkbox"**: Tạo lựa chọn hộp kiểm (chọn nhiều phương án)
      + **type="color"**: Tạo điều khiển chọn màu sắc
      + **type="date"**: Tạo điều khiển chọn ngày tháng
      + **type="email"**: 	Tạo điều khiển nhập email
      + **type="file"**: 	Tạo điều khiển chọn file upload
      + **type="time"**: Tạo điều khiển nhập giờ 
      + **type="url"**: Tạo điều khiển nhập địa chỉ URL
  + Thẻ `<textarea>`:Thẻ textarea tạo ra một hộp nhập dữ liệu dạng text có nhiều dòng. Có thuộc tính col độ rộng và row số dòng.
  ```html
  <textarea name="info" rows="5" cols="30">
  Tôi đang học HTML
  </textarea>
  ```
  + Thẻ `<button>`:
    + Tạo các nut bấm như trên có thể dùng <input> với type bằng submit, reset. Thì bạn cũng có thể dùng phần tử <button> với type bằng submit hoặc reset
    ```html
    <button type="submit">Gửi thông tin</button>
    ```

























