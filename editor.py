import ryvencore_qt as rc
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QHBoxLayout, QApplication

from .nodes.basic import export_nodes as nodes_basic


class EditorWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent, Qt.WindowCloseButtonHint | Qt.WindowSystemMenuHint | Qt.WindowTitleHint)

        self.apply_stylesheet()
        self.resize(800, 500)
        self.setWindowTitle('Ryven Blender')

        self.setLayout(QHBoxLayout())

        # build core
        self.session = rc.Session(
            flow_theme_name='Blender',
            performance_mode='fast',
        )
        self.session.register_nodes(
            nodes_basic
        )
        self.script = self.session.create_script(
            title='main',
            create_default_logs=False,
            flow_view_size=[10000, 10000],
        )

        self.layout().addWidget(
            self.session.flow_views[self.script]
        )

        ...

    def apply_stylesheet(self):
        """
        Applies a Ryven-based stylesheet to the editor window.
        Even though this dialog will get the Blender window as parent, the inherited styling produces lots of problems
        so far, but ultimately it would be cool to inherit Blender's widget styling (without issues).
        """

        import os
        f = open(os.path.join(os.path.dirname(__file__), 'styles_template.css'))

        from jinja2 import Template
        jinja_template = Template(f.read())

        f.close()

        app = QApplication.instance()

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

        def hex_to_rgb(hex: str):
            return tuple(int(hex[i:i + 2], 16) for i in (1, 3, 5))

        app.setStyleSheet(jinja_template.render({
            **colors,
            **{     # rgb inline versions
                'rgb_inline_' + cname: str(hex_to_rgb(val))[1:-1]
                for cname, val in colors.items()
            },
        }))
