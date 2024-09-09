# Regex for chunking 
## Chunking
+ Chunking là kỹ thuật chia nhỏ thông tin thành các cụm nhỏ hơn để có thể dễ dàng xử lý và ghi nhớ
+ Chunking involves breaking down texts into smaller, manageable pieces called "chunks."
+ LLMs have a limited context window, making it unrealistic to provide all data simultaneously.
+ Chunking ensures that only relevant context is sent to the LLM, enhancing the efficiency and relevance of the responses generated.

## Regex
+ https://t3h.edu.vn/tin-tuc/regex-trong-python-tim-hieu-ve-bieu-thuc-chinh-quy-trong-python
+ https://viblo.asia/p/python-regex-Qbq5QMeE5D8

+ Regex - Regular expression hay còn gọi là biểu thức chính quy trong Python.  Regex là một chuỗi miêu tả một bộ các chuỗi khác, theo những quy tắc cú pháp nhất định.
+ RegEx hay biểu thức chính quy (Regular Expression) là `một chuỗi ký tự tạo thành một biểu mẫu tìm kiếm` (search pattern). RegEx được sử dụng để `kiểm tra xem một chuỗi có chưa mẫu tìm kiêms được chỉ định hay không`
+ Regular Expression trong Python được thể hiện qua `module re`, re Module cung cấp sự hỗ trợ đầy đủ các Regular Expression trong Python

+ VD:
```
    Tìm kiễm chuỗi bắt đầu bằng 'The' và kết thúc bằng 'Spain': 

    import re
    txt = "The rain in Spain"
    x = re.search("^The.*Spain$", txt)
```

+ Các hàm Regex trong Python:
    + `match`: Hàm này khớp với mẫu regex trong chuỗi với cờ tùy chọn. Nó trả về true nếu một kết quả khớp được tìm thấy trong chuỗi nếu không nó trả về false.
    + `search`: Hàm này trả về đối tượng khớp nếu có một kết quả khớp được tìm thấy trong chuỗi.
    + `findall`: Trả về một list các kết quả phù hợp
    + ...

## Syntax regrex:
### Regex trong Python - Xây dựng bằng ký tự đặc biệt 
+ `\A` : Nó trả về một kết quả khớp nếu các ký tự được chỉ định có mặt ở đầu chuỗi. `"\AThe"	"The world"`
+ `\b` : Nó trả về một kết quả khớp nếu các ký tự được chỉ định có mặt ở đầu hoặc cuối chuỗi. 
    r"\bSpa" -  "The rain in Spain"
    r"ain\b" -	"He is Bi Rain"
+ `\B` : Nó trả về một kết quả khớp nếu các ký tự được chỉ định có mặt ở đầu chuỗi nhưng không ở cuối chuỗi.
    r"\BSpa" - "This is GSpan company"
    r"ain\B" - "No words are rains"
+ `\d` : Nó trả về một kết quả khớp nếu chuỗi chứa các chữ số [0-9].
+ `\D`: Nó trả về một kết quả khớp nếu chuỗi không chứa các chữ số [0-9].
+ `\s` : Nó trả về một kết quả khớp nếu chuỗi chứa bất kỳ ký tự khoảng trắng nào.
+ `\S`: Nó trả về một kết quả khớp nếu chuỗi không chứa bất kỳ ký tự khoảng trắng nào.
...
### Regex trong Python - Xây dựng bằng set
+ `[arn]`: Trả về một kết quả khớp nếu chuỗi chứa bất kỳ ký tự nào được chỉ định trong tập hợp.
+ `[a-n]`: Trả về một kết quả khớp nếu chuỗi chứa bất kỳ ký tự nào từ a đến n.
+ `[^arn]`: Trả về một kết quả khớp nếu chuỗi chứa các ký tự ngoại trừ a, r và n.
+ ...
### Xây dựng bằng Metacharacter
+ `[]`	: Một tập hợp các ký tự - `"[a-e]"	"adbc"`
+ `\`	: Tín hiệu thể hiện một chuỗi đặc biệt (hoặc sử dụng để thoát các ký tự đặc biệt) - ` "\d"	"123"`
+ `.`	: Bất kỳ ký tự nào (ngoại trừ ký tự dòng mới)	- `"he..o"	"henno"`
+ `^`	: Bắt đầu chuỗi	- `"^hello"	 "hello gua"`
+ `$`	: Kết thúc chuỗi	- `"world$"	 "helo world"`
+ `()`: Nhóm các thành phần.
+ ...

# Link
+ https://gist.github.com/hanxiao/3f60354cf6dc5ac698bc9154163b4e6a

# Java script to python
## Basic Regex Syntax:
+ JavaScript uses `\` as an escape character, which is also the case in Python.
+ Both languages use similar regex syntax for patterns like `\d (digit)`, `\s (whitespace)`, etc.
## String Formatting
+ In JavaScript, string interpolation is done with `${}` inside template literals (backticks).
+ In Python, use `f-strings` for interpolation or the `.format()` method.
## Line Continuation
+ JavaScript uses `+ `to concatenate strings.
+ Python can use backslashes `\` to continue a regex pattern `on the next line` or just concatenate strings without the need for the `+` operator
## Substituting Variables
+ Replace JavaScript string interpolation `${VARIABLE}` with Python’s `{VARIABLE}`.
## Regex Compilation
+ Use the re module in Python for regex operations.