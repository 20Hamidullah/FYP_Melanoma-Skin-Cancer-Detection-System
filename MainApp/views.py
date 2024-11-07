import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse

from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from urllib.parse import quote
from .models import patient_details  
import re
from .models import *
from django.core.files.storage import FileSystemStorage
from django.middleware import csrf
from django.http import HttpResponseBadRequest
import os
import numpy as np
import cv2

# Keras
from tensorflow import keras 
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from keras.preprocessing import image as keras_image 
import PIL
from PIL import Image


MODEL_PATH_1 = './models/SkinNonSkinVGG16_Weights_and_architecture.h5'
MODEL_PATH_2 = './models/VGG16_Weights_and_architecture.h5'
#Load your trained model
model_1 = load_model(MODEL_PATH_1)
model_2 = load_model(MODEL_PATH_2)
class_dict_1 = {0:"Non-Skin",
             1:"Skin"}

class_dict_2 = {0:"Benign",
             1:"Malignant"}



# Create your views here.
def AdminPage(request):
    if request.method == 'POST':
        doctor_name = request.POST['doctor_name']
        doctor_email = request.POST['doctor_email']

        if availabledoctors.objects.filter(doctor_email=doctor_email).exists():
            doctors = availabledoctors.objects.all()
            error_message = 'Doctor with the same email already exists.'
            return render(request, 'AdminPagedoc.html', {'doctors': doctors, 'error_message': error_message})

        # Rest of the code for saving the new doctor record
        doctor_age = request.POST['doctor_age']
        doctor_gender = request.POST['doctor_gender']
        doctor_mobile = request.POST['doctor_mobile']
        doctor_qualification = request.POST['doctor_qualification']
        doctor_jobstatus = request.POST['doctor_jobstatus']
        doctor_image = request.FILES.get('doctor_image')
        doctor_password = request.POST['doctor_password']

        query = availabledoctors(doctor_name=doctor_name, doctor_email=doctor_email, doctor_age=doctor_age, doctor_gender=doctor_gender, doctor_mobile=doctor_mobile, doctor_qualification=doctor_qualification, doctor_jobstatus=doctor_jobstatus, doctor_image=doctor_image, doctor_password=doctor_password)
        query.save()

        return redirect('/AdminPage/')
    else:
        doctors = availabledoctors.objects.all()
        return render(request, 'AdminPagedoc.html', {'doctors': doctors})

def AdminLogin(request):
    if request.method == 'POST':
        email = request.POST['email']  
        password = request.POST['password'] 
        query = admin_details.objects.filter(admin_email=email, admin_password=password).first()  

        if not query:
            return render(request, 'Admin_login.html', {'error': 'Invalid email or password'})
        else:
            admin_id = query.id
            admin_name = query.admin_name
            admin_email = query.admin_email
            request.session['admin_id_session_var'] = admin_id
            request.session['admin_name_session_var'] = admin_name
            request.session['admin_email_session_var'] = admin_email

            return redirect('/AdminPage/')
    return render(request, 'Admin_login.html')

def doctor_record_edit(request, doctor_id):
    query = availabledoctors.objects.filter(id=doctor_id).first()
    csrf_token = csrf.get_token(request)

    if not query:
        # Handle the case when the doctor record is not found
        return redirect('/AdminPage/')

    if request.method == 'POST':
        # Process the form data and update the doctor record
        doctor_name = request.POST['doctor_name']
        doctor_email = request.POST['doctor_email']
        doctor_age = request.POST['doctor_age']
        doctor_gender = request.POST['doctor_gender']
        doctor_mobile = request.POST['doctor_mobile']
        doctor_qualification = request.POST['doctor_qualification']
        doctor_jobstatus = request.POST['doctor_jobstatus']
        doctor_image = request.FILES.get('doctor_image')
        doctor_password = request.POST['doctor_password']

        # Update the doctor record with the new values
        query.doctor_name = doctor_name
        query.doctor_email = doctor_email
        query.doctor_age = doctor_age
        query.doctor_gender = doctor_gender
        query.doctor_mobile = doctor_mobile
        query.doctor_qualification = doctor_qualification
        query.doctor_jobstatus = doctor_jobstatus
        query.doctor_password = doctor_password

        if doctor_image:
            query.doctor_image = doctor_image

        query.save()

        return redirect('/AdminPage/')

    return render(request, 'AdminUpdateDoc.html', {
        'doctor': query,
        'csrf_token': csrf_token
    })

