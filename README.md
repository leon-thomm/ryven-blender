![](screenshot1.png)

This project is not ready to use. It's a plugin for Blender to integrate a simple Ryven-like editor, but there are lots of features, and especially nodes, still missing. If you have ideas for how to combine the flow structure with the Blender Python API, please consider contributing.

## setup

To integrate the plugin you need to have Blender installed and access to Blender's local Python installation. Using *this* Python installation, install [`ryvencore-qt`](https://github.com/leon-thomm/ryvencore-qt)

```
pip install ryvencore-qt
```

However, you probably have a global Python installation already on your system, so you might have to run this by manually specifying the paths to Blender's Python, like this

```
<BP>/<ver>/python/bin> python.exe "<BP>/<ver>/python/lib/site-packages/pip" install ryvencore-qt
```

where `<BP>` is the path to your Blender installation and `<ver>` is the version.

Then place this repository under `<BP>/<ver>/scripts/addons/` and restart blender. Under `Edit => Preferences => Add-ons` you should now find `Open Ryven Editor` as command.