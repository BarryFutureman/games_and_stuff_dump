import flet as ft


def main(page: ft.Page):
    page.window_bgcolor = ft.colors.TRANSPARENT
    page.bgcolor = ft.colors.TRANSPARENT
    page.window_frameless = True
    page.window_title_bar_hidden = True
    page.window_center()
    page.window_to_front()
    page.window_movable = True
    page.window_width = 400
    page.window_height = 200

    def on_submit(e):
        print(e.control.value)
        e.control.value = ""
        page.update()

    page.add(
        ft.Row(
            [
                ft.WindowDragArea(ft.Container(padding=20), expand=True),
                ft.IconButton(ft.icons.DRAG_INDICATOR_SHARP, on_click=lambda _: page.window_close())
            ]
        )
    )

    tb = ft.TextField(hint_text="Say something...", filled=True, border=ft.InputBorder.UNDERLINE,
                      border_color=ft.colors.WHITE60, suffix_icon=ft.icons.SEND_SHARP, multiline=True,
                      shift_enter=True, on_submit=on_submit)
    page.add(tb)


ft.app(target=main)