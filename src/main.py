import flet as ft
import re
# Импортируем наши представления
from views.login_view import login_view
from views.main_view import main_view
from views.settings_view import settings_view
from views.album_view import album_view
from views.registration_view import registration_view
from views.profile_view import profile_view
from views.edit_view import edit_view
# Импортируем наш обновленный плеер-компонент
from views.player_view import AudioPlayer

CURRENT_USER_ID = None

def main(page: ft.Page):
    print(f"[MAIN] ID страницы: {id(page)}")

    page.title = "Music service."
    page.theme_mode = ft.ThemeMode.DARK # Для музыкальных сервисов темная тема — стандарт
    page.window.width = 1280       # Начальная ширина
    page.window.height = 800       # Начальная высота
    
    page.window.min_width = 1024   # Минимальная ширина (меньше нельзя сжать)
    page.window.min_height = 768   # Минимальная высота
    
    page.window.max_width = 1920   # Максимальная ширина (опционально)
    page.window.max_height = 1080  # Максимальная высота (опционально)

    # Инициализируем глобальный плеер и сохраняем ссылку в объект page,
    # чтобы иметь к нему доступ из других файлов (views)
    # Внутри функции main(page: ft.Page) в main.py:
    page.audio_player = AudioPlayer(page) # Передаем page, внутри класса он примется как app_page
    # Добавляем в overlay именно wrapper плеера!
    page.overlay.append(
        ft.Stack(
            controls=[
                page.audio_player
            ],
            bottom=10,  # Прижимаем стек к низу
            left=10,    # Отступ слева
            right=10,   # Отступ справа
            width=100,
            height=100,
        )
    )
    page.update()


    # Функция, которая строго строит экран на основе переданного пути
    def render_views(current_route: str):
        
        page.views.clear()
        
        # 1. Экран авторизации
        if current_route == "/login" or current_route == "/":
            page.audio_player.visible = False
            page.views.append(login_view(page))
            
        # 2. Главный экран
        elif current_route == "/main":
            page.views.append(main_view(page))
            
        # 3. Экран альбома (поддерживает динамические параметры)
        #elif current_route.startswith("/album"):
            # Строим стек: Главная -> Альбом
            #page.views.append(main_view(page))
            #page.views.append(album_view(page))
            
        # 4. Экран плеера
        #elif current_route.startswith("/player"):
            # Строим стек: Главная -> Альбом -> Плеер
            #page.views.append(main_view(page))
            #page.views.append(album_view(page))
            #page.views.append(player_view(page))
        
        # 5. Экран настроек
        elif current_route.startswith("/settings"):
            # Строим стек: Главная -> Настройки
            page.views.append(main_view(page))
            page.views.append(settings_view(page))

        # 6. Экран конкретного альбома с id.
        elif match := re.match(r"^/album/(\d+)$", current_route):
            # Извлекаем ID из группы захвата (первые скобки в RegEx)
            album_id = match.group(1)
            # Строим стек: Главная -> Альбом
            page.views.append(main_view(page))
            page.views.append(album_view(page, album_id))
        
        # 7. Экран регистрации пользователя
        elif current_route.startswith("/registration"):
            page.views.append(registration_view(page))
        
        # 8. Профиль пользователя
        elif current_route.startswith("/profile"):
            page.views.append(profile_view(page))
        
        # 9. Изменение профиля
        elif current_route.startswith("/edit"):
            page.views.append(edit_view(page))
        page.update()

    # Обработчик изменения маршрута (теперь он безопасен, так как не вызывает push_route)
    def route_change(e: ft.RouteChangeEvent):
        print(f"[ROUTE CHANGE] Переход на: {e.route}")
        render_views(e.route)

    # Обработчик кнопки "Назад"
    def view_pop(e: ft.ViewPopEvent):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            # Безопасно меняем маршрут без run_task
            page.route = top_view.route
            page.update()
    
    # Привязываем события к странице
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # --- Старт приложения и Hot Reload ---
    # Если это Hot Reload (маршрут уже есть), или первый запуск (маршрута нет)
    initial_route = page.route if page.route else "/login"
    print(f"[START/RELOAD] Инициализация маршрута: {initial_route}")
    
    # Принудительно отрисовываем UI при старте/перезапуске
    render_views(initial_route)

#if __name__ == "__main__":
#    ft.run(main)

if __name__ == "__main__":
    # Указываем путь к папке assets относительно корня, где запускается проект
    #ft.app(target=main, assets_dir="src/assets")
    ft.run(main)