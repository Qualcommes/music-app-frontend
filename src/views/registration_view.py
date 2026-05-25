import flet as ft
import requests


def registration_view(page: ft.Page) -> ft.View:
    page.theme_mode = ft.ThemeMode.DARK
    print(f"[REGISTRATION VIEW] ID страницы: {id(page)}")
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

    '''
    password_field_ref = ft.Ref[ft.TextField]()
    password_confirmation_field_ref = ft.Ref[ft.TextField]()

    
    def toggle_password_visibility(e):
        # Переключаем видимость текста
        password_field_ref.current.password = not password_field_ref.current.password
        # Меняем иконку в зависимости от состояния
        e.control.icon = (
            ft.Icons.VISIBILITY_OFF if password_field_ref.current.password else ft.Icons.VISIBILITY
        )
        page.update()
        '''

    password_field = ft.TextField( 
        hint_text="ваш пароль",
        #ref=password_field_ref,
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
        can_reveal_password=True,
    )
    '''
    password_confirmation_field = ft.TextField( 
        hint_text="подтверждение пароля",
        #ref=password_confirmation_field_ref,
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
        can_reveal_password=True,
        )
        '''

    nickname_field = ft.TextField( 
        hint_text="ваш ник",
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
    # ДОБАВЛЕНО ПОЛЕ EMAIL
    login_field = ft.TextField( 
        hint_text="ваш логин",
        hint_style=ft.TextStyle(color=ft.Colors.BLACK),
        content_padding=ft.Padding(top=0, bottom=0, left=10),
        filled=True,
        width=400,
        height=70,
        bgcolor="#029084",
        color="#000000",
        border_radius=0,
        cursor_color=ft.Colors.BLACK,
    )

        
            # Функция-обработчик регистрации.
#===========================================================================================================================
    def clicked_registration(e):
        response = requests.post(
            "http://127.0.0.1:8000/api/auth/register", # Наш эндпоинт FastAPI
            json={
                "username": nickname_field.value,
                "email": login_field.value,
                "password": password_field.value
                }
            )
        '''
        # --- ИСПРАВЛЕННАЯ НАВИГАЦИЯ И УВЕДОМЛЕНИЕ ---
        # 1. Сначала осуществляем переход на экран логина
        # Используем run_task и push_route, как это сделано во всем твоем проекте
        page.run_task(page.push_route, "/login")
            
        # 2. Создаем SnackBar и сразу открываем его поверх нового экрана
        success_snackbar = ft.SnackBar(
            content=ft.Text("Регистрация прошла успешно! Войдите в аккаунт."),
            bgcolor=ft.Colors.GREEN_700,
            show_close_icon=True
        )
        page.overlay.append(success_snackbar)
        page.open(success_snackbar) # Сигнализирует Flet открыть этот SnackBar
            
        page.update()
            '''
        # --- ВАРИАНТ ДЛЯ FLET 0.85.1 (СЛОВАРЬ) ---
        # Сохраняем флаг успешной регистрации в сессию
        # page.session["reg_success"] = True
            
        page.reg_success = True

        # Перенаправляем на логин
        page.run_task(page.push_route, "/login")
#===========================================================================================================================

    access_button = ft.FilledButton(
        content=ft.Text(
            value="Зарегистрироваться",
            size=29, # Прямое управление размером внутри ft.Text
            weight=ft.FontWeight.BOLD,
        ),
        style = custom_style,
        width = 400,
        height = 70,
        on_click=clicked_registration,
    )


    registration_error_label = ft.Text(
        value="",
        color=ft.Colors.RED,
        size=21,
        visible=False,
    )
    registration_successful_label = ft.Text(
        value="Successful.",
        color=ft.Colors.GREEN,
        size=21,
        visible=False,
    )

    middle_reg_area=ft.Column(
        controls=[nickname_field, login_field, password_field],#, password_confirmation_field],
        margin=ft.Margin(top=20, bottom=90),
    )

    bottom_reg_area=ft.Column(
        controls=[access_button, registration_error_label, registration_successful_label],
        margin=ft.Margin(0),
    )

    

    column = ft.Column(
        controls = [middle_reg_area, bottom_reg_area,],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    return ft.View(
        route="/registration",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[column],
        bgcolor="#260C14",
        )