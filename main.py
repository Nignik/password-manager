from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# Colors
BLACK = "#0D0208"
BLUE = "#150050"
PURPLE = "#3F0071"
PINK = "#FB2576"
MATRIX = "#008F11"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_symbols + password_numbers + password_letters
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SEARCH FOR PASSWORD ------------------------------- #
def search():

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="You haven't created any entries yet.")

    else:
        try:
            passwd = data[website_entry.get()]["password"]

        except KeyError:
            messagebox.showinfo(title="Oops", message="You don't have any information saved for that site.")

        else:
            password_entry.insert(0, f"{passwd}")

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")

    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} \nPassword: {password}\nIs it ok to save")

        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)

            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=BLACK)

canvas = Canvas(height=200, width=200, bg=BLACK, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:", bg=BLACK, fg=MATRIX)
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:", bg=BLACK, fg=MATRIX)
email_label.grid(row=2, column=0)

password_label = Label(text="Password:", bg=BLACK, fg=MATRIX)
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=34)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=53)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "maksymilian.olbrys@gmail.com")

password_entry = Entry(width=34)
password_entry.grid(row=3, column=1)

# Buttons
search_button = Button(text="Search",width=14, bg=BLACK, fg=MATRIX, command=search)
search_button.grid(row=1, column=2, columnspan=2)

generate_password_button = Button(text="Generate Password", bg=BLACK, fg=MATRIX, command=generate_password)
generate_password_button.config(highlightbackground=MATRIX, highlightcolor=MATRIX)
generate_password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=45, bg=BLACK, fg=MATRIX, highlightthickness=2, command=save)
add_button.config(highlightbackground=MATRIX, highlightcolor=MATRIX)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
