from PySide2.QtCore import Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QPushButton, QSlider, QPlainTextEdit, QTextEdit
from ryvencore_qt import *
import bpy


class NodeBase(Node):
    identifier_prefix = 'basic'


# class ValNode(NodeBase):
#     title = 'val'
#     init_inputs = [
#         NodeInputBP(dtype=dtypes.Data(size='s'))
#     ]
#     init_outputs = [
#         NodeOutputBP()
#     ]
#     style = 'small'
#
#     def place_event(self):
#         self.set_display_title('')
#
#     def update_event(self, inp=-1):
#         self.set_output_val(0, self.input(0))
#
#
# class ResultNode(NodeBase):
#     title = 'result'
#     init_inputs = [
#         NodeInputBP(dtype=dtypes.Data(size='l'))
#     ]
#     style = 'small'
#
#     def place_event(self):
#         self.set_display_title('')


class GetSceneNode(NodeBase):
    title = 'scene'
    init_outputs = [
        NodeOutputBP()
    ]

    def place_event(self):
        self.update()

    def update_event(self, inp=-1):
        self.set_output_val(0, bpy.context.scene)


class GetSceneObjectsNode(NodeBase):
    title = 'scene objs'
    init_outputs = [
        NodeOutputBP()
    ]

    def place_event(self):
        self.update()

    def update_event(self, inp=-1):
        self.set_output_val(0, bpy.context.scene.objects)


# ---------------------------------------------------------------------------------------

# SHAMELESSLY STOLEN FROM RYVEN...

class Checkpoint_Node(NodeBase):
    """Provides a simple checkpoint to reroute your connections"""

    title = 'checkpoint'
    init_inputs = [
        NodeInputBP(type_='data'),
    ]
    init_outputs = [
        NodeOutputBP(type_='data'),
    ]
    style = 'small'

    def __init__(self, params):
        super().__init__(params)

        self.display_title = ''

        self.active = False

        # initial actions
        self.actions['add output'] = {
            'method': self.add_output
        }
        self.actions['remove output'] = {
            '0': {'method': self.remove_output, 'data': 0}
        }
        self.actions['make active'] = {
            'method': self.make_active
        }

    """State transitions"""

    def clear_ports(self):
        # remove all outputs
        for i in range(len(self.outputs)):
            self.delete_output(0)

        # remove all inputs
        for i in range(len(self.inputs)):
            self.delete_input(0)

    def make_active(self):
        self.active = True

        # rebuild inputs and outputs
        self.clear_ports()
        self.create_input(type_='exec')
        self.create_output(type_='exec')

        # update actions
        del self.actions['make active']
        self.actions['make passive'] = {
            'method': self.make_passive
        }
        self.actions['remove output'] = {
            '0': {'method': self.remove_output, 'data': 0}
        }

    def make_passive(self):
        self.active = False

        # rebuild inputs and outputs
        self.clear_ports()
        self.create_input(type_='data')
        self.create_output(type_='data')

        # update actions
        del self.actions['make passive']
        self.actions['make active'] = {
            'method': self.make_active
        }
        self.actions['remove output'] = {
            '0': {'method': self.remove_output, 'data': 0}
        }

    """Actions"""

    def add_output(self):
        index = len(self.outputs)

        if self.active:
            self.create_output(type_='exec')
        else:
            self.create_output(type_='data')

        self.actions['remove output'][str(index)] = {
            'method': self.remove_output,
            'data': index,
        }

    def remove_output(self, index):
        self.delete_output(index)

        del self.actions['remove output'][str(len(self.outputs))]

    """Behavior"""

    def update_event(self, inp=-1):
        if self.active and inp == 0:
            for i in range(len(self.outputs)):
                self.exec_output(i)

        elif not self.active:
            data = self.input(0)
            for i in range(len(self.outputs)):
                self.set_output_val(i, data)

    """State Reload"""

    def get_state(self) -> dict:
        return {
            'active': self.active,
            'num outputs': len(self.outputs),
        }

    def set_state(self, data: dict):
        self.actions['remove output'] = {
            {'method': self.remove_output, 'data': i}
            for i in range(data['num outputs'])
        }

        if data['active']:
            self.make_active()


class Slider_Node(NodeBase):

    class SliderNode_MainWidget(MWB, QSlider):
        def __init__(self, params):
            MWB.__init__(self, params)
            QSlider.__init__(self, Qt.Horizontal)

            self.setRange(0, 1000)
            self.valueChanged.connect(self.value_changed)

        def value_changed(self, v):
            self.node.val = v / 1000
            self.update_node()

        def get_state(self) -> dict:
            return {
                'val': self.value(),
            }

        def set_state(self, data: dict):
            self.setValue(data['val'])

    title = 'slider'
    init_inputs = [
        NodeInputBP(dtype=dtypes.Integer(default=1), label='scl'),
        NodeInputBP(dtype=dtypes.Boolean(default=False), label='round'),
    ]
    init_outputs = [
        NodeOutputBP(),
    ]
    main_widget_class = SliderNode_MainWidget
    main_widget_pos = 'below ports'

    def __init__(self, params):
        super().__init__(params)

        self.val = 0

    def place_event(self):
        self.update()

    def view_place_event(self):
        # when running in gui mode, the value might come from the input widget
        self.update()

    def update_event(self, inp=-1):

        v = self.input(0) * self.val
        if self.input(1):
            v = round(v)

        self.set_output_val(0, v)

    def get_state(self) -> dict:
        return {
            'val': self.val,
        }

    def set_state(self, data: dict):
        self.val = data['val']


