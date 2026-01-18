## CHẠY ALEMBIC

1. Lệnh tạo file Migration (Quét code tạo kịch bản)

- Lệnh này sẽ bảo Alembic soi các class Models của ní và so sánh với Database hiện tại để tự viết code tạo bảng:

```bash
alembic revision --autogenerate -m "Message"
```

2. Lệnh nâng cấp Database (Thực thi tạo bảng)

- Sau khi file script đã được tạo trong thư mục versions/, ní chạy lệnh này để nó chính thức "đổ" bảng vào Postgres:

```bash
alembic upgrade head
```
