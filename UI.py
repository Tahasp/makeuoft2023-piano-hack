import tkinter as tk
from tkinter import HORIZONTAL, CENTER, BROWSE
import glob


def quit(win):
    win.quit()


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

    button = tk.Button(text="Switch", width=10, height=20, bg="white", fg="blue", font=("Courier", 18))
    button.place(x=0, y=0)

    button1 = tk.Button(text="Reset", width=10, height=20, bg="white", fg="blue", font=("Courier", 18))
    button1.place(x=700, y=0)

    button2 = tk.Button(text="Quit", width=15, height=8, bg="cyan", fg="red", font=("Courier", 18), command=lambda: quit(win))
    button2.place(x=250, y=400)

    # s1 = tk.Scale(win, variable=v1, from_=0.5, to=2.5, orient=HORIZONTAL)
    s1 = tk.Scale(win, from_=0.5, to=2.5, digits=2, resolution=0.05,
                  orient=HORIZONTAL, sliderlength=60, length=300, width=50)
    s1.set(1.0)

    l3 = tk.Label(win, text="Slowness", font=("Courier", 20))

    def s2():
        l2 = tk.Listbox(bg="white", height=5, font=("Courier", 20), selectmode=BROWSE)
        for i, song in enumerate(glob.glob("./*.mid")):
            l2.insert(i + 1, song)

        l2.place(x=250, y=250)

        def selected_item():

            # Traverse the tuple returned by
            # curselection method and print
            # corresponding value(s) in the listbox
            for i in l2.curselection():
                print(l2.get(i))

        selected_item()
        #print("h", a)

    b1 = tk.Button(win, text="Song List", command=s2, bg="yellow")
    b1.place(x=250, y=150)

    l1 = tk.Label(win)
    l1.pack()

    s1.pack(anchor=CENTER)
    l3.pack()

    win.mainloop()

# button = tk.Button(text="Switch", width=15, height=20, bg="white", fg="blue", font=("Courier", 20))
#     button.place(x=(width//2 - width//3), y=height//4)
#
#     button1 = tk.Button(text="Reset", width=15, height=20, bg="white", fg="blue", font=("Courier", 20))
#     button1.place(x=(width//2 + width//4), y=height//4)
#
#     button2 = tk.Button(text="Quit", width=15, height=12, bg="black", fg="red", font=("Courier", 20))
#     button2.place(x=width//2, y=height//4 + height//3)