"""
Модуль для окна настроек приложения
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class SettingsWindow:
    """
    Окно настроек приложения
    """
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window  # Сохраняем ссылку на главное окно
        
        # Создание диалогового окна
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Настройки")
        self.dialog.geometry("600x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Центрирование окна
        self.dialog.geometry(f"+{parent.winfo_rootx() + 50}+{parent.winfo_rooty() + 50}")
        
        # Создание интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        """
        Создание виджетов интерфейса
        """
        # Основной фрейм с вкладками
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Вкладка "Основные"
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="Основные")
        
        # Вкладка "Безопасность"
        security_frame = ttk.Frame(notebook)
        notebook.add(security_frame, text="Безопасность")
        
        # Вкладка "Уведомления"
        notifications_frame = ttk.Frame(notebook)
        notebook.add(notifications_frame, text="Уведомления")
        
        # Вкладка "Резервное копирование"
        backup_frame = ttk.Frame(notebook)
        notebook.add(backup_frame, text="Резервное копирование")
        
        # Заполнение вкладки "Основные"
        self.create_general_tab(general_frame)
        
        # Заполнение вкладки "Безопасность"
        self.create_security_tab(security_frame)
        
        # Заполнение вкладки "Уведомления"
        self.create_notifications_tab(notifications_frame)
        
        # Заполнение вкладки "Резервное копирование"
        self.create_backup_tab(backup_frame)
        
        # Кнопки управления
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text="Сохранить", command=self.save_settings).pack(side='right', padx=5)
        ttk.Button(button_frame, text="Отмена", command=self.dialog.destroy).pack(side='right')
        
    def create_general_tab(self, parent):
        """
        Создание вкладки "Основные"
        """
        # Тема оформления
        theme_frame = ttk.LabelFrame(parent, text="Тема оформления")
        theme_frame.pack(fill='x', padx=10, pady=10)
        
        self.theme_var = tk.StringVar(value="Светлая")
        ttk.Radiobutton(theme_frame, text="Светлая", variable=self.theme_var, value="Светлая").pack(anchor='w', padx=10, pady=5)
        ttk.Radiobutton(theme_frame, text="Тёмная", variable=self.theme_var, value="Тёмная").pack(anchor='w', padx=10, pady=5)
        
        ttk.Button(theme_frame, text="Применить тему", command=self.apply_theme).pack(anchor='w', padx=10, pady=10)
        
        # Язык интерфейса
        lang_frame = ttk.LabelFrame(parent, text="Язык интерфейса")
        lang_frame.pack(fill='x', padx=10, pady=10)
        
        self.lang_var = tk.StringVar(value="Русский")
        languages = ["Русский", "English"]
        
        for lang in languages:
            ttk.Radiobutton(lang_frame, text=lang, variable=self.lang_var, value=lang).pack(anchor='w', padx=10, pady=2)
        
        # Автозагрузка
        startup_frame = ttk.LabelFrame(parent, text="Автозагрузка")
        startup_frame.pack(fill='x', padx=10, pady=10)
        
        self.startup_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(startup_frame, text="Запускать приложение при старте системы", 
                      variable=self.startup_var).pack(anchor='w', padx=10, pady=5)
        
    def create_security_tab(self, parent):
        """
        Создание вкладки "Безопасность"
        """
        # Мастер-пароль
        master_password_frame = ttk.LabelFrame(parent, text="Мастер-пароль")
        master_password_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(master_password_frame, text="Текущий мастер-пароль:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
        ttk.Entry(master_password_frame, show="*").grid(row=0, column=1, sticky='ew', padx=10, pady=5)
        
        ttk.Label(master_password_frame, text="Новый мастер-пароль:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
        ttk.Entry(master_password_frame, show="*").grid(row=1, column=1, sticky='ew', padx=10, pady=5)
        
        ttk.Label(master_password_frame, text="Подтверждение:").grid(row=2, column=0, sticky='w', padx=10, pady=5)
        ttk.Entry(master_password_frame, show="*").grid(row=2, column=1, sticky='ew', padx=10, pady=5)
        
        ttk.Button(master_password_frame, text="Изменить", command=self.change_master_password).grid(
            row=3, column=0, columnspan=2, pady=10)
        
        # Двухфакторная аутентификация
        mfa_frame = ttk.LabelFrame(parent, text="Двухфакторная аутентификация")
        mfa_frame.pack(fill='x', padx=10, pady=10)
        
        self.mfa_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(mfa_frame, text="Включить двухфакторную аутентификацию", 
                      variable=self.mfa_var, command=self.toggle_mfa).pack(anchor='w', padx=10, pady=5)
        
        # Уровень шифрования
        encryption_frame = ttk.LabelFrame(parent, text="Уровень шифрования")
        encryption_frame.pack(fill='x', padx=10, pady=10)
        
        self.encryption_var = tk.StringVar(value="AES-256")
        ttk.Radiobutton(encryption_frame, text="AES-256 (Рекомендуется)", 
                       variable=self.encryption_var, value="AES-256").pack(anchor='w', padx=10, pady=5)
        
    def create_notifications_tab(self, parent):
        """
        Создание вкладки "Уведомления"
        """
        # Уведомления о слабых паролях
        weak_passwords_frame = ttk.LabelFrame(parent, text="Уведомления о слабых паролях")
        weak_passwords_frame.pack(fill='x', padx=10, pady=10)
        
        self.weak_passwords_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(weak_passwords_frame, text="Уведомлять о слабых паролях", 
                      variable=self.weak_passwords_var).pack(anchor='w', padx=10, pady=5)
        
        ttk.Label(weak_passwords_frame, text="Проверять при запуске приложения").pack(anchor='w', padx=30, pady=2)
        ttk.Label(weak_passwords_frame, text="Проверять при добавлении нового пароля").pack(anchor='w', padx=30, pady=2)
        
        # Уведомления об утечках данных
        breaches_frame = ttk.LabelFrame(parent, text="Уведомления об утечках данных")
        breaches_frame.pack(fill='x', padx=10, pady=10)
        
        self.breaches_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(breaches_frame, text="Проверять пароли на наличие в утечках данных", 
                      variable=self.breaches_var).pack(anchor='w', padx=10, pady=5)
        
        ttk.Label(breaches_frame, text="Проверять раз в неделю").pack(anchor='w', padx=30, pady=2)
        
        # Уведомления о необходимости обновления
        update_frame = ttk.LabelFrame(parent, text="Уведомления о необходимости обновления")
        update_frame.pack(fill='x', padx=10, pady=10)
        
        self.update_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(update_frame, text="Уведомлять о необходимости обновления паролей", 
                      variable=self.update_var).pack(anchor='w', padx=10, pady=5)
        
        ttk.Label(update_frame, text="Проверять пароли старше 90 дней").pack(anchor='w', padx=30, pady=2)
        
    def create_backup_tab(self, parent):
        """
        Создание вкладки "Резервное копирование"
        """
        # Автоматическое резервное копирование
        auto_backup_frame = ttk.LabelFrame(parent, text="Автоматическое резервное копирование")
        auto_backup_frame.pack(fill='x', padx=10, pady=10)
        
        self.auto_backup_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(auto_backup_frame, text="Включить автоматическое резервное копирование", 
                      variable=self.auto_backup_var, command=self.toggle_auto_backup).pack(anchor='w', padx=10, pady=5)
        
        # Периодичность
        ttk.Label(auto_backup_frame, text="Периодичность:").pack(anchor='w', padx=30, pady=5)
        
        self.backup_frequency_var = tk.StringVar(value="Еженедельно")
        frequencies = ["Ежедневно", "Еженедельно", "Ежемесячно"]
        
        for freq in frequencies:
            ttk.Radiobutton(auto_backup_frame, text=freq, variable=self.backup_frequency_var, 
                          value=freq).pack(anchor='w', padx=50, pady=2)
        
        # Папка для резервных копий
        ttk.Label(auto_backup_frame, text="Папка для резервных копий:").pack(anchor='w', padx=30, pady=5)
        
        backup_path_frame = ttk.Frame(auto_backup_frame)
        backup_path_frame.pack(fill='x', padx=30, pady=5)
        
        self.backup_path_var = tk.StringVar(value="")
        ttk.Entry(backup_path_frame, textvariable=self.backup_path_var, width=40).pack(side='left', fill='x', expand=True)
        ttk.Button(backup_path_frame, text="Выбрать", command=self.select_backup_path).pack(side='left', padx=5)
        
        # Ручное резервное копирование
        manual_backup_frame = ttk.LabelFrame(parent, text="Ручное резервное копирование")
        manual_backup_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(manual_backup_frame, text="Создать резервную копию сейчас", 
                  command=self.create_manual_backup).pack(pady=10)
        
        ttk.Label(manual_backup_frame, text="Последняя резервная копия: Нет данных").pack()
        
    def toggle_mfa(self):
        """
        Переключение двухфакторной аутентификации
        """
        if self.mfa_var.get():
            result = messagebox.askyesno(
                "Двухфакторная аутентификация",
                "Вы уверены, что хотите включить двухфакторную аутентификацию?\n\n"
                "Это повысит безопасность вашего хранилища паролей, но потребует дополнительный шаг при входе.",
                parent=self.dialog
            )
            if not result:
                self.mfa_var.set(False)
        
    def toggle_auto_backup(self):
        """
        Переключение автоматического резервного копирования
        """
        if self.auto_backup_var.get():
            if not self.backup_path_var.get():
                messagebox.showwarning(
                    "Папка для резервных копий",
                    "Пожалуйста, выберите папку для резервных копий.",
                    parent=self.dialog
                )
                self.auto_backup_var.set(False)
        
    def select_backup_path(self):
        """
        Выбор папки для резервных копий
        """
        path = filedialog.askdirectory(parent=self.dialog, title="Выберите папку для резервных копий")
        if path:
            self.backup_path_var.set(path)
            # Если включено автоматическое резервное копирование, разрешаем его
            if not self.auto_backup_var.get():
                result = messagebox.askyesno(
                    "Автоматическое резервное копирование",
                    "Хотите включить автоматическое резервное копирование с этой папкой?",
                    parent=self.dialog
                )
                if result:
                    self.auto_backup_var.set(True)
        
    def create_manual_backup(self):
        """
        Создание ручной резервной копии
        """
        if not self.backup_path_var.get():
            messagebox.showwarning(
                "Папка для резервных копий",
                "Пожалуйста, сначала выберите папку для резервных копий.",
                parent=self.dialog
            )
            return
        
        # Здесь будет реализовано создание резервной копии
        messagebox.showinfo(
            "Резервное копирование",
            "Функция создания резервной копии будет реализована позже.",
            parent=self.dialog
        )
        
    def change_master_password(self):
        """
        Изменение мастер-пароля
        """
        messagebox.showinfo(
            "Изменение мастер-пароля",
            "Функция изменения мастер-пароля будет реализована позже.",
            parent=self.dialog
        )
        
    def apply_theme(self):
        """
        Применить выбранную тему
        """
        theme_name = self.theme_var.get()
        
        # Для Windows используем встроенную тему, для других ОС можно добавить поддержку темной темы
        if theme_name == "Тёмная":
            # Попробуем использовать тему 'alt' или 'clam' для тёмной темы
            available_themes = self.main_window.style.theme_names()
            if 'clam' in available_themes:
                theme_to_use = 'clam'
            elif 'alt' in available_themes:
                theme_to_use = 'alt'
            else:
                theme_to_use = 'winnative'
                messagebox.showwarning("Тема", "Тёмная тема недоступна в этой системе.", parent=self.dialog)
        else:
            theme_to_use = 'winnative'
        
        # Применяем тему
        self.main_window.style.theme_use(theme_to_use)
        self.main_window.current_theme = theme_to_use
        
        # Обновляем цвета фона и текста для достижения эффекта тёмной темы
        if theme_name == "Тёмная" and theme_to_use in ['clam', 'alt']:
            # Настройка цветов для тёмной темы
            self.main_window.style.configure(".", background="#2b2b2b", foreground="white", 
                                     fieldbackground="#3c3c3c", selectbackground="#555555")
            
            # Обновляем все виджеты
            self.main_window.root.configure(bg="#2b2b2b")
            
            # Обновляем цвета для всех дочерних виджетов
            self._update_widget_colors(self.main_window.root)
        
        # Показываем сообщение
        messagebox.showinfo("Тема", f"Тема '{theme_name}' применена.", parent=self.dialog)
        
    def _update_widget_colors(self, parent):
        """
        Рекурсивно обновить цвета всех виджетов в иерархии
        """
        for child in parent.winfo_children():
            try:
                child.configure(bg="#2b2b2b", fg="white", insertbackground="white" if hasattr(child, 'configure') else None)
            except tk.TclError:
                pass  # Некоторые виджеты могут не поддерживать эти опции
            
            # Рекурсивно обновляем дочерние виджеты
            self._update_widget_colors(child)
            
    def save_settings(self):
        """
        Сохранение настроек
        """
        # Здесь будут сохраняться настройки, включая тему
        if self.theme_var.get() == "Тёмная":
            self.apply_theme()  # Применяем тему при сохранении
            
        messagebox.showinfo(
            "Настройки",
            "Настройки сохранены успешно.",
            parent=self.dialog
        )
        self.dialog.destroy()