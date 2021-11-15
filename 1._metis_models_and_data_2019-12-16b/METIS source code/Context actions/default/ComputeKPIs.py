########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""

This context action computes all KPIs of the current context at once

"""

from com.artelys.CrystalEditor.scripting import Crystal

def onExecute(action, event):
    sourceContext = action.getSourceContext()
    destContext = action.getDestinationContext()
    Crystal.computeAllKPIs(sourceContext, True)
    if sourceContext != destContext and destContext != None:
        Crystal.computeAllKPIs(destContext, True)

