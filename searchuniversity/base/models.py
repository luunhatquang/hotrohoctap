from django.db import models
from django.contrib.auth.models import User

class School(models.Model):
    code = models.CharField(max_length=20, unique=True)    
    name = models.CharField(max_length=255)                
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    REGION_CHOICES = [
        ('HN', 'Hà Nội'),
        ('HCM', 'TP HCM'),
        ('DN', 'Đà Nẵng'),
        ('CT', 'Cần Thơ'),
        ('OTHER', 'Khác'),
    ]
    region = models.CharField(max_length=20, choices=REGION_CHOICES, default='OTHER') 
    decription = models.TextField(blank=True)
    TYPE = [
        ('DH', 'Đại học'),
        ('CĐ', 'Cao đẳng'),
        ('TC', 'Trung cấp')
    ]
    type_school = models.CharField(max_length=2, choices=TYPE, default='DH')
    transcript = models.FileField(upload_to='transcripts/', null=True, blank=True)
    def __str__(self):
        return f"{self.code} - {self.name}"

class Program(models.Model):
    school = models.ForeignKey(School, related_name='programs', on_delete=models.CASCADE)  
    code = models.CharField(max_length=50, unique=True)      
    name = models.CharField(max_length=255)          
    TYPE = [
        ('khoa_hoc_cong_nghe', 'Khoa học – Công nghệ – Kỹ thuật'),
        ('giao_duc_du_lich', 'Giáo dục – Du lịch – Dịch vụ'),
        ('toan_thong_ke', 'Toán – Thống kê – Khoa học dữ liệu'),
        ('nong_lam_ngu', 'Nông – Lâm – Ngư nghiệp – Môi trường'),
        ('nghe_thuat_thiet_ke', 'Nghệ thuật – Thiết kế – Truyền thông'),
        ('luat_hanh_chinh', 'Luật – Hành chính – Chính trị – Xã hội'),
        ('kinh_te_quan_tri', 'Kinh tế – Quản trị – Tài chính'),
    ]
    type = models.CharField(max_length=255, choices=TYPE)    
    admission_code = models.CharField(max_length=50, blank=True, null=True, help_text="Tùy chọn: mã tham chiếu tới Điểm chuẩn")
    subject_combinations = models.CharField(max_length=255, blank=True)  
    tuition = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Admission(models.Model):
    program = models.ForeignKey(Program, related_name='admissions', on_delete=models.CASCADE) 
    code = models.CharField(max_length=50, blank=True, null=True) 
    score = models.FloatField(null=True, blank=True)              
    year = models.PositiveIntegerField(null=True, blank=True) 
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.program.code} - {self.year}: {self.score}"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    
    full_name = models.CharField(max_length=255, blank=True, default='', verbose_name="Họ và tên")
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name="Tuổi")
    phone = models.CharField(max_length=20, blank=True, default='', verbose_name="Số điện thoại")
    address = models.TextField(blank=True, default='', verbose_name="Địa chỉ")

    target_school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    target_program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    target_score = models.FloatField(null=True, blank=True, help_text="Điểm mục tiêu")

    ielts_score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.full_name:
            return f"{self.full_name} ({self.user.username})"
        return f"Học sinh: {self.user.username}"

class TrialExam(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name='trial_exams')
    attempt_number = models.PositiveIntegerField(default=1, verbose_name="Lần thi thứ")
    
    subject1_name = models.CharField(max_length=100, blank=True)
    subject1_score = models.FloatField(null=True, blank=True)

    subject2_name = models.CharField(max_length=100, blank=True)
    subject2_score = models.FloatField(null=True, blank=True)

    subject3_name = models.CharField(max_length=100, blank=True)
    subject3_score = models.FloatField(null=True, blank=True)

    date_exam = models.DateField(null=True, blank=True, verbose_name="Ngày thi")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['student', 'attempt_number']
    
    @property
    def total_score(self):
        """Tính tổng điểm 3 môn"""
        score1 = self.subject1_score or 0
        score2 = self.subject2_score or 0
        score3 = self.subject3_score or 0
        return score1 + score2 + score3

    def __str__(self):
        return f"Thi thử lần {self.attempt_number} - Tổng: {self.total_score} điểm - {self.student.user.username}"

class HsaExam(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name='hsa_exams')
    attempt_number = models.PositiveIntegerField(default=1, verbose_name="Lần thi thứ")
    
    subject1_score = models.FloatField(null=True, blank=True, verbose_name="Điểm môn 1")
    subject2_score = models.FloatField(null=True, blank=True, verbose_name="Điểm môn 2")
    subject3_score = models.FloatField(null=True, blank=True, verbose_name="Điểm môn 3")
    date_exam = models.DateField(null=True, blank=True, verbose_name="Ngày thi")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['student', 'attempt_number']
    
    @property
    def total_score(self):
        """Tính tổng điểm 3 môn"""
        score1 = self.subject1_score or 0
        score2 = self.subject2_score or 0
        score3 = self.subject3_score or 0
        return score1 + score2 + score3

    def __str__(self):
        return f"HSA lần {self.attempt_number} - Tổng: {self.total_score} điểm - {self.student.user.username}"


class TsaExam(models.Model):
    student = models.ForeignKey('StudentProfile', on_delete=models.CASCADE, related_name='tsa_exams')
    attempt_number = models.PositiveIntegerField(default=1, verbose_name="Lần thi thứ")
    
    subject1_score = models.FloatField(null=True, blank=True, verbose_name="Điểm môn 1")
    subject2_score = models.FloatField(null=True, blank=True, verbose_name="Điểm môn 2")
    subject3_score = models.FloatField(null=True, blank=True, verbose_name="Điểm môn 3")
    date_exam = models.DateField(null=True, blank=True, verbose_name="Ngày thi")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['student', 'attempt_number']
    
    @property
    def total_score(self):
        """Tính tổng điểm 3 môn"""
        score1 = self.subject1_score or 0
        score2 = self.subject2_score or 0
        score3 = self.subject3_score or 0
        return score1 + score2 + score3

    def __str__(self):
        return f"TSA lần {self.attempt_number} - Tổng: {self.total_score} điểm - {self.student.user.username}"
    
class ChatConversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_conversations')
    title = models.CharField(max_length=255, blank=True, default='Cuộc trò chuyện mới')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Cuộc trò chuyện"
        verbose_name_plural = "Các cuộc trò chuyện"

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.created_at.strftime('%d/%m/%Y')})"

    def get_messages_count(self):
        """Đếm số tin nhắn trong conversation"""
        return self.messages.count()

    def get_last_message(self):
        """Lấy tin nhắn cuối cùng"""
        return self.messages.last()


class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('ai', 'AI'),
    ]
    
    conversation = models.ForeignKey(
        ChatConversation, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = "Tin nhắn"
        verbose_name_plural = "Tin nhắn"

    def __str__(self):
        preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"[{self.role}] {preview}"

    def is_from_user(self):
        return self.role == 'user'

    def is_from_ai(self):
        return self.role == 'ai'