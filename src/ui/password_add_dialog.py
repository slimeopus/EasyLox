"""
Модуль для диалогового окна добавления пароля
"""
import tkinter as tk
from tkinter import ttk, messagebox

class PasswordAddDialog:
    """
    Диалоговое окно для добавления нового пароля
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.result = None
        
        # Создание диалогового окна
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Добавить новый пароль")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Центрирование окна
        self.dialog.geometry(f"+{parent.winfo_rootx() + 50}+{parent.winfo_rooty() + 50}")
        
        # Создание интерфейса
        self.create_widgets()
        
        # Блокировка родительского окна
        self.dialog.focus_set()
        
    def create_widgets(self):
        """
        Создание виджетов диалогового окна
        """
        # Основной фрейм с прокруткой
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Контейнер для полей ввода
        form_frame = ttk.LabelFrame(main_frame, text="Информация о пароле")
        form_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Служба
        ttk.Label(form_frame, text="Сервис:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.service_var = tk.StringVar()
        service_entry = ttk.Entry(form_frame, textvariable=self.service_var, width=40)
        service_entry.grid(row=0, column=1, columnspan=2, sticky='ew', padx=5, pady=5)
        service_entry.focus()
        
        # Логин
        ttk.Label(form_frame, text="Логин:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.login_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.login_var, width=40).grid(row=1, column=1, columnspan=2, sticky='ew', padx=5, pady=5)
        
        # Пароль
        ttk.Label(form_frame, text="Пароль:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(form_frame, textvariable=self.password_var, width=30, show="*")
        password_entry.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
        
        # Кнопка генерации пароля
        ttk.Button(form_frame, text="Сгенерировать", command=self.generate_password).grid(row=2, column=2, sticky='ew', padx=5, pady=5)
        
        # Категория
        ttk.Label(form_frame, text="Категория:").grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(form_frame, textvariable=self.category_var, state="readonly", width=37)
        category_combo['values'] = ("", "Личные", "Рабочие", "Финансовые", "Социальные сети", "Электронная почта", "Другое")
        category_combo.grid(row=3, column=1, columnspan=2, sticky='ew', padx=5, pady=5)
        category_combo.set("")
        
        # Заметка
        ttk.Label(form_frame, text="Заметка:").grid(row=4, column=0, sticky='nw', padx=5, pady=5)
        self.notes_text = tk.Text(form_frame, height=4, width=40)
        self.notes_text.grid(row=4, column=1, columnspan=2, sticky='ew', padx=5, pady=5)
        
        # Настройка растягивания столбцов
        form_frame.columnconfigure(1, weight=1)
        
        # Кнопки управления
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=10)
        
        ttk.Button(button_frame, text="Сохранить", command=self.save).pack(side='right', padx=5)
        ttk.Button(button_frame, text="Отмена", command=self.cancel).pack(side='right')
        
        # Привязка клавиш
        self.dialog.bind('<Return>', self.save)
        self.dialog.bind('<Escape>', self.cancel)
        
    def generate_password(self):
        """
        Открыть генератор паролей
        """
        # Позже будет интегрирован генератор паролей
        messagebox.showinfo("Генератор паролей", "Функция генерации пароля будет добавлена позже.", parent=self.dialog)
    
    def save(self, event=None):
        """
        Сохранить введённые данные
        """
        service = self.service_var.get().strip()
        login = self.login_var.get().strip()
        password = self.password_var.get()
        
        if not service:
            messagebox.showerror("Ошибка", "Введите название сервиса!", parent=self.dialog)
            return
        
        if not password:
            if messagebox.askyesno("Внимание", "Вы не ввели пароль. Продолжить без пароля?", parent=self.dialog):
                pass  # Продолжаем без пароля
            else:
                return
        
        self.result = {
            'service': service,
            'login': login,
            'password': password,
            'category': self.category_var.get(),
            'notes': self.notes_text.get('1.0', 'end-1c')
        }
        
        self.dialog.destroy()
    
    def cancel(self, event=None):
        """
        Отменить добавление
        """
        self.result = None
        self.dialog.destroy()
    
    def show(self):
        """
        Отобразить диалог и вернуть результат
        """
        self.dialog.wait_window()
        return self.result