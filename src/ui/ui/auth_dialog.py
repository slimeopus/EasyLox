"""
Модуль для диалогового окна аутентификации (создание/ввод мастер-пароля)
"""
import tkinter as tk
from tkinter import ttk, messagebox
import hashlib

class AuthDialog:
    """
    Диалоговое окно для создания или ввода мастер-пароля
    """
    
    def __init__(self, parent, password_manager, is_first_run=False):
        self.parent = parent
        self.password_manager = password_manager
        self.is_first_run = is_first_run
        self.result = None
        
        # Создание диалогового окна
        self.dialog = tk.Toplevel()
        self.dialog.title("Аутентификация")
        self.dialog.geometry("400x300")
        self.dialog.grab_set()
        
        # Центрирование окна по центру экрана
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        window_width = 400
        window_height = 300
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Создание интерфейса
        self.create_widgets()
        
        # Блокировка родительского окна
        self.dialog.focus_set()
        
    def create_widgets(self):
        """
        Создание виджетов диалогового окна
        """
        # Основной фрейм
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Заголовок
        if self.is_first_run:
            title = "Создание мастер-пароля"
            message = "Пожалуйста, создайте мастер-пароль для защиты ваших данных:"
        else:
            title = "Ввод мастер-пароля"
            message = "Введите ваш мастер-пароль для доступа к приложению:"
        
        ttk.Label(main_frame, text=title, font=("Helvetica", 12, "bold")).pack(pady=5)
        ttk.Label(main_frame, text=message, wraplength=350).pack(pady=5)
        
        # Поле ввода пароля
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill='x', pady=10)
        
        ttk.Label(password_frame, text="Мастер-пароль:").pack(side='left')
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var, width=30, show="*")
        self.password_entry.pack(side='left', padx=5)
        self.password_entry.focus()
        
        # Поле подтверждения (только при создании)
        self.confirm_frame = ttk.Frame(main_frame)
        if self.is_first_run:
            self.confirm_frame.pack(fill='x', pady=5)
            ttk.Label(self.confirm_frame, text="Подтверждение:").pack(side='left')
            self.confirm_var = tk.StringVar()
            ttk.Entry(self.confirm_frame, textvariable=self.confirm_var, width=30, show="*").pack(side='left', padx=5)
        
        # Кнопки управления
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=10)
        
        ttk.Button(button_frame, text="ОК", command=self.authenticate).pack(side='right', padx=5)
        ttk.Button(button_frame, text="Отмена", command=self.cancel).pack(side='right')
        
        # Привязка клавиш
        self.dialog.bind('<Return>', self.authenticate)
        self.dialog.bind('<Escape>', self.cancel)
        
        # Обновляем заголовок окна
        self.dialog.title(title)
        
    def authenticate(self, event=None):
        """
        Аутентификация пользователя
        """
        password = self.password_var.get()
        
        if not password:
            messagebox.showerror("Ошибка", "Пожалуйста, введите мастер-пароль!", parent=self.dialog)
            return
        
        if self.is_first_run:
            # Режим создания мастер-пароля
            confirm_password = self.confirm_var.get()
            if password != confirm_password:
                messagebox.showerror("Ошибка", "Пароли не совпадают! Пожалуйста, попробуйте снова.", parent=self.dialog)
                self.password_var.set("")
                self.confirm_var.set("")
                self.password_entry.focus()
                return
            
            # Устанавливаем мастер-пароль
            if self.password_manager.set_master_password(password):
                messagebox.showinfo("Успех", "Мастер-пароль успешно создан!", parent=self.dialog)
                self.result = True
                self.dialog.destroy()
            else:
                messagebox.showerror("Ошибка", "Не удалось создать мастер-пароль. Попробуйте снова.", parent=self.dialog)
        else:
            # Режим ввода мастер-пароля
            if self.password_manager.verify_master_password(password):
                self.result = True
                self.dialog.destroy()
            else:
                messagebox.showerror("Ошибка", "Неверный мастер-пароль! Пожалуйста, попробуйте снова.", parent=self.dialog)
                self.password_var.set("")
                self.password_entry.focus()
                
    def cancel(self, event=None):
        """
        Отменить аутентификацию
        """
        self.result = None
        self.dialog.destroy()
    
    def show(self):
        """
        Отобразить диалог и вернуть результат
        """
        self.dialog.wait_window()
        return self.result