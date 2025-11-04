from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import School, Program, Admission, StudentProfile, TrialExam, HsaExam, TsaExam
from .form import StudentProfileForm, TrialExamForm, HsaExamForm, TsaExamForm
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Sai tên đăng nhập hoặc mật khẩu, vui lòng thử lại')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def LogoutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if (form.is_valid()):
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('login')
        else:
            messages.error(request,"Có lỗi xảy ra trong quá trình đăng ký, vui lòng thử lại!")
    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    page_number = request.GET.get('page')
    list_uni_qs = School.objects.filter(Q(region__icontains=q) | Q(name__icontains=q))
    pagination = Paginator(list_uni_qs, 20)
    try:
        uni_list = pagination.page(page_number)
    except PageNotAnInteger:
        page_number = 1
        uni_list = pagination.page(page_number)
    except EmptyPage:
        uni_list = pagination.page(pagination.num_pages)
    
    uni_count = list_uni_qs.count()
    context = {'list_uni': uni_list, 'uni_count': uni_count}
    return render(request, 'base/home.html', context)


def home_program(request):
    category     = request.GET.get('category', '')
    min_score    = request.GET.get('min_score')
    max_score    = request.GET.get('max_score')
    year         = request.GET.get('year') or '2025'
    min_tuition  = request.GET.get('min_tuition')
    max_tuition  = request.GET.get('max_tuition')
    page_number  = request.GET.get('page')
    select       = request.GET.get('select','')
    try:
        stprofile = request.user.student_profile if request.user.is_authenticated else None
    except StudentProfile.DoesNotExist:
        stprofile = None
    
    max_total = None
    best_exam = None
    if (stprofile):
        trial_exams = TrialExam.objects.filter(student=stprofile)
        if trial_exams.exists():
            max_score_value = 0
            for exam in trial_exams:
                total = exam.total_score
                if total > max_score_value:
                    max_score_value = total
                    best_exam = exam
            max_total = max_score_value if max_score_value > 0 else None
    admissions_qs = Admission.objects.filter(year=int(year))
    if min_score:
        admissions_qs = admissions_qs.filter(
            score__gte=float(min_score)
        )
    if max_score:
        admissions_qs = admissions_qs.filter(
            score__lte=float(max_score)
        )
    admissions_qs = admissions_qs.order_by('-year')
    if (select):
        if(stprofile and max_total):
            # Tìm các ngành có điểm chuẩn từ (điểm thi thử - 1) đến (điểm thi thử + 1)
            admissions_qs = admissions_qs.filter(
                score__gte=float(max_total) - 1,
                score__lte=float(max_total) + 1,
            )
        else:
            messages.error(request, 'Vui lòng tạo hồ sơ hoặc đăng nhập để sử dụng tính năng này!')
            return redirect('login')
    qs = (
        Program.objects
        .select_related('school')
        .prefetch_related(
            Prefetch(
                'admissions',
                queryset=admissions_qs.order_by('-year'),
                to_attr='filtered_admissions'
            )
        )
    )
    
    if category:
        qs = qs.filter(type__icontains=category)
    if min_tuition:
        qs = qs.filter(tuition__gte=float(min_tuition))
    if max_tuition:
        qs = qs.filter(tuition__lte=float(max_tuition))

    qs = qs.filter(admissions__in=admissions_qs).distinct()
    
    list_program = qs
    program_count = list_program.count()
    pagination = Paginator(list_program, 20)
    try:
        program_list = pagination.page(page_number)
    except PageNotAnInteger:
        page_number = 1
        program_list = pagination.page(page_number)
    except EmptyPage:
        program_list = pagination.page(pagination.num_pages)
    
    context = {
        'list_program': program_list,
        'program_count': program_count,
        'max_trial_score': max_total if select else None,
        'best_exam': best_exam if select else None,
    }    
    return render(request,'base/search_program.html', context)
def uni_details(request, code):
    uni_room = School.objects.get(code=code)
    program = Program.objects.filter(school=uni_room).prefetch_related('admissions').order_by('name')
    pagination = Paginator(program, 20)
    page_number = request.GET.get('page')
    try:
        program = pagination.page(page_number)
    except PageNotAnInteger:
        page_number = 1
        program = pagination.page(page_number)
    except EmptyPage:
        program = pagination.page(pagination.num_pages)
    list_program = program
    context = {
        'uni_room': uni_room,
        'program': list_program,
    }
    return render(request, 'base/uni_details.html', context)

