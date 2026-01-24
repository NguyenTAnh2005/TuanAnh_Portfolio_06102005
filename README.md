# 🚀 Personal Portfolio Project

> **Mục đích:** Xây dựng ứng dụng Fullstack để làm chủ bộ công nghệ React + FastAPI và rèn luyện tư duy viết code chuẩn.

---

## 🛠 Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** ReactJS
- **Database:** PostgreSQL
- **Migration:** Alembic
- **Authentication:** JWT (JSON Web Token)
- **Validation:** Pydantic

---

## 🗺️ Lộ trình phát triển (Roadmap)

## 🏗️ Chặng 1:

- [x] Nghiên cứu và thiết kế Database (ERD).
- [x] Định nghĩa các Models hệ thống.
- [x] Tích hợp Pydantic Settings, cài đặt và cấu hình Alembic để quản lý migration, cấu hình kết nối Database, chạy alembic tạo bảng.
- [x] Nghiên cứu fetch API github (chức năng dự án cần), Hash password, Seed Data
- [x] Viết module bảo mật: JWT.
- [x] Hoàn thiện Schemas và CRUD cho My Info (Table) (Kiểm thử với JWT).

```bash
# Viết JWT tutorial setup basic
Điều kiện:  có schemas để tích hợp pydantic
- Viết file chứa function trả về user (dạng models thông qua data trong jwt)
- Viết file chứa function sinh ra 1 Access Token
- Viết file auth chứa endpoint login => Test (sinh ra JWT ko)
- Viết thêm 1 endpoint cần phân quyền và test Authorization

# 1. Cấu trúc Token
Mỗi mã JWT được bóc tách thành 3 phần rõ rệt:

- Header: Khai báo thuật toán mã hóa (mặc định là HS256).

- Payload: Chứa thông tin định danh (Claims) bao gồm user_id, email và thời gian hết hạn (exp). (Phần này chỉ mã hóa Base64 để truyền tải, không lưu trữ thông tin nhạy cảm như mật khẩu.)

- Signature: Chữ ký số được tạo ra từ (Header + Payload) kết hợp với Secret Key riêng biệt của hệ thống.

# 2. Quy trình Xác thực (Verification Workflow)

- Khi nhận Request, Server tách Token thành 3 phần.

- Server dùng Secret Key đang giữ bí mật để tính toán lại một "Chữ ký mới" từ Header và Payload của khách gửi lên. (Giải mã header để lấy thuật toán hash Signature, sau đó trộn header + Payload + SecretKey và mã hóa bằng mã đã giải trước đó! )

- Nếu chữ ký tự tính toán khớp 100% với Signature đính kèm trong Token, dữ liệu được coi là toàn vẹn và tin cậy.
# 3: Access Token
- Phần 1: Header (Màu đỏ - Thường bắt đầu bằng eyJ...)

    Nó chứa thông tin về loại token (JWT) và thuật toán (HS256).

    Nó chỉ được mã hóa Base64 (ai cũng dịch ra được).

- Phần 2: Payload (Màu tím - Chứa user_id, email, exp)

    Đây là "ruột" của token, chứa các thông tin (Claims) mà ní đã nạp vào.

    Nó cũng chỉ được mã hóa Base64 (ai cũng đọc được).

- Phần 3: Signature (Màu xanh - Chữ ký)

    Đây mới là cái Signature mà ní đang hỏi.

    Nó là kết quả của việc lấy (Header + Payload) đem đi "xào nấu" với Secret Key.

    Nó đóng vai trò là cái tem niêm phong.
```

- [x] Viết script Seed Data mẫu.
- [x] Chạy Uvicorn và test API qua Swagger UI.

## 🛠️ Chặng 2: M

### Viết Schemas và hàm CRUD cho các Models còn lại:

- [x] Roles
- [x] User
- [x] Project
- [ ] Coding api helping recovery admin password when I has forgot.
- [ ] CategoryBlog
- [ ] Blog
- [ ] Contact
- [ ] System Config
- [ ] Timeline
- [ ] CategoryAchievement
- [ ] Achievement

### Nghiên cứu và triển khai các chức năng nâng cao:

- []

## 🎨 Chặng 3:

- [ ] Khởi tạo project React, cấu hình Middleware CORS.
- [ ] Viết logic gọi API (Fetch/Axios) để kiểm tra kết nối.
- [ ] Học và áp dụng kiến thức nâng cao về React (Hooks, Context).
- [ ] Triển khai giao diện Portfolio hoàn chỉnh.

## ☁️ Chặng 4: (Deployment)

- [ ] Chuẩn bị môi trường và Deploy ứng dụng.

---

_Dự án đang trong quá trình phát triển 🛠️_
