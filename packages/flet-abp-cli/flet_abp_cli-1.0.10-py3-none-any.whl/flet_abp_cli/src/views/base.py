import flet as ft
from router import router


class BaseView:
    """
    Базовый класс страницы, от него нужно наследовать все остальные страницы

    Возможно последовательное наследование:
    например есть класс FirstView(BaseView) и SecondView(FirstView)
    чтобы страница отрисовала все элементы своего родителя
    необходимо:

    build(self): return super().build() + [новые компоненты]
    """

    def __init__(self):
        components = self.build()
        self.components = components if isinstance(components, list) else [components]

    def build(self):
        return []

    def show_action(self):
        pass

    def hide_action(self):
        pass

    def show(self):
        for component in self.components:
            component.visible = True
        self.show_action()

    def hide(self):
        for component in self.components:
            component.visible = False
        self.hide_action()


class BaseFormView(BaseView):
    form = None

    def __init__(self):
        self.form_build = self.form(self.submit)
        super().__init__()

    def build(self):
        return super().build() + [
            ft.ElevatedButton(
                "Back",
                icon="ARROW_BACK",
                icon_color="blue",
                on_click=lambda _: router.change_route(router.previous_route)
            ),
            ft.Column(controls=[
                self.form_build
            ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
        ]

    def submit(self, data):
        raise NotImplementedError
