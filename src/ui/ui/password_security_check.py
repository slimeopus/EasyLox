"""
Модуль для проверки безопасности паролей
"""
import tkinter as tk
from tkinter import ttk, messagebox

class PasswordSecurityCheck:
    """
    Окно для проверки безопасности паролей
    """
    
    def __init__(self, parent, password_manager):
        self.parent = parent
        self.password_manager = password_manager
        
        # Создание диалогового окна
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Проверка безопасности паролей")
        self.dialog.geometry("700x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Центрирование окна
        self.dialog.geometry(f"+{parent.winfo_rootx() + 50}+{parent.winfo_rooty() + 50}")
        
        # Создание интерфейса
        self.create_widgets()
        
        # Выполнение проверки при открытии
        self.check_passwords()
        
    def create_widgets(self):
        """
        Создание виджетов интерфейса
        """
        # Основной фрейм
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Проверка безопасности паролей", 
                               font=("Helvetica", 14, "bold"))
        title_label.pack(pady=10)
        
        # Описание
        desc_label = ttk.Label(main_frame, text="Система проверила ваши пароли и выявила следующие проблемы:", 
                              wraplength=600)
        desc_label.pack(pady=5)
        
        # Treeview для отображения результатов
        columns = ("service", "login", "security", "issues")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
        
        # Настройка колонок
        self.tree.heading("service", text="Сервис")
        self.tree.heading("login", text="Логин")
        self.tree.heading("security", text="Безопасность")
        self.tree.heading("issues", text="Проблемы")
        
        self.tree.column("service", width=150)
        self.tree.column("login", width=150)
        self.tree.column("security", width=100, anchor="center")
        self.tree.column("issues", width=200)
        
        # Добавление полос прокрутки
        vsb = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(main_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Размещение виджетов
        self.tree.pack(side='top', fill='both', expand=True, pady=5)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        
        # Рамка для кнопок
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=10)
        
        # Кнопки
        ttk.Button(button_frame, text="Рекомендации", command=self.show_recommendations).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Обновить", command=self.check_passwords).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Закрыть", command=self.dialog.destroy).pack(side='right', padx=5)
        
        # Настройка стилей для цветовой индикации
        self.tree.tag_configure('strong', background='#d4edda', foreground='#155724')
        self.tree.tag_configure('medium', background='#fff3cd', foreground='#856404')
        self.tree.tag_configure('weak', background='#f8d7da', foreground='#721c24')
        
    def check_passwords(self):
        """
        Выполнить проверку безопасности всех паролей
        """
        # Очистка предыдущих данных
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Получение всех паролей
        passwords = self.password_manager.get_all_passwords()
        
        if not passwords:
            messagebox.showinfo("Информация", "Нет сохранённых паролей для проверки.", parent=self.dialog)
            return
        
        # Проверка каждого пароля
        for password in passwords:
            result = self.analyze_password(password)
            
            # Определение тега для цветовой индикации
            if result['score'] >= 80:
                tag = 'strong'
            elif result['score'] >= 50:
                tag = 'medium'
            else:
                tag = 'weak'
            
            # Добавление строки в treeview
            self.tree.insert('', 'end', values=(
                password['service'],
                password['login'],
                result['security_level'],
                result['issues_text']
            ), tags=(tag,))
        
    def analyze_password(self, password_data):
        """
        Проанализировать пароль и вернуть результаты проверки
        
        Args:
            password_data: Данные пароля
        
        Returns:
            dict: Результаты анализа
        """
        password = password_data['password']
        score = 0
        max_score = 100
        issues = []
        
        # Проверка длины
        length = len(password)
        if length < 8:
            issues.append("Слишком короткий (менее 8 символов)")
            score += 10
        elif length < 12:
            score += 20
        elif length < 16:
            score += 30
        else:
            score += 40
        
        # Проверка наличия разных типов символов
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        if not has_lower:
            issues.append("Нет строчных букв")
            score += 15
        if not has_upper:
            issues.append("Нет прописных букв")
            score += 15
        if not has_digit:
            issues.append("Нет цифр")
            score += 15
        if not has_symbol:
            issues.append("Нет специальных символов")
            score += 15
        
        # Проверка на простые последовательности
        common_sequences = ["123", "234", "345", "456", "567", "678", "789", "890",
                          "abc", "bcd", "cde", "def", "efg", "fgh", "ghi", "hij", "ijk",
                          "jkl", "klm", "lmn", "mno", "nop", "opq", "pqr", "qrs", "rst",
                          "stu", "tuv", "uvw", "vwx", "wxy", "xyz"]
        
        password_lower = password.lower()
        for seq in common_sequences:
            if seq in password_lower:
                issues.append(f"Содержит простую последовательность '{seq}'")
                score += 10
                break
        
        # Проверка на повторяющиеся символы
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                issues.append("Содержит повторяющиеся символы")
                score += 10
                break
        
        # Проверка на имя пользователя или имя сервиса
        if password_data['login'].lower() in password_lower:
            issues.append("Содержит логин")
            score += 20
        if password_data['service'].lower() in password_lower:
            issues.append("Содержит название сервиса")
            score += 20
        
        # Определение уровня безопасности
        if score < 50:
            security_level = "Слабый"
        elif score < 80:
            security_level = "Средний"
        else:
            security_level = "Надёжный"
        
        return {
            'score': score,
            'security_level': security_level,
            'issues': issues,
            'issues_text': "; ".join(issues) if issues else "Нет проблем"
        }
    
    def show_recommendations(self):
        """
        Показать рекомендации по улучшению безопасности
        """
        recommendations = """
Рекомендации по улучшению безопасности паролей:

1. Используйте пароли длиной не менее 12 символов
2. Включайте в пароль строчные и прописные буквы, цифры и специальные символы
3. Избегайте простых последовательностей (123, abc и т.д.)
4. Не используйте личную информацию (имена, даты рождения)
5. Не повторяйте одинаковые символы подряд
6. Используйте уникальные пароли для разных сервисов
7. Регулярно обновляйте пароли, особенно для важных учётных записей
8. Рассмотрите возможность использования двухфакторной аутентификации
        """
        
        messagebox.showinfo("Рекомендации", recommendations, parent=self.dialog)