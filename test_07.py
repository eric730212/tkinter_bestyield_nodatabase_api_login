import tkinter as tk

root = tk.Tk()
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox = tk.Listbox(root, yscrollcommand=scrollbar.set)
for i in range(100):
    listbox.insert(0, str(i))

listbox.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar.config(command=listbox.yview)
root.mainloop()
