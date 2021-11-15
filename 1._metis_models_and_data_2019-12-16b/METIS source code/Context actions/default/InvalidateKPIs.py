########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""

This context action deletes all KPI values in the current context

"""

from com.artelys.CrystalEditor.scripting import Crystal
from com.artelys.platform.gui.dialogs import CrystalOptionDialog

def onExecute(action, event):
    Crystal.displayInfoNotification("Invalidate KPI cache", "KPI cache has been invalidated", "Context action query: KPI cache has been invalidated")
    invalidateKPIs(action, event)

def onParametersChange(action, event):
    invalidateKPIs(action, event)

def onStructureChange(action, event):
    invalidateKPIs(action, event)

def invalidateKPIs(action, event):
    """
    Invalidate the KPIs results of source and destination context of the action
    """
    sourceContext = action.getSourceContext()
    destContext = action.getDestinationContext()
    
    sourceContext.getKPIContainer().invalideKPIs()
    if sourceContext != destContext and destContext != None:
        destContext.getKPIContainer().invalideKPIs()

askOnParametersChange = False
askOnStructureChange = False
