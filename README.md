## Ryven plugin for Blender

This repo consists of a tiny file for loading [Ryven](https://github.com/leon-thomm/ryven) as a plugin in Blender, as well as nodes packages. **Notice that there are no nodes at all available yet, because I don't know the Blender Python API well**. If you do, please consider contributing.

While Blender itself already has an impressive built-in nodes-based material editor, the simplicity of Ryven together with the extensive Blender Python API might enable much more rapid development of new nodes.

![](screenshot1.png)

## setup

### Step 1: Find the path to your Blender's Python executable

something like

```
C:\Program Files\Blender Foundation\Blender 2.93\2.93\python\bin\python
```

I will refer to the Blender Python path as `<BPP>` from now on.

### Step 2: Install Ryven and bqt

Run a terminal with admin/root privileges and execute

```
"<BPP>" -m pip install ryven
"<BPP>" -m pip install bqt
```

Installing packages into Blender's Python can be quite fiddly sometimes.

### Step 3: Add the plugin

Clone this repository into the addons dir of your Blender installation

```
cd <Blender-Path>/<ver>/scripts/addons/
git clone https://github.com/leon-thomm/ryven-blender
```

### Step 4: Load the plugin

Open Blender *as administrator* (to grant ryven read access to its installation directory in Blender's Python). Under `Edit => Preferences => Add-ons` you should now find `Open Ryven Editor`. If not, click `install` and select the `ryven-blender/__init__.py` file.

By pressing `F3` in Blender you should now find `Open Ryven Editor` as command which simply shows the editor window, closing the Ryven editor window doesn't kill its content.

## adding nodes

To add nodes, see `blender_nodes/nodes.py` and `blender_nodes/basic.py` for some examples.
