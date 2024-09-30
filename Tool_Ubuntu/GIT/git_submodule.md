# Git submodule
+ Git Submodule là một tính năng của Git cho phép bạn bao gồm một repository Git khác (gọi là submodule) bên trong một repository chính.
+ Submodule rất hữu ích khi bạn có một dự án phụ thuộc vào một dự án khác, và bạn muốn quản lý chúng một cách độc lập. 
+ Thay vì sao chép mã nguồn của dự án con vào repository chính, submodule cho phép bạn giữ các dự án đó tách biệt nhưng vẫn liên kết với nhau.

# Command
## Thêm một repository Git khác làm submodule
+ git submodule add <URL-repository>
+ `git submodule add https://github.com/user/library.git`
## Khởi tạo và tải submodule sau khi clone repository chính
+ Khi bạn clone một repository có chứa submodule, submodule không tự động được tải về.
+ Để khởi tạo và cập nhật các submodule, bạn chạy các lệnh sau:
+ `git submodule init / git submodule update`
+ `git submodule update --init --recursive`
  + init: Khởi tạo các submodule nếu chúng chưa được khởi tạo.
  + update: Tải về nội dung của submodule và đặt nó ở đúng commit.
  + recursive: Thực hiện các hành động này không chỉ với các submodule chính, mà còn với tất cả các submodule lồng nhau (nếu có)
## Cập nhật submodule
+ Lấy phiên bản mới nhất từ nhánh mặc định của submodule.
+ Khi một submodule có các thay đổi mới (ví dụ như khi submodule được cập nhật từ repository riêng của nó), 
bạn có thể cập nhật submodule trong repository chính bằng lệnh:
+ `git submodule update --remote`
## Xóa submodule
+ Xóa mục trong file .gitmodules: `git rm --cached <path-to-submodule>`
+ Xóa thư mục submodule: `rm -rf <path-to-submodule>`
+ Xóa các thông tin submodule khỏi Git: 
  + `git config -f .git/config --remove-section submodule.<path-to-submodule>`
  + `git rm --cached <path-to-submodule>`
  + `rm -rf .git/modules/<path-to-submodule>`
## Liệt kê các submodule
+ git submodule
## Thay đổi nhánh trong submodule
+ Nếu bạn muốn chuyển đổi sang một nhánh khác trong submodule, bạn cần chuyển vào thư mục của submodule và dùng các lệnh Git thông thường
+ Nếu bạn clone một repository có submodule, nhưng submodule không được tải về cùng lúc
+ bạn có thể clone cả repository chính và submodule bằng lệnh sau:
+ `git clone --recurse-submodules <URL-repository>`
## Push thay đổi submodule
+ Khi bạn thay đổi trong submodule (ví dụ, chuyển nhánh hoặc commit mới), sau đó bạn cần commit thay đổi này trong repository chính:
  + cd <path-to-submodule>
  + git add <file>
  + git commit -m "Cập nhật submodule"
  + git push
+ Tiếp theo, quay lại repository chính và commit cập nhật:
  + cd ..
  + git add <path-to-submodule>
  + git commit -m "Cập nhật tham chiếu submodule"
  + git push

+ https://repo.oryza.vn/oryza/ecosystem/ai-projects/-/merge_requests/13

