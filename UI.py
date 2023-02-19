import tkinter as tk
from tkinter import HORIZONTAL, CENTER, BROWSE


# button = tk.Button(
#     text="Switch to NM",
#     width=10,
#     height=10,
#     bg="grey",
#     fg="yellow"
# )

def run_display():
    win = tk.Tk()

    width = win.winfo_screenwidth()
    height = win.winfo_screenheight()

    win.geometry("%dx%d" % (width,height))
    win.configure(bg="grey")

    # win.attributes('-fullscreen', True)
    win.title('Piano Specialist')

    label = tk.Label(win, text="Paino Specialist Menu")
    label.pack()

    button = tk.Button(text="Switch", width=15, height=20, bg="black", fg="blue", font=("Courier", 20))
    button.place(x=50, y=250)

    button1 = tk.Button(text="Reset", width=15, height=20, bg="black", fg="blue", font=("Courier", 20))
    button1.place(x=1190, y=250)

    button2 = tk.Button(text="Quit", width=15, height=12, bg="cyan", fg="red", font=("Courier", 20))
    button2.place(x=635, y=600)

    # s1 = tk.Scale(win, variable=v1, from_=0.5, to=2.5, orient=HORIZONTAL)
    s1 = tk.Scale(win, from_=0.5, to=2.5, digits=2, resolution=0.05,
                  orient=HORIZONTAL, sliderlength=60, length=300, width=50)

    l3 = tk.Label(win, text="Slowness", font=("Courier", 20))

    def s2():
        l2 = tk.Listbox(bg="black", font=("Courier", 20), selectmode=BROWSE)
        l2.insert(1, "Beethoven")
        l2.insert(2, "Beethoven")
        l2.insert(3, "Beethoven")
        l2.insert(4, "Beethoven")

        l2.place(x=635, y= 250)

    b1 = tk.Button(win, text="Song List", command=s2, bg="yellow")
    b1.place(x=635, y=200)

    l1 = tk.Label(win)
    l1.pack()

    s1.pack(anchor=CENTER)
    l3.pack()

    win.mainloop()