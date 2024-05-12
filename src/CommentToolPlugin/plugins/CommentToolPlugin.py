import maya.api.OpenMaya as om
import maya.cmds as cmds
import maya._OpenMayaUI as OpenMayaUI1
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from CommentToolMaya import CommentToolDialog

'''
def maya_useNewAPI():
    """
    Can either use this function (which works on earlier versions)
    or we can set maya_useNewAPI = True
    """
    pass
'''

maya_useNewAPI = True
comment_tool_dialog = None


# gonna be called when we call doIt()
def CommentToolUIScript(restore = False) :
    global comment_tool_dialog
    if restore == True:
        restored_control = OpenMayaUI1.MQtUtil.getCurrentParent()
    if comment_tool_dialog is None :
        print("creating new UI")
        comment_tool_dialog = CommentToolDialog()
        comment_tool_dialog.setObjectName('CommentToolDialog')
    if restore == True:
        mixin_ptr = OpenMayaUI1.MQtUtil.findControl(comment_tool_dialog.objectName())
        OpenMayaUI1.MQtUtil.addWidgetToMayaLayout(int(mixin_ptr), int(restored_control))
    else :
        comment_tool_dialog.show(dockable = True,width=800, height=800, 
                                 uiScript='CommentToolUIScript(restore=True)')



class CommentTool(om.MPxCommand):

    CMD_NAME = "CommentTool"

    def __init__(self):
        super(CommentTool, self).__init__()

    def doIt(self, args):
        ui = CommentToolUIScript()
        if ui is not None:
            try :
                cmds.workspaceControl("CommentToolDialogWorkspaceControl", e=True, restore=True)
            except :
                pass
        return ui     

    @classmethod
    def creator(cls):
        """
        Think of this as a factory
        """
        return CommentTool()


def initializePlugin(plugin):
    """
    Load our plugin
    """
    vendor = "NCCA"
    version = "1.0.0"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)

    try:
        plugin_fn.registerCommand(CommentTool.CMD_NAME, CommentTool.creator)
    except:
        om.MGlobal.displayError(
            "Failed to register command: {0}".format(CommentTool.CMD_NAME)
        )


def uninitializePlugin(plugin):
    """
    Exit point for a plugin
    """
    plugin_fn = om.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterCommand(CommentTool.CMD_NAME)
    except:
        om.MGlobal.displayError(
            "Failed to deregister command: {0}".format(CommentTool.CMD_NAME)
        )


if __name__ == "__main__":
    """
    So if we execute this in the script editor it will be a __main__ so we can put testing code etc here
    Loading the plugin will not run this
    As we are loading the plugin it needs to be in the plugin path.
    """

    plugin_name = "HellolMaya.py"

    cmds.evalDeferred(
        'if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(
            plugin_name
        )
    )
    cmds.evalDeferred(
        'if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(
            plugin_name
        )
    )