def doctor_record_delete(request, doctor_id):
    if request.method == 'POST':
        # Retrieve the doctor record to be deleted
        doctor = availabledoctors.objects.filter(id=doctor_id).first()

        if doctor:
            # Delete the doctor record
            doctor.delete()

    return redirect('/AdminPage/')


def funcHome(request):

    query = patient_details.objects.count()
    # query2 = patient_history.objects.filter(model_prediction).count()
    query2 = patient_history.objects.filter(model_prediction__isnull=False).count()
    query3 = patient_history.objects.filter(model_prediction = 'Malignant').count()
    print(query3)
    params = {'total_patients' : query,'total_prediction':query2,'milagnant_pre':query3}
    return render(request, 'home.html', params)


# ===============================================================================



def funLoginPatient(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        query = patient_details.objects.filter(patient_email = email, patient_password = password).first()

        if not query:
            
            return render(request, 'login-patient.html', {'error': 'Invalid email or password'})
        else:
            patient_id = query.id
            patient_firstname = query.patient_firstname
            patient_email = query.patient_email
            patient_mobile = query.patient_mobile
            request.session['patient_id_session_var'] = patient_id
            request.session['patient_firstname_session_var'] = patient_firstname
            request.session['patient_email_session_var'] = patient_email
            request.session['patient_mobile_session_var'] = patient_mobile

            return redirect('/patient_dashboard/')
        
    return render(request, 'login-patient.html')



# ===============================================================================


def funcSignupPatient(request):
    
    sweetalert = []

    if request.method == 'POST':
        nickname = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        rpassword = request.POST['rpassword']

        # Validate email format
        if not validate_email(email):
            return render(request, 'signup-patient.html', {'error': 'Invalid email format'})

        # Redirect user to Google login if the email is not valid
        if not validate_email_with_google(email):
            return render(request, 'signup-patient.html', {'error': 'Email must be a Google account'})

        if password == rpassword:
            query = patient_details.objects.filter(patient_email=email)
            if query.exists():
                return render(request, 'signup-patient.html', {'error': 'Email already exists'})
            else:
                # Send verification email
                send_verification_email(email, nickname)

                # Save user details (consider adding a field to mark email as unverified)
                patient_details.objects.create(patient_username=nickname, patient_email=email, patient_password=password)
                return redirect('/login-patient/')
        else:
            return render(request, 'signup-patient.html', {'error': 'Passwords do not match'})

    return render(request, 'signup-patient.html')

def verify_email(request, email):
    # Decode the email if needed, but usually not necessary since we directly use it
    # patient = get_object_or_404(patient_details, patient_email=email)
    
    try:
        patient = patient_details.objects.get(patient_email=email)
        patient.is_verified = True  # Assuming you have an is_verified field
        patient.save()  # Save the updated record
        return HttpResponse("Email verified successfully!")
    except patient_details.DoesNotExist:
        return HttpResponse("Verification failed: Email not found.")

def validate_email(email):
    # Simple regex for validating an email address
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def validate_email_with_google(email):
    # Check if the email ends with a valid Google domain
    valid_domains = ['gmail.com', 'googlemail.com']
    if any(email.endswith(domain) for domain in valid_domains):
        return True
    return False

def send_verification_email(email, username):
    subject = 'Please verify your email address'
    # Encode the email address to ensure it's URL safe
    email_encoded = quote(email)
    # Create the verification link with a trailing slash
    verification_link = f'http://127.0.0.1:8000/verify-email/{email_encoded}/'
    message = f'Hi {username},\n\nThank you for signing up. Please verify your email address by clicking the link below:\n\n{verification_link}\n\nThank you!'
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email])


# ===============================================================================



