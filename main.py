from tkinter import *
import pandas
from random import choice
from PIL import Image, ImageTk

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    df = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_df = pandas.read_csv("data/french_words.csv")
    to_learn = original_df.to_dict(orient="records")
else:
    to_learn = df.to_dict(orient="records")


# ---------------------------- PROGRAM LOGIC ------------------------------- #
def next_card():
    global current_card, delay
    window.after_cancel(delay)
    current_card = choice(to_learn)
    canvas.itemconfig(lang_title, text="French", fill="black")
    canvas.itemconfig(lang_word, text=current_card["French"], fill="black")
    canvas.itemconfig(canvas_img, image=front_img)
    delay = window.after(3000, func=flip_card)


def flip_card():
    """PhotoImage objects should not be created inside a function. Otherwise, it will not work."""
    canvas.itemconfig(lang_title, text="English", fill="white")
    canvas.itemconfig(lang_word, text=current_card["English"], fill="white")
    canvas.itemconfig(canvas_img, image=back_img)


def is_known():
    to_learn.remove(current_card)
    df = pandas.DataFrame(to_learn)
    df.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Language Learning Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

delay = window.after(3000, func=flip_card)

# Icon setup
ico = Image.open("images/icon.png")
photo = ImageTk.PhotoImage(ico)
window.wm_iconphoto(False, photo)

# Buttons
unknown_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=unknown_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

known_image = PhotoImage(file="images/right.png")
known_button = Button(image=known_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

# Front Side: Flash Card Canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
canvas_img = canvas.create_image(400, 263, image=front_img)
lang_title = canvas.create_text(400, 150, text="", fill="black", font=("Arial", 40, "italic"))
lang_word = canvas.create_text(400, 263, text="", fill="black", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)


next_card()


window.mainloop()
