import flet as ft
import requests
import app_state  # <-- Импортируем новое состояние


def main_view(page: ft.Page) -> ft.View:
    page.theme_mode = ft.ThemeMode.DARK
    
    # Значение автоматически подставится из файла, если произошел Hot Reload!
    user_id = app_state.current_user_id or getattr(page, "current_user_id", None)
    profile_src = app_state.current_user_avatar
    print(f"[MAIN VIEW] Начальный аватар из кэша: {profile_src}")
    
    # --- ДЕЛАЕМ ЗАПРОС К API ДЛЯ ПОЛУЧЕНИЯ ДАННЫХ ПОЛЬЗОВАТЕЛЯ (ЕСЛИ НЕТ АВАТАРА) ---
    if user_id and not profile_src:
        try:
            print(f"[MAIN VIEW] Запрос профиля для user_id {user_id} к бэкенду...")
            user_response = requests.get(f"http://127.0.0.1:8000/api/users/{user_id}")
            
            if user_response.status_code == 200:
                user_data = user_response.json()
                profile_src = user_data.get("avatar_url")
                fetched_username = user_data.get("username") or app_state.current_username
                
                print(f"[MAIN VIEW] Успешно получено из API: avatar_url={profile_src}")
                
                # Пересохраняем обновленные данные в кэш разработки на диск
                app_state.save_cache(user_id=user_id, username=fetched_username, avatar_url=profile_src)
            else:
                print(f"[MAIN VIEW] Бэкенд вернул статус {user_response.status_code} при запросе пользователя")
        except Exception as e:
            print(f"[MAIN VIEW] Ошибка при запросе профиля пользователя: {e}")

    # Дефолтная заглушка, если у пользователя действительно нет аватара в бэкенде/MinIO
    DEFAULT_AVATAR = "/images/wheels.jpg"
    if not profile_src:
        profile_src = DEFAULT_AVATAR
        
    print(f"[MAIN VIEW] Итоговый путь аватарки для отображения: {profile_src}")

    def on_settings_clicked(e):
        page.run_task(page.push_route, "/profile")
    
    '''
    settings = ft.GestureDetector(
        content=ft.Container(
            content=ft.CircleAvatar(
                content=ft.Text("Settings.", size=11),
                color=ft.Colors.BLACK,
                bgcolor="#029084",
                width=70,
                height=70,
            ),
            shape=ft.BoxShape.CIRCLE,
        ),
        on_tap=on_settings_clicked,
        mouse_cursor="pointer"
    )
    '''

    profile = ft.GestureDetector(
        content=ft.Container(
            content=ft.Image(
                        src=profile_src,
                        width=70,
                        height=70,
                        fit="cover",
                    ),
            shape=ft.BoxShape.CIRCLE,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, # КРИТИЧЕСКИ ВАЖНО: обрезает углы картинки по форме круга
        ),
        on_tap=on_settings_clicked,
        mouse_cursor="pointer",
        margin=ft.Margin(right=20)

    )
    
    logo = ft.CircleAvatar(
        content=ft.Text("Logo."),
        color=ft.Colors.BLACK,
        bgcolor="#029084",
        width=50,
        height=50,
    )
    projects_name = ft.Text("Project's name.", color="#029084", size=42)
    
    search_field = ft.TextField(
        hint_text="введите ваш запрос.",
        hint_style=ft.TextStyle(color=ft.Colors.BLACK),
        shift_enter=True,
        content_padding=ft.Padding(0),
        max_lines=1,
        filled=True,
        width = 640,
        height= 70,
        bgcolor="#029084",
        color = "#000000",
        border_radius=0,
        cursor_color = ft.Colors.BLACK,
    )
    '''
    # Функция-обработчик изменения выбора
    def dropdown_changed(e):
        return

    # Создаем выпадающий список
    genre_dropdown = ft.Dropdown(
        label="Треки/альбомы",                  # Текст-подсказка сверху
        hint_text="Выберите вариант отображения", 
        width=300,
        bgcolor=ft.Colors.WHITE,       # Цвет фона раскрытого меню
        text_style=ft.TextStyle(color=ft.Colors.BLACK), # Цвет текста
        on_select=dropdown_changed,    # Событие при выборе
        # Элементы списка
        options=[
            ft.dropdown.Option("Альбомы"),
            ft.dropdown.Option("Треки"),
        ]
    )
    '''

    def card_clicked(e):
        # e.control.data содержит ID альбома
        album_id = e.control.data
        page.go(f"/album/{album_id}")

    # Создаем ListView для карточек альбомов
    cards_column = ft.ListView(expand=True, spacing=10, padding=20)

    # ДЕЛАЕМ ЗАПРОС К БЭКЕНДУ
    try:
        # Передаем user_id параметром для фильтрации приватности на бэкенде
        response = requests.get("http://127.0.0.1:8000/api/albums/",
                                 params={"user_id": user_id})
        
        if response.status_code == 200:
            albums_list = response.json()
            
            for album in albums_list:
                # Берём обложку из MinIO, если её нет — ставим заглушку
                cover_src = album.get("cover_url") or "https://via.placeholder.com/150"
                album_title = album.get("title", "Без названия")
                artist_name = album.get("artist_name") or "Неизвестный исполнитель"
                

                album_photo = ft.Container(
                    content=ft.Image(
                        src=cover_src,
                        width=150,
                        height=150,
                        fit="cover",
                    ),
                    bgcolor="#029084",
                    padding=8, # Этот отступ заставляет фон выпирать, создавая рамку
                    height=180,
                    width=180,
                    )
                
                album_info = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(album_title, weight=ft.FontWeight.BOLD, size=28, color=ft.Colors.BLACK),
                            ft.Text(artist_name, size=21, color=ft.Colors.BLACK),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=5,
                    ),
                    padding=ft.Padding(left=10, top=5, bottom=5, right=5),
                    height=200,
                    width=700,
                )
                
                album_card = ft.Container(
                    content=ft.Container(
                        content=ft.Row(
                            controls=[album_photo, album_info],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER, 
                        ),
                        padding=12,
                    ),
                    bgcolor="#928602",
                    data=album["id"],  # Исправлено: берем id из текущего словаря цикла
                    on_click=card_clicked,
                )
                
                cards_column.controls.append(album_card)
        else:
            cards_column.controls.append(ft.Text("Не удалось загрузить альбомы", color=ft.Colors.RED))
            
    except Exception as err:
        cards_column.controls.append(ft.Text(f"Ошибка соединения с сервером: {err}", color=ft.Colors.RED))

    # СБОРКА ИНТЕРФЕЙСА (вынесена за пределы try-блока)
    logo_panel = ft.Row(controls=[logo, projects_name])
    search_panel = ft.Row(controls=[search_field])
    left_top_panel = ft.Column(controls=[logo_panel, search_panel])
    settings_panel = ft.Column(controls=[profile]) #settings
    
    top_panel = ft.Row(
        controls=[left_top_panel, settings_panel],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    column = ft.Column(
        #controls=[top_panel, genre_dropdown, cards_column],
        controls=[top_panel, cards_column],
        expand=True,
    )

    return ft.View(
        route="/main",
        controls=[column],
        bgcolor="#260C14",
        padding=10,
    )
'''
def main_view(page: ft.Page) -> ft.View:
    page.theme_mode = ft.ThemeMode.DARK

    def on_settings_clicked(e):
            page.run_task(page.push_route, "/settings")

    settings = ft.GestureDetector(
         content=
            ft.Container(
              content = ft.CircleAvatar(
                   content=ft.Text("Settings."),
                   color=ft.Colors.BLACK,
                   bgcolor="#029084",
                   width=80,
                   height=80,
                ),
            shape=ft.BoxShape.CIRCLE,
            ),
            on_tap=on_settings_clicked,
            mouse_cursor = "pointer"
        )
    
    logo = ft.CircleAvatar(
                content=ft.Text("Logo."),
                color=ft.Colors.BLACK,
                bgcolor="#029084",
                width=50,
                height=50,
            )
    projects_name = ft.Text("Project's name.", color="#029084", size=42)
    search_field = ft.TextField(
        hint_text="введите ваш запрос.",
        hint_style=ft.TextStyle(color=ft.Colors.BLACK),
        shift_enter=True,
        content_padding=ft.Padding(0),
        max_lines=1,
        filled=True,
        width = 800,
        height= 70,
        bgcolor="#029084",
        color = "#000000",
        border_radius=0,
        cursor_color = ft.Colors.BLACK,
    )

    def card_clicked(e):
            clicked_id = e.control.data
            page.run_task(page.push_route, f"/album/{clicked_id}")

    
    # Работа с карточками
    #=======================================================================================
    # Данные для карточек (замените URL-адреса на свои при необходимости)
    cards_data = [
        {
            "id": "0",
            "img": "/images/LZ.jpg",
            "title": "Led Zeppelin III",
            "desc": "1971"
        },
        {
            "id": "1",
            "img": "/images/Demon.jpg",
            "title": "The Unexpected Guest",
            "desc": "1982"
        },
        {
            "id": "2",
            "img": "/images/wheels.jpg",
            "title": "Wheels of Fire",
            "desc": "1968"
        },
        {
            "id": "3",
            "img": "/images/Opus.jpg",
            "title": "Opus Eponymous",
            "desc": "2011"
        },
        {
              "id": "4",
              "img": "/images/BS.jpg",
              "title": "Paranoid (Black Sabbath)",
              "desc": "1970"
        },
        {
              "id": "5",
              "img": "/images/KT.jpg",
              "title": "Князь тишины (Наутилус Помпилиус)",
              "desc": "1988"
        }
        ]
    


#===============================================================================================================================
    cards_column = ft.ListView(
        expand=True, # Занимает все доступное пространство
        spacing=10,
        padding=20,
        margin=ft.Margin(right=30)
    )

    for data in cards_data:
        # 1. Подкарточка (Рамка для картинки)
        album_photo = ft.Container(
            content=ft.Image(
                src=data['img'],
                width=84,
                height=84,
                border_radius=0,
            ),
            bgcolor="#029084",
            padding=8, # Этот отступ заставляет фон выпирать, создавая рамку
            height=180,
            width=180,
        )
        
        # 2. Блок описания (занимает больше места по горизонтали)
        album_info = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(data["title"], weight=ft.FontWeight.BOLD, size=28, color=ft.Colors.BLACK),
                    ft.Text(data["desc"], size=24, color=ft.Colors.BLACK),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=5,
            ),
            # Расширяем контейнер на все доступное пространство справа 
            padding=ft.Padding(left=10, top=5, bottom=5, right=5),
            height=200,
            width=700,
        )
        
        # 3. Основная карточка
        album_card = ft.Container(
            content=ft.Container(
                content=ft.Row(
                    controls=[album_photo, album_info,],
                    # Выравниваем по центру вертикали, чтобы они были одинаковыми визуально
                    vertical_alignment=ft.CrossAxisAlignment.CENTER, 
                ),
                padding=12,
            ),
            bgcolor="#928602",
            data=data["id"],
            on_click=card_clicked,
        )
        
        cards_column.controls.append(album_card)
    #========================================================================================

    logo_panel = ft.Row(
        controls=[logo, projects_name]
    )
    search_panel = ft.Row(
        controls=[search_field]
    )
    left_top_panel = ft.Column(
        controls=[logo_panel, search_panel],
    )
    settings_panel= ft.Column(
        controls=[settings]
    )
    top_panel = ft.Row(
        controls=[left_top_panel, settings_panel],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, # Красиво разнесет логотип и настройки по краям
    )

    column = ft.Column(
        controls=[top_panel, cards_column,],
        expand=True,
    )
    return ft.View(
        route="/main",
        controls=[column],
        bgcolor="#260C14",
        padding=10,
    )
    '''