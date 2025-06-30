import flet as ft
import random
import time


def main(page: ft.Page):
    page.title = "Battery"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.CENTER, width=90, height=40)

    '''
    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=plus_click, icon_color="blue400",),
                ft.Icon(name="settings", color="#c1c1c1"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )'''

    # =====================================

    t = ft.Text(
        "100%",
        size=30,
        font_family="RobotoSlab",
        weight=ft.FontWeight.W_100,
    )

    def width_changed(e):
        t.weight = f"w{int(e.control.value)}"
        t.update()

    # ======================================

    def toggle_icon_button(e):
        e.control.selected = not e.control.selected
        if t.value == "0%":
            for i in range(0, 101, 5):
                t.value = f"{i}%"
                time.sleep(0.0001)
                t.update()
        else:
            for i in range(100, -1, -5):
                t.value = f"{i}%"
                time.sleep(0.0001)
                t.update()
        e.control.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.BATTERY_1_BAR,
                    selected_icon=ft.icons.BATTERY_FULL,
                    on_click=toggle_icon_button,
                    selected=False,
                    style=ft.ButtonStyle(color={"selected": ft.colors.GREEN, "": ft.colors.RED}),
                    width=60, height=60,
                    icon_size=45,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

    page.add(
        ft.Row([t], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(
            [
                ft.Slider(
                    min=100,
                    max=900,
                    divisions=8,
                    label="{value}",
                    width=200,
                    on_change=width_changed,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

    def animate_container(e):
        c1.top = random.randint(0, 50)
        c1.left = random.randint(420, 450)
        c1.content.color = ft.colors.YELLOW
        page.update()

    c1 = ft.Container(ft.Icon(name=ft.icons.OFFLINE_BOLT, color=ft.colors.WHITE),
                      alignment=ft.alignment.center,
                      width=200,
                      height=200,
                      animate_position=100,
                      on_click=animate_container,
                      left=400)

    page.add(
        ft.Row(
            [
                ft.Stack([c1], height=250),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )


ft.app(target=main)