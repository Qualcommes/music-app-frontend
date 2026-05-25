import flet as ft
import requests
import app_state  # <-- Импортируем наше локальное состояние сессии


def profile_view(page: ft.Page) -> ft.View:
    page.theme_mode = ft.ThemeMode.DARK
    
    # 1. Сначала проверяем ID в app_state (для Hot Reload), а затем в page
    user_id = app_state.current_user_id or getattr(page, "current_user_id", None)
    
    # Заглушки на случай, если бэкенд недоступен или пользователя нет
    username_value = "Загрузка..."
    email_value = "Загрузка..."
    avatar_source = app_state.current_user_avatar # Пробуем взять аватар сразу из кэша

    if not user_id:
        # Если зашли без ID — мягко редиректим на вход
        # Внутри функций представлений лучше делать это через отложенную задачу
        page.run_task(page.push_route, "/login")
        return ft.View(route="/profile", controls=[ft.Text("Перенаправление...")])

    # 2. Делаем запрос к нашему FastAPI бэкенду (только если кэш пустой или для подстраховки)
    if username_value == "Загрузка..." or username_value == "None" or not avatar_source:
        try:
            response = requests.get(f"http://127.0.0.1:8000/api/users/{user_id}")
            if response.status_code == 200:
                user_data = response.json()
                print(f"JSON: {user_data}")
                username_value = user_data.get("username", "Без имени")
                email_value = user_data.get("email", "")
                avatar_source = user_data.get("avatar_url") # Прямая ссылка на MinIO
                print(f"Сохраняем username, email, avatar: {username_value}, {email_value}, {avatar_source}.")
                # Синхронизируем кэш разработки, чтобы при возврате на main_view всё было актуально
                app_state.save_cache(user_id=user_id, username=username_value, avatar_url=avatar_source)
            else:
                username_value = "Пользователь не найден"
        except Exception as err:
            username_value = "Ошибка сервера"
            print(f"Не удалось связаться с бэкендом: {err}")
    else:
        # Если всё уже было в кэше — берем оттуда
        username_value = app_state.current_username or "Без имени"
        
    # 3. Элементы интерфейса
    # Если аватарки в MinIO нет, покажем стандартную иконку профиля
    if avatar_source:
        # ИСПРАВЛЕНО: Для версии 0.85.1 делаем круг через контейнер + clip_behavior, а fit задаем строкой "cover"
        avatar_image = ft.Container(
            content=ft.Image(
                src=avatar_source,
                width=150,
                height=150,
                fit="cover", # ИСПРАВЛЕНО: Строковый литерал вместо ft.ImageFit.COVER
            ),
            shape=ft.BoxShape.CIRCLE,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            width=250,
            height=250,
            margin=ft.Margin(top=20, bottom=10)
        )
    else:
        DEFAULT_AVATAR = "/images/wheels.jpg"
        profile_src = DEFAULT_AVATAR
        app_state.save_cache(user_id=user_id, avatar_url=profile_src, username=username_value)
        avatar_image = ft.Container(
            content=ft.Image(
                src=profile_src,
                width=150,
                height=150,
                fit="cover", # ИСПРАВЛЕНО: Строковый литерал вместо ft.ImageFit.COVER
            ),
            shape=ft.BoxShape.CIRCLE,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            width=250,
            height=250,
            margin=ft.Margin(top=20, bottom=10)
        )

    username_text = ft.Text(value=username_value, size=32)
    email_text = ft.Text(value=email_value, size=18, color=ft.Colors.GREY_400)
    

    def change_button_clicked(e):
        page.go("/edit")
    
    # ИСПРАВЛЕНО: ElevatedButton устарел с версии 0.80.0, заменяем на универсальный Button или оставляем flat-стиль
    # Но для сохранения работоспособности навигации используем безопасный вызов:
    change_button = ft.FilledButton(
        content="Изменить",
        on_click=change_button_clicked,
        style=ft.ButtonStyle(bgcolor="#029084", color=ft.Colors.BLACK)
    )

    # Собираем всё в один аккуратный Layout
    column = ft.Column(
                controls=[
                    avatar_image,
                    username_text,
                    #email_text,
                    ft.Container(height=20),
                    change_button
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
            

    return ft.View(
        route="/profile",
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[column],
        bgcolor="#260C14"
    )