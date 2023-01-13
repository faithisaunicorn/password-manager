from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

FONT_NAME = "Courier"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','0', '1', '2', '3', '4', '5', '6', '7', '8', '9','!', '#', '$', '%', '&', '(', ')', '*', '+']

def generate_pw():
    global chars
    global pw_output
    pw_output.delete('0',END)
    password = []
    for char in range(1, 13):
        password.append(random.choice(chars))
    random.shuffle(password)
    pw_string = ''.join(password)
    pw_output.insert('0',pw_string)
    pyperclip.copy(pw_string)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_acc():
    retrieve_website = website_name.get()
    retrieve_email = email_entry.get()
    retrieve_password = pw_output.get()

    new_data = {
        retrieve_website: {
            "email": retrieve_email,
            "password": retrieve_password,
        }
    }

    if len(retrieve_website) == 0 or len(retrieve_email) == 0 or len(retrieve_password) == 0:
        messagebox.showinfo(title = "Oops!", message = "Please don't leave any fields empty")
    else:
        ###Let user verify if input is correct before saving
        is_ok = messagebox.askokcancel(title=retrieve_website, message = f"These are the details entered:\nUsername/Email: {retrieve_email} \n PW: {retrieve_password} \n Would you like to save it?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file) #Reading old data
            except FileNotFoundError: #if there's no json file created yet, this exception catches it
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent = 4) #Saving new data
            else:
                data.update(new_data) #Updating old data
                with open("data.json","w") as data_file:
                    json.dump(data,data_file,indent=4) #Saving updated data
            finally:
                website_name.delete(0,END)
                pw_output.delete(0,END)

# ---------------------------- SEARCH ------------------------------- #
def search():
    find_website = website_name.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            messagebox.showinfo(title = "Search Results", message = f"Email: {data[find_website]['email']}\n Password: {data[find_website]['password']}")
    except KeyError:
        messagebox.showinfo(title = "Error!", message = "Sorry, we can't find that website!")
    except FileNotFoundError:
        messagebox.showinfo(title = "Error!", message = "Sorry, we can't find the data file!")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx = 20, pady = 20)

###Canvas is the lock pic
canvas = Canvas(width=200, height=200)
lock_pic = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_pic)
canvas.grid(column=2, row=1)

#The labels
website = Label(text= "Website:", width=18, height=2)
website.grid(row=2, column=1)
email = Label(text= "Emails/Username:", width=20, height=2)
email.grid(row=3, column=1)
pw = Label(text= "Password:", width=20, height=2)
pw.grid(row=4, column=1)

#The Entries
website_name = Entry(width=36)
website_name.grid(row=2, column=2, columnspan=2)
website_name.focus()

email_entry = Entry(width=36)
email_entry.grid(row=3, column=2, columnspan=2)
email_entry.insert(0, "faithchoo126@hotmail.com") #helps prepopulate field

pw_output = Entry(width=20)
pw_output.grid(row=4, column=2)

#The buttons
search_button = Button(text= "Search", command = search, width=12, height=1)
search_button.grid(row=2, column=3)

save = Button(text= "Add", command = add_acc, width=34, height=1)
save.grid(row=5, column=2, columnspan=2)

new_pw = Button(text= "Generate Password", command = generate_pw, width=12, height=1)
new_pw.grid(row=4, column=3)


window.mainloop()