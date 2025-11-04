
# HƯỚNG DẪN NHẬP DỮ LIỆU NGÀNH HỌC

## CÁC CỘT BẮT BUỘC:

1. **STT**: Số thứ tự (tự động, không bắt buộc)
2. **Mã ngành**: Mã duy nhất của ngành (VD: 7340204, EP09) - BẮT BUỘC
3. **Tên ngành**: Tên đầy đủ ngành học - BẮT BUỘC
4. **Loại ngành**: Mã loại ngành (xem danh sách bên dưới) - BẮT BUỘC
5. **Tổ hợp môn**: Các tổ hợp xét tuyển, cách nhau bởi dấu phẩy (VD: A00,A01,D01) - Không bắt buộc
6. **Học phí (triệu/năm)**: Số tiền học phí tính bằng triệu VNĐ (VD: 18, 25.5) - Không bắt buộc
7. **Điểm chuẩn 2025**: Điểm chuẩn năm 2025 - Không bắt buộc
8. **Điểm chuẩn 2024**: Điểm chuẩn năm 2024 - Không bắt buộc
9. **Điểm chuẩn 2023**: Điểm chuẩn năm 2023 - Không bắt buộc
10. **Ghi chú**: Thông tin bổ sung - Không bắt buộc

## DANH SÁCH LOẠI NGÀNH:

- **khoa_hoc_cong_nghe**: Khoa học – Công nghệ – Kỹ thuật
- **kinh_te_quan_tri**: Kinh tế – Quản trị – Tài chính
- **luat_hanh_chinh**: Luật – Hành chính – Chính trị – Xã hội
- **y_duoc**: Y – Dược – Sức khỏe
- **nghe_thuat_thiet_ke**: Nghệ thuật – Thiết kế – Truyền thông
- **nong_lam_ngu**: Nông – Lâm – Ngư nghiệp – Môi trường
- **toan_thong_ke**: Toán – Thống kê – Khoa học dữ liệu
- **giao_duc_du_lich**: Giáo dục – Du lịch – Dịch vụ

## LƯU Ý:

1. **Mã ngành** phải duy nhất (không trùng lặp)
2. **Học phí** chỉ nhập số (VD: 18, 25.5), không nhập "triệu" hoặc "VNĐ"
3. **Điểm chuẩn** nhập số thập phân (VD: 24.75, 26.29)
4. Có thể để trống các cột không bắt buộc (học phí, điểm chuẩn các năm cũ)
5. Nếu ngành có nhiều năm điểm chuẩn, điền vào các cột tương ứng

## VÍ DỤ:

| STT | Mã ngành | Tên ngành | Loại ngành | Tổ hợp môn | Học phí | Điểm 2025 | Điểm 2024 | Điểm 2023 |
|-----|----------|-----------|------------|------------|---------|-----------|-----------|-----------|
| 1 | 7340204 | Quản trị kinh doanh | kinh_te_quan_tri | A00,A01,D01 | 18 | 24.75 | 24.5 | 24.2 |
| 2 | EP09 | Kinh doanh quốc tế | kinh_te_quan_tri | A00,A01 | 25 | 26.29 | 26.0 | 25.8 |

## CÁCH IMPORT:

```bash
python manage.py import_programs <MÃ_TRƯỜNG> <NĂM> <ĐƯỜNG_DẪN_FILE>
```

Ví dụ:
```bash
python manage.py import_programs BKA 2025 program_import_template.xlsx --type kinh_te_quan_tri
```
