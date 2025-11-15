from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("uni/<str:code>/", views.uni_details, name = "uni"),
    path("create/", views.createQLDS, name = "createQLDS"),
    path("update/<str:pk>/", views.updateQLDS, name = "updateQLDS"),
    path("st_detail/",views.showQLDS, name = "showQLDS"),
    
    path("trial/add/<str:profile_id>/", views.addTrialExam, name = "addTrialExam"),
    path("trial/edit/<str:profile_id>/<str:exam_id>/", views.editTrialExam, name = "editTrialExam"),
    path("trial/delete/<str:profile_id>/<str:exam_id>/", views.deleteTrialExam, name = "deleteTrialExam"),
    

    path("hsa/add/<str:profile_id>/", views.addHsaExam, name = "addHsaExam"),
    path("hsa/edit/<str:profile_id>/<str:exam_id>/", views.editHsaExam, name = "editHsaExam"),
    path("hsa/delete/<str:profile_id>/<str:exam_id>/", views.deleteHsaExam, name = "deleteHsaExam"),

    path("tsa/add/<str:profile_id>/", views.addTsaExam, name = "addTsaExam"),
    path("tsa/edit/<str:profile_id>/<str:exam_id>/", views.editTsaExam, name = "editTsaExam"),
    path("tsa/delete/<str:profile_id>/<str:exam_id>/", views.deleteTsaExam, name = "deleteTsaExam"),
    
    path("st_detail/delete/<str:pk>/", views.deleteUserProfile, name = "deleteUserProfile"),
    path("program/<str:program_code>", views.detailProgram, name = "detailProgram"),
    
    path("login/", views.loginPage, name = "login"),
    path("logout/", views.LogoutUser, name = "logout"),
    path("register/", views.registerUser, name = "register"),
    
    path("home/program", views.home_program, name = "home_program"),
    path("chat-ai/", views.chat_ai, name = "chat_ai"),
    path("chat-ai/api/", views.chat_api, name="chat_api"),

]