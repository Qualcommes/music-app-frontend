import flet as ft
import requests
import app_state  # <-- Импортируем наше новое уникальное состояние


def login_view(page: ft.Page) -> ft.View:
    page.theme_mode = ft.ThemeMode.DARK
    print(f"[LOGIN VIEW] ID страницы: {id(page)}")
    MY_BRAND_COLOR = "#260C14" 
    
    custom_style = ft.ButtonStyle(
        # Цвет текста
        color=ft.Colors.WHITE,
        # Цвет фона (можно использовать разные цвета для разных состояний, но об этом ниже)
        bgcolor= "#029084",
        # Расстояние между текстом и границами кнопки
        padding=0, 
        # Настройка формы и скругления углов
        shape=ft.RoundedRectangleBorder(radius=0),
        # Настройка границы (цвет и толщина)
        side=ft.BorderSide(1, ft.Colors.BLACK),
        # Размер тени
        elevation=0,
    )

    projects_name = ft.Text(
        value ="Project's name.",
        color = "#029084",
        size = 43,
    )

    password_field_ref = ft.Ref[ft.TextField]()

    def toggle_password_visibility(e):
        # Переключаем видимость текста
        password_field_ref.current.password = not password_field_ref.current.password
        # Меняем иконку в зависимости от состояния
        e.control.icon = (
            ft.Icons.VISIBILITY_OFF if password_field_ref.current.password else ft.Icons.VISIBILITY
        )
        page.update()

    password_field = ft.TextField( 
        hint_text="ваш пароль",
        ref=password_field_ref,
        hint_style=ft.TextStyle(color=ft.Colors.BLACK),
        shift_enter=True,
        max_lines=1,
        filled=True,
        width = 400,
        height = 70,
        bgcolor="#029084",
        color = "#000000",
        border_radius=0,
        password=True,
        cursor_color = ft.Colors.BLACK,
        content_padding=ft.Padding(top=0, bottom=0, left=10),
        suffix=ft.IconButton(
                icon=ft.Icons.VISIBILITY_OFF,
                icon_color=ft.Colors.BLACK, # <--- Цвет иконки «глаза»
                on_click=toggle_password_visibility,
                # --- РЕШЕНИЕ ПРОБЛЕМЫ С РАЗМЕРОМ ---
                icon_size=15,  # Уменьшаем сам размер иконки (по умолчанию около 24)
                padding=0,     # Сбрасываем внутренние отступы кнопки до нуля
                margin=0,
                visual_density=ft.VisualDensity.COMPACT, # Максимально сжимаем контейнер кнопки
            )
        )

    login_field = ft.TextField( 
        hint_text="ваш логин",
        hint_style=ft.TextStyle(color=ft.Colors.BLACK),
        shift_enter=True,
        content_padding=ft.Padding(top=0, bottom=0, left=10),
        max_lines=1,
        filled=True,
        width = 400,
        height= 70,
        bgcolor="#029084",
        color = "#000000",
        border_radius=0,
        cursor_color = ft.Colors.BLACK,
        )

    
    def clicked_enter(e):
        # Берем данные из полей ввода
        email = login_field.value 
        password = password_field_ref.current.value
        # Базовая проверка на пустоту
        if not email or not password:
            # Тут можно вывести Snackbar с просьбой заполнить поля
            print("Заполните все поля!")
            return

        try:
            # Отправляем данные на проверку (используем data=, так как бэкенд ждет Form)
            response = requests.post(
                "http://127.0.0.1:8000/api/auth/login",
                data={
                    "email": email, 
                    "password": password
                }
            )

            if response.status_code == 200:
                # Бэкенд пустил! Достаем данные из ответа
                data = response.json()
                user_id = data.get("user_id")

                # Сохраняем и в память приложения, и одновременно на жесткий диск в .cache/
                app_state.save_cache(user_id=user_id)
                page.current_user_id = user_id

                print(f"user_id={user_id}")
            
                # Переводим пользователя на главную страницу или профиль
                # (Убедись, что маршрут "/main" или "/profile" настроен у тебя в маршрутизаторе)
                page.go("/main") 
            
            else:
                # Бэкенд не пустил (ошибка 400 или 404)
                error_detail = response.json().get("detail", "Ошибка авторизации")
            
                # Тут в идеале нужно вывести текст в твой label для ошибок:
                error_label.value = error_detail
                error_label.visible = True
                page.update()
                print(f"Ошибка входа: {error_detail}")

        except requests.exceptions.RequestException as err:
            print(f"Сервер недоступен: {err}")

    access_button = ft.FilledButton(
        content=ft.Text(
            value="Войти",
            size=41, # Прямое управление размером внутри ft.Text
            weight=ft.FontWeight.BOLD,
        ),
        style = custom_style,
        width = 400,
        height = 70,
        on_click=clicked_enter,
    )


    error_label = ft.Text(
        value="Incorrect login or password.",
        color=ft.Colors.RED,
        size=21,
        visible=False,
    )

    top_logo_area=ft.Column(
        controls=[projects_name],
        margin=ft.Margin(top=20, bottom=110),
    )

    middle_auth_area=ft.Column(
        controls=[login_field, password_field],
        margin=ft.Margin(top=20, bottom=90),
    )

    bottom_entry_area=ft.Column(
        controls=[access_button, error_label],
        margin=ft.Margin(0),
    )

    def clicked_registration(e):
        page.run_task(page.push_route, "/registration")

    registration_label = ft.TextButton(
        content=ft.Text(
            "Нет аккаунта? Зарегистрироваться",
            size=17,
            color="#928602"
        ),
        on_click=clicked_registration,
    )

    column = ft.Column(
        controls = [top_logo_area, middle_auth_area, bottom_entry_area, registration_label],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # --- ВАРИАНТ ДЛЯ FLET 0.85.1 (СЛОВАРЬ) ---
    # Безопасно проверяем, есть ли флаг в сессии
    '''
    if page.session.get("reg_success") or "reg_success" in page.session:
        # Удаляем флаг из словаря сессии
    
        page.session.pop("reg_success", None)
        
        # Создаем и показываем SnackBar
        success_snackbar = ft.SnackBar(
            content=ft.Text("Регистрация прошла успешно! Войдите в аккаунт."),
            bgcolor=ft.Colors.GREEN_700,
            show_close_icon=True
        )
        page.overlay.append(success_snackbar)
        success_snackbar.open = True
    '''
    if getattr(page, "reg_success", False):
        page.reg_success = False
        # код показа SnackBar...
        success_snackbar = ft.SnackBar(
            content=ft.Text("Регистрация прошла успешно! Войдите в аккаунт."),
            bgcolor=ft.Colors.GREEN_700,
            show_close_icon=True
        )
        page.overlay.append(success_snackbar)
        success_snackbar.open = True
    
    return ft.View(
        route="/login",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[column],
        bgcolor="#260C14",
        )

