import tkinter as tk
from tkinter import ttk

class Ui(tk.Tk):
    def __init__(self, app):
        super().__init__()
        self.title("Controle de Dieta")
        self.geometry("600x400")
        
        self.app = app
        
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for Page in (MenuPage, LoginPage, CadastroPage):
            page_name = Page.__name__
            frame = Page(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.show_frame("MenuPage")

    def show_frame(self, page_name):
        self.frames[page_name].tkraise()

class MenuPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        ttk.Label(self, text="Menu Inicial").pack(pady=10)
        ttk.Button(self, text="Login",
                   command=lambda: controller.show_frame("LoginPage")).pack(pady=5)
        ttk.Button(self, text="Cadastro",
                   command=lambda: controller.show_frame("CadastroPage")).pack(pady=5)

class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        ttk.Label(self, text="Login").pack(pady=10)
        self.usuario = tk.StringVar()
        self.senha = tk.StringVar()
        ttk.Entry(self, textvariable=self.usuario).pack(pady=5)
        ttk.Entry(self, textvariable=self.senha, show="*").pack(pady=5)
        ttk.Button(self, text="Entrar").pack(pady=5)
        ttk.Button(self, text="Voltar",
                   command=lambda: controller.show_frame("MenuPage")).pack(pady=5)

class CadastroPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=20)
        ttk.Label(self, text="Cadastro").pack(pady=10)
        self.nome = tk.StringVar()
        self.idade = tk.StringVar()
        ttk.Entry(self, textvariable=self.nome).pack(pady=5)
        ttk.Entry(self, textvariable=self.idade).pack(pady=5)
        ttk.Button(self, text="Salvar").pack(pady=5)
        ttk.Button(self, text="Voltar",
                   command=lambda: controller.show_frame("MenuPage")).pack(pady=5)