def funcPatientDashboard(request):
    session_patient_id = request.session.get('patient_id_session_var')
    query = patient_details.objects.filter(id = session_patient_id).first()
    patient_totalCases = patient_history.objects.filter(patient_id = session_patient_id).count()
    if query.patient_image:
        print(query.patient_image)
    if request.method == 'POST':
        random_newCasenumber = random.randint(10000, 99999)
        request.session['patient_case_No_session_var'] = random_newCasenumber
        return redirect(f'/patient_newCase/')
    return render(request, 'patient_dashboard.html', {'session_patient_id' : session_patient_id, 'patient_firstname':query.patient_firstname, 'patient_secondname' : query.patient_secondname, 'patient_age': query.patient_age, 'patient_gender': query.patient_gender, 'patient_mobile': query.patient_mobile, 'patient_email': query.patient_email, 'patient_civilstatus': query.patient_civilstatus, 'patient_dob': query.patient_dob, 'patient_image': query.patient_image,'patient_total_cases':patient_totalCases})



# ===============================================================================




def funcPatientRecordEdit(request):
    session_patient_id = request.session.get('patient_id_session_var')
    query = patient_details.objects.filter(id=session_patient_id).first()
    csrf_token = csrf.get_token(request)
    if request.method == 'POST':
        
        patient_firstname = request.POST['patient_firstname']
        patient_secondname = request.POST['patient_secondname']
        patient_age = request.POST['patient_age']
        patient_gender = request.POST['patient_gender']
        patient_mobile = request.POST['patient_mobile']
        patient_civilstatus = request.POST['patient_civilstatus']
        patient_dob = request.POST['patient_dob']
        patient_image = request.FILES.get('patient_imgfile')

        if query:
            query.patient_firstname = patient_firstname
            query.patient_secondname = patient_secondname
            query.patient_age = patient_age
            query.patient_gender = patient_gender
            query.patient_mobile = patient_mobile
            query.patient_civilstatus = patient_civilstatus
            query.patient_dob = patient_dob

            if patient_image:
                query.patient_image = patient_image

            query.save()
            return redirect('/patient_dashboard/')
        else:
            print('Failed')
            return redirect('/patient_record_edit/')

    return render(request, 'patient_record_edit.html', {
        'patient_firstname': query.patient_firstname,
        'patient_secondname': query.patient_secondname,
        'patient_age': query.patient_age,
        'patient_gender': query.patient_gender,
        'patient_mobile': query.patient_mobile,
        'patient_email': query.patient_email,
        'patient_civilstatus': query.patient_civilstatus,
        'patient_dob': query.patient_dob,
        'patient_image': query.patient_image,
        'csrf_token': csrf_token  # Pass the CSRF token to the template
    })

# ===============================================================================



def funcPatient_mycases(request):

    session_patient_id = request.session.get('patient_id_session_var')

    query = patient_history.objects.filter( patient_id =  session_patient_id).all()
    query2 = doctor_remarks.objects.filter( patient_id =  session_patient_id).all()

    params = {'complete_query' : query,'case_no_complete': query2}
    return render(request,'patient_mycase.html', params)



# ===============================================================================



def funcPatient_newCase(request):


    cancer_result = request.session.get('cancer_result_session_var')

    session_patient_id = request.session.get('patient_id_session_var')
    query = patient_details.objects.filter(id = session_patient_id).first()
    randomCaseno = request.session['patient_case_No_session_var']
    
    query.save()
    if request.method == 'POST':
        randomCaseno = request.session['patient_case_No_session_var']
        value1 = request.POST.get('history1')
        value2 = request.POST.get('history2')
        value3 = request.POST.get('history3')
        value4 = request.POST.get('history4')
        value5 = request.POST.get('history5')
        value6 = request.POST.get('history6')
        value7 = request.POST.get('history7')
        value8 = request.POST.get('history8')

        query2 = patient_history(patient_id = session_patient_id, case_no = randomCaseno, model_prediction = cancer_result , abdominalproblem = value1, heartproblem = value5, anyseriousinjury = value2, kidneybladderinfection = value6, asthma = value3, skinalergy = value7, brokenbones = value4, visiteddoctorbefore = value8)
        query2.save()
        if query2:
            return redirect('/doctor_list/')
        else:
            print('db submit failed')
    return render(request, 'patient_newCase.html', {'patient_id': session_patient_id,'case_no':randomCaseno, 'patient_firstname':query.patient_firstname, 'patient_secondname' : query.patient_secondname, 'patient_age': query.patient_age, 'patient_gender': query.patient_gender, 'patient_mobile': query.patient_mobile, 'patient_email': query.patient_email, 'patient_civilstatus': query.patient_civilstatus, 'patient_dob': query.patient_dob,'model_prediction':cancer_result})


