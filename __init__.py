import bpy

from .editor import init_editor

bl_info = {
    "name": "Open Ryven Editor",
    "author": "Leon Thomm",
    "version": (0, 0, 0),
    "description": "A Ryven-like node editor plugin for Blender",
    "blender": (2, 93, 4),
    "category": "Object",
}


class OpenEditor(bpy.types.Operator):
    """Operator to quickly reopen the editor"""

    bl_idname = "ryven.open_editor"
    bl_label = "Open Ryven Blender"

    def execute(self, context):
        editor.show()
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(OpenEditor.bl_idname)


def register():
    global editor
    global session

    editor, session = init_editor()

    bpy.utils.register_class(OpenEditor)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(OpenEditor)


if __name__ == '__main__':
    editor = None
    session = None
    register()
