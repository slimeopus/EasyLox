"""
Модуль для управления паролями и шифрования данных
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

# Импортируем библиотеку для шифрования
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import uuid


class PasswordManager:
    """
    Класс для управления операциями с паролями
    """
    
    def __init__(self, data_file: str = "passwords.json", password_file: str = "master_password.json"):
        self.data_file = data_file
        self.password_file = password_file
        self.passwords = []  # Список для хранения паролей
        self.fernet = None  # Ключ шифрования
        self.load_data()  # Загружаем данные при инициализации

    def clear_memory(self) -> None:
        """
        Явно очистить чувствительные данные из памяти
        """
        if hasattr(self, 'passwords'):
            for password_entry in self.passwords:
                if 'password' in password_entry:
                    password_entry['password'] = '***REDACTED***'
            self.passwords.clear()
        self.fernet = None
    
    def add_password(self, service: str, login: str, password: str, 
                    category: str = "", notes: str = "") -> bool:
        """
        Добавить новый пароль
        
        Args:
            service: Название сервиса
            login: Логин
            password: Пароль
            category: Категория пароля
            notes: Дополнительные заметки
        
        Returns:
            bool: True если успешно добавлен
        """
        # Проверка на пустые обязательные поля
        if not service or not login:
            return False
        
        # Создаем новую запись
        password_entry = {
            'id': self._generate_id(),
            'service': service,
            'login': login,
            'password': password,
            'category': category,
            'notes': notes,
            'created_date': datetime.now().isoformat(),
            'modified_date': datetime.now().isoformat()
        }
        
        self.passwords.append(password_entry)
        self.save_data()  # Сохраняем данные
        return True
    
    def get_all_passwords(self) -> List[Dict]:
        """
        Получить все пароли
        
        Returns:
            List[Dict]: Список всех паролей
        """
        return self.passwords
    
    def get_password_by_id(self, password_id: str) -> Optional[Dict]:
        """
        Получить пароль по ID
        
        Args:
            password_id: ID пароля
        
        Returns:
            Optional[Dict]: Пароль или None если не найден
        """
        for password in self.passwords:
            if password['id'] == password_id:
                return password
        return None
    
    def search_passwords(self, query: str) -> List[Dict]:
        """
        Поиск паролей по запросу
        
        Args:
            query: Поисковый запрос
        
        Returns:
            List[Dict]: Список найденных паролей
        """
        if not query:
            return self.passwords
            
        query = query.lower()
        return [p for p in self.passwords 
                if query in p['service'].lower() or 
                   query in p['login'].lower() or
                   query in p['category'].lower()]
    
    def update_password(self, password_id: str, service: str = None, 
                       login: str = None, password: str = None, 
                       category: str = None, notes: str = None) -> bool:
        """
        Обновить пароль
        
        Args:
            password_id: ID пароля для обновления
            service: Новое название сервиса
            login: Новый логин
            password: Новый пароль
            category: Новая категория
            notes: Новые заметки
        
        Returns:
            bool: True если успешно обновлен
        """
        for i, p in enumerate(self.passwords):
            if p['id'] == password_id:
                if service is not None:
                    self.passwords[i]['service'] = service
                if login is not None:
                    self.passwords[i]['login'] = login
                if password is not None:
                    self.passwords[i]['password'] = password
                if category is not None:
                    self.passwords[i]['category'] = category
                if notes is not None:
                    self.passwords[i]['notes'] = notes
                
                self.passwords[i]['modified_date'] = datetime.now().isoformat()
                self.save_data()  # Сохраняем изменения
                return True
        return False
    
    def delete_password(self, password_id: str) -> bool:
        """
        Удалить пароль по ID
        
        Args:
            password_id: ID пароля для удаления
        
        Returns:
            bool: True если успешно удален
        """
        for i, p in enumerate(self.passwords):
            if p['id'] == password_id:
                del self.passwords[i]
                self.save_data()  # Сохраняем изменения
                return True
        return False
    
    def _generate_id(self) -> str:
        """
        Сгенерировать уникальный ID для пароля
        
        Returns:
            str: Уникальный ID
        """
        return str(uuid.uuid4())
    
    def load_data(self) -> None:
        """
        Загрузить данные из файла
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    
                # Если файл пустой или содержит только пробелы
                if not content:
                    self.passwords = []
                    return
                    
                # Пытаемся расшифровать и загрузить данные
                if self.fernet:
                    decrypted_data = self.fernet.decrypt(content.encode()).decode('utf-8')
                    self.passwords = json.loads(decrypted_data)
                else:
                    # Ключ шифрования недоступен — не можем расшифровать
                    self.passwords = []
            else:
                self.passwords = []
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            self.passwords = []
    
    def save_data(self) -> None:
        """
        Сохранить данные в файл
        """
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                data = json.dumps(self.passwords, ensure_ascii=False, indent=2)
                if self.fernet:
                    # Шифруем данные перед записью
                    encrypted_data = self.fernet.encrypt(data.encode()).decode('utf-8')
                    f.write(encrypted_data)
                else:
                    # Если мастер-пароль установлен, но ключ шифрования недоступен, не сохраняем данные в открытом виде
                    raise RuntimeError("Cannot save data: encryption key is missing")
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")
    
    # Константы для PBKDF2
    PBKDF2_ITERATIONS = 100000  # Можно увеличить в будущем
    PBKDF2_ALGORITHM = hashes.SHA256()
    PBKDF2_KEY_LENGTH = 32
    
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """
        Вывести ключ шифрования из мастер-пароля и соли
        
        Args:
            password: Мастер-пароль
            salt: Соль для ключа
        
        Returns:
            bytes: Ключ шифрования
        """
        kdf = PBKDF2HMAC(
            algorithm=self.PBKDF2_ALGORITHM,
            length=self.PBKDF2_KEY_LENGTH,
            salt=salt,
            iterations=self.PBKDF2_ITERATIONS
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def set_master_password(self, password: str) -> bool:
        """
        Установить мастер-пароль
        
        Args:
            password: Пароль для установки
        
        Returns:
            bool: True если успешно установлен
        """
        try:
            # Генерируем соль
            salt = os.urandom(16)
            # Выводим ключ шифрования
            key = self._derive_key(password, salt)
            # Инициализируем Fernet
            self.fernet = Fernet(key)
            # Генерируем случайный маркер
            verification_token = os.urandom(32)
            # Шифруем маркер с помощью ключа
            encrypted_token = self.fernet.encrypt(verification_token)
            # Сохраняем соль, зашифрованный маркер и параметры PBKDF2 в файл
            with open(self.password_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "salt": base64.b64encode(salt).decode('utf-8'),
                    "encrypted_token": base64.b64encode(encrypted_token).decode('utf-8'),
                    "pbkdf2_iterations": self.PBKDF2_ITERATIONS,
                    "pbkdf2_algorithm": "SHA256"
                }, f, ensure_ascii=False, indent=2)
            # Сохраняем текущее состояние данных в зашифрованном виде
            self.save_data()
            return True
        except Exception as e:
            print(f"Ошибка установки мастер-пароля: {e}")
            return False
    
    def verify_master_password(self, password: str) -> bool:
        """
        Проверить мастер-пароль
        
        Args:
            password: Пароль для проверки
        
        Returns:
            bool: True если пароль верный
        """
        try:
            with open(self.password_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                saved_salt = data.get("salt")
                saved_encrypted_token = data.get("encrypted_token")
                saved_iterations = data.get("pbkdf2_iterations", self.PBKDF2_ITERATIONS)
                
            if not saved_salt or not saved_encrypted_token:
                return False
            
            # Восстанавливаем параметры PBKDF2
            salt = base64.b64decode(saved_salt)
            
            # Выводим ключ шифрования из введенного пароля и сохраненной соли
            kdf = PBKDF2HMAC(
                algorithm=self.PBKDF2_ALGORITHM,
                length=self.PBKDF2_KEY_LENGTH,
                salt=salt,
                iterations=saved_iterations
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            self.fernet = Fernet(key)
            
            # Пытаемся расшифровать сохраненный маркер
            try:
                encrypted_token = base64.b64decode(saved_encrypted_token)
                self.fernet.decrypt(encrypted_token)
            except Exception:
                return False  # Ошибка расшифровки — неверный пароль
            
            return True
        except Exception as e:
            print(f"Ошибка проверки мастер-пароля: {e}")
            return False
    
    def is_master_password_set(self) -> bool:
        """
        Проверить, установлен ли мастер-пароль
        
        Returns:
            bool: True если мастер-пароль установлен
        """
        try:
            if os.path.exists(self.password_file):
                with open(self.password_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Проверяем наличие обязательных полей для нового формата
                    if "salt" in data and "encrypted_token" in data:
                        return True  # Мастер-пароль установлен
            return False  # Файл не существует или не содержит необходимых данных
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка проверки наличия мастер-пароля: {e}")
            return False