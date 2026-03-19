"""
Главный файл запуска приложения Passdefender
"""
import tkinter as tk
from tkinter import messagebox
from .core.password_manager import PasswordManager
from .ui.main_window import MainWindow
from .ui.auth_dialog import AuthDialog

# Пути к файлам данных
DATA_FILE = "passwords.json"
MASTER_PASSWORD_FILE = "master_password.json"

def main():
    """
    Основная функция запуска приложения
    """
    # Создаем менеджер паролей
    password_manager = PasswordManager(DATA_FILE, MASTER_PASSWORD_FILE)
    
    # Создаем главное окно
    root = tk.Tk()
    root.withdraw()  # Скрываем главное окно до успешной аутентификации
    
    # Проверяем, первый ли это запуск (существует ли файл с мастер-паролем)
    is_first_run = not password_manager.master_password_hash
    
    # Создаем и показываем диалог аутентификации
    auth_dialog = AuthDialog(root, password_manager, is_first_run)
    auth_result = auth_dialog.show()
    
    # Если аутентификация отменена или неуспешна, закрываем приложение
    if not auth_result:
        root.destroy()
        return
    
    # Создаем и показываем главное окно приложения
    root.deiconify()  # Показываем главное окно
    app = MainWindow(root, password_manager)
    
    # Запускаем главный цикл
    root.mainloop()

if __name__ == "__main__":
    main()