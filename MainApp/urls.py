from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import funcSignupPatient, verify_email  # Include your verify_email view
from . import views  # Import your views

urlpatterns = [
    path('', views.funcHome, name='home'),
    path('home/', views.funcHome),
    path('login-patient/', views.funLoginPatient),
    path('signup-patient/', views.funcSignupPatient, name='signup_patient'),
    path('verify-email/<str:email>/', verify_email, name='verify_email'),  # URL pattern for email verification
    path('patient_dashboard/', views.funcPatientDashboard),
    path('patient_record_edit/', views.funcPatientRecordEdit),
    path('patient_newCase/', views.funcPatient_newCase),
    path('doctor_list/', views.funcDoctorList),
    path('patient_mycase/', views.funcPatient_mycases),
    path('login-doctor/', views.funcLogin_doctor),
    path('doctor_dashboard/', views.funcDoctor_dashboard),
    path('doc_available_cases/', views.funcDoc_available_cases),
    path('doc_recommendation/', views.doc_Recommendations),
    path('Delete_doctorCase/', views.funcDelete_doctorCase),

    path('Prediction/predictImage/', views.predictImage, name='predictImage'),
    path('Prediction/', views.Prediction),
    path('patient_prediction/', views.funcPrediction),
    path('patient_prediction/patient_predictImage/', views.predict_patient_Image, name='patient_predictImage'),

    path('delete_record/<int:case_no>/', views.funcDeleteRecord, name='patient_delete_record'),
    path('privacypolice/', views.funcPrivacy),
    path('faq/', views.funcFAQ),
    path('terms_of_use/', views.funcTermsOfUse),
    path('contact/', views.funcContact),
    path('about_us/', views.funcAboutus),
    path('patient_logout/', views.funcPatient_logout),
    path('doctor_logout/', views.funcDoctor_logout),
    path('home_logout/', views.funcHome_logout),
    path('admin_logout/', views.funcAdmin_logout),

    path('AdminPage/', views.AdminPage),
    path('AdminLogin/', views.AdminLogin),
    path('doctor_record_edit/<int:doctor_id>/', views.doctor_record_edit, name='doctor_record_edit'),
    path('doctor_record_delete/<int:doctor_id>/', views.doctor_record_delete, name='doctor_record_delete'),

    # New URL pattern for email verification
    path('verify-email/<str:email>/', views.verify_email, name='verify_email'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # for media files
