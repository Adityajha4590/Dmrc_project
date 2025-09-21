# Metro Face Recognition System 🚇

A Python-based desktop application that simulates a metro station face recognition system for passenger registration and journey management. This system includes features like passenger registration, live webcam capture of images/faces, balance management, and voice notifications for journey actions.

---

## Features

- **Passenger Registration**  
  - Register new passengers with Name, ID, and initial Balance.
  - Capture **full image** or **face image** via webcam.
  - Preview captured images before saving.
  - Duplicate Passenger ID validation.

- **Journey Management**  
  - Start a journey using Passenger ID.
  - Automatic fare deduction from balance.
  - Voice notification for journey start and gate entry.
  - Insufficient balance alerts.

- **Database Handling**  
  - Passenger data is saved in an Excel file (`passenger_database.xlsx`).
  - Data includes Name, ID, Balance, and Photo path.

- **Modern & Interactive UI**  
  - Colorful and attractive 3D-like cards.
  - Gradient headers and shadowed buttons.
  - Live video feed integrated in the registration and journey tabs.

---

## Installation

1. **Clone this repository:**

```bash
git clone <repository-url>
cd Metro-Face-Recognition-System


**2. Install required Python packages:**
pip install opencv-python pandas pillow pyttsx3

**3. Run the application:**
python gui.py

Usage
**Register a Passenger**
Go to Register Passenger tab.
Enter Name, ID, and Balance.
Use Capture Image to take a full image.
Use Capture Face to take a face-only photo.
Click Register Passenger to save the data.

**Start a Journey**
Go to Start Journey tab.
Enter your Passenger ID.
Click Start Journey to deduct fare and simulate gate entry.
Voice notification will confirm the journey.

**Directory Structure**
Metro-Face-Recognition-System/
│
├─ gui.py                  # Main application script
├─ passenger_database.xlsx  # Excel database (auto-generated)
├─ photos/                 # Folder to store captured images
└─ README.md               # Project documentation

**Dependencies**
Python 3.x
OpenCV (opencv-python)
pandas
Pillow (PIL)
pyttsx3

**Install via pip:**
pip install opencv-python pandas pillow pyttsx3

Screenshots
<img width="1918" height="1078" alt="image" src="https://github.com/user-attachments/assets/19407292-12b8-4af5-8416-4c37a4539f42" />
<img width="1918" height="1078" alt="image" src="https://github.com/user-attachments/assets/1c84f284-ac57-47d7-9483-1a2de8b30773" />

