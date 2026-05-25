# views/player_view.py
import flet as ft

class AudioPlayer(ft.Container):
    def __init__(self, app_page: ft.Page):
        super().__init__()
        self.app_page = app_page
        
        # 1. В современных версиях Flet плеер инициализируется напрямую через страницу,
        # либо мы создаем его объект, если он доступен в корне модуля.
        # Проверим самый стабильный для 2026 года вариант:
        try:
            self.audio_engine = ft.Audio(
                src="",
                autoplay=False,
                volume=1.0,
                on_state_change=self._on_status_changed
            )
            self.app_page.overlay.append(self.audio_engine)
        except AttributeError:
            # Если в 0.85.1 его зашили прямо в медиа-плагины страницы:
            # Используем фабричный метод (если ft.Audio выдает ошибку)
            raise RuntimeError("Не удалось инициализировать ft.Audio. Проверь синтаксис ft.Audio в документации твоей версии.")

        # 2. Элементы интерфейса плеера
        self.track_title = ft.Text("Название трека", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD)
        self.play_btn = ft.IconButton(
            icon=ft.Icons.PLAY_ARROW_ROUNDED, 
            icon_color="#029084", 
            icon_size=40,
            on_click=self.toggle_play
        )
        
        # 3. Настройки визуального контейнера панели
        self.bgcolor = "#1A080E"
        self.height = 90
        self.padding = ft.Padding(left=20, right=20)
        self.visible = False
        
        # Позиционирование панели в самом низу экрана
        self.bottom = 0
        self.left = 0
        self.right = 0
        self.expand = True
        
        # Собираем UI плеера
        self.content = ft.Row(
            controls=[
                # Блок информации (Слева)
                ft.Container(
                    content=ft.Column(
                        controls=[
                            self.track_title,
                            ft.Text("Исполнитель", color="#029084", size=12),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=2,
                    ),
                    width=250,
                ),
                # Кнопки управления (Центр)
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.IconButton(icon=ft.Icons.SKIP_PREVIOUS, icon_color=ft.Colors.WHITE),
                            self.play_btn,
                            ft.IconButton(icon=ft.Icons.SKIP_NEXT, icon_color=ft.Colors.WHITE),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    expand=True,
                ),
                # Кнопка закрытия (Справа)
                ft.IconButton(
                    icon=ft.Icons.CLOSE, 
                    icon_color=ft.Colors.RED_400,
                    on_click=self.close_player
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def play_track(self, track_url: str, track_title: str = "Без названия"):
        """Метод запускает аудиофайл по URL и обновляет UI плеера"""
        print(f"[PLAYER] Запуск трека: {track_title} -> {track_url}")
        
        self.track_title.value = track_title
        self.visible = True
        self.app_page.update()
        
        self.audio_engine.src = track_url
        self.audio_engine.update()
        self.audio_engine.play()
        
        self.play_btn.icon = ft.Icons.PAUSE_ROUNDED
        self.play_btn.update()

    def toggle_play(self, e):
        """Ставит на паузу или возобновляет воспроизведение"""
        if self.play_btn.icon == ft.Icons.PAUSE_ROUNDED:
            self.audio_engine.pause()
            self.play_btn.icon = ft.Icons.PLAY_ARROW_ROUNDED
        else:
            self.audio_engine.resume()
            self.play_btn.icon = ft.Icons.PAUSE_ROUNDED
        self.play_btn.update()

    def close_player(self, e):
        """Останавливает музыку и прячет панель плеера"""
        self.audio_engine.pause()
        self.visible = False
        self.app_page.update()

    def _on_status_changed(self, e):
        pass

'''
class AudioPlayer(ft.Container):
    # Изменяем имя аргумента на app_page, чтобы избежать конфликта со встроенным свойством page
    def __init__(self, app_page: ft.Page):
        super().__init__()
        self.app_page = app_page
        
        # Ссылки на элементы, которые будем менять динамически
        self.track_title = ft.Text("Название трека", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD)
        
        # Настройки самого контейнера плеера
        self.bgcolor = "#1A080E"  # Чуть темнее основного фона
        #self.bgcolor=ft.Colors.TRANSPARENT
        #self.border = ft.Border(1, "#029084")
        self.height = 90
        self.padding = ft.Padding(left=20, right=20)
        self.visible = False

        # Позиционирование в overlay (прижимаем к низу на всю ширину)
        self.bottom = 10
        self.left = 10
        self.right = 10 

        self.content = ft.Column(
            controls=[
                self.track_title,
                ft.Text("Hello!", size=10, color=ft.Colors.WHITE)
            ],
        )


        # Простейший интерфейс плеера
        self.content = ft.Row(
            controls=[
                # Блок с информацией о треке
                ft.Column(
                    controls=[
                        self.track_title,
                        ft.Text("Исполнитель", color="#029084", size=12),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2,
                ),
                # Кнопки управления посередине
                ft.Container(
                    content=ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.Icons.SKIP_PREVIOUS, icon_color=ft.Colors.WHITE),
                        ft.IconButton(icon=ft.Icons.PLAY_ARROW_ROUNDED, icon_color="#029084", icon_size=40),
                        ft.IconButton(icon=ft.Icons.SKIP_NEXT, icon_color=ft.Colors.WHITE),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    expand=True,
                ),
                # Кнопка закрытия плеера справа
                ft.IconButton(
                    icon=ft.Icons.CLOSE, 
                    icon_color=ft.Colors.RED_400,
                    on_click=self.close_player
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN, # Распределяет компоненты: Слева - Центр - Справа
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            #height=90,
        )

    def play_track(self, track_name: str):
        """Метод для запуска трека из любого места приложения"""
        self.track_title.value = track_name
        # Включаем видимость обёртки, которая сидит в overlay
        self.visible = True
        self.update()
        self.app_page.update()

    def close_player(self, e):
        """Прячет плеер при нажатии на крестик"""
        self.visible = False
        self.update()
        self.app_page.update()
        '''


'''
# Простейший интерфейс плеера
        self.content = ft.Row(
            controls=[
                # Блок с информацией о треке
                ft.Column(
                    controls=[
                        self.track_title,
                        ft.Text("Исполнитель", color="#029084", size=12),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=2,
                ),
                # Кнопки управления посередине
                ft.Container(
                    content=ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.Icons.SKIP_PREVIOUS, icon_color=ft.Colors.WHITE),
                        ft.IconButton(icon=ft.Icons.PLAY_ARROW_ROUNDED, icon_color="#029084", icon_size=40),
                        ft.IconButton(icon=ft.Icons.SKIP_NEXT, icon_color=ft.Colors.WHITE),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    expand=True,
                ),
                # Кнопка закрытия плеера справа
                ft.IconButton(
                    icon=ft.Icons.CLOSE, 
                    icon_color=ft.Colors.RED_400,
                    on_click=self.close_player
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN, # Распределяет компоненты: Слева - Центр - Справа
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            width=100,
            height=90,
        )
        '''