# ===============================================================================



def funcDoctorList(request):

    cancer_image = request.session.get('cancer_image_session_var')
    doctor_id_fetch = request.POST.get('doctor_id')
    session_patient_id = request.session.get('patient_id_session_var')
    patient_case_no = request.session['patient_case_No_session_var']
    patient_firstname_session = request.session['patient_firstname_session_var']
    patient_email_session = request.session['patient_email_session_var']
    patient_mobile_session = request.session['patient_mobile_session_var']
    query2 = availabledoctors.objects.all()

    if request.method == 'POST':
        doctor_id_fetch = request.POST.get('doctor_id')
        query = patienttodoctor(patient_id = session_patient_id, patient_firstname = patient_firstname_session, patient_email = patient_email_session, patient_mobile = patient_mobile_session, case_no = patient_case_no, doctor_id = doctor_id_fetch)
        query.save()
        query3 = patienttodoctor.objects.filter(case_no =patient_case_no,doctor_id =doctor_id_fetch).first()
        query3.patient_image = cancer_image
        query3.save()
       
        if query3:
            print('passed to database')

        else:
         print('failed')

        if query:
            return redirect('/patient_dashboard/')
        else:
            print("patient to doc failed")

    params = { 'available_doctors_records': query2 ,
              'patient_id': session_patient_id,
              'patient_case_no': patient_case_no}
    
    return render(request, 'doctor_list.html', params)



# ===============================================================================



def funcDeleteRecord(request,case_no):
    Case_no1 = case_no
    query = patient_history.objects.filter(case_no=Case_no1)
    query1 = doctor_remarks.objects.filter(case_no = Case_no1)
    query1.delete()
    query.delete()
    return redirect('/patient_mycase/')


# ===============================================================================



