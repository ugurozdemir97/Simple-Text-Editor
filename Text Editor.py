from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import ttk
from tkinter import font
import smtplib
from smtplib import SMTPAuthenticationError

DOCUMENT = ""
WRAP = 0

window = Tk()
window.title("Simple Text Editor")
window.geometry("500x500")
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# ---------------- AVAILABLE FONTS ---------------- #

f = list(font.families())
f.sort()  # It is reverse because otherwise spinbox starts from bottom.

font_var = StringVar(window)
font_var.set("Arial")
size_var = IntVar()
size_var.set(11)

# ------------------------------------------------- #


# --------------------------------------- MENU FUNCTIONS --------------------------------------- #

def new_file():
    if text.get("1.0", END) == DOCUMENT or text.compare("end-1c", "==", "1.0"):
        text.delete("1.0", END)
    else:
        if messagebox.askyesno(title="Unsaved Text", message="You didn't save your document. Do you want to continue?",
                               icon="question"):
            text.delete("1.0", END)


def open_file():
    global DOCUMENT
    if text.compare("end-1c", "==", "1.0") or text.get("1.0", END) == DOCUMENT:
        path = filedialog.askopenfilename(title="Open",
                                          filetypes=[("Text File", ".txt"),
                                                     ("Microsoft Word Documents", ".doc"),
                                                     ("Microsoft Word Template", ".dotx"),
                                                     ("Microsoft Word Document", ".docx"),
                                                     ("All Files", "*.*")])
        if path:
            try:
                text.delete("1.0", END)
                with open(path, "r") as data:
                    document = data.read()
                    text.insert("1.0", document)
            except UnicodeDecodeError:
                messagebox.showinfo(title="Unsupported Document", message="This file is not supported!", icon="error")
        DOCUMENT = text.get("1.0", END)
    else:
        if messagebox.askyesno(title="Unsaved Text", message="You didn't save your document. Do you want to continue?",
                               icon="question"):
            path = filedialog.askopenfilename(title="Open",
                                              filetypes=[("Text File", ".txt"),
                                                         ("Microsoft Word Documents", ".doc"),
                                                         ("Microsoft Word Template", ".dotx"),
                                                         ("Microsoft Word Document", ".docx"),
                                                         ("All Files", "*.*")])
            if path:
                try:
                    text.delete("1.0", END)
                    with open(path, "r") as data:
                        document = data.read()
                        text.insert("1.0", document)
                except UnicodeDecodeError:
                    messagebox.showinfo(title="Unsupported Document", message="This file is not supported!",
                                        icon="error")
            DOCUMENT = text.get("1.0", END)


def save_file():
    global DOCUMENT
    path = filedialog.asksaveasfile(title="Save", defaultextension=".txt",
                                    filetypes=[("Text File", ".txt"), ("Microsoft Word Documents", ".doc"),
                                               ("Microsoft Word Template", ".dotx"),
                                               ("Microsoft Word Document", ".docx"),
                                               ("All Files", "*.*")])
    if path:
        filetext = str(text.get("1.0", END))
        path.write(filetext)
        path.close()
    DOCUMENT = text.get("1.0", END)


def copy():
    text.event_generate("<<Copy>>")


def cut():
    text.event_generate("<<Cut>>")


def paste():
    text.event_generate("<<Paste>>")


def wrap():
    global WRAP
    if WRAP % 2 == 0:
        text.config(wrap="char")
        view.entryconfig(0, label="Wrap by Word")
        WRAP += 1
    else:
        text.config(wrap="word")
        view.entryconfig(0, label="Wrap by Char")
        WRAP += 1


def text_area():
    tcolor = list(colorchooser.askcolor())
    text_area_color = str(tcolor[1])
    if text_area_color != "None":
        text.config(bg=text_area_color)
        if tcolor[0][0] < 140 or tcolor[0][1] < 140 or tcolor[0][2] < 140:
            text.config(insertbackground="white")
        else:
            text.config(insertbackground="black")


def about():
    messagebox.showinfo(title="Simple Text Editor", message="This program is written by Uğur Özdemir in 2022.\n"
                                                            "You can use it for free.", icon="info")


