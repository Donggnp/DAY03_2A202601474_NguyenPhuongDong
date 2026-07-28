# 🛠️ XÁC ĐỊNH CÁC TRƯỜNG HỢP TOOL BỊ LỖI (FAILURE MODES)

> **Đề tài**: Chatbot Định Hướng Sự Nghiệp  
> **Role 3 - Prompt Engineer**: Xác định và chuẩn bị xử lý các trường hợp tool có thể bị lỗi

---

## 📋 TỔNG QUAN 3 DẠNG LỖI CHÍNH

| Dạng lỗi | Biểu hiện | Mức độ nghiêm trọng | Cách xử lý |
|:---------|:----------|:-------------------|:-----------|
| **Unknown Tool** | AI gọi tool không tồn tại | 🔴 Cao | Trả về danh sách tools hợp lệ |
| **Malformed Args** | Tham số sai cú pháp/thiếu | 🟡 Trung bình | Gợi ý cú pháp đúng |
| **Invalid Data** | Dữ liệu không hợp lệ | 🟢 Thấp | Trả lỗi, Agent thử cách khác |

---

## 🔴 DẠNG 1: UNKNOWN TOOL (Tool không tồn tại)

### Mô tả
Agent gọi tên tool không có trong `AVAILABLE_TOOLS`

### Ví dụ cụ thể cho đề tài:

#### Case 1.1: Tool name sai chính tả
```
❌ AI gọi: serach_careers["công nghệ"]  (thiếu chữ 'a')
✅ Tool đúng: search_careers

→ Observation: LỖI: Tool 'serach_careers' không tồn tại.
   Tools hợp lệ: search_careers, get_career_info, 
   suggest_universities, get_salary_range
```

#### Case 1.2: Agent tự bịa tool
```
❌ AI gọi: predict_future_career["AI engineer"]
✅ Không có tool này trong hệ thống

→ Observation: LỖI: Tool 'predict_future_career' không tồn tại.
   Vui lòng chỉ sử dụng các tools sau:
   - search_careers: Tìm kiếm ngành nghề
   - get_career_info: Lấy thông tin chi tiết ngành
   - suggest_universities: Gợi ý trường đại học
   - get_salary_range: Lấy mức lương tham khảo
```

### Guardrail cần thiết:
```python
if tool_name not in AVAILABLE_TOOLS:
    return f"LỖI: Tool '{tool_name}' không tồn tại. " \
           f"Tools hợp lệ: {', '.join(AVAILABLE_TOOLS.keys())}"
```

---

## 🟡 DẠNG 2: MALFORMED ARGS (Tham số sai cú pháp)

### Mô tả
Tool đúng nhưng tham số truyền vào sai format, thiếu, hoặc thừa

### Ví dụ cụ thể cho đề tài:

#### Case 2.1: Thiếu dấu ngoặc
```
❌ AI gọi: search_careers["công nghệ thông tin'
✅ Đúng: search_careers["công nghệ thông tin"]

→ Observation: LỖI: Cú pháp không hợp lệ. 
   Format đúng: search_careers["tên_ngành"]
```

#### Case 2.2: Thiếu tham số bắt buộc
```
❌ AI gọi: get_career_info()
✅ Đúng: get_career_info["AI Engineer"]

→ Observation: LỖI: Thiếu tham số bắt buộc 'career_name'.
   Cách dùng: get_career_info["tên_ngành"]
```

#### Case 2.3: Thừa tham số
```
❌ AI gọi: search_careers["công nghệ", "đại học", "lương cao"]
✅ Đúng: search_careers["công nghệ"]

→ Observation: LỖI: Tool chỉ nhận 1 tham số, bạn truyền 3.
   Cách dùng: search_careers["keyword"]
```

#### Case 2.4: Kiểu dữ liệu sai
```
❌ AI gọi: get_salary_range[123]
✅ Đúng: get_salary_range["Data Scientist"]

→ Observation: LỖI: Tham số phải là string, nhận được: int
```

### Guardrail cần thiết:
```python
def validate_args(tool_name, args):
    if not args or len(args) == 0:
        return f"LỖI: Tool '{tool_name}' cần tham số"
    if not isinstance(args[0], str):
        return f"LỖI: Tham số phải là string"
    return None  # Valid
```

---

## 🟢 DẠNG 3: INVALID DATA (Dữ liệu không hợp lệ)

### Mô tả
Tool và tham số đúng format nhưng dữ liệu không tồn tại trong database

### Ví dụ cụ thể cho đề tài:

#### Case 3.1: Tên ngành không có trong database
```
✅ AI gọi: get_career_info["Phi hành gia"]
❌ Database không có ngành này

→ Observation: LỖI: Không tìm thấy thông tin cho ngành 'Phi hành gia'.
   Các ngành có sẵn: Công nghệ thông tin, Kế toán, 
   Marketing, Kinh doanh, Y khoa, Luật...
```

#### Case 3.2: Trường đại học không tồn tại
```
✅ AI gọi: suggest_universities["Đại học ABC XYZ"]
❌ Trường không có trong hệ thống

→ Observation: LỖI: Không tìm thấy thông tin về 'Đại học ABC XYZ'.
```

