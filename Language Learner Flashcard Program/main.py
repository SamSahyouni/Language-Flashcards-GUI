from tkinter import *
import random
import pandas
import pyarrow

BACKGROUND_COLOR = '#B1DDC6'
# --------- creating new flash cards ------------ #
try:
    data_file = pandas.read_csv('updated_words_to_learn.csv')
except FileNotFoundError:
    data_file = pandas.read_csv('data/spanish most frequent words - Sheet1.csv')
words_to_learn = data_file.to_dict(orient='records')
current_card= {}

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(words_to_learn)
    spanish_word = current_card['Spanish']
    canvas.itemconfig(card_title, text='Spanish',fill='black')
    canvas.itemconfig(card_word,text=spanish_word,fill='black')
    canvas.itemconfig(card_image,image=card_front)
    flip_timer = window.after(3000, func=flip_card)

def correct_next_card():
    words_to_learn.remove(current_card)
    words_dict = pandas.DataFrame(words_to_learn)
    words_dict.to_csv('data/updated_words_to_learn.csv',index=False)
    next_card()

def flip_card():
    global current_card
    english_word = current_card['English']
    canvas.itemconfig(card_title,text='English',fill='white')
    canvas.itemconfig(card_image,image=card_back)
    canvas.itemconfig(card_word,text=f'{english_word}',fill='white')

# ------- UI -------- #
window = Tk()
window.title("Flashcards")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# flashcard canvas
canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file='images\card_front.png')
card_back = PhotoImage(file='images\card_back.png')
card_image = canvas.create_image(400, 263, image=card_front)
# title label
card_title = canvas.create_text(400, 150, text="Language", font=("Ariel", 40, "italic"))
# word label
card_word = canvas.create_text(400, 263, text='Word', font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

# correct/incorrect buttons
correct_image = PhotoImage(file='images/right.png')
correct_button = Button(image=correct_image, highlightthickness=0,command= correct_next_card)
correct_button.grid(column=1, row=1)
incorrect_image = PhotoImage(file='images/wrong.png')
incorrect_button = Button(image=incorrect_image, highlightthickness=0,command=next_card)
incorrect_button.grid(column=0, row=1)

next_card()

window.mainloop()