def mail_page():

    # -------------------------------- SEND MAIL --------------------------------- #

    def send_mail():
        to = "pythontester946@yahoo.com"
        if messagebox.askyesno(title="Contact",
                               message="This program will not store your email address or password, this process "
                                       "will not work unless you use your 'app password', not the real one. "
                                       "Do yo want to continue?",
                               icon="question"):
            try:
                with smtplib.SMTP("smtp.gmail.com", 587, timeout=120) as connection:
                    connection.starttls()
                    connection.login(user=mail_entry.get(), password=password_entry.get())
                    connection.sendmail(from_addr=mail_entry.get(), to_addrs=to,
                                        msg=f"Subject:{subject_entry.get()}\n\n"
                                            f"{message_area.get('1.0', END)}".encode("utf-8"))
            except SMTPAuthenticationError:
                messagebox.showinfo(title="Failed", message="Authentication is failed. Your mail address or "
                                                            "password is wrong.", icon="error")
            except UnicodeEncodeError:
                messagebox.showinfo(title="Failed", message="Unicode error, you may have a typo.", icon="error")
            else:
                messagebox.showinfo(title="Email Successfully Sent",
                                    message="Your mail is sent! Thank you for using my program.", icon="info")

    # ---------------------------- GREYED OUT TEXTS ------------------------------- #

    def handle_focus_in1(_):
        if mail_entry.get() == "E.g: amazon@gmail.com":
            mail_entry.delete(0, END)
            mail_entry.config(fg='black')

    def handle_focus_in2(_):
        if subject_entry.get() == "E.g: Title":
            subject_entry.delete(0, END)
            subject_entry.config(fg='black')

    def handle_focus_out1(_):
        if not mail_entry.get():
            mail_entry.config(fg='grey')
            mail_entry.insert(0, "E.g: amazon@gmail.com")

    def handle_focus_out2(_):
        if not subject_entry.get():
            subject_entry.config(fg='grey')
            subject_entry.insert(0, "E.g: Title")

    # -------------------------------- SHOW PASSWORD ------------------------------- #

    def show():
        if checked_state.get():
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    # -------------------------------- MAIL WINDOW --------------------------------- #

    mail_window = Toplevel()
    mail_window.config(bg="white", pady=20, padx=100)

    mail_logo = PhotoImage(master=mail_window, file="gmail.png")

    mail_canvas = Canvas(mail_window, width=100, height=75, bg="white", highlightthickness=0)
    mail_canvas.create_image(1, 1, image=mail_logo, anchor=NW)
    mail_canvas.image = mail_logo  # Basically this adds an attribute to the object, when there is an attribute
    # Garbage Collector will not collect this image object and, it will appear. Otherwise, images on second window got
    # caught by the garbage collector.

    check_frame = Frame(mail_window, width=20, height=20)
    checked_state = IntVar()
    show_pass = Checkbutton(check_frame, variable=checked_state, bg="white", command=show)

    mail_label = Label(mail_window, text="Email: ", bg="white")
    password_label = Label(mail_window, text="Password: ", bg="white")
    subject_label = Label(mail_window, text="Subject: ", bg="white")

    mail_entry = Entry(mail_window, width=32, fg="grey")
    password_entry = Entry(mail_window, width=32, show="*")
    subject_entry = Entry(mail_window, width=32, fg="grey")

    mail_entry.insert(0, "E.g: amazon@gmail.com")
    subject_entry.insert(0, "E.g: Title")

    mail_entry.bind("<FocusIn>", handle_focus_in1)
    mail_entry.bind("<FocusOut>", handle_focus_out1)
    subject_entry.bind("<FocusIn>", handle_focus_in2)
    subject_entry.bind("<FocusOut>", handle_focus_out2)

    text_frame = Frame(mail_window)
    scrollbar = Scrollbar(text_frame)
    message_area = Text(text_frame, width=40, height=4)

    message_area.config(yscrollcommand=scrollbar.set, font=("Arial", 9))
    scrollbar.config(command=message_area.yview)

    send = Button(mail_window, text="Send", command=send_mail, bg="white")

    mail_canvas.grid(row=0, column=0, columnspan=2, pady=20)
    mail_label.grid(row=1, column=0, sticky=E)
    mail_entry.grid(row=1, column=1, sticky=E)
    password_label.grid(row=2, column=0, sticky=E)
    password_entry.grid(row=2, column=1, sticky=E)
    check_frame.grid(row=2, column=2, sticky=E)
    show_pass.place(x=0, y=0)
    subject_label.grid(row=3, column=0, sticky=E)
    subject_entry.grid(row=3, column=1, sticky=E)
    text_frame.grid(row=4, column=0, columnspan=3, pady=(10, 5), sticky=E)
    scrollbar.pack(side=RIGHT, fill=Y)
    message_area.pack(expand=True, fill=BOTH, side=LEFT)
    send.grid(row=5, column=0, columnspan=3, pady=(0, 30), sticky=W + E)


