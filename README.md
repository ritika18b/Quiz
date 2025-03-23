# Quiz App

This is a simple History Quiz App built using Python and Tkinter. The app fetches questions from the Open Trivia Database API and allows users to answer multiple-choice questions. At the end of the quiz, users can enter their name and save their score.

## Features

- Fetches questions from the Open Trivia Database API
- Displays multiple-choice questions
- Allows users to submit answers and move to the next question
- Displays the correct answer after submission
- Saves the user's name and score to a CSV file

## Requirements

- Python 3.x
- Tkinter
- Requests
- Pillow

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/ritika18b/quiz-app.git
    cd quiz-app
    ```

2. Install the required packages:

    ```sh
    pip install requests pillow
    ```

3. Place your background image and icon in the project directory and update the paths in the code:

    ```python
    background_image_path = "background.jpg"  # Replace with your image path
    icon_path = "icon.ico"  # Replace with your icon path
    ```

## Usage

Run the `quiz.py` script to start the Quiz App:

```sh
python [quiz.py]
