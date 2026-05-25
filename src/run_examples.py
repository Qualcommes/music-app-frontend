# python_example.py
from backend.database import init_db, SessionLocal, engine, Base
from backend import crud, models

cards_data = [
    {"id": "0", "img": "/images/LZ.jpg", "title": "Led Zeppelin III", "desc": "1971", "artist": "Led Zeppelin"},
    {"id": "1", "img": "/images/Demon.jpg", "title": "The Unexpected Guest", "desc": "1982", "artist": "Demon"},
    {"id": "2", "img": "/images/wheels.jpg", "title": "Wheels of Fire", "desc": "1968", "artist": "Cream"},
    {"id": "3", "img": "/images/Opus.jpg", "title": "Opus Eponymous", "desc": "2011", "artist": "Ghost"},
    {"id": "4", "img": "/images/BS.jpg", "title": "Paranoid", "desc": "1970", "artist": "Black Sabbath"},
    {"id": "5", "img": "/images/KT.jpg", "title": "Князь тишины", "desc": "1988", "artist": "Наутилус Помпилиус"}
]

def run_demo():
    print("Инициализация базы данных...")
    models.Album.__table__.drop(bind=engine, checkfirst=True)
    # 1. Создаем таблицы, если их еще нет в PostgreSQL
    init_db()

    # 2. Открываем сессию для работы с данными
    db = SessionLocal()

    try:
        # 1. Гарантируем наличие администратора с ID = 6
        admin_id = 6
        admin = db.query(models.User).filter_by(id=admin_id).first()
        
        if not admin:
            print(f"Администратор с ID {admin_id} не найден. Создаем...")
            # Принудительно задаем ID через объект модели, так как это инициализация
            admin = models.User(
                id=admin_id,
                username="admin",
                email="admin@1.gmail.com",
                password_hash="$2b$12$e9QvkRKnGnoBGBz31bL8ye2DkGHMdmNSPDUg3osZZjaChQzUZ9hla"
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print(f"Успешно создан пользователь: {admin.username} (ID: {admin.id})")
        else:
            print(f"Администратор {admin.username} (ID: {admin.id}) уже существует.")

        # 2. Наполнение альбомами
        print("\nЗаполнение базы данных альбомами...")
        for card in cards_data:
            title = card["title"]
            artist = card["artist"]
            year = card["desc"]
            if year is None:
                year = "неизвестный год"
            
            # Проверяем, нет ли уже такого альбома в базе (по названию и артисту)
            existing_album = db.query(models.Album).filter_by(title=title, artist_name=artist).first()
            
            if not existing_album:
                new_album = models.Album(
                    title=title,
                    artist_name=artist,
                    uploader_id=admin.id,
                    is_public=True,  # Делаем публичными, чтобы их видели все во views
                    year = int(year),
                )
                db.add(new_album)
                print(f" Добавлен альбом: {artist} — {title}")
            else:
                print(f" Альбом уже существует: {artist} — {title}")
                
        db.commit()
        print("\nВсе доступные альбомы успешно синхронизированы с БД!")

    except Exception as e:
        db.rollback()
        print(f"Произошла ошибка при заполнении БД: {e}")
    finally:
        db.close()
        print("Сессия закрыта.")

if __name__ == "__main__":
    run_demo()