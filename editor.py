import ryven
from PySide2.QtWidgets import QApplication
import os
import sys


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

    #   important: relative imports don't work here our of the box;
    #   this file's dir serves now as base directory for relative imports within this package
    sys.path.append(os.path.dirname(__file__))

    # register nodes (though Ryven!)
    editor.import_nodes(path=os.path.join(os.path.dirname(__file__), 'blender_nodes'))

    # create main script
    session.create_script('main')

    return editor, session
