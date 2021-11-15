########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""

This context action deletes the calculated results in the current context

"""

from com.artelys.CrystalEditor.scripting import Crystal
from com.artelys.platform.gui.dialogs import CrystalOptionDialog

def onExecute(action, event):
    context = action.getDestinationContext()
    if context != action.getSourceContext():
        Crystal.showErrorDialog("Cannot execute script: source and destination contexts are different!")
        return
    
    ret = CrystalOptionDialog.showConfirmDialog(None, "Are you sure you want to delete results?", "Delete results?", CrystalOptionDialog.YES_NO_OPTION)
    if ret != 0: return
    
    facade = context.get_facade()
    facade.viderResultats()
    facade.notifyResults(context.getScope().getId())
    