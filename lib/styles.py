import tkinter as tk

class InputLabel(tk.Label):
    def __init__(self, parent, text, **kwargs):
        super().__init__(parent, text=text, bg='lightgrey', fg='black', font=('Helvetica', 8, 'bold'), padx=3, pady=3, **kwargs)

class InputButton(tk.Button):
    def __init__(self, parent, text, command=None, **kwargs):
        button_kwargs = {'bg': 'lightgrey', 'fg': 'black', 'font': ('Helvetica', 8, 'bold'), 'bd': 2, 'relief': 'raised'}
        button_kwargs.update(kwargs)
        super().__init__(parent, text=text, command=command, **button_kwargs)