#### Case 3.3: Tham số rỗng hoặc chỉ có khoảng trắng
```
❌ AI gọi: search_careers["   "]
❌ AI gọi: search_careers[""]

→ Observation: LỖI: Từ khóa tìm kiếm không được để trống.
```

#### Case 3.4: Ký tự đặc biệt hoặc injection attempt
```
❌ AI gọi: search_careers["'; DROP TABLE careers; --"]

→ Observation: LỖI: Từ khóa chứa ký tự không hợp lệ.
   Chỉ chấp nhận chữ cái, số và dấu cách.
```

### Guardrail cần thiết:
```python
def get_career_info(career_name: str) -> str:
    # Sanitize input
    career_name = career_name.strip()
    
    if not career_name:
        return "LỖI: Tên ngành không được để trống"
    
    # Check database
    if career_name not in CAREER_DATABASE:
        available = ", ".join(list(CAREER_DATABASE.keys())[:5])
        return f"LỖI: Không tìm thấy '{career_name}'. " \
               f"Một số ngành có sẵn: {available}..."
    
    return CAREER_DATABASE[career_name]
```

---

## 🔄 DẠNG 4: REPEATED ACTION (Lặp vô hạn)

### Mô tả
Agent cứ gọi lại cùng một tool với cùng tham số dù đã nhận lỗi

### Ví dụ:

#### Case 4.1: Loop detection
```
Iteration 1:
Action: get_career_info["Phi hành gia"]
Observation: LỖI: Không tìm thấy thông tin cho ngành 'Phi hành gia'

Iteration 2:
Action: get_career_info["Phi hành gia"]  ← TRÙNG LẶP!
Observation: LỖI: Không tìm thấy thông tin cho ngành 'Phi hành gia'

... (lặp tiếp)

→ Sau 5 lần lặp, MAX_ITERATIONS kích hoạt:
Final Answer: Xin lỗi, tôi không thể tìm thấy thông tin về 
ngành 'Phi hành gia'. Bạn có thể thử tìm kiếm với từ khóa khác không?
```

### Guardrail cần thiết:
```python
MAX_ITERATIONS = 5
action_history = []

def detect_loop(current_action):
    if action_history.count(current_action) >= 2:
        return True  # Phát hiện lặp
    return False
```

---

## 🚨 DẠNG 5: TOOL EXECUTION ERROR (Lỗi khi chạy tool)

### Mô tả
Tool gặp lỗi ngoại lệ khi thực thi (network error, timeout, exception)

### Ví dụ:

#### Case 5.1: Network timeout (nếu gọi API thật)
```
Action: get_salary_range["Data Scientist"]
→ Exception: requests.exceptions.Timeout

Observation: LỖI: Không thể kết nối đến nguồn dữ liệu. 
Vui lòng thử lại sau.
```

#### Case 5.2: Internal exception
```
Action: suggest_universities["Công nghệ thông tin"]
→ Exception: KeyError trong code tool

Observation: LỖI: Đã xảy ra lỗi khi xử lý yêu cầu. 
Vui lòng liên hệ quản trị viên.
```

### Guardrail cần thiết:
```python
def safe_execute_tool(tool_func, *args):
    try:
        return tool_func(*args)
    except Exception as e:
        return f"LỖI: Tool gặp sự cố khi thực thi. Chi tiết: {str(e)}"
```

---

## 📊 BẢNG TỔNG HỢP ĐỐI SÁCH XỬ LÝ

| Dạng lỗi | Phát hiện bởi | Xử lý | Có cho phép retry? |
|:---------|:--------------|:------|:-------------------|
| Unknown Tool | Parser | Liệt kê tools hợp lệ | ✅ Có |
| Malformed Args | Parser | Gợi ý cú pháp đúng | ✅ Có |
| Invalid Data | Tool function | Trả lỗi + gợi ý | ✅ Có |
| Repeated Action | Loop detector | Dừng bằng MAX_ITERATIONS | ❌ Không |
| Execution Error | Try-catch | Safe fallback | ✅ Có (1 lần) |

---

## ✅ CHECKLIST XÁC ĐỊNH FAILURE MODES

### Mốc 1 (20 phút):
- [x] Liệt kê đầy đủ 5 dạng lỗi chính
- [x] Viết ví dụ cụ thể cho từng case với đề tài "Định Hướng Sự Nghiệp"
- [x] Xác định mức độ nghiêm trọng của từng lỗi
- [x] Đề xuất Guardrails tương ứng

### Mốc 3 (60 phút):
- [ ] Implement Guardrails vào `src/prompts.py`
- [ ] Test từng failure mode với câu hỏi bẫy
- [ ] Xác nhận MAX_ITERATIONS hoạt động
- [ ] Ghi log trace vào `docs/trace_eval.md`

---

## 🎯 KẾT LUẬN

**3 nguyên tắc vàng xử lý tool errors:**

1. **Không crash** → Trả chuỗi lỗi cho Agent đọc
2. **Gợi ý rõ ràng** → Giúp Agent tự sửa lỗi
3. **Có phanh an toàn** → MAX_ITERATIONS ngăn lặp vô hạn

---

*Tài liệu này phục vụ cho Role 3 - Prompt Engineer trong việc thiết kế Guardrails*  
*Cập nhật: 2026-07-28*
