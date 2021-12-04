import ryven
from PySide2.QtWidgets import QApplication
from .nodes.basic import export_nodes as nodes_basic


def init_editor():

    # create new editor instance
    app = QApplication.instance()
    blender_window = app.blender_widget
    # editor = EditorWindow(main_window)
    editor = ryven.run_ryven(
        qt_app=app, show_dialog=False,
        gui_parent=blender_window, window_title='Ryven Blender',
        flow_theme='Blender'
    )
    session = editor.session

    # register nodes

    session.register_nodes(nodes_basic)

    # create main script
    session.create_script('main')

    return editor, session
