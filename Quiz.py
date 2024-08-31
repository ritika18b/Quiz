import tkinter as tk
from tkinter import messagebox
import csv
import os

background_image_path = "quiz_background.jpg"
# Questions, options, and answers
questions = (
    "What is the capital of India?",
    "Which country is famous for the Taj Mahal?",
    "Which planet is known as the Red Planet?",
    "Who wrote the play 'Romeo and Juliet'?",
)

options = (
    ("Paris", "New Delhi", "Japan", "Berlin"),
    ("America", "China", "India", "France"),
    ("Mars", "Jupiter", "Venus", "Saturn"),
    ("William Shakespeare", "George Bernard Shaw", "Oscar Wilde", "Jane Austen"),
)

answers = (1, 2, 0, 0)  # Correct option indices
record_file = "quiz_records.csv"

def create_file_if_not_exists():
    if not os.path.isfile(record_file):
        with open(record_file, "w", newline="") as csvfile:
            fieldnames = ["Name", "Score"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

def display_question(question, options):
    question_label.config(text=question)
    for i, option in enumerate(options):
        radio_buttons[i].config(text=option)
    selected_option_var.set(-1)  # Reset the selected option

def user_choice():
    selected_option = selected_option_var.get()
    return selected_option

def calculate_score(answers, user_answers):
    score = 0
    for answer, user_answer in zip(answers, user_answers):
        if answer == user_answer:
            score += 1
    return score

def save_score(name, score):
    with open(record_file, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["Name", "Score"])
        writer.writerow({"Name": name, "Score": score})

def submit_answer():
    user_answer = user_choice()
    if user_answer == -1:
        messagebox.showwarning("Warning", "Please select an option before submitting!")
        return

    user_answers.append(user_answer)
    
    global question_index
    if question_index < len(questions) - 1:
        question_index += 1
        display_question(questions[question_index], options[question_index])
    else:
        score = calculate_score(answers, user_answers)
        save_score(name_entry.get(), score)
        submit_button.config(state=tk.DISABLED)
        show_score_button.pack(pady=10)  # Show the "Show Score" button
        restart_button.pack(pady=10)  # Show the restart button

def restart_quiz():
    global question_index, user_answers
    question_index = 0
    user_answers = []
    submit_button.config(state=tk.NORMAL)
    restart_button.pack_forget()  
    show_score_button.pack_forget()  
    display_question(questions[question_index], options[question_index])

def show_score():
    score = calculate_score(answers, user_answers)
    score_window = tk.Toplevel(window)
    score_window.title("Your Score")
    score_window.geometry("300x150")
    score_window.configure(bg="#f0f0f0")

    score_label = tk.Label(score_window, text=f"{name_entry.get()}, your score is {score}/{len(answers)}", bg="#f0f0f0", font=("Arial", 14, "bold"))
    score_label.pack(pady=20)

    close_button = tk.Button(score_window, text="Close", command=score_window.destroy, font=("Arial", 12), bg="#2196F3", fg="white")
    close_button.pack(pady=10)

# Create the main window
window = tk.Tk()
window.title("Quiz App")
window.geometry("400x300")
window.configure(bg="#f0f0f0")

# Initialize variables
selected_option_var = tk.IntVar()  # Initialize before creating radio buttons
selected_option_var.set(-1)  # Ensure no option is selected by default
user_answers = []
question_index = 0

# Create and place widgets
name_label = tk.Label(window, text="Enter your name:", bg="#f0f0f0", font=("Arial", 12))
name_label.pack(pady=10)

name_entry = tk.Entry(window, font=("Arial", 12))
name_entry.pack(pady=5)

question_label = tk.Label(window, text="", bg="#f0f0f0", font=("Arial", 14, "bold"))
question_label.pack(pady=20)

radio_frame = tk.Frame(window, bg="#f0f0f0")
radio_frame.pack(pady=10)

radio_buttons = [tk.Radiobutton(radio_frame, text="", variable=selected_option_var, value=i, font=("Arial", 12), bg="#f0f0f0", anchor="w") for i in range(4)]
for radio_button in radio_buttons:
    radio_button.pack(fill="x", padx=20, pady=2)

submit_button = tk.Button(window, text="Submit", command=submit_answer, font=("Arial", 12), bg="#4CAF50", fg="white", width=15)
submit_button.pack(pady=20)

restart_button = tk.Button(window, text="Restart Quiz", command=restart_quiz, font=("Arial", 12), bg="#2196F3", fg="white", width=15)
restart_button.pack_forget()  

show_score_button = tk.Button(window, text="Show Score", command=show_score, font=("Arial", 12), bg="#FF5722", fg="white", width=15)
show_score_button.pack_forget()  

create_file_if_not_exists()
display_question(questions[question_index], options[question_index])


window.mainloop()
