import tkinter as tk
import time
from tkinter import ttk
import csv
import random


def get_word_list():
    global word_list
    words_label.config(text="")
    with open("words.csv", newline="") as csvfile:
        lines = csv.reader(csvfile)
        words = [word[0] for word in lines]
    word_list = random.sample(words, 100)
    word_para = " ".join(word_list)
    words_label.config(text=word_para)


def find_wpm():
    type_text = input_text.get("1.0", 'end-1c')
    type_text_words = type_text.split(" ")
    filtered_words = [word for word in type_text_words if word and word in word_list]
    words_no = len(filtered_words)
    wpm_label.config(text=f"Your WPM is {words_no}. Click Start to try again.")


def reset_textbox():
    input_text.config(state=tk.NORMAL)
    input_text.delete('1.0', tk.END)
    input_text.focus()


def check_time_elapsed():
    current_time = time.monotonic()  # Get current time in seconds since an unspecified time
    elapsed_seconds = current_time - start_time

    # Check if at least 60 seconds (1 minute) have passed
    if elapsed_seconds >= 60:
        input_text.config(state=tk.DISABLED)  # Disable the entry widget
        find_wpm()
        root.after(60000, reset_textbox)  # after 60 seconds
    else:
        # Reschedule to check again after a short interval (e.g., 1000 ms = 1 second)
        root.after(1000, check_time_elapsed)


def start_timer():
    global start_time
    get_word_list()
    reset_textbox()
    start_time = time.monotonic()
    check_time_elapsed()


# Create the main window
root = tk.Tk()
root.title("Typing Speed Test")
# root.geometry()

outer_padding = 30
main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, padx=outer_padding, pady=outer_padding)

# Create a label for the title
title_label = tk.Label(main_frame, text="Typing Speed Test", font=("Arial", 24))
title_label.pack(pady=20)

# Create a label to display the words
words_label = tk.Label(main_frame, width=80, text="Words to type will appear here. Click 'Start' button to begin.", wraplength=800, font=("Arial", 14),
                       relief="sunken", height=12)
words_label.pack(pady=5, padx=5)  # , fill='x'

# Create a text box for typing input
input_text = tk.Text(main_frame, height=5, wrap='word', font=("Arial", 14))
input_text.pack(pady=20, padx=20, fill='x')

wpm_label = tk.Label(main_frame, text="", font=("Arial", 12))
wpm_label.pack(pady=20)

# Create a button to start the test
start_button = ttk.Button(main_frame, text="Start", command=start_timer)
start_button.pack(pady=20)

# Start the main event loop
root.mainloop()
