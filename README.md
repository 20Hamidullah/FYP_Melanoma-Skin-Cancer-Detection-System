# 🩺 Skin Cancer Detection and Classification System Using Deep Learning

### COMSATS University Islamabad – Abbottabad Campus  
**Authors:** Sayed Hamidullah (CIIT/FA19-BCS-129/ATD), Hammad Khalil (CIIT/FA19-BCS-059/ATD)  
**Supervisor:** Muhammad Mateen Yaqoob  

---

## 📘 Overview

**Skin Cancer Detection and Classification System Using Deep Learning** is a final-year BSCS project that utilizes **Convolutional Neural Networks (CNN)** and **Transfer Learning (VGG16)** to detect and classify melanoma skin cancer as *benign* or *malignant* from dermoscopic images.

This system aims to:
- Improve early diagnosis of melanoma.
- Minimize human error in detection.
- Reduce unnecessary biopsies.
- Provide a clinical workflow where a **dermatologist module** verifies AI predictions and adds recommendations.

---

## 🚀 Features

- **Dual Deep Learning Models**:
  - Custom CNN model (83% accuracy).
  - Transfer Learning model (VGG16 – 85% accuracy).

- **Web Application (Django)**:
  - Patient, Doctor, and Admin dashboards.
  - Secure authentication and case management.
  - Real-time image upload and prediction.
  - Doctor verification and feedback interface.

- **Automated Classification**:
  - Detects whether uploaded image is a valid skin lesion.
  - Classifies lesion as *benign* or *malignant*.
  - Stores case results in database for doctor review.

---

## 🧠 Methodology

### 1. Data
- Dataset: **13,141 dermoscopic images** (Benign & Malignant)
- Sources: ISIC, SIIM-ISIC Melanoma Classification, Kaggle datasets
- Augmentation: Rotation, flipping, and normalization

### 2. Models
- **CNN Model:** Built from scratch using TensorFlow/Keras.
- **VGG16 Model:** Transfer Learning with fine-tuned fully connected layers.

### 3. Workflow
1. Patient uploads an image.
2. Model 1 verifies if the image is a valid skin lesion.
3. Model 2 predicts the stage (*Benign/Malignant*).
4. Case is sent to a doctor for confirmation and recommendation.

---

## 🧩 System Architecture

**Frontend:** HTML, CSS, Bootstrap  
**Backend:** Django Framework (Python)  
**Database:** SQLite  
**Deep Learning Libraries:** TensorFlow, Keras, NumPy, OpenCV  
**Deployment Platform:** Localhost / PythonAnywhere  

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/<yourusername>/skin-cancer-detection.git
cd skin-cancer-detection
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # for Linux/Mac
venv\Scripts\activate      # for Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Launch the Server
```bash
python manage.py runserver
```
Open the project in your browser at: [http://localhost:8000](http://localhost:8000)

---

## 📂 Project Structure

```
├── models/
│   ├── cnn_model.h5
│   ├── vgg16_model.h5
├── static/
│   ├── css/
│   └── images/
├── templates/
│   ├── home.html
│   ├── login.html
│   └── dashboard.html
├── melanoma/
│   ├── views.py
│   ├── urls.py
│   └── models.py
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🧪 Testing

- **Manual testing:** All web pages and model integration verified.
- **Unit testing:** Each Django component and model module tested independently.
- **Functional testing:** End-to-end workflow tested for both Patient and Doctor modules.

Example test case:

| Step | Input | Expected Output | Result |
|------|--------|----------------|--------|
| 1 | Upload skin image (.jpg/.png) | Model verifies & classifies | ✅ Pass |
| 2 | Upload non-skin image | Rejected by validation model | ✅ Pass |

---

## 📈 Results

| Model | Accuracy | Dataset Size |
|--------|-----------|--------------|
| CNN | 83% | 13,141 |
| VGG16 | 85% | 13,141 |

The integrated doctor verification module further improves diagnostic reliability.

---

## 🔮 Future Work

- Improve prediction accuracy using hybrid ensemble models.  
- Integrate IoT-based real-time lesion monitoring.  
- Deploy as a scalable web API for medical institutions.  
- Expand dataset to include other types of skin cancer (Basal & Squamous Cell Carcinoma).

---

## 📜 License

This project was developed as part of the **Bachelor of Science in Computer Science (2019-2023)** degree at **COMSATS University Islamabad, Abbottabad Campus**.  
All rights reserved © 2023 by the authors.

---

## 💬 Contact

For research collaboration or technical inquiries:

**Sayed Hamidullah**  
📧 [11hamidullah@gmail.com]  
 

---

> “Early detection saves lives — empowering dermatology through deep learning.”
