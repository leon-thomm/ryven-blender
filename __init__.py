import bpy
from .editor import EditorWindow
from PySide2.QtWidgets import QApplication

bl_info = {
    "name": "Open Ryven Editor",
    "blender": (2, 93, 4),
    "category": "Object",
}


class OpenEditor(bpy.types.Operator):
    bl_idname = "open.editor"
    bl_label = "Open Ryven Editor"

    def execute(self, context):
        editor.show()
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(OpenEditor.bl_idname)


def register():
    # create new editor instance
    main_window = QApplication.instance().blender_widget
    global editor
    editor = EditorWindow(main_window)
    editor.show()

    bpy.utils.register_class(OpenEditor)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(OpenEditor)


if __name__ == '__main__':
    editor = None
    register()
