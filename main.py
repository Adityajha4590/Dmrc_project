import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import pandas as pd
import os
import pyttsx3

DATABASE_FILE = "passenger_database.xlsx"
FARE = 10
engine = pyttsx3.init()

# Load database
if os.path.exists(DATABASE_FILE):
    passenger_df = pd.read_excel(DATABASE_FILE, dtype={"ID": str})
    passenger_df = passenger_df[["Name", "ID", "Balance", "Photo"]]
else:
    passenger_df = pd.DataFrame(columns=["Name", "ID", "Balance", "Photo"])
    passenger_df.to_excel(DATABASE_FILE, index=False)

def save_database():
    passenger_df.to_excel(DATABASE_FILE, index=False)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def register_passenger(name, pid, balance, photo_path):
    global passenger_df
    if not name or not pid or not balance:
        messagebox.showerror("Error", "All fields are required!")
        return False
    pid = str(pid).strip()
    if pid in passenger_df["ID"].values:
        messagebox.showerror("Error", "Passenger ID already exists!")
        return False
    photo_path = photo_path if photo_path else ""
    new_row = {"Name": name, "ID": pid, "Balance": balance, "Photo": photo_path}
    passenger_df = pd.concat([passenger_df, pd.DataFrame([new_row])], ignore_index=True)
    save_database()
    messagebox.showinfo("Success", f"Passenger {name} registered successfully!")
    speak(f"Passenger {name} registered successfully")
    return True

class MetroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚇 Metro Face Recognition System")
        self.root.geometry("1200x800")
        self.root.configure(bg="#e0f7fa")

        self.cap = cv2.VideoCapture(0)
        self.captured_photo = None
        self.face_captured = None

        # Header
        header = tk.Label(root, text="Metro Face Recognition System",
                          font=("Segoe UI", 28, "bold"),
                          bg="#ff6a00", fg="white", pady=20)
        header.pack(fill="x")

        # Notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)

        # Tabs
        self.create_registration_tab()
        self.create_journey_tab()

        self.update_video_feed()

    def create_registration_tab(self):
        frame = tk.Frame(self.notebook, bg="#e0f7fa")
        self.notebook.add(frame, text="🆕 Register Passenger")

        card = tk.Frame(frame, bg="#fff9c4", bd=2, relief="groove")
        card.pack(pady=20, padx=20, fill="x")

        tk.Label(card, text="Register New Passenger", font=("Segoe UI", 22, "bold"),
                 bg="#fff9c4", fg="#2c3e50").pack(pady=10)

        # Form
        form_frame = tk.Frame(card, bg="#fff9c4")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Name:", bg="#fff9c4", font=("Segoe UI", 13)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.name_entry = ttk.Entry(form_frame, width=35)
        self.name_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="ID:", bg="#fff9c4", font=("Segoe UI", 13)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.id_entry = ttk.Entry(form_frame, width=35)
        self.id_entry.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Balance:", bg="#fff9c4", font=("Segoe UI", 13)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.balance_entry = ttk.Entry(form_frame, width=35)
        self.balance_entry.grid(row=2, column=1, pady=5)

        # Video feed
        self.video_label = tk.Label(card, bg="#b2ebf2", width=600, height=300, relief="ridge", bd=3)
        self.video_label.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(card, bg="#fff9c4")
        btn_frame.pack(pady=10)

        self.capture_image_btn = tk.Button(btn_frame, text="📸 Capture Image", bg="#ff7043", fg="white",
                                           font=("Segoe UI", 12, "bold"), relief="raised", padx=20, pady=10,
                                           command=self.capture_image)
        self.capture_image_btn.grid(row=0, column=0, padx=10)

        self.capture_face_btn = tk.Button(btn_frame, text="🟢 Capture Face", bg="#66bb6a", fg="white",
                                          font=("Segoe UI", 12, "bold"), relief="raised", padx=20, pady=10,
                                          command=self.capture_face)
        self.capture_face_btn.grid(row=0, column=1, padx=10)

        self.register_btn = tk.Button(btn_frame, text="✅ Register Passenger", bg="#29b6f6", fg="white",
                                      font=("Segoe UI", 12, "bold"), relief="raised", padx=20, pady=10,
                                      command=self.register_passenger_action)
        self.register_btn.grid(row=0, column=2, padx=10)

        # Preview
        self.preview_label = tk.Label(card, bg="#e1f5fe", width=200, height=200, relief="sunken", bd=3)
        self.preview_label.pack(pady=10)

    def create_journey_tab(self):
        frame = tk.Frame(self.notebook, bg="#e0f7fa")
        self.notebook.add(frame, text="🚇 Start Journey")
        card = tk.Frame(frame, bg="#c8e6c9", bd=2, relief="groove")
        card.pack(pady=20, padx=20, fill="x")
        tk.Label(card, text="Start Metro Journey", font=("Segoe UI", 22, "bold"),
                 bg="#c8e6c9", fg="#2c3e50").pack(pady=10)
        self.journey_video_label = tk.Label(card, bg="#b2dfdb", width=600, height=300, relief="ridge", bd=3)
        self.journey_video_label.pack(pady=10)
        tk.Label(card, text="Enter your Passenger ID:", bg="#c8e6c9", font=("Segoe UI", 13)).pack(pady=5)
        self.journey_id_entry = ttk.Entry(card, width=30)
        self.journey_id_entry.pack(pady=5)
        tk.Button(card, text="▶ Start Journey", bg="#26a69a", fg="white",
                  font=("Segoe UI", 13, "bold"), relief="raised", padx=20, pady=10,
                  command=self.start_journey).pack(pady=10)

    # ================== VIDEO FEED ==================
    def update_video_feed(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame).resize((600, 300))
            imgtk = ImageTk.PhotoImage(img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            self.journey_video_label.imgtk = imgtk
            self.journey_video_label.configure(image=imgtk)
        self.root.after(30, self.update_video_feed)

    # ================== ACTIONS ==================
    def capture_image(self):
        ret, frame = self.cap.read()
        if not ret: messagebox.showerror("Error","Camera error"); return
        pid = str(self.id_entry.get()).strip()
        if not pid: messagebox.showerror("Error","Enter Passenger ID!"); return
        os.makedirs("photos", exist_ok=True)
        filename = os.path.join("photos", f"{pid}_full.jpg")
        cv2.imwrite(filename, frame)
        self.captured_photo = filename
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).resize((200,200))
        self.preview_label.imgtk = ImageTk.PhotoImage(img)
        self.preview_label.configure(image=self.preview_label.imgtk)
        messagebox.showinfo("Success", f"Full Image Captured: {filename}")

    def capture_face(self):
        ret, frame = self.cap.read()
        if not ret: messagebox.showerror("Error","Camera error"); return
        pid = str(self.id_entry.get()).strip()
        if not pid: messagebox.showerror("Error","Enter Passenger ID!"); return
        os.makedirs("photos", exist_ok=True)
        filename = os.path.join("photos", f"{pid}_face.jpg")
        cv2.imwrite(filename, frame)
        self.face_captured = filename
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).resize((200,200))
        self.preview_label.imgtk = ImageTk.PhotoImage(img)
        self.preview_label.configure(image=self.preview_label.imgtk)
        messagebox.showinfo("Success", f"Face Image Captured: {filename}")

    def register_passenger_action(self):
        name = self.name_entry.get().strip()
        pid = str(self.id_entry.get()).strip()
        bal = self.balance_entry.get().strip()
        photo = self.face_captured if self.face_captured else self.captured_photo
        if register_passenger(name,pid,bal,photo):
            self.name_entry.delete(0,"end")
            self.id_entry.delete(0,"end")
            self.balance_entry.delete(0,"end")
            self.preview_label.configure(image="")
            self.captured_photo = None
            self.face_captured = None

    def start_journey(self):
        pid = str(self.journey_id_entry.get()).strip()
        if not pid: messagebox.showerror("Error","Enter your Passenger ID!"); return
        passenger = passenger_df[passenger_df["ID"]==pid]
        if passenger.empty: messagebox.showerror("Error","Passenger ID not found!"); return
        balance = float(passenger.iloc[0]["Balance"])
        if balance<FARE: messagebox.showerror("Error","Insufficient balance!"); speak("Insufficient balance"); return
        passenger_df.loc[passenger_df["ID"]==pid,"Balance"]=balance-FARE
        save_database()
        speak(f"Entry gate opened. Fare deducted {FARE}")
        messagebox.showinfo("Journey", f"Journey started!\nFare deducted: {FARE}\nRemaining balance: {balance-FARE}")

if __name__=="__main__":
    root=tk.Tk()
    app=MetroApp(root)
    root.mainloop()
