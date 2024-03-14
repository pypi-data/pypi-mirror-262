import flet as ft
from components.modals.base import BaseModal
from router import router
from services.post import post_service
from utils.storage import storage


class PostModal(BaseModal):
    title = 'Are you sure???'

    def build_actions(self):
        return ft.Row([ft.TextButton(text='yes', on_click=self.yes_handler),
                       ft.TextButton(text='no', on_click=self.no_handler)],
                      alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def yes_handler(self, e=None):
        post_service.delete_post(storage.get_or_none('current_post_id'))
        router.change_route('/')
        self.close()

    def no_handler(self, e=None):
        router.change_route('/')
        self.close()


post_modal = PostModal()
