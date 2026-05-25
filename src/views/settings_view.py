import flet as ft

def settings_view(page: ft.Page) -> ft.View:
    page.theme_mode = ft.ThemeMode.DARK
    
    return ft.View(
        route="/settings",
        controls=[ft.Text("Settings view.", size=48, color="#029084")],
        bgcolor="#260C14",
        padding=10,
    )