import flet as ft

from router import router


class BaseRailNavbar(ft.UserControl):
    destinations = None

    def __init__(self, *args, **kwargs):
        # destinations = [{'icon': icon, 'label': label, 'url': url}]
        super().__init__(*args, **kwargs)

    def build(self):
        destinations = []
        for destination in self.destinations:
            destinations.append(
                ft.NavigationRailDestination(
                    icon=destination['icon'],
                    label=destination['label'],
                ))
        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            width=100,
            group_alignment=-0.9,
            destinations=destinations,
            on_change=self.route_change,
        )
        return ft.Row([
            rail,
            ft.VerticalDivider(width=1),
        ], width=100)

    def route_change(self, e=None):
        index = e.control.selected_index
        router.change_route(self.destinations[index]['url'])
