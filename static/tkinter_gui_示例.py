from tkinter import *
root = Tk()
frame = Frame(root, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH, expand=1)
label = Label(frame, text="Hello, World")
label.pack(fill=X, expand=1)
button = Button(frame, text="Exit", command=root.destroy)
button.pack(side=BOTTOM)
root.mainloop()
