
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

answers = (2, 3, 1, 1)
record="record.txt"

def display_question(question, options):
    print("--------------------")
    print(question)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print()

def user_choice():
    choice = input("Enter your choice (1-4): ")
    if choice.isdigit() and 1 <= int(choice) <= 4:
        return int(choice)
    else:
        print("Invalid choice. Please enter a number from 1 to 4.")
        return user_choice()

def calculate_score(answers, user_answers):
    score = 0
    for answer, user_answer in zip(answers, user_answers):
        if answer == user_answer:
            score += 1
    return score

def save_score(name,score):
    with open(record, "a") as file:
        file.write(f"{name}: {score}/{len(answers)}\n") 
    

def run_quiz(questions, options, answers):
    user_answers = []
    
    name = input("Enter your name: ")
    
    for question, option in zip(questions, options):
        display_question(question, option)
        choice = user_choice()
        user_answers.append(choice)
    
    score = calculate_score(answers, user_answers)
    print(f"Quiz ended. Your score: {score}/{len(answers)}")
    
    save_score(name,score)
    
run_quiz(questions, options, answers)
