from django.db import models

# Create your models here.

class admin_details(models.Model):
    admin_name = models.CharField(max_length=100, null=True)
    admin_email = models.CharField(max_length=100, null=True)
    admin_password = models.CharField(max_length=100, null=True)

class patient_details(models.Model):
    patient_username = models.CharField(max_length=100,null=True)
    patient_firstname = models.CharField(max_length=100,null=True)
    patient_secondname = models.CharField(max_length=100,null=True)
    patient_email = models.CharField(max_length=100,null=True)
    patient_password = models.CharField(max_length=100,null=True)
    is_verified = models.BooleanField(default=False)  # Add this field
    patient_mobile = models.CharField(max_length=100,null=True)
    patient_gender = models.CharField(max_length=6,null=True)
    patient_dob = models.DateField(null=True)
    patient_civilstatus = models.CharField(max_length=20,null=True)
    patient_age = models.IntegerField(null=True)
    patient_image = models.ImageField(upload_to='db_images/patient_images' , blank=True, null=True)

    def __str__(self):
        return self.patient_email


class availabledoctors(models.Model):
    doctor_name = models.CharField(max_length=100, null=True)
    doctor_email = models.CharField(max_length=200, null=True)
    doctor_age = models.IntegerField(null=True)
    doctor_gender = models.CharField(max_length=6, null=True)
    doctor_mobile = models.CharField(max_length=100, null=True)
    doctor_qualification = models.CharField(max_length=100, null=True)
    doctor_jobstatus = models.CharField(max_length=50, null=True)
    doctor_image = models.ImageField(upload_to='db_images/doctor_images', default='')
    doctor_password = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.doctor_email

class doctor_remarks(models.Model):
    patient_id = models.IntegerField(null=True)
    case_no = models.IntegerField(null= True)
    doctor_name = models.CharField(max_length=100, null= True)
    doctor_email = models.CharField(max_length=100, null= True)
    doctor_remarks = models.CharField(max_length=300, null= True)

class patienttodoctor(models.Model):
    patient_id = models.IntegerField(null=True)
    patient_firstname = models.CharField(max_length=100, null=True)
    patient_email = models.CharField(max_length=100, null=True)
    patient_mobile = models.CharField(max_length=100, null=True)
    case_no = models.IntegerField(null=True)
    doctor_id = models.IntegerField(null=True)
    patient_image = models.CharField(max_length=300, null=True)
    doctor_respond = models.CharField(max_length=500, default='No')

    def __str__(self):
        return self.patient_firstname

class patient_history(models.Model):
    patient_id = models.IntegerField(null=True)
    case_no = models.IntegerField(null=True)
    model_prediction = models.CharField(max_length=100, null=True)
    abdominalproblem = models.CharField(max_length=10, null=True)
    heartproblem = models.CharField(max_length=10, null=True)
    anyseriousinjury = models.CharField(max_length=10, null=True)
    kidneybladderinfection = models.CharField(max_length=10, null=True)
    asthma = models.CharField(max_length=10, null=True)
    skinalergy = models.CharField(max_length=10, null=True)
    brokenbones = models.CharField(max_length=10, null=True)
    visiteddoctorbefore = models.CharField(max_length=10, null=True)