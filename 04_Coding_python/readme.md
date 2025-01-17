# New Syntax
1. assert
    + The assert statement exists in almost every programming language. It helps detect problems early in your program, where the cause is clear, rather than later when some other operation fails
        [link](https://stackoverflow.com/questions/5142418/what-is-the-use-of-assert-in-python)
    + code:
   ```python
    assert len(boxes_face) == len(track_ids)
    ```
   
2. What does the star and doublestar operator mean in a function call?
   1. Ref [here](https://stackoverflow.com/questions/2921847/what-does-the-star-and-doublestar-operator-mean-in-a-function-call)
   2. The single star * unpacks the sequence/collection into positional arguments.
   3. The double star ** does the same, only using a dictionary
2. Thread one arguments
    + t = KThread(target=main, args=(input_path,))
    + Have "," after args
    + [link](https://stackoverflow.com/questions/37116721/typeerror-in-threading-function-takes-x-positional-argument-but-y-were-given)
3. Sort string base on number inside
    ```python
    list_image.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
    ```

## Code Hung
1. `MAX_STRIP_SUGGESTION: Final[int] = 10`
   + `Final` là một chỉ thị từ thư viện `typing` trong Python, được sử dụng để chỉ định rằng giá trị của biến này `không nên 
bị thay đổi` sau khi được gán.
2. `class DailyHeartRateSummary(pt.Summary):`
   + Lớp này kế thừa từ lớp Summary trong module pt.
   + Điều này có nghĩa là DailyHeartRateSummary sẽ `thừa hưởng` tất cả các `thuộc tính và phương thức` của lớp `pt.Summary`,
và có thể mở rộng hoặc ghi đè chúng nếu cần.
3. `Một dấu gạch dưới (_) ở đầu tên hàm hoặc biến:`
Đây là một quy ước để chỉ ra rằng hàm hoặc biến này là "protected" (bảo vệ) và không nên được truy cập trực tiếp từ bên ngoài lớp.
Tuy nhiên, nó chỉ là một quy ước và không ngăn cản việc truy cập từ bên ngoài.

4. `Hai dấu gạch dưới (__) ở đầu tên hàm hoặc biến:`
Đây là một cơ chế "name mangling" (làm rối tên) của Python để tránh xung đột tên trong các lớp con. 
Python sẽ thay đổi tên của biến hoặc hàm này để bao gồm tên lớp, làm cho nó khó truy cập từ bên ngoài lớp.
Ví dụ: `__get_id_event` sẽ được Python đổi tên thành `_ClassName__get_id_event` để tránh xung đột tên.
5. `@df.timeit`
+ `decorator` timeit thường được sử dụng để đo thời gian thực thi của hàm.


# Numpy 
