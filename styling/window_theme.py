from PySide2.QtWidgets import QApplication
from os.path import dirname, abspath, join


def hex_to_rgb(hex: str):
    return tuple(int(hex[i:i + 2], 16) for i in (1, 3, 5))


class WindowTheme:

    name = ''
    colors = {}
    rules = {}

    def __init__(self):
        self.init_rules()

    def init_rules(self):
        self.rules = {
            # colors
            **self.colors,

            # rgb inline versions
            **{
                'rgb_inline_'+cname: str(hex_to_rgb(val))[1:-1]
                for cname, val in self.colors.items()
            },
        }


class WindowTheme_Dark(WindowTheme):
    name = 'dark'
    colors = {
        'primaryColor': '#448aff',
        'primaryLightColor': '#83b9ff',
        'secondaryColor': '#1E242A',
        'secondaryLightColor': '#272d32',
        'secondaryDarkColor': '#0C1116',
        'primaryTextColor': '#E9E9E9',
        'secondaryTextColor': '#9F9F9F',
        'danger': '#dc3545',
        'warning': '#ffc107',
        'success': '#17a2b8',
    }


class WindowTheme_Light(WindowTheme):
    name = 'light'
    colors = {
        'primaryColor': '#448aff',
        'primaryLightColor': '#508AD8',
        'secondaryColor': '#FFFFFF',
        'secondaryLightColor': '#E8EAEC',
        'secondaryDarkColor': '#ECEDEF',
        'primaryTextColor': '#1A1A1A',
        'secondaryTextColor': '#6E6E6E',
        'danger': '#dc3545',
        'warning': '#ffc107',
        'success': '#17a2b8',
    }


def apply_stylesheet(style: str):

    # set to None if not used
    icons_dir = None  # '../../resources/stylesheets/icons'

    # path to the template stylesheet file
    template_file = 'styles_template.css'

    # ------------------------------

    def path(rel_path: str):
        return abspath(join(dirname(__file__), rel_path))

    if icons_dir is not None:
        from qtpy.QtCore import QDir
        d = QDir()
        d.setSearchPaths('icon', [path(icons_dir)])

    if style == 'dark':
        window_theme = WindowTheme_Dark()
    else:
        window_theme = WindowTheme_Light()

    f = open(path(template_file))

    from jinja2 import Template
    jinja_template = Template(f.read())

    f.close()

    app = QApplication.instance()
    app.setStyleSheet(jinja_template.render(window_theme.rules))

    return window_theme
