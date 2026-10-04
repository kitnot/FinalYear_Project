# Smart Attendance Management System

A web-based **Smart Attendance Management System** built with Python,
Flask, SQLite, OpenCV YuNet, and SFace face recognition.

## Features

-   Student management
-   Add, edit, search, and delete students
-   Import an entire class using CSV/XLSX
-   Batch face registration
-   Multiple face samples per student
-   Continuous webcam-based attendance
-   Multi-frame recognition confirmation
-   Duplicate attendance prevention
-   Admin and staff accounts
-   SQLite database
-   Attendance records and confidence scores
-   Responsive web interface
-   Windows setup script

## Technology Stack

  Component          Technology
  ------------------ -----------------------
  Language           Python
  Backend            Flask
  Database           SQLite
  ORM                Flask-SQLAlchemy
  Authentication     Flask-Login
  Face Detection     OpenCV YuNet
  Face Recognition   OpenCV SFace
  Frontend           HTML, CSS, JavaScript
  Camera             Browser WebRTC

## Project Structure

``` text
SmartAttendance/
├── app.py
├── config.py
├── extensions.py
├── create_admin.py
├── requirements.txt
├── setup.bat
├── backups/
├── face_data/
├── instance/
├── face_engine/
├── models/
├── routes/
├── static/
└── templates/
```

## AI Models

The following model files are required:

``` text
models/yunet/face_detection_yunet_2023mar.onnx
models/sface/face_recognition_sface_2021dec.onnx
```

YuNet is used for face detection and SFace is used for face feature
extraction and comparison.

## Requirements

Recommended:

-   Windows 10 or Windows 11
-   Python 3.11 or 3.12, 64-bit
-   Webcam
-   At least 4 GB RAM

## Installation on a New Windows PC

Install Python 3.11 or 3.12 and enable **Add Python to PATH**.

Copy the complete `SmartAttendance` folder to the new computer.

Then double-click:

``` text
setup.bat
```

The setup script creates the virtual environment, installs
`requirements.txt`, checks important packages and AI models, creates
required folders, and starts the application.

### Manual installation

``` cmd
cd /d "PATH_TO\SmartAttendance"
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python create_admin.py
python app.py
```

Open:

``` text
http://127.0.0.1:5000
```

## Whole-Class Import

The class import feature allows many students to be added at once.

Example CSV:

``` csv
student_id,name,email,phone,course,semester,division
24BIT01,Ahmad,ahmad@example.com,9876543210,BSc IT,VI,Batch 2
24BIT02,Rahul,rahul@example.com,9876543211,BSc IT,VI,Batch 2
24BIT03,Sameer,sameer@example.com,9876543212,BSc IT,VI,Batch 2
```

`student_id` and `name` should be unique/valid. Other fields provide
additional student information.

## Batch Face Registration

1.  Open **Students**.
2.  Choose **Batch Face Registration**.
3.  Select a student.
4.  Start/allow camera access.
5.  Capture the required face samples.
6.  Move to the next student.
7.  Continue until the class is registered.

For better recognition, use good lighting, a clear face, and natural
variations in position.

## Continuous Attendance

Open:

``` text
http://127.0.0.1:5000/attendance/
```

Click **Start Attendance** and allow camera access.

The application continuously sends camera frames to the Flask backend.
Detected faces are compared against registered face embeddings. The
application uses confirmation logic before recording attendance and
prevents duplicate attendance for the same student on the same day.

## Database

The SQLite database is normally stored at:

``` text
instance/smart_attendance.db
```

Backups can be stored in:

``` text
backups/
```

Do not manually modify the database unless you understand the schema.

## User Roles

### Administrator

Administrators can manage application users, roles, and account status.

### Staff

Staff users can perform normal student and attendance operations allowed
by the application.

## Troubleshooting

### Python is not recognized

Run:

``` cmd
python --version
```

or:

``` cmd
py --version
```

Install Python if neither command works.

### Requirements installation fails

Run:

``` cmd
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Keep the complete error output if installation fails.

### AI model not found

Verify:

``` text
models/yunet/face_detection_yunet_2023mar.onnx
models/sface/face_recognition_sface_2021dec.onnx
```

### Camera does not work

Check Windows camera permissions, browser camera permissions, and
whether another application is using the webcam.

### Face is not detected

Improve lighting, move closer to the camera, keep the face unobstructed,
and verify the YuNet model file.

### Recognition is inaccurate

Recognition quality depends on registration samples, lighting, camera
quality, face angle, distance, and the configured recognition threshold.
Re-registering faces with better samples can help.

## Security and Privacy

This system processes facial biometric information. Before real-world
deployment:

-   Obtain appropriate consent and authorization.
-   Restrict access to authorized users.
-   Protect the database and face embeddings.
-   Keep backups secure.
-   Do not expose the Flask development server directly to the public
    internet.
-   Define appropriate data retention and deletion policies.
-   Follow applicable privacy and data-protection requirements.

The current multi-frame confirmation mechanism is **not a certified
anti-spoofing/liveness system**. Stronger protection requires a
validated liveness/anti-spoofing model or suitable depth/IR hardware.

## Current Development Status

Implemented:

-   [x] Flask application
-   [x] Login
-   [x] Admin controls
-   [x] Student management
-   [x] Whole-class import
-   [x] Batch face registration
-   [x] YuNet face detection
-   [x] SFace face recognition
-   [x] Continuous attendance
-   [x] Multi-frame confirmation
-   [x] Duplicate attendance prevention
-   [x] Responsive UI
-   [x] Windows setup script

Future improvements:

-   [ ] Stronger liveness/anti-spoofing
-   [ ] In-memory face embedding cache
-   [ ] Per-session recognition state
-   [ ] Automatic scheduled backups
-   [ ] Advanced reports/export
-   [ ] Final PyInstaller Windows executable
-   [ ] Installer package

## Quick Start

For a new Windows computer:

``` text
Install Python
      ↓
Copy SmartAttendance
      ↓
Double-click setup.bat
      ↓
Create administrator account
      ↓
Import class
      ↓
Register faces
      ↓
Start Attendance
```

Application:

``` text
http://127.0.0.1:5000
```

## License

This project is intended for educational and institutional use. Before
commercial distribution, verify the licenses of all third-party
packages, OpenCV components, and model files used by the project.

## Project Information

**Project:** Smart Attendance Management System\
**Platform:** Windows / Local Web Application\
**Backend:** Python + Flask\
**Database:** SQLite\
**Computer Vision:** OpenCV YuNet + SFace