class Eval_Node(NodeBase):
    class EvalNode_MainWidget(MWB, QPlainTextEdit):
        def __init__(self, params):
            MWB.__init__(self, params)
            QPlainTextEdit.__init__(self)

            self.setFont(QFont('Consolas', 9))
            self.textChanged.connect(self.text_changed)
            self.setMaximumHeight(50)
            self.setMaximumWidth(200)

        def text_changed(self):
            self.node.expression_code = self.toPlainText()
            self.update_node()

        def get_state(self) -> dict:
            return {
                'text': self.toPlainText(),
            }

        def set_state(self, data: dict):
            self.setPlainText(data['text'])

    title = 'eval'
    init_inputs = [
        # NodeInputBP(),
    ]
    init_outputs = [
        NodeOutputBP(),
    ]
    main_widget_class = EvalNode_MainWidget
    main_widget_pos = 'between ports'

    def __init__(self, params):
        super().__init__(params)

        self.actions['add input'] = {'method': self.add_param_input}

        self.number_param_inputs = 0
        self.expression_code = None

    def place_event(self):
        if self.number_param_inputs == 0:
            self.add_param_input()

    def add_param_input(self):
        self.create_input()

        index = self.number_param_inputs
        self.actions[f'remove input {index}'] = {
            'method': self.remove_param_input,
            'data': index
        }

        self.number_param_inputs += 1

    def remove_param_input(self, index):
        self.delete_input(index)
        self.number_param_inputs -= 1
        del self.actions[f'remove input {self.number_param_inputs}']

    def update_event(self, inp=-1):
        inp = [self.input(i) for i in range(self.number_param_inputs)]
        self.set_output_val(0, eval(self.expression_code))

    def get_state(self) -> dict:
        return {
            'num param inputs': self.number_param_inputs,
            'expression code': self.expression_code,
        }

    def set_state(self, data: dict):
        self.number_param_inputs = data['num param inputs']
        self.expression_code = data['expression code']


class _DynamicPorts_Node(NodeBase):
    init_inputs = []
    init_outputs = []

    def __init__(self, params):
        super().__init__(params)

        self.actions['add input'] = {'method': self.add_inp}
        self.actions['add output'] = {'method': self.add_out}

        self.num_inputs = 0
        self.num_outputs = 0

    def add_inp(self):
        self.create_input()

        index = self.num_inputs
        self.actions[f'remove input {index}'] = {
            'method': self.remove_inp,
            'data': index
        }

        self.num_inputs += 1

    def remove_inp(self, index):
        self.delete_input(index)
        self.num_inputs -= 1
        del self.actions[f'remove input {self.num_inputs}']

    def add_out(self):
        self.create_output()

        index = self.num_outputs
        self.actions[f'remove output {index}'] = {
            'method': self.remove_out,
            'data': index
        }

        self.num_outputs += 1

    def remove_out(self, index):
        self.delete_output(index)
        self.num_outputs -= 1
        del self.actions[f'remove output {self.num_outputs}']

    def get_state(self) -> dict:
        return {
            'num inputs': self.num_inputs,
            'num outputs': self.num_outputs,
        }

    def set_state(self, data: dict):
        self.num_inputs = data['num inputs']
        self.num_outputs = data['num outputs']


class Exec_Node(_DynamicPorts_Node):

    class CodeNode_MainWidget(MWB, QTextEdit):
        def __init__(self, params):
            MWB.__init__(self, params)
            QTextEdit.__init__(self)

            self.setFont(QFont('Consolas', 9))
            self.textChanged.connect(self.text_changed)
            self.setFixedHeight(150)
            self.setFixedWidth(300)

        def text_changed(self):
            self.node.code = self.toPlainText()
            self.update_node()

        def get_state(self) -> dict:
            return {
                'text': self.toPlainText(),
            }

        def set_state(self, data: dict):
            self.setPlainText(data['text'])

    title = 'exec'
    main_widget_class = CodeNode_MainWidget
    main_widget_pos = 'between ports'

    def __init__(self, params):
        super().__init__(params)

        self.code = None

    def place_event(self):
        pass

    def update_event(self, inp=-1):
        exec(self.code)

    def get_state(self) -> dict:
        return {
            **super().get_state(),
            'code': self.code,
        }

    def set_state(self, data: dict):
        super().set_state(data)
        self.code = data['code']


export_nodes = [
    # ValNode,
    # ResultNode,
    GetSceneNode,
    GetSceneObjectsNode,
    Checkpoint_Node,
    Slider_Node,
    Eval_Node,
    Exec_Node,
]
