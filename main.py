import loginSignup
import FinanceManagerApp
import customtkinter as ctk
import sessionManager

class Mainapp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x700")
        self.title("BOOM")

        self.login_frame=loginSignup.LoginSignup(self)
        self.login_frame.pack(expand=True, fill="both")

    def show_banking_app(self):
        self.login_frame.forget()
        self.banking_frame=FinanceManagerApp.FinanceManagerApp(self)


app=Mainapp()
app.protocol("WM_DELETE_WINDOW", sessionManager.on_close)
app.mainloop()

