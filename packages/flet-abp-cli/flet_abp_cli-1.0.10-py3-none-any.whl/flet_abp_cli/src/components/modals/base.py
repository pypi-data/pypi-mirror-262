import flet as ft

from utils.storage import storage


class BaseModal:
    title: str = ''

    def __init__(self):
        content = self.build_content()
        content = content if isinstance(content, list) else [content]
        actions = self.build_actions()
        actions = actions if isinstance(actions, list) else [actions]
        main_component = ft.Column(scroll=ft.ScrollMode.AUTO)
        main_component.controls = content
        self.modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(self.title),
            content=main_component,
            actions=actions,
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def build_content(self):
        return []

    def build_actions(self):
        return []

    def open(self, e=None):
        storage.page.dialog = self.modal
        self.modal.open = True
        storage.page.update()

    def close(self, e=None):
        self.modal.open = False
        storage.page.update()


class BaseFormModal(BaseModal):
    title: str = ''
    form = None

    def __init__(self):
        self.form_build = self.form(self.submit, with_submit=False)
        super().__init__()

    def build_actions(self):
        return [
            ft.TextButton("Submit", on_click=self.form_build.validate_form),
            ft.TextButton("Close", on_click=self.close_button_handler),
        ]

    def build_content(self):
        return [
            self.form_build
        ]

    def close_button_handler(self, e=None):
        self.clear()
        self.close()

    def submit(self, data):
        raise NotImplementedError

    def clear(self):
        # для того чтобы ресетать форму и чистить сторадж
        pass
