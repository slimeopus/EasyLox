"""
Файл для запуска приложения Passdefender
"""
if __name__ == "__main__":
    import sys
    import os
    # Добавляем корневую директорию в путь
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        from src.main import main
        main()
    except ImportError:
        try:
            from src.ui.main_window import MainWindow
            import tkinter as tk
            
            root = tk.Tk()
            app = MainWindow(root)
            root.mainloop()
        except Exception as e:
            print(f"Ошибка запуска приложения: {e}")
            input("Нажмите Enter для выхода...")