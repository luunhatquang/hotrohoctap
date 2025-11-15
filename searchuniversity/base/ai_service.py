import google.generativeai as genai
import os
from decouple import config
from .models import School, Program, Admission, StudentProfile, TrialExam, HsaExam, TsaExam
from django.conf import settings

API_KEY = config('GEMINI_API_KEY',default='')

if API_KEY:
    genai.configure(api_key=API_KEY)

generation_config = {
    "temperature": 0.8,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

def get_user_context(user):
    try:
        stprofile = StudentProfile.objects.get(user=user)
        trial_exam = TrialExam.objects.filter(student=stprofile).order_by('-attempt_number')
        best_trial_score = None
        best_trial_detail = None
        if trial_exam.exists():
            best_exam = max(trial_exam, key=lambda x: x.total_score)
            best_trial_score = best_exam.total_score
            best_trial_detail = f"{best_exam.subject1_name}: {best_exam.subject1_score},{best_exam.subject2_name}: {best_exam.subject2_score}, {best_exam.subject3_name}: {best_exam.subject3_score}"
        hsa_exam = HsaExam.objects.filter(student=stprofile).order_by('-attempt_number')
        best_hsa_score = None
        best_hsa_detail = None
        if hsa_exam.exists():
            best_exam = max(hsa_exam, key=lambda x: x.total_score)
            best_hsa_score = best_exam.total_score
            best_hsa_detail = f"{best_exam.subject1_score},{best_exam.subject2_score},{best_exam.subject3_score}"
        tsa_exam = TsaExam.objects.filter(student=stprofile).order_by('-attempt_number')
        best_tsa_score = None
        best_tsa_detail = None
        if tsa_exam.exists():
            best_exam = max(tsa_exam, key=lambda x: x.total_score)
            best_tsa_score = best_exam.total_score
            best_tsa_detail = f"{best_exam.subject1_score},{best_exam.subject2_score},{best_exam.subject3_score}"
        context = {
            'has_profile': True,
            'full_name': stprofile.full_name or 'Bạn',
            'age': stprofile.age,
            'address': stprofile.address,
            'target_school': stprofile.target_school.name if stprofile.target_school else None,
            'target_program': stprofile.target_program.name if stprofile.target_program else None,
            'target_score': stprofile.target_score,
            'ielts_score': stprofile.ielts_score,
            'best_trial_score': best_trial_score,
            'best_trial_detail': best_trial_detail,
            'best_hsa_score': best_hsa_score,
            'best_hsa_detail': best_hsa_detail,
            'best_tsa_score': best_tsa_score,
            'best_tsa_detail': best_tsa_detail,
            'trial_exams_count': trial_exam.count(),
            'trial_exams': trial_exam,
        }
    except StudentProfile.DoesNotExist:
        context = {
            'has_profile': False,
            'full_name': user.username
        }
    return context

def get_system_context():
    total_schools = School.objects.count()
    total_programs = Program.objects.count()
    latest_admission = Admission.objects.order_by('-year').first()
    year = latest_admission.year if latest_admission else 'N/A'
    context = {
        'total_schools': total_schools,
        'total_programs': total_programs,
        'current_year': year,
    }
    return context

def build_system_prompt(user_context, system_context, relevant_programs=None):
    prompt = f"""Bạn là một trợ lý ảo thông minh giúp học sinh Việt Nam trong các vấn đề học tập

THÔNG TIN HỆ THỐNG:
- Có {system_context['total_schools']} trường đại học
- Có {system_context['total_programs']} ngành học
- Năm tuyển sinh hiện tại: {system_context['current_year']}

"""
    if user_context['has_profile']:
        prompt += f"""THÔNG TIN HỌC SINH:
- Tên: {user_context['full_name']}
"""
        if user_context['age']:
            prompt += f"- Tuổi: {user_context['age']}\n"
        if user_context.get('trial_exams') and user_context['trial_exams'].exists():
            prompt += f"\nLỊCH SỬ THI THỬ ({user_context['trial_exams_count']} lần):\n"
            for exam in user_context['trial_exams']:
                prompt += f"  • Lần {exam.attempt_number}: {exam.total_score:.1f} điểm "
                prompt += f"({exam.subject1_name}: {exam.subject1_score}, "
                prompt += f"{exam.subject2_name}: {exam.subject2_score}, "
                prompt += f"{exam.subject3_name}: {exam.subject3_score})"
                if exam.date_exam:
                    prompt += f" - Ngày: {exam.date_exam.strftime('%d/%m/%Y')}"
                prompt += "\n"
            prompt += f" Điểm cao nhất: {user_context['best_trial_score']:.1f} điểm\n"
        
        if user_context['best_hsa_score']:
            prompt += f"- Điểm HSA: {user_context['best_hsa_score']:.1f}\n"
        
        if user_context['best_tsa_score']:
            prompt += f"- Điểm TSA: {user_context['best_tsa_score']:.1f}\n"
        
        if user_context['ielts_score']:
            prompt += f"- Điểm IELTS: {user_context['ielts_score']}\n"
        
        if user_context['target_school']:
            prompt += f"- Trường mục tiêu: {user_context['target_school']}\n"
        
        if user_context['target_program']:
            prompt += f"- Ngành mục tiêu: {user_context['target_program']}\n"
    
    else:
        prompt += f"""THÔNG TIN HỌC SINH:
- Tên: {user_context['full_name']}
- Chưa có hồ sơ trong hệ thống (khuyên tạo hồ sơ để nhận tư vấn tốt hơn)

"""
    if relevant_programs:
        prompt += "\n" + "="*60 + "\n"
        prompt += "CÁC NGÀNH PHÙ HỢP VỚI ĐIỂM SỐ CỦA HỌC SINH:\n"
        prompt += "="*60 + "\n\n"
        
        for i, prog in enumerate(relevant_programs, 1):
            prompt += f"[{i}] {prog['program_name']}\n"
            prompt += f"    🏫 Trường: {prog['school_name']} ({prog['school_region']})\n"
            prompt += f"    📍 Địa chỉ: {prog['school_address']}\n"
            prompt += f"    📊 Điểm chuẩn {prog['admission_year']}: {prog['admission_score']:.1f}\n"
            prompt += f"    💰 Học phí: {prog['tuition']:,.0f} VNĐ/năm\n"
            prompt += f"    📚 Tổ hợp môn: {prog['subject_combinations']}\n"
            prompt += f"    🏷️  Loại ngành: {prog['program_type']}\n"
            
            # Đánh giá độ phù hợp
            score_diff = prog['score_diff']
            if score_diff <= 0.5:
                prompt += f"    ✅ Rất phù hợp! (Điểm của bạn cao hơn {score_diff:.1f} điểm)\n"
            elif score_diff <= 1:
                prompt += f"    ✅ Phù hợp (Điểm của bạn cao hơn {score_diff:.1f} điểm)\n"
            elif score_diff <= 2:
                prompt += f"    ⚠️  Cần cố gắng thêm (Cần thêm {score_diff:.1f} điểm)\n"
            else:
                prompt += f"    ❌ Khó đỗ (Cần thêm {score_diff:.1f} điểm)\n"
            
            prompt += "\n"
    
    prompt += """
VAI TRÒ CỦA BẠN:
1. Tư vấn chọn trường, ngành dựa trên điểm số và sở thích
2. Giải thích về điểm chuẩn, học phí, khu vực
3. So sánh các trường/ngành khác nhau
4. Đưa ra chiến lược đăng ký nguyện vọng
5. Trả lời các câu hỏi về tuyển sinh đại học
6. Đưa ra lời khuyên cải thiện kết quả học tập
7. Tư vấn, hỗ trợ các vấn đề trong học tập

CÁCH TRẢ LỜI:
- Ngắn gọn, dễ hiểu, thân thiện
- Sử dụng tiếng Việt
- Dựa trên thông tin thực tế của học sinh
- Dựa trên danh sách các ngành phù hợp ở trên (nếu có)
- Nếu có lịch sử thi thử, hãy đánh giá xu hướng tiến bộ (tăng/giảm/ổn định)
- Nếu học sinh chưa có điểm, khuyên làm bài thi thử
- Format rõ ràng với bullet points khi cần
- Đưa ra lời khuyên cụ thể, có số liệu
- Trích dẫn số thứ tự [1], [2],... khi đề cập đến ngành
- Nhận xét về sự tiến bộ qua các lần thi (nếu có nhiều lần thi)

HÃY TRẢ LỜI CÂU HỎI SAU:
"""
    return prompt

def get_relevant_programs(user_context, user_query=""):
    if not user_context.get('best_trial_score'):
        return []
    
    user_score = user_context['best_trial_score']
   
    relevant_admissions = (
        Admission.objects
        .filter(
            score__lte=user_score + 1,
            score__gte=user_score - 3,
        )
        .select_related('program', 'program__school')
        .order_by('-year', '-score')[:50]  
    )
    
    keywords = {
        'it_cntt': ['công nghệ', 'it', 'phần mềm', 'máy tính', 'ai', 'data', 'khoa học máy tính', 
                    'an toàn thông tin', 'mạng', 'hệ thống thông tin', 'trí tuệ nhân tạo'],
        
        'kinh_te': ['kinh tế', 'quản trị', 'marketing', 'kinh doanh', 'tài chính', 
                    'kế toán', 'ngân hàng', 'thương mại', 'logistics'],
        
        'y_duoc': ['y', 'dược', 'điều dưỡng', 'răng hàm', 'y tế', 'bác sĩ', 
                   'y khoa', 'dược học'],
        
        'ky_thuat': ['kỹ thuật', 'cơ khí', 'điện', 'xây dựng', 'hóa', 
                     'cơ điện tử', 'tự động hóa', 'công nghiệp'],
        
        'giao_duc': ['giáo dục', 'sư phạm', 'mầm non', 'tiểu học', 'giáo viên'],
        
        'ngoai_ngu': ['ngoại ngữ', 'tiếng anh', 'tiếng trung', 'tiếng nhật', 
                      'tiếng hàn', 'ngôn ngữ'],
        
        'luat': ['luật', 'pháp luật', 'tư pháp', 'hành chính'],
    }
    
    region_keywords = {
        'ha_noi': ['hà nội', 'hn', 'thủ đô'],
        'hcm': ['hồ chí minh', 'sài gòn', 'hcm', 'tp hcm'],
        'da_nang': ['đà nẵng', 'dn'],
        'can_tho': ['cần thơ', 'ct'],
    }
    
    filtered_programs = []
    
    for admission in relevant_admissions:
        program = admission.program
        school = program.school 
        program_name = program.name.lower()
        school_name = school.name.lower()
        school_region = school.get_region_display().lower()
        
        priority_score = 0
        
        matched_category = False
        for category, words in keywords.items():
            if any(word in user_query.lower() for word in words):
                if any(word in program_name for word in words):
                    priority_score += 10
                    matched_category = True
                    break
        
        for region, words in region_keywords.items():
            if any(word in user_query.lower() for word in words):
                if any(word in school_name for word in words) or any(word in school_region for word in words):
                    priority_score += 5
                    break
        
        score_diff = abs(admission.score - user_score)
        if score_diff <= 0.5:
            priority_score += 8
        elif score_diff <= 1:
            priority_score += 5
        elif score_diff <= 2:
            priority_score += 2
            
        if user_context.get('target_school') and school.name == user_context['target_school']:
            priority_score += 15
        
        if user_context.get('target_program') and program.name == user_context['target_program']:
            priority_score += 15
        
        has_keyword = any(any(word in user_query.lower() for word in words) for words in keywords.values())
        if has_keyword and not matched_category:
            continue
        
        filtered_programs.append({
   
            'school_name': school.name,
            'school_code': school.code,
            'school_region': school.get_region_display(),
            'school_type': school.get_type_school_display(),
            'school_address': school.address,
            'school_website': school.website,
            'school_phone': school.phone,
         
            'program_name': program.name,
            'program_code': program.code,
            'program_type': program.get_type_display() if program.type else 'Chưa phân loại',
            'tuition': program.tuition or 0,
            
            'admission_score': admission.score,
            'admission_year': admission.year,
            'subject_combinations': program.subject_combinations or 'Chưa cập nhật',
           
            'priority': priority_score,
            'score_diff': score_diff,
        })
   
    filtered_programs.sort(key=lambda x: (-x['priority'], x['score_diff']))
    
    return filtered_programs[:10] 

def generate_ai_response(user_message, user, conversation_history=None):
    if not API_KEY:
        return "AI service is currently unavailable."
    
    try:
        user_context = get_user_context(user)
        system_context = get_system_context()
        relevant_programs = get_relevant_programs(user_context, user_message)
        prompt = build_system_prompt(user_context, system_context, relevant_programs)
        model = genai.GenerativeModel(
            model_name="models/gemini-2.5-flash",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )
        full_prompt = prompt + "\n" + user_message
        
        if conversation_history:
            history_text = ""
            for msg in conversation_history[-5:]:
                history_text += f"User: {msg.get('user', '')}\n"
                history_text += f"AI: {msg.get('ai', '')}\n\n"
            full_prompt = history_text + full_prompt
            
        response = model.generate_content(full_prompt)
        
        return response.text
    except Exception as e:
        error_msg = str(e)
        if "quota" in error_msg.lower() or "limit" in error_msg.lower():
            return "Xin lỗi, hệ thống đã vượt quá giới hạn requests của Gemini API. Vui lòng thử lại sau."
        else:
            return f"Xin lỗi, đã có lỗi xảy ra: {error_msg}"