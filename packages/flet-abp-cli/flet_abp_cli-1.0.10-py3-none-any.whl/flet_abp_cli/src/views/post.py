import flet as ft

from utils.storage import storage
from views.base import BaseView
from components.navbars.rail import rail_navbar
from router import router
from services.post import post_service


class PostView(BaseView):
    def show_action(self):
        self.table.rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(post['id'])),
                        ft.DataCell(ft.Text(post['content'])),
                        ft.DataCell(ft.Text(post['tag'])),
                    ],
                    on_select_changed=self.open_edit_post,
                    data=post['id']
                ) for post in post_service.get_posts()]
        self.table.update()

    def build(self):
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("id"), numeric=True),
                ft.DataColumn(ft.Text("Content")),
                ft.DataColumn(ft.Text("Tag"), numeric=True),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(post['id'])),
                        ft.DataCell(ft.Text(post['content'])),
                        ft.DataCell(ft.Text(post['tag'])),
                    ],
                    on_select_changed=self.open_edit_post,
                    data=post['id']
                ) for post in post_service.get_posts()]
        )
        return super().build() + [
            ft.Row([
                rail_navbar,
                ft.Column([
                    ft.Row([
                        ft.ElevatedButton('Create post', on_click=lambda e: router.change_route('/post/form')),
                    ], alignment=ft.MainAxisAlignment.END, height=50),
                    self.table
                ], expand=True, scroll=ft.ScrollMode.ADAPTIVE, alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START),
            ], expand=True, vertical_alignment=ft.CrossAxisAlignment.START)
        ]

    def open_edit_post(self, e=None):
        storage.set('current_post_id', e.control.data)
        router.change_route('/post/form')
