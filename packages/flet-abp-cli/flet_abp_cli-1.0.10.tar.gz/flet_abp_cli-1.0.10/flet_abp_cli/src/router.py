import flet as ft


class Router:
    """
    Класс роутера для рендера и переключения страниц
    """
    def __init__(self):
        self.routes: dict = {}
        self.current_route = '/'
        self.previous_route = '/'
        self.page = None

    def init(self, page: ft.Page):
        self.page = page
        for key in self.routes.keys():
            page.add(*self.routes[key].components)
            self.routes[key].hide()
        self.page.update()
        self.routes['/'].show()
        self.page.update()

    def set_routers(self, routes: dict):
        self.routes = routes.copy()

    def change_route(self, route: str):
        if self.page:
            self.previous_route = self.current_route
            self.routes[self.current_route].hide()
            self.routes[route].show()
            self.current_route = route
            self.page.update()


router = Router()
