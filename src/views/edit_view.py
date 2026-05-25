import flet as ft
import requests



def edit_view(page: ft.Page) -> ft.View:
    page.theme_mode = ft.ThemeMode.DARK

    username_value = app_state.current_username
    # Заглушки на случай, если бэкенд недоступен или пользователя нет
    username_value = app_state.current_username
    email_value = "Загрузка..."
    avatar_source = app_state.current_user_avatar # Пробуем взять аватар сразу из кэша
    print(f"username, avatar_src: {username_value}, {avatar_source}")

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
    
    username_label = ft.Text(
        value=username_value,
    )
    

    def save_button_clicked(e):
        pass
    
    # ИСПРАВЛЕНО: ElevatedButton устарел с версии 0.80.0, заменяем на универсальный Button или оставляем flat-стиль
    # Но для сохранения работоспособности навигации используем безопасный вызов:
    change_button = ft.FilledButton(
        content="Сохранить",
        on_click=save_button_clicked,
        style=ft.ButtonStyle(bgcolor="#029084", color=ft.Colors.BLACK)
    )

    # Собираем всё в один аккуратный Layout
    column = ft.Column(
                controls=[
                    avatar_image,
                    username_label,
                    #email_text,
                    ft.Container(height=20),
                    change_button
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
            

    return ft.View(
        route="/edit",
        vertical_alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[column],
        bgcolor="#260C14"
    )