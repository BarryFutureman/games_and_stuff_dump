import flet as ft
import random


def main(page: ft.Page):
    def animate_container(e):
        c1.top = random.randint(50, 200)
        c1.left = random.randint(50, 200)
        c1.content.color = ft.colors.YELLOW
        page.update()

    c1 = ft.Container(ft.Icon(name=ft.icons.OFFLINE_BOLT, color=ft.colors.WHITE),
                      alignment=ft.alignment.center,
                      width=20,
                      height=20,
                      animate_position=100,
                      on_click=animate_container)

    page.add(
        ft.Stack([c1], height=250),
    )


ft.app(target=main)