# -------------------------------------- BUTTON FUNCTIONS -------------------------------------- #

def font_color():
    text_color = str(colorchooser.askcolor()[1])
    if text_color != "None":
        text.config(fg=text_color)


def change_font(_):
    current_font = fonts.get()
    size = font_size.get()
    text.config(font=(current_font, size))


def change_fontsize():
    current_font = fonts.get()
    size = font_size.get()
    text.config(font=(current_font, size))


def font_examples():
    global f
    row = 1
    pop_up = Toplevel()
    canvas_pop = Canvas(pop_up, bg="white")
    frame_pop = Frame(canvas_pop, bg="white")
    scrollbar_pop = Scrollbar(pop_up, command=canvas_pop.yview)
    canvas_pop.configure(yscrollcommand=scrollbar_pop.set)
    canvas_pop.create_window((18, 4), window=frame_pop, anchor="nw")
    frame_pop.bind("<Configure>", lambda event: canvas_pop.configure(scrollregion=canvas_pop.bbox("all")))

    scrollbar_pop.pack(side="right", fill=Y)
    canvas_pop.pack(side="left", fill=BOTH, expand=True)

    for i in f:
        Label(frame_pop, font=(i, 16, "normal"), text=i, bg="white").grid(row=row, column=1)
        row = row + 1


# ------------------------------------------- MENU BAR ----------------------------------------- #

menu = Menu(window)
window.config(menu=menu)

file = Menu(menu, tearoff=0)
edit = Menu(menu, tearoff=0)
view = Menu(menu, tearoff=0)
help = Menu(menu, tearoff=0)

menu.add_cascade(label="File", menu=file)
menu.add_cascade(label="Edit", menu=edit)
menu.add_cascade(label="View", menu=view)
menu.add_cascade(label="Help", menu=help)

file.add_command(label="New", command=new_file)
file.add_command(label="Open", command=open_file)
file.add_command(label="Save", command=save_file)
file.add_separator()
file.add_command(label="Exit", command=window.quit)

edit.add_command(label="Copy", command=copy)
edit.add_command(label="Cut", command=cut)
edit.add_command(label="Paste", command=paste)

view.add_command(label="Wrap by Char", command=wrap)
view.add_command(label="Text Area Color", command=text_area)

help.add_command(label="About", command=about)
help.add_separator()
help.add_separator()
help.add_command(label="Contact", command=mail_page)

# ------------------------------------ SCROLL BAR & TEXT AREA ---------------------------------- #

frame = Frame(window, height=100, width=200)
frame.grid(sticky=W + N + E + S)

scroll = Scrollbar(frame)
scroll.pack(side=RIGHT, fill=Y)

text = Text(frame, pady=15, padx=15, wrap="word")
text.pack(expand=True, fill=BOTH, side=LEFT, padx=10, pady=(10, 0))

text.config(yscrollcommand=scroll.set, font=("Arial", 11))
scroll.config(command=text.yview)

# ------------------------------------------- BUTTONS ------------------------------------------ #

frame_bottom = Frame(window)
frame_bottom.grid_columnconfigure(3, weight=1)
frame_bottom.grid(sticky=S + E + W, padx=10, pady=5)

color = Button(frame_bottom, text="Text Color", command=font_color, bg="white", padx=15, relief="raised", bd=1)

fonts = ttk.Combobox(frame_bottom, textvariable=font_var, values=f)
fonts.bind("<<ComboboxSelected>>", change_font)

font_size = Spinbox(frame_bottom, textvariable=size_var, from_=6, to=200, increment=3, width=5, command=change_fontsize)

example = Button(frame_bottom, text="Font Examples", bg="white", relief="raised", bd=1, command=font_examples)

color.grid(row=0, column=0, sticky=W)
fonts.grid(row=0, column=1, sticky=W, padx=10)
font_size.grid(row=0, column=2, sticky=W)
example.grid(row=0, column=3, sticky=E, padx=(5, 17))

window.mainloop()
