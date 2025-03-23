import tkinter as tk
from tkinter import messagebox
import requests
import os
import random
from PIL import Image, ImageTk
import csv

# Open Trivia Database API URL
API_URL = "https://opentdb.com/api.php?amount=5&category=23&type=multiple"

# Background image and icon paths
background_image_path = "background.jpg"  # Replace with your image path
icon_path = "icon.ico"  # Replace with your icon path

# File to store quiz records
record_file = "quiz_records.csv"

def fetch_questions():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return data["results"]
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch questions: {e}")
        return []

def create_file_if_not_exists():
    if not os.path.isfile(record_file):
        with open(record_file, "w", newline="") as csvfile:
            fieldnames = ["Name", "Score"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

def display_question(question_data):
    question_label.config(text=question_data["question"])
    options = question_data["incorrect_answers"] + [question_data["correct_answer"]]
    random.shuffle(options)
    
    global correct_answer
    correct_answer = question_data["correct_answer"]
    
    for i, option in enumerate(options):
        checkbox_vars[i].set(0)
        checkboxes[i].config(text=option, state=tk.NORMAL)

    correct_answer_label.pack_forget()
    submit_button.pack(side=tk.LEFT, padx=10,pady=0)
    next_button.pack_forget()

def select_answer():
    global selected_answer_indices
    selected_answer_indices = [i for i, var in enumerate(checkbox_vars) if var.get() == 1]

def calculate_score(correct_answer, selected_answers, options):
    if correct_answer in [options[i] for i in selected_answers]:
        return 1
    return 0

def save_score(name, score):
    with open(record_file, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Name", "Score"])
        writer.writerow({"Name": name, "Score": score})

def submit_answer():
    global total_score
    if not selected_answer_indices:
        messagebox.showwarning("Warning", "Please select an option before submitting!")
        return
    
    options = [checkbox.cget("text") for checkbox in checkboxes]
    is_correct = calculate_score(correct_answer, selected_answer_indices, options)
    total_score += is_correct
    
    correct_answer_label.config(text=f"Correct answer: {correct_answer}", fg="red")
    correct_answer_label.pack(pady=10)
    
    submit_button.pack_forget()
    next_button.pack(side=tk.LEFT, padx=10,pady=0)

def next_question():
    global question_index, selected_answer_indices
    if question_index < len(questions) - 1:
        question_index += 1
        selected_answer_indices = []
        display_question(questions[question_index])
    else:
        user_details_page()

def user_details_page():
    global name_entry, finish_button
    for widget in window.winfo_children():
        if widget not in [bg_label]:
            widget.pack_forget()

    name_label = tk.Label(window, text="Enter your name:", font=("Arial", 12), bg="white")
    name_label.pack(pady=10)

    name_entry = tk.Entry(window, font=("Arial", 12))
    name_entry.pack(pady=5)

    finish_button = tk.Button(window, text="Finish", command=finish_quiz, font=("Arial", 12), bg="#4CAF50", fg="white", width=15)
    finish_button.pack(pady=20)

def finish_quiz():
    name = name_entry.get()
    if not name:
        messagebox.showwarning("Warning", "Please enter your name!")
        return
    
    save_score(name, total_score)
    for widget in window.winfo_children():
        if widget not in [bg_label]:
            widget.pack_forget()
    
    # Display the score
    score_label.config(text=f"{name}, your score is {total_score}/{len(questions)}", font=("Arial", 14, "bold"), bg="white")
    score_label.pack(pady=200)

window = tk.Tk()
window.title("Quiz App")

if os.path.exists(icon_path):
    window.iconbitmap(icon_path)

if os.path.exists(background_image_path):
    bg_image = Image.open(background_image_path)
    window.geometry(f"{bg_image.width}x{bg_image.height}")
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(window, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

questions = fetch_questions()
if not questions:
    messagebox.showerror("Error", "Failed to fetch questions. Please try again later.")
    window.destroy()

question_index = 0
total_score = 0
selected_answer_indices = []
checkbox_vars = [tk.IntVar() for _ in range(4)]

question_label = tk.Label(window, text="", font=("Arial", 14, "bold"), wraplength=500, bg="white")
question_label.pack(pady=20)

checkbox_frame = tk.Frame(window, bg="white")
checkbox_frame.pack(pady=10)

checkboxes = [tk.Checkbutton(checkbox_frame, text="", variable=checkbox_vars[i], command=select_answer, font=("Arial", 12), bg="white") for i in range(4)]
for checkbox in checkboxes:
    checkbox.pack(fill="x", padx=20, pady=5)

button_frame = tk.Frame(window, bg="white",width=15)
button_frame.pack(pady=20)

submit_button = tk.Button(button_frame, text="Submit", command=submit_answer, font=("Arial", 12), bg="#4CAF50", fg="white", width=15)
submit_button.pack(side=tk.LEFT, padx=10, pady=0)

next_button = tk.Button(button_frame, text="Next", command=next_question, font=("Arial", 12), bg="#2196F3", fg="white", width=15)
next_button.pack_forget()

correct_answer_label = tk.Label(window, text="", font=("Arial", 12), bg="white", fg="red")
correct_answer_label.pack(pady=10)

score_label = tk.Label(window, text="", font=("Arial", 12, "bold"), bg="white")
score_label.pack(pady=20)

display_question(questions[question_index])
window.mainloop()
