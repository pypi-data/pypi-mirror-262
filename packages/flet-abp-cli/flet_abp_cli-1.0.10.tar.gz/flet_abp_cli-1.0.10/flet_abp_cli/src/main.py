import flet as ft

from core.database import add_sample_data
from router import router


from utils.storage import storage
from views.post import PostView
from views.post_form import PostFormView


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_min_width = 800
    page.window_min_height = 500
    page.title = 'Application'
    add_sample_data()
    storage.set('page', page)  # чтобы иметь доступ к странице из любого компонента

    router.set_routers({
        '/': PostView(),
        '/post/form': PostFormView(),
    })
    router.init(page)

    page.on_route_change = router.change_route


ft.app(target=main)