@login_required(login_url='login')
def createQLDS(request):
    if (StudentProfile.objects.filter(user = request.user).exists()):
        messages.warning(request, 'Bạn đã có hồ sơ rồi! Vui lòng chỉnh sửa hồ sơ hiện có.')
        return redirect('showQLDS')
    form = StudentProfileForm()
    if (request.method == 'POST'):
        form = StudentProfileForm(request.POST)
        if (form.is_valid()):
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Tạo hồ sơ thành công!')
            redirect('home')
            return;
    context = {'form': form}
    return render(request, 'base/room_form.html',context)

@login_required(login_url='login')
def updateQLDS(request, pk):
    stprofile = StudentProfile.objects.get(id=pk)
    if (stprofile.user != request.user):
        messages.error(request,"Bạn không có quyền chỉnh sửa hồ sơ này!")
        return redirect('home')
    form = StudentProfileForm(instance=stprofile)
    if (request.method == "POST"):
        form = StudentProfileForm(request.POST, instance=stprofile)
        if (form.is_valid()):
            form.save()
            messages.success(request, 'Cập nhật hồ sơ thành công!')
            return redirect('showQLDS')
            
    context = {'form': form}
    return render(request, 'base/update_profile.html', context)
    
@login_required(login_url='login')
def showQLDS(request):
    stprofile = StudentProfile.objects.filter(user=request.user)
    context = {'stprofile': stprofile}
    return render(request, 'base/student_profile.html', context)

@login_required(login_url='login')
def addTrialExam(request, profile_id):
    profile = StudentProfile.objects.get(id=profile_id)

    if profile.user != request.user:
        messages.error(request, 'Bạn không có quyền!')
        return redirect('home')
    
    if request.method == 'POST':
        form = TrialExamForm(request.POST)
        if form.is_valid():
            trial_exam = form.save(commit=False)
            trial_exam.student = profile

            existing = TrialExam.objects.filter(
                student=profile, 
                attempt_number=trial_exam.attempt_number
            ).exists()
            
            if existing:
                messages.error(request, f'Lần thi thứ {trial_exam.attempt_number} đã tồn tại! Vui lòng chọn số khác.')
                context = {'form': form, 'exam': None}
                return render(request, 'base/trial_exam_form.html', context)
            
            trial_exam.save()
            messages.success(request, f'Đã thêm điểm thi thử lần {trial_exam.attempt_number}!')
            return redirect('showQLDS')
    else:
        form = TrialExamForm()
    
    context = {'form': form, 'exam': None}
    return render(request, 'base/trial_exam_form.html', context)

@login_required(login_url='login')
def editTrialExam(request, profile_id, exam_id):
    profile = StudentProfile.objects.get(id = profile_id)
    exam = TrialExam.objects.get(id = exam_id)
    if (profile.user != request.user):
        messages.error(request, 'Bạn không có quyền! Vui lòng đăng nhập!')
        return redirect('login')
    form = TrialExamForm(instance = exam)
    if request.method == 'POST':
        form = TrialExamForm(request.POST, instance = exam)
        if form.is_valid():
            form.save()
            messages.success(request,'Cập nhật dữ liệu thành công')
            return redirect('showQLDS')
    context = {'form': form}
    return render(request, 'base/trial_exam_form.html', context)

@login_required(login_url='login')
def addHsaExam(request, profile_id):
    profile = StudentProfile.objects.get(id = profile_id)
    
    if (profile.user != request.user):
        messages.error(request, 'Bạn không có quyền! Vui lòng đăng nhập!')
        return redirect('login')
    if request.method == 'POST':
        form = HsaExamForm(request.POST)
        if form.is_valid():
            hsa_exam = form.save(commit=False)
            hsa_exam.student = profile
            
            existing = HsaExam.objects.filter(
                student = profile,
                attempt_number = hsa_exam.attempt_number
            ).exists()
            if existing:
                messages.error(request, f'Lần thi thứ {hsa_exam.attempt_number} đã tồn tại! Vui lòng chọn số khác.')
                context = {'form': form, 'exam': None}
                return render(request, 'base/hsa_exam_form.html', context)
            hsa_exam.save()
            messages.success(request, f'Đã thêm điểm thi HSA lần {hsa_exam.attempt_number}!')
            return redirect('showQLDS')
    else:
        form = HsaExamForm()
    context = {'form': form, 'exam': None}
    return render(request, 'base/hsa_exam_form.html', context)

