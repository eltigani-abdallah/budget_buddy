

def destroy_widgets(window):
    for widget in window.winfo_children():
        widget.destroy()

def forget_widgets(window):
    for widget in window.winfo_children():
        widget.forget()

