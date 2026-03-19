"""
Модуль для генерации паролей
"""
import random
import string

class PasswordGenerator:
    """
    Класс для генерации безопасных паролей
    """
    
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def generate(self, length=12, use_lowercase=True, use_uppercase=True, 
                use_digits=True, use_symbols=True, exclude_ambiguous=False):
        """
        Сгенерировать пароль по заданным параметрам
        
        Аргументы:
            length: длина пароля (по умолчанию 12)
            use_lowercase: использовать строчные буквы
            use_uppercase: использовать прописные буквы
            use_digits: использовать цифры
            use_symbols: использовать специальные символы
            exclude_ambiguous: исключить неоднозначные символы (0, O, l, 1 и т.д.)
        """
        if length < 1:
            raise ValueError("Длина пароля должна быть больше 0")
        
        # Формируем набор символов для генерации
        chars = ""
        if use_lowercase:
            chars += self.lowercase
        if use_uppercase:
            chars += self.uppercase
        if use_digits:
            chars += self.digits
        if use_symbols:
            chars += self.symbols
        
        if exclude_ambiguous:
            ambiguous = "0O1lI"
            chars = ''.join(c for c in chars if c not in ambiguous)
        
        if not chars:
            raise ValueError("Нет доступных символов для генерации пароля")
        
        # Генерируем пароль
        password = ''.join(random.choice(chars) for _ in range(length))
        
        # Убедимся, что пароль содержит хотя бы по одному символу из каждой выбранной категории
        if use_lowercase and not any(c in self.lowercase for c in password):
            password = self._ensure_category(password, chars, self.lowercase)
        if use_uppercase and not any(c in self.uppercase for c in password):
            password = self._ensure_category(password, chars, self.uppercase)
        if use_digits and not any(c in self.digits for c in password):
            password = self._ensure_category(password, chars, self.digits)
        if use_symbols and use_symbols and not any(c in self.symbols for c in password):
            password = self._ensure_category(password, chars, self.symbols)
        
        return password
    
    def _ensure_category(self, password, all_chars, category):
        """
        Убедиться, что пароль содержит хотя бы один символ из указанной категории
        """
        idx = random.randint(0, len(password) - 1)
        char = random.choice(category)
        return password[:idx] + char + password[idx+1:]
    
    def generate_with_keywords(self, keywords, length=12, use_lowercase=True, 
                              use_uppercase=True, use_digits=True, use_symbols=False):
        """
        Сгенерировать пароль с использованием ключевых слов
        
        Предупреждение: использование ключевых слов может снизить безопасность
        """
        if not keywords:
            return self.generate(length, use_lowercase, use_uppercase, use_digits, use_symbols)
        
        # Объединяем ключевые слова и очищаем от пробелов
        keyword_part = ''.join(keywords.split())
        
        # Если часть из ключевых слов слишком длинная, обрезаем
        if len(keyword_part) >= length:
            return keyword_part[:length]
        
        # Генерируем оставшуюся часть пароля
        remaining_length = length - len(keyword_part)
        random_part = self.generate(remaining_length, use_lowercase, use_uppercase, use_digits, use_symbols)
        
        # Смешиваем ключевую часть и случайную часть
        password = keyword_part + random_part
        
        # Перемешиваем символы для большей безопасности
        password_list = list(password)
        random.shuffle(password_list)
        return ''.join(password_list)