@login_required(login_url='login')
def editHsaExam(request, profile_id, exam_id):
    profile = StudentProfile.objects.get(id = profile_id)
    exam = HsaExam.objects.get(id = exam_id)
    if (profile.user != request.user):
        messages.error(request, 'Bạn không có quyền! Vui lòng đăng nhập!')
        return redirect('login')
    form = HsaExamForm(instance = exam)
    if request.method == 'POST':
        form = HsaExamForm(request.POST, instance = exam)
        if form.is_valid():
            form.save()
            messages.success(request,'Cập nhật dữ liệu thành công')
            return redirect('showQLDS')
    context = {'form': form}
    return render(request, 'base/hsa_exam_form.html', context)

@login_required(login_url='login')
def addTsaExam(request, profile_id):
    profile = StudentProfile.objects.get(id = profile_id)
    if (profile.user != request.user):
        messages.error(request, 'Bạn không có quyền! Vui lòng đăng nhập!')
        return redirect('login')
    if request.method == 'POST':
        form = TsaExamForm(request.POST)
        if form.is_valid():
            tsa_exam = form.save(commit=False)
            tsa_exam.student = profile
            
            existing = TsaExam.objects.filter(
                student = profile,
                attempt_number = tsa_exam.attempt_number
            ).exists()
            if existing:
                messages.error(request, f'Lần thi thứ {tsa_exam.attempt_number} đã tồn tại! Vui lòng chọn số khác.')
                context = {'form': form, 'exam': None}
                return render(request, 'base/tsa_exam_form.html', context)
            tsa_exam.save()
            messages.success(request, f'Đã thêm điểm thi TSA lần {tsa_exam.attempt_number}!')
            return redirect('showQLDS')
    else:
        form = TsaExamForm()
    context = {'form': form, 'exam': None}
    return render(request, 'base/tsa_exam_form.html', context)

@login_required(login_url='login')
def editTsaExam(request, profile_id, exam_id):
    profile = StudentProfile.objects.get(id = profile_id)
    exam = TsaExam.objects.get(id = exam_id)
    if (profile.user != request.user):
        messages.error(request,"Bạn không có quyền! Vui lòng đăng nhập!")
        return redirect('login')
    form = TsaExamForm(instance = exam)
    if request.method == "POST":
        form = TsaExamForm(request.POST, instance = exam)
        if form.is_valid:
            form.save()
            messages.success(request,"Cập nhật dữ liệu thành công")
            return redirect("showQLDS")
    context = {'form': form}
    return render(request, 'base/tsa_exam_form.html',context)
            
@login_required(login_url='login')
def deleteTrialExam(request, profile_id, exam_id):
    profile = StudentProfile.objects.get(id=profile_id)
    if (profile.user != request.user):
        messages.error(request, 'Bạn không có quyền! Vui lòng đăng nhập!')
        return redirect('login')
    trial_exam = TrialExam.objects.get(id = exam_id)
    trial_exam.delete()
    messages.success(request, 'Xóa thành công!')
    return redirect('showQLDS')

@login_required(login_url='login')
def deleteHsaExam(request, profile_id, exam_id):
    profile = StudentProfile.objects.get(id = profile_id)
    if (profile.user != request.user):
        messages.error(request,"Bạn không có quyền! Vui lòng đăng nhập!")
        return redirect('login')
    hsa_exam = HsaExam.objects.get(id = exam_id)
    hsa_exam.delete()
    messages.success(request, 'Xóa thành công!')
    return redirect('showQLDS')

@login_required(login_url='login')
def deleteTsaExam(request, profile_id, exam_id):
    profile = StudentProfile.objects.get(id = profile_id)
    if (profile.user != request.user):
        messages.error(request,"Bạn không có quyền! Vui lòng đăng nhập!")
        return redirect('login')
    tsa_exam = TsaExam.objects.get(id = exam_id)
    tsa_exam.delete()
    messages.success(request, 'Xóa thành công!')
    return redirect('showQLDS')
        
@login_required(login_url='login')
def deleteUserProfile(request, pk):
    try:
        profile = StudentProfile.objects.get(id=pk)
    except StudentProfile.DoesNotExist:
        messages.error(request, "Hồ sơ không tồn tại!")
        return redirect('home')
    
    if profile.user != request.user:
        messages.error(request, "Bạn không có quyền xóa hồ sơ này!")
        return redirect('home')

    profile.trial_exams.all().delete()
    profile.hsa_exams.all().delete()
    profile.tsa_exams.all().delete()

    profile.delete()
    messages.success(request, 'Đã xóa toàn bộ hồ sơ thành công!')
    return redirect('home')

def detailProgram(request, program_code):
    program = Program.objects.get(code=program_code)
    context = {'program': program}
    return render(request, 'base/program_detail.html', context)
