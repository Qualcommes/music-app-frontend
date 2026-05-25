# Файл: src/app_state.py
import json
import os

# Переменные в оперативной памяти приложения
current_user_id = None
current_user_avatar = None
current_username = None  # <-- Новая переменная для имени пользователя

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, ".cache")
CACHE_FILE = os.path.join(CACHE_DIR, "dev_session.json")


def load_cache():
    """Загружает сохраненные данные профиля из кэша разработки"""
    global current_user_id, current_user_avatar, current_username
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                current_user_id = data.get("user_id")
                current_user_avatar = data.get("avatar_url")
                current_username = data.get("username")  # <-- Читаем username
                print(f"[CACHE] Восстановлено: id={current_user_id}, username={current_username}, avatar={current_user_avatar}")
        except Exception as e:
            print(f"[CACHE] Ошибка чтения кэша: {e}")
            clear_memory()
    else:
        clear_memory()


def save_cache(user_id: int, username: str = None, avatar_url: str = None):
    """Сохраняет ID, имя и аватар на жесткий диск в .cache/"""
    global current_user_id, current_user_avatar, current_username
    current_user_id = user_id
    current_username = username
    current_user_avatar = avatar_url

    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        payload = {
            "user_id": user_id,
            "username": username,  # <-- Добавляем в JSON-файл
            "avatar_url": avatar_url
        }
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=4)
        print(f"[CACHE] Данные успешно сохранены на диск!")
    except Exception as e:
        print(f"[CACHE] Не удалось сохранить кэш: {e}")


def clear_memory():
    global current_user_id, current_user_avatar, current_username
    current_user_id = None
    current_user_avatar = None
    current_username = None


# Автоматическая загрузка кэша при старте/Hot Reload
load_cache()