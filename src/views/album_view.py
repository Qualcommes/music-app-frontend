import flet as ft
import requests



def album_view(page: ft.Page, album_id: str) -> ft.View:
    page.theme_mode = ft.ThemeMode.DARK

    album_column = ft.ListView(
        expand=True, # Занимает все доступное пространство
        spacing=10,
        padding=20,
        margin=ft.Margin(right=30)
    )

    # --- ИЗМЕНЕННЫЙ ОБРАБОТЧИК КЛИКА ---
    def card_clicked(e):
        # Получаем URL трека в MinIO из переданных в data данных
        track_url = e.control.data
        if hasattr(page, "audio_player"):
            page.audio_player.play_track(track_url)

    # --- ЗАПРОС К БЭКЕНДУ ЗА РЕАЛЬНЫМИ ТРЕКАМИ ---
    try:
        response = requests.get(f"http://127.0.0.1:8000/api/albums/{album_id}/tracks")
        
        if response.status_code == 200:
            tracks_list = response.json()  # Ожидаем список [ {"id": 1, "title": "...", "file_url": "..."}, ... ]
            
            for track in tracks_list:
                track_title = track.get("title", "Без названия")
                track_file_url = track.get("file_url", "")

                # 2. Блок описания (занимает больше места по горизонтали)
                album_info = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(track_title, weight=ft.FontWeight.BOLD, size=28, color=ft.Colors.BLACK),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=5,
                    ),
                    # Расширяем контейнер на все доступное пространство справа 
                    padding=ft.Padding(left=10, top=5, bottom=5, right=5),
                    height=100,
                    width=300,
                )
                
                # 3. Основная карточка
                album_card = ft.Container(
                    content=ft.Container(
                        content=ft.Row(
                            controls=[album_info,],
                            # Выравниваем по центру вертикали, чтобы они были одинаковыми визуально
                            vertical_alignment=ft.CrossAxisAlignment.CENTER, 
                        ),
                        padding=12,
                    ),
                    bgcolor="#928602",
                    data=track_file_url,  # Сохраняем URL аудиофайла в свойство data кнопки
                    on_click=card_clicked,
                )
                
                album_column.controls.append(album_card)
        else:
            album_column.controls.append(
                ft.Text("Альбом пуст или не найден", color=ft.Colors.RED, size=18)
            )
            
    except Exception as err:
        album_column.controls.append(
            ft.Text(f"Ошибка загрузки треков: {err}", color=ft.Colors.RED, size=18)
        )

    # --- КНОПКА НАЗАД (Визуал полностью сохранен) ---
    def go_back(e):
        page.go("/main")

    back_button = ft.ElevatedButton(
        content="Назад",
        on_click=go_back,
        bgcolor="#029084",
        color=ft.Colors.WHITE,
    )

    column = ft.Column(
        controls=[back_button, album_column],
        expand=True,
    )

    return ft.View(
        route=f"/album/{album_id}",
        controls=[column],
    )

