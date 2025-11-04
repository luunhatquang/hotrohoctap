# 🎓 Cổng tra cứu Tuyển sinh - Search University

Website tra cứu thông tin tuyển sinh đại học với giao diện hiện đại, thân thiện.

## ✨ Tính năng

- 🔍 **Tìm kiếm trường đại học**: Tìm theo tên, mã trường, hoặc vùng miền
- 🎯 **Lọc theo vùng**: Hà Nội, TP HCM, Đà Nẵng, Cần Thơ, và các tỉnh thành khác
- 📊 **Xem điểm chuẩn**: Hiển thị điểm chuẩn các ngành học theo từng năm
- 👤 **Quản lý hồ sơ**: Tạo và quản lý hồ sơ học sinh
- 🔐 **Đăng nhập/Đăng ký**: Hệ thống xác thực người dùng
- 📱 **Responsive**: Tương thích với mọi thiết bị

## 🚀 Hướng dẫn chạy dự án

### 1. Kích hoạt môi trường ảo

```bash
cd /Users/luuquang/django/searchuniversity
source env/bin/activate
```

### 2. Chạy migrations (nếu cần)

```bash
python manage.py migrate
```

### 3. Chạy server

```bash
python manage.py runserver
```

### 4. Truy cập website

Mở trình duyệt và truy cập: **http://127.0.0.1:8000**

## 📁 Cấu trúc dự án

```
searchuniversity/
├── base/                           # App chính
│   ├── templates/base/            # Templates
│   │   ├── home.html             # Trang chủ
│   │   ├── uni_details.html      # Chi tiết trường
│   │   ├── login_register.html   # Đăng nhập/Đăng ký
│   │   ├── student_profile.html  # Xem hồ sơ
│   │   └── room_form.html        # Tạo hồ sơ
│   ├── models.py                  # Database models
│   ├── views.py                   # Views/Controllers
│   ├── urls.py                    # URL routing
│   └── form.py                    # Forms
├── searchuniversity/
│   ├── settings.py               # Cấu hình Django
│   ├── urls.py                   # Root URL config
│   └── static/
│       └── css/
│           └── style.css         # CSS chính
├── templates/
│   ├── main.html                 # Template gốc
│   └── navbar.html               # Navigation bar
└── db.sqlite3                    # Database

```

## 🎨 Giao diện

### Trang chủ
- Header với logo và menu điều hướng
- Banner quảng cáo
- Tabs tìm kiếm (Tìm trường, Tìm ngành, Tìm theo điểm, Tìm theo học phí)
- Search box với dropdown lọc
- Nút lọc theo vùng miền
- Danh sách trường đại học với tính năng yêu thích

### Trang chi tiết trường
- Header với thông tin liên hệ đầy đủ
- Danh sách ngành học
- Hiển thị điểm chuẩn theo từng năm
- Thông tin tổ hợp môn và học phí

### Trang đăng nhập/đăng ký
- Form đăng nhập/đăng ký đẹp mắt
- Gradient background hiện đại
- Icon và validation messages

### Trang hồ sơ học sinh
- Hiển thị thông tin cá nhân
- Điểm thi chứng chỉ (IELTS, HSA, TSA)
- Kết quả thi thử
- Bảng điểm chi tiết

## 🎯 URLs

- `/` - Trang chủ (danh sách trường)
- `/uni/<code>/` - Chi tiết trường đại học
- `/login/` - Đăng nhập
- `/register/` - Đăng ký
- `/logout/` - Đăng xuất
- `/create/` - Tạo hồ sơ học sinh
- `/st_detail/` - Xem danh sách hồ sơ

## 🛠️ Công nghệ sử dụng

- **Backend**: Django 5.2.7
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Icons**: Font Awesome 6.4.0
- **Responsive**: CSS Grid & Flexbox

## 📝 Models

### School (Trường học)
- code: Mã trường
- name: Tên trường
- address: Địa chỉ
- phone, email, website: Thông tin liên hệ
- region: Vùng miền (HN, HCM, DN, CT, OTHER)

### Program (Ngành học)
- school: ForeignKey đến School
- code: Mã ngành
- name: Tên ngành
- subject_combinations: Tổ hợp môn
- tuition: Học phí

### Admission (Điểm chuẩn)
- program: ForeignKey đến Program
- score: Điểm chuẩn
- year: Năm tuyển sinh

### StudentProfile (Hồ sơ học sinh)
- user: OneToOne với User
- target_school, target_program: Trường/ngành mục tiêu
- target_score, ielts_score, hsa_score, tsa_score: Các điểm số
- transcript: File học bạ

## 🎨 CSS Classes

### Layout
- `.container` - Container chính
- `.main-wrapper` - Wrapper cho content và sidebar
- `.sidebar` - Sidebar bên phải

### Components
- `.navbar` - Navigation bar
- `.search-section` - Phần tìm kiếm
- `.uni-item` - Item trường đại học
- `.program-card` - Card ngành học
- `.auth-card` - Card đăng nhập/đăng ký
- `.profile-card` - Card hồ sơ

### Buttons
- `.btn-primary` - Button chính
- `.btn-outline` - Button outline
- `.btn-submit` - Button submit form

## 📱 Responsive Breakpoints

- Desktop: > 1024px
- Tablet: 768px - 1024px
- Mobile: < 768px

## 🔧 Cấu hình Static Files

```python
# settings.py
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "searchuniversity/static",
]
```

## 👨‍💻 Development

### Thêm dữ liệu mẫu

Sử dụng Django Admin để thêm dữ liệu:
1. Tạo superuser: `python manage.py createsuperuser`
2. Truy cập: http://127.0.0.1:8000/admin
3. Thêm School, Program, Admission

### Tùy chỉnh giao diện

- CSS chính: `searchuniversity/static/css/style.css`
- Templates: `base/templates/base/`
- Navbar: `templates/navbar.html`

## 📄 License

This project is for educational purposes.

---

Made with ❤️ by Luu Quang