def funcLogin_doctor(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        query = availabledoctors.objects.filter(doctor_email = email, doctor_password = password).first()

        if not query:
            return render(request, 'login-doctor.html', {'error': 'Invalid email or password'})
        else:
            doctor_id = query.id
            doctor_name = query.doctor_name
            doctor_email = query.doctor_email
            request.session['doctor_id_session_var'] = doctor_id
            request.session['doctor_name_session_var'] = doctor_name
            request.session['doctor_email_session_var'] = doctor_email

            return redirect('/doctor_dashboard/')
        
    return render(request, 'login-doctor.html')



# ===============================================================================



def funcDoctor_dashboard(request):

    doctor_id_session = request.session.get('doctor_id_session_var')    
    query = availabledoctors.objects.filter(id = doctor_id_session).first()
    
    doc_respond_query = patienttodoctor.objects.filter(doctor_id = doctor_id_session,doctor_respond='No').count()
    doc_replied_query = patienttodoctor.objects.filter(doctor_id = doctor_id_session,doctor_respond='YES').count()

    print(query.doctor_image)

    return render(request,'doctor_dashboard.html', {'doctor_name': query.doctor_name, 'doctor_email': query.doctor_email, 'doctor_age': query.doctor_age, 'doctor_gender': query.doctor_gender, 'doctor_mobile': query.doctor_mobile, 'doctor_qualification': query.doctor_qualification, 'doctor_jobstatus': query.doctor_jobstatus, 'doctor_image': query.doctor_image ,'doc_respond': doc_respond_query,'doc_replied':doc_replied_query})



# ===============================================================================



def funcDoc_available_cases(request):

    view_history_get = request.POST.get('view_history')
    cancer_image = request.session.get('cancer_image_session_var')

    doctor_id_session = request.session.get('doctor_id_session_var')
    query = patienttodoctor.objects.filter(doctor_id = doctor_id_session).all()

    view_history = patient_history.objects.filter(case_no = view_history_get).all()
    params = {'complete_query':query,'view_history_query':view_history}
        
    if request.method == 'POST':

        return render(request,'doc_available_cases.html',params)
    else:

        return render(request,'doc_available_cases.html',params)
    


# ===============================================================================



def doc_Recommendations(request):

    case_no = request.GET.get('case_no')
    patient_id = request.GET.get('patient')

    # sessions of doctor
    doctor_name = request.session.get('doctor_name_session_var')
    doctor_email = request.session.get('doctor_email_session_var')
    
    params = {'patient_case_no' : case_no,'patient_id':patient_id}

    if request.method == 'POST':
        doctorRemarks = request.POST.get('remarks_area')
        print(doctorRemarks)
        int_case_no = int(case_no)
        query1 = patienttodoctor.objects.filter(case_no = int_case_no).first()
        
        if query1.doctor_respond == "YES":
            query2 = doctor_remarks.objects.filter(case_no = int_case_no).first()
            query2.doctor_remarks = doctorRemarks
            query2.save()
            print("internal if passed")
            return redirect('/doc_available_cases/')

        else:
            query3 =  doctor_remarks(patient_id = patient_id, case_no = int_case_no, doctor_name = doctor_name, doctor_email = doctor_email, doctor_remarks = doctorRemarks)
            query3.save()
            query1.doctor_respond = "YES"
            query1.save()
            print("internal else passed")
            return redirect('/doc_available_cases/')
            
    return render(request,'recommendation.html',params)



# ===============================================================================



def funcDelete_doctorCase(request):

    case_no1 = request.GET.get('case_no')

    query = patienttodoctor.objects.filter(case_no = case_no1)
    query.delete()
    return redirect('/doc_available_cases/')


# ===============================================================================




def funcContact(request):

    return render(request,'contact.html')




# ===============================================================================




def funcAboutus(request):
    return render(request,'aboutus.html')


# ===============================================================================




def funcPatient_logout(request): # to be made separtely for doc and patient
    request.session.flush()
    return redirect('/login-patient/')



 # ===============================================================================




def funcDoctor_logout(request): # to be made separtely for doc and patient
    request.session.flush()
    return redirect('/login-doctor/')



# ===============================================================================



def funcHome_logout(request): # to be made separtely for doc and patient
    request.session.flush()
    return redirect('/home/')


# ===============================================================================

def funcAdmin_logout(request):
    request.session.flush()
    return redirect('/AdminLogin/')

#================================================================================



def funcPrivacy(request):
    return render(request,'privacy_policies.html')
    



# ===============================================================================




def funcFAQ(request):
    return render(request,'faqfooter.html')



# ===============================================================================




def funcTermsOfUse(request):
    return render(request,'termofuse.html')


# ===============================================================================



def Prediction(request):
    return render(request, 'Prediction.html')




# ===============================================================================

def predictImage(request):
    print(request)
    print(request.POST.dict())

    # Ensure the file is uploaded
    if 'filePath' not in request.FILES:
        return HttpResponseBadRequest("No file uploaded.")

    fileObj = request.FILES['filePath']
    fs = FileSystemStorage()
    filePathName = fs.save(fileObj.name, fileObj)  # Save the file
    print(f"File saved as: {filePathName}")  # Debug print

    # Get the full file path to read the image
    file_path_full = fs.path(filePathName)  # Get the actual file path
    print(f"Full path to the image: {file_path_full}")

    # Load the image using OpenCV
    image = cv2.imread(file_path_full, cv2.IMREAD_UNCHANGED)

    # Check if the image was loaded correctly
    if image is None:
        return HttpResponseBadRequest("Failed to load image.")

    # Check if the image has an alpha channel and convert if necessary
    if image.shape[-1] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

    # Resize and preprocess the image
    image = cv2.resize(image, (256, 256))
    img = keras.preprocessing.image.img_to_array(image)
    img = np.expand_dims(img, axis=0)
    img = img.astype('float32') / 255

    preds = model_1.predict(img)[0]
    if preds < 0.5:
        result = class_dict_1[0]
    else:
        result = class_dict_1[1]
        if result == 'Skin':
            filePathName_2 = filePathName
            img = keras.preprocessing.image.img_to_array(image)
            img = np.expand_dims(img, axis=0)
            img = img.astype('float32') / 255
            preds = model_2.predict(img)[0]
            if preds < 0.5:
                result_2 = class_dict_2[0]
            else:
                result_2 = class_dict_2[1]
            return render(request, 'Prediction.html', {
                'filePathName': settings.MEDIA_URL + filePathName,  # Ensure the correct URL is passed
                'filePathName_2': settings.MEDIA_URL + filePathName_2,
                'result': result,
                'result_2': result_2
            })

    context = {
        'filePathName': settings.MEDIA_URL + filePathName,  # Ensure the correct URL is passed
        'result': result
    }
    return render(request, 'Prediction.html', context)

# ===============================================================================


def funcPrediction(request):

    return render(request,'patient_prediction.html')



# ===============================================================================
"""

def predict_patient_Image(request):
    print(request)
    print(request.POST.dict())
    print(request.FILES['filePath'])
    fileObj = request.FILES['filePath']
    fs = FileSystemStorage()
    filePathName=fs.save(fileObj.name,fileObj)
    filePathName = fs.url(filePathName)
    # the following filePathName_2 is there for created if the uploaded image is skin, for
    # benign of malignant display the image in second div in non-skin case image is displayed only in first div
    filePathName_2=fs.save(fileObj.name,fileObj)
    filePathName_2 = fs.url(filePathName_2)
    ImageForPrediction = request.FILES['filePath']
    img = Image.open(ImageForPrediction.file).resize((256, 256))#target_size must agree with what the trained model expects!!
    count = 0

    # Preprocessing the image
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img.astype('float32')/255
   
    preds = model_1.predict(img)[0]
    if preds < 0.5:
        result = class_dict_1[0]
    else:
        result = class_dict_1[1]
        if result == 'Skin':
            ImageForPrediction = request.FILES['filePath']
            img = Image.open(ImageForPrediction.file).resize((256, 256))#target_size must agree with what the trained model expects!!
            # Preprocessing the image
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img = img.astype('float32')/255
            preds = model_2.predict(img)[0]
            if preds < 0.5:
                result_2 = class_dict_2[0]

            else:
                result_2 = class_dict_2[1]
    
            request.session['cancer_result_session_var'] = result_2
            request.session['cancer_image_session_var'] = filePathName_2
            return render(request,'patient_prediction.html', {'filePathName':filePathName,'filePathName_2':filePathName_2,'result':result,'result_2': result_2})



    context ={'filePathName':filePathName, 'result':result}
    return render(request,'patient_prediction.html',context)

"""

def predict_patient_Image(request):
    print(request)
    print(request.POST.dict())
    print(request.FILES['filePath'])
    fileObj = request.FILES['filePath']
    fs = FileSystemStorage()
    filePathName = fs.save(fileObj.name, fileObj)
    filePathName = fs.url(filePathName)

    # Load the image and resize it
    ImageForPrediction = request.FILES['filePath']
    img = Image.open(ImageForPrediction.file).resize((256, 256))  # Resize image

    # Check if image has an alpha channel (RGBA) and convert to RGB
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    # Preprocessing the image
    img_array = keras.preprocessing.image.img_to_array(img)  # Convert to array
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = img_array.astype('float32') / 255  # Normalize

    preds = model_1.predict(img_array)[0]  # Model prediction
    if preds < 0.5:
        result = class_dict_1[0]
    else:
        result = class_dict_1[1]
        if result == 'Skin':
            filePathName_2 = filePathName
            # Reprocess the image for the second model
            img = img.resize((256, 256))  # Resize again if needed
            img_array = keras.preprocessing.image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = img_array.astype('float32') / 255
            preds = model_2.predict(img_array)[0]
            if preds < 0.5:
                result_2 = class_dict_2[0]
            else:
                result_2 = class_dict_2[1]

            # Save results in session
            request.session['cancer_result_session_var'] = result_2
            request.session['cancer_image_session_var'] = filePathName

            return render(request, 'patient_prediction.html', {
                'filePathName': filePathName,
                'filePathName_2' : filePathName_2, 
                'result': result,
                'result_2': result_2
            })

    context = {'filePathName': filePathName, 'result': result}
    return render(request, 'patient_prediction.html', context)
