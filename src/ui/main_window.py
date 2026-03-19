"""
Модуль для главного окна приложения
"""
import tkinter as tk
from tkinter import ttk, messagebox

class MainWindow:
    """
    Главное окно приложения менеджера паролей
    """
    
    def __init__(self, root, password_manager):
        self.root = root
        self.password_manager = password_manager
        self.root.title("Пароль-Гид")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)
        
        # Настройка стиля
        self.style = ttk.Style()
        self.current_theme = 'winnative'  # Сохраняем текущую тему
        self.style.theme_use(self.current_theme)
        
        # Инициализация переменных для темы
        self.dark_mode = False
        
        # Создание интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        """
        Создание виджетов интерфейса
        """
        # Верхняя панель с поиском и настройками
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill='x', padx=10, pady=5)
        
        # Поле поиска
        ttk.Label(top_frame, text="Поиск:").pack(side='left')
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(top_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side='left', padx=5, fill='x', expand=True)
        search_entry.bind('<KeyRelease>', self.on_search)
        
        # Кнопка настроек
        settings_btn = ttk.Button(top_frame, text="Настройки", command=self.open_settings)
        settings_btn.pack(side='right')
        
        # Основная область с карточками паролей
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Заголовок
        title_label = ttk.Label(self.main_frame, text="Пароль-Гид", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)
        
        # Контейнер для карточек паролей
        self.cards_frame = ttk.Frame(self.main_frame)
        self.cards_frame.pack(fill='both', expand=True)
        
        # Инициализация поисковой строки
        self.search_var.trace_add('write', self.on_search)
        
        # Создание интерфейса для отображения паролей
        self.refresh_passwords()
        
        # Нижняя панель с кнопками действий
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(bottom_frame, text="Добавить новый пароль", command=self.add_new_password).pack(side='left', padx=5)
        ttk.Button(bottom_frame, text="Сгенерировать пароль", command=self.generate_password).pack(side='left', padx=5)
        ttk.Button(bottom_frame, text="Проверить безопасность", command=self.check_security).pack(side='left', padx=5)
        
    def create_password_cards(self, passwords):
        """
        Создание карточек паролей из списка паролей
        
        Args:
            passwords: Список паролей для отображения
        """
        # Очистка предыдущих карточек
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        
        if not passwords:
            # Сообщение об отсутствии паролей
            no_passwords_label = ttk.Label(self.cards_frame, text="Нет сохранённых паролей", font=("Helvetica", 14))
            no_passwords_label.pack(expand=True)
            return
        
        cards_container = ttk.Frame(self.cards_frame)
        cards_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        for password in passwords:
            service = password['service']
            login = password['login']
            last_modified = password['modified_date'][:10]  # Только дата
            
            card = ttk.LabelFrame(cards_container, text=service, width=200)
            card.pack(side='left', padx=10, pady=10, fill='y')
            card.pack_propagate(False)
            
            # Информация о карточке
            ttk.Label(card, text=f"Логин: {login}").pack(anchor='w', padx=5, pady=2)
            ttk.Label(card, text=f"Изменён: {last_modified}").pack(anchor='w', padx=5, pady=2)
            
            # Кнопки действий
            btn_frame = ttk.Frame(card)
            btn_frame.pack(pady=10)
            
            ttk.Button(btn_frame, text="Показать", width=8, command=lambda p=password: self.show_password(p)).pack(side='left', padx=2)
            ttk.Button(btn_frame, text="Копировать", width=8, command=lambda p=password: self.copy_password(p)).pack(side='left', padx=2)
            ttk.Button(btn_frame, text="Редактировать", width=8, command=lambda p=password: self.edit_password(p)).pack(side='left', padx=2)
    def on_search(self, *args):
        """
        Обработка события поиска (вызывается при изменении строки поиска)
        """
        query = self.search_var.get().strip()
        passwords = self.password_manager.search_passwords(query)
        self.create_password_cards(passwords)
        
    def add_new_password(self):
        """
        Открыть окно добавления нового пароля
        """
        from .password_add_dialog import PasswordAddDialog
        dialog = PasswordAddDialog(self.root)
        result = dialog.show()
        if result:
            print(f"Добавлен пароль для сервиса: {result['service']}")
            # Добавляем пароль через PasswordManager
            if self.password_manager.add_password(
                result['service'],
                result['login'],
                result['password'],
                result['category'],
                result['notes']
            ):
                # Обновляем отображение карточек
                self.refresh_passwords()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить пароль!", parent=self.root)
        
    def edit_password(self, password):
        """
        Редактировать существующий пароль
        
        Args:
            password: Пароль для редактирования
        """
        from .password_add_dialog import PasswordAddDialog
        
        # Создаем диалог с заполненными полями
        dialog = PasswordAddDialog(self.root)
        dialog.service_var.set(password['service'])
        dialog.login_var.set(password['login'])
        dialog.password_var.set(password['password'])
        dialog.category_var.set(password['category'])
        dialog.notes_text.delete('1.0', tk.END)
        dialog.notes_text.insert('1.0', password['notes'])
        
        result = dialog.show()
        if result:
            print(f"Обновлён пароль для сервиса: {result['service']}")
            # Обновляем пароль через PasswordManager
            if self.password_manager.update_password(
                password['id'],
                result['service'],
                result['login'],
                result['password'],
                result['category'],
                result['notes']
            ):
                # Обновляем отображение карточек
                self.refresh_passwords()
            else:
                messagebox.showerror("Ошибка", "Не удалось обновить пароль!", parent=self.root)
        
    def refresh_passwords(self):
        """
        Обновить отображение карточек паролей
        """
        passwords = self.password_manager.get_all_passwords()
        self.create_password_cards(passwords)
    def generate_password(self):
        """
        Открыть генератор паролей
        """
        from ..utils.password_generator import PasswordGenerator
        from .password_add_dialog import PasswordAddDialog
        
        # Создаем генератор
        generator = PasswordGenerator()
        
        # Генерируем пример пароля
        password = generator.generate(length=12, use_symbols=True)
        print(f"Сгенерирован пароль: {password}")
        
        # Пока показываем в диалоговом окне добавления
        dialog = PasswordAddDialog(self.root)
        dialog.password_var.set(password)  # Устанавливаем сгенерированный пароль
        result = dialog.show()
        
    def check_security(self):
        """
        Проверить безопасность паролей
        """
        from .password_security_check import PasswordSecurityCheck
        # Создаем временный менеджер паролей с тестовыми данными
        class MockPasswordManager:
            def get_all_passwords(self):
                return [
                    {'service': 'Яндекс', 'login': 'user123@yandex.ru', 'password': 'weak123'},
                    {'service': 'Госуслуги', 'login': 'user456@gosuslugi.ru', 'password': 'Str0ngP@ssw0rd!'},
                    {'service': 'Онлайн-банк', 'login': 'client789@bank.ru', 'password': '123456'}
                ]
        
        mock_manager = MockPasswordManager()
        PasswordSecurityCheck(self.root, mock_manager)
        
    def open_settings(self):
        """
        Открыть окно настроек
        """
        from .settings_window import SettingsWindow
        SettingsWindow(self.root, self)