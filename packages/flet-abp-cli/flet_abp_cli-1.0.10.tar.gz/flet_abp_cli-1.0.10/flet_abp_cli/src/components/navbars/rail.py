import flet as ft

from components.navbars.base import BaseRailNavbar


class RailNavbar(BaseRailNavbar):
    destinations = [
        {
            'icon': ft.icons.POST_ADD, 'label': 'posts', 'url': '/',
        }
    ]


rail_navbar = RailNavbar(width=100)
