import pandas as pd
import random
from tkinter import *

# ---------------------------- FUNCTIONS ------------------------------- #
def next_card():
	global current_card, flip_timer
	window.after_cancel(flip_timer)
	current_card = random.choice(to_learn)
	canvas.itemconfig(title_text, text = "French", fill = "black")
	canvas.itemconfig(word_text, text = f"{current_card["French"]}", fill = "black")
	canvas.itemconfig(back_ground_img, image = card_front_img)
	flip_timer = window.after(3000, func = flip_card)

def flip_card():
	canvas.itemconfig(title_text, text = "English", fill = "white")
	canvas.itemconfig(word_text, text = f"{current_card["English"]}", fill = "white")
	canvas.itemconfig(back_ground_img, image = card_back_img)

def is_known():
	to_learn.remove(current_card)
	words_to_learn = pd.DataFrame(to_learn)
	words_to_learn.to_csv("data/words_to_learn.csv", index = False)
	next_card()

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_STYLE = ("Ariel", 40, "italic")
WORD_STYLE = ("Ariel", 60, "bold")
current_card = {}
to_learn = {}

# ---------------------------- DATAFRAME SETUP ------------------------------- #
try:
	df = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
	original_data = pd.read_csv("data/french_words.csv")
	to_learn = original_data.to_dict(orient = "records")
else:
	to_learn = df.to_dict(orient = "records")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx = 50, pady = 50, bg = BACKGROUND_COLOR)
flip_timer = window.after(3000, func = flip_card)

# ------ BACKGROUND SETUP --------- #
canvas = Canvas(width = 800, height = 526, highlightthickness = 0, bg = BACKGROUND_COLOR)
card_front_img = PhotoImage(file = "images/card_front.png")
card_back_img = PhotoImage(file = "images/card_back.png")
back_ground_img = canvas.create_image(400, 263, image = card_front_img)

# ------ TEXT SETUP --------- #
title_text = canvas.create_text(400, 150, text = f"", font = LANGUAGE_STYLE)
word_text = canvas.create_text(400, 263, text = f"", font = WORD_STYLE)
canvas.grid(column = 0, row = 0, columnspan = 2)

# ------ BUTTON SETUP --------- #
correct_answer_img = PhotoImage(file = "images/right.png")
correct_answer_btn = Button(image = correct_answer_img, highlightthickness = 0, borderwidth = 0, command = is_known)
correct_answer_btn.grid(column = 1, row = 1)

wrong_answer_img = PhotoImage(file = "images/wrong.png")
wrong_answer_btn = Button(image = wrong_answer_img, highlightthickness = 0, borderwidth = 0, command = next_card)
wrong_answer_btn.grid(column = 0, row = 1)


next_card()
window.mainloop()