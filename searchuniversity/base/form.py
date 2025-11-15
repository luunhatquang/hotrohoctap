from django.forms import ModelForm, DateInput, CharField, Select
from .models import StudentProfile, TrialExam, HsaExam, TsaExam, Program

class StudentProfileForm(ModelForm):
    
    class Meta:
        model = StudentProfile
        fields = ['full_name', 'age', 'phone', 'address', 'target_school', 'target_score', 'ielts_score', 'target_program_type']
        labels = {
            'full_name': 'Họ và tên',
            'age': 'Tuổi',
            'phone': 'Số điện thoại',
            'address': 'Địa chỉ',
            'target_school': 'Trường mục tiêu',
            'target_program_type': 'Nhóm ngành mục tiêu',
            'target_score': 'Điểm mục tiêu',
            'ielts_score': 'Điểm IELTS',
        }
        help_texts = {
            'full_name': 'VD: Nguyễn Văn A',
            'age': 'Nhập tuổi của bạn',
            'phone': 'VD: 0123456789',
            'target_score': 'Tổng điểm 3 môn mục tiêu',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'target_program' in self.fields:
            del self.fields['target_program']
       
        if self.instance and self.instance.pk and not self.instance.target_program_type and self.instance.target_program:
            self.initial['target_program_type'] = self.instance.target_program.type
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        target_program_type = instance.target_program_type
        if target_program_type:
            if instance.target_school:
                program = Program.objects.filter(
                    type=target_program_type,
                    school=instance.target_school
                ).first()
            else:
                program = Program.objects.filter(type=target_program_type).first()
            instance.target_program = program
        else:
            instance.target_program = None
        if commit:
            instance.save()
        return instance

class TrialExamForm(ModelForm):
    class Meta:
        model = TrialExam
        fields = [
            'attempt_number',
            'subject1_name',
            'subject1_score',
            'subject2_name',
            'subject2_score',
            'subject3_name',
            'subject3_score',
            'date_exam',
        ]
        labels = {
            'attempt_number': 'Lần thi thử thứ',
            'subject1_name': 'Môn thi thứ nhất:',
            'subject1_score': 'Điểm môn thi thứ nhất:',
            'subject2_name': 'Môn thi thứ hai:',
            'subject2_score': 'Điểm môn thi thứ hai:',
            'subject3_name': 'Môn thi thứ ba:',
            'subject3_score': 'Điểm môn thi thứ ba:',
            'date_exam': 'Ngày thi thử:',
        }
        
        help_texts = {
            'attempt_number': 'VD: 1, 2, 3...',
            'subject1_name': 'VD: Toán',
            'subject1_score': 'VD: 3.6',
            'subject2_name': 'VD: Vật lý',
            'subject2_score': 'VD: 1.8',
            'subject3_name': 'VD: Hoá Học',
            'subject3_score': 'VD: 3.5',
            'date_exam': 'Chọn ngày thi thử',
        }
        
        widgets = {
            'date_exam': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class HsaExamForm(ModelForm):
    class Meta:
        model = HsaExam
        fields = [
            'attempt_number',
            'subject1_score',
            'subject2_score',
            'subject3_score',
            'date_exam',
        ]
        labels = {
            'attempt_number': 'Lần thi thứ',
            'subject1_score': 'Điểm phần 1. Tư duy định lượng',
            'subject2_score': 'Điểm phần 2. Tư duy định tính',
            'subject3_score': 'Điểm phần 3. Khoa học hoặc tiếng anh',
            'date_exam': 'Ngày thi',
        }
        help_texts = {
            'attempt_number': 'VD: 1, 2, 3...',
            'subject1_score': 'VD: 36',
            'subject2_score': 'VD: 18',
            'subject3_score': 'VD: 35',
            'date_exam': 'Chọn ngày thi',
        }
        
        widgets = {
            'date_exam': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class TsaExamForm(ModelForm):
    class Meta:
        model = TsaExam
        fields = [
            'attempt_number',
            'subject1_score',
            'subject2_score',
            'subject3_score',
            'date_exam',
        ]
        labels = {
            'attempt_number': 'Lần thi thứ',
            'subject1_score': 'Điểm Tư duy Toán học',
            'subject2_score': 'Điểm Tư duy đọc hiểu',
            'subject3_score': 'Điểm Tư duy Khoa học/Giải quyết vấn đề',
            'date_exam': 'Ngày thi',
        }
        help_texts = {
            'attempt_number': 'VD: 1, 2, 3...',
            'subject1_score': 'VD: 36.36',
            'subject2_score': 'VD: 18.18',
            'subject3_score': 'VD: 35.35',
            'date_exam': 'Chọn ngày thi',
        }
        
        widgets = {
            'date_exam': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }