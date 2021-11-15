########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""

This view shows all the assets of the context, physical and financial, linked to the relevant delivery point(s).
A small arrow is present in every link between asset and delivery point to indicate the direction of the main flow.

"""
import math
from com.artelys.platform.config import Constantes
from com.artelys.platform.genericassets.configuration import ConfigModele
from com.artelys.platform.genericassets.datamodel import NumericData

from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'/decoratorUtils.py')

ARROW_WIDTH = 0.7

def configurePhysicalAssetRenderable(renderable,physicalAsset):

    CONTEXT = CONTEXTS.getObjectContext(physicalAsset)
    
    if CONTEXT is None:
        Crystal.logError("Error: Could not find context for asset "+str(physicalAsset.toString())+". Please reload decorator.")
        return

    scope = CONTEXT.getScope()

    setAssetBasicRenderable(physicalAsset, renderable)

    if VIEW_MODE == 'NORMAL':
        # Normal view mode
        renderable.setDisplayAnnotation(stringify(physicalAsset, scope))

    else:
        configureComparisonRenderable(CONTEXT, renderable, physicalAsset)

    arrow_position = 0.2
    for energy in Crystal.listConsumedEnergies(CONTEXT, physicalAsset):
        for dpin in Crystal.listConsumptionDeliveryPoint(CONTEXT, physicalAsset, energy):
            renderable.addArrow(dpin, physicalAsset, ARROW_WIDTH, arrow_position, Color(96,96,96,196))   

    for energy in Crystal.listProducedEnergies(CONTEXT, physicalAsset):
        for dpout in Crystal.listProductionDeliveryPoint(CONTEXT, physicalAsset, energy):
            renderable.addArrow(physicalAsset, dpout, ARROW_WIDTH, arrow_position, Color(96,96,96,196))


def configureModelObjectRenderable(renderable,modelObject):
    updateModelObjectRenderable(renderable,modelObject)


def configureFinancialAssetRenderable(renderable,financialAsset):

    CONTEXT = CONTEXTS.getObjectContext(financialAsset)
    
    if CONTEXT is None:
        Crystal.logError("Error: Could not find context for asset "+str(financialAsset.toString())+". Please reload decorator.")
        return

    scope = CONTEXT.getScope()

    setAssetBasicRenderable(financialAsset, renderable)

    if VIEW_MODE == 'NORMAL':
        # Normal view mode
        renderable.setDisplayAnnotation(stringify(financialAsset, scope))

    else:
        configureComparisonRenderable(CONTEXT, renderable, financialAsset)
    
    arrow_position = 0.2
    if financialAsset.isBuyContract():
        for dpin in Crystal.listDeliveryPoints(CONTEXT, financialAsset):
            renderable.addArrow(financialAsset, dpin, ARROW_WIDTH, arrow_position, Color(96,96,96,196))  
    else:
        for dpin in financialAsset.get_deliveryPoints():
            renderable.addArrow(dpin, financialAsset, ARROW_WIDTH, arrow_position, Color(96,96,96,196))  

def configureDeliveryPointRenderable(renderable,deliveryPoint):
    sgOtherDeliveryPointLabel(renderable, deliveryPoint)
    updateDeliveryPointRenderable(renderable, deliveryPoint, 0, 'Year')
    

def updateDeliveryPointRenderable(renderable, deliveryPoint, timeCursor, aggregateMode) :   
    CONTEXT = CONTEXTS.getObjectContext(deliveryPoint)
    if CONTEXT is None:
        Crystal.logError("Error: Could not find context for delivery point "+str(deliveryPoint.toString())+". Please reload decorator.")
        return
    setDateOnPane(CONTEXT,timeCursor)

def getDisplayPriority():
    # Just above "Countries" decorator
    return 2



