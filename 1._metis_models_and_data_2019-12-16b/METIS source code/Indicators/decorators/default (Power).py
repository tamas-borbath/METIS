########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""

This view shows all the assets of the context, physical and financial, related to the power market.
It also shows an arrow that is showing the flow between the assets and the relevant delivery point(s)

"""

from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'/decoratorUtils.py')

USED_ENERGY = ELECTRICITY

#########################
# IMPORTANT WARNING !!!!
#########################
# All the code in this decorator is also used by "default(Gas).py"
# 
# DO NOT MODIFY THIS FILE WITHOUT CHECKING THE IMPACT ON THE OTHER DECORATOR !!!
#
# "default(Gas).py" just redefine the variable USED_ENERGY (cf above), and calls directly the function defined below


def configurePhysicalAssetRenderable(renderable, physicalAsset):

    CONTEXT = CONTEXTS.getObjectContext(physicalAsset)

    if CONTEXT is None:
        Crystal.logError("Error: Could not find context for asset "+str(physicalAsset.toString())+". Please reload decorator.")
        return

    scope = CONTEXT.getScope()

    setAssetBasicRenderable(physicalAsset, renderable)

    arrowPosition = 0.2
    LAYER.setVariable(physicalAsset.getName() + "c", arrowPosition)
    LAYER.setVariable(physicalAsset.getName() + "p", arrowPosition)

    updatePhysicalAssetRenderable(renderable,physicalAsset,CONTEXT.getIndex(1),None)

    if VIEW_MODE == 'NORMAL':
        # Normal view mode
        renderable.setDisplayAnnotation(stringify(physicalAsset, scope))

    else:
        configureComparisonRenderable(CONTEXT, renderable, physicalAsset)

def updatePhysicalAssetRenderable(renderable,physicalAsset,timeCursor, aggregateMode):
    context = CONTEXTS.getObjectContext(physicalAsset)
    scope   = context.getScope().getId()
    results = Crystal.getComputationResults(context, scope, TEST_CASE)
    energy  = Crystal.getEnergy(context, USED_ENERGY)
    computeScale(context,TEST_CASE,timeCursor, aggregateMode)
    SCALE_TIME_CURSOR = 'scale%s'%(timeCursor)
    
    if energy <> None :
        if not renderable.hasVariable("%s"%(timeCursor)) :
            # clear variables on first update
            renderable.clearVariables()
            renderable.setVariable("%s"%(timeCursor),"ok")
            # advance arrow position to simulate a flow
            LAYER.setVariable(physicalAsset.getName()+"c", ((LAYER.getVariable(physicalAsset.getName()+"c")*100+5) % 100)/100)
            LAYER.setVariable(physicalAsset.getName()+"p", ((LAYER.getVariable(physicalAsset.getName()+"p")*100+5) % 100)/100)

        # Clear arrows to avoid multiple arrows per asset / context in compare mode
        renderable.clearArrows()
        
        #Add arrows for all other asset interface
        arrow_position = 0.2
        ARROW_WIDTH = 0.7
        for otherEnergy in Crystal.listConsumedEnergies(CONTEXT, physicalAsset):
            if energy != otherEnergy:
                for dpin in Crystal.listConsumptionDeliveryPoint(CONTEXT, physicalAsset, otherEnergy):
                    renderable.addArrow(dpin, physicalAsset, ARROW_WIDTH, arrow_position, Color(96,96,96,196))

        for otherEnergy in Crystal.listProducedEnergies(CONTEXT, physicalAsset):
            if energy != otherEnergy:
                for dpout in Crystal.listProductionDeliveryPoint(CONTEXT, physicalAsset, otherEnergy):
                    renderable.addArrow(physicalAsset, dpout, ARROW_WIDTH, arrow_position, Color(96,96,96,196))
        
        # iterate through asset consumptions
        if (results != None and results.isComputed()) and energy in physicalAsset.get_consumedEnergies(context.getPortfolioInterface()):
            consumption = sumAggregate(results.getConsumption(physicalAsset, energy),timeCursor,aggregateMode)
            if consumption > 0:
                width = - min(10,5 * consumption / LAYER.getVariable(SCALE_TIME_CURSOR))
            else:
                width = 0
        else :
            width = 0

        # difference mode
        if (renderable.hasVariable(physicalAsset.getName()+"wc")) :
            width = width - renderable.getVariable(physicalAsset.getName()+"wc")
        else :
            renderable.setVariable(physicalAsset.getName()+"wc",width)

        # draw consumption arrows
        for deliveryPointIn in Crystal.listConsumptionDeliveryPoint(context, physicalAsset, energy):
            renderable.addArrow(deliveryPointIn,physicalAsset,abs(width), 0.2 + LAYER.getVariable(physicalAsset.getName()+"c") * 0.6, colorizer(physicalAsset.getType()) if VIEW_MODE=="NORMAL" else differenceColorizer(width))

        # iterate through asset productions
        if (results != None and results.isComputed()) and energy in physicalAsset.get_producedEnergies(context.getPortfolioInterface()):
            production = sumAggregate(results.getProduction(physicalAsset, energy),timeCursor,aggregateMode)
            if production > 0:
                width = min(10,5 * production / LAYER.getVariable(SCALE_TIME_CURSOR))
            else:
                width = 0
        else :
            width = 0

        # difference mode
        if (renderable.hasVariable(physicalAsset.getName()+"wp")) :
            width = - (renderable.getVariable(physicalAsset.getName()+"wp") - width)
        else :
            renderable.setVariable(physicalAsset.getName()+"wp",width)

        # draw production arrows
        for deliveryPointOut in Crystal.listProductionDeliveryPoint(context, physicalAsset, energy):
            renderable.addArrow(physicalAsset, deliveryPointOut, abs(width), 0.2 + LAYER.getVariable(physicalAsset.getName()+"p") * 0.6,  colorizer(physicalAsset.getType()) if VIEW_MODE=="NORMAL" else differenceColorizer(width))


def configureFinancialAssetRenderable(renderable,financialAsset):

    CONTEXT = CONTEXTS.getObjectContext(financialAsset)

    if CONTEXT is None:
        Crystal.logError(
            "Error: Could not find context for asset " + str(financialAsset.toString()) + ". Please reload decorator.")
        return

    scope = CONTEXT.getScope() 

    setAssetBasicRenderable(financialAsset, renderable)

    renderable.clearArrows()
    arrowPosition = 0.2
    LAYER.setVariable(financialAsset.getName(), arrowPosition)

    updateFinancialAssetRenderable(renderable,financialAsset,CONTEXT.getIndex(1),None)

    if VIEW_MODE == 'NORMAL':
        # Normal view mode
        renderable.setDisplayAnnotation(stringify(financialAsset, scope))

    else:
        configureComparisonRenderable(CONTEXT, renderable, financialAsset)


def updateFinancialAssetRenderable(renderable,financialAsset,timeCursor, aggregateMode) :
    context = CONTEXTS.getObjectContext(financialAsset)
    scope   = context.getScope().getId()
    results = Crystal.getComputationResults(context, scope, TEST_CASE)
    energy  = Crystal.getEnergy(context, USED_ENERGY)
    SCALE_TIME_CURSOR = 'scale%s'%(timeCursor)
    computeScale(context,TEST_CASE,timeCursor, aggregateMode)

    if energy <> None :
        if not renderable.hasVariable("%s"%(timeCursor)) :
            # clear variables on first update
            renderable.clearVariables()
            renderable.setVariable("%s"%(timeCursor),"ok")
            # advance arrow position to simulate a flow
            LAYER.setVariable(financialAsset.getName(), ((LAYER.getVariable(financialAsset.getName())*100+5) % 100)/100)

        # Clear arrows to avoid multiple arrows per asset / context in compare mode
        renderable.clearArrows()

        # iterate through financial assets
        # Uncommenting the previous line would prevent from seeing energies other than power from and to financial assets
        #if (results <> None) and energy == financialAsset.getEnergy():
        if (results != None and results.isComputed()):
            renderable.clearArrows()
            volume = abs(sumAggregate(results.getVolume(financialAsset),timeCursor,aggregateMode))
            width = min(10,5 * volume / LAYER.getVariable(SCALE_TIME_CURSOR))
        else :
            width = 0

        if (renderable.hasVariable(financialAsset.getName()+"wv")) :
            width = - (renderable.getVariable(financialAsset.getName()+"wv") - width)
        else :
            renderable.setVariable(financialAsset.getName()+"wv",width)

        if financialAsset.isBuyContract():
            for deliveryPointIn in Crystal.listDeliveryPoints(context, financialAsset):
                renderable.addArrow(financialAsset,deliveryPointIn, abs(width), 0.2 + LAYER.getVariable(financialAsset.getName()) * 0.6, colorizer(financialAsset.getEnergy().getName()) if VIEW_MODE=="NORMAL" else differenceColorizer(width))
        else:
            for deliveryPointOut in financialAsset.get_deliveryPoints():
                renderable.addArrow(deliveryPointOut,financialAsset,abs(width), 0.2 + LAYER.getVariable(financialAsset.getName()) * 0.6, colorizer(financialAsset.getEnergy().getName()) if VIEW_MODE=="NORMAL" else differenceColorizer(width))

def configureDeliveryPointRenderable(renderable,deliveryPoint):

        if isNotVisible(deliveryPoint.getName()):
            sgOtherDeliveryPointLabel(renderable, deliveryPoint)

        elif (not renderable.hasVariable(deliveryPoint.getName())) :
            renderable.setVariable(deliveryPoint.getName(),"ok")

            sgDefaultDeliveryPointLabel(renderable, deliveryPoint)

        else :
            renderable.setShapeBackground(Color.PINK)
            renderable.setDisplayTextSize(12)
            renderable.setDisplayText(deliveryPoint.getName())

        # updateDeliveryPointRenderable(renderable, deliveryPoint, 0, 'Year')

# def updateDeliveryPointRenderable(renderable, deliveryPoint, timeCursor, aggregateMode) :
    # context = CONTEXTS.getObjectContext(deliveryPoint)
    # setDateOnPane(context,timeCursor)
    # results = Crystal.getComputationResults(context, TEST_CASE)
    # if results == None or (not results.isComputed()):
        # LAYER.setOverlayInformation("No results to display")

def configureZoneRenderable(renderable,zone):
    setZoneShape(renderable,zone)
    renderable.setDisplayAnnotation(zone.getName())
    pass

def configureModelObjectRenderable(renderable,modelObject):
    updateModelObjectRenderable(renderable,modelObject)

def computeScale(context,testCase,timeCursor, aggregateMode):
    SCALE_TIME_CURSOR = 'scale%s'%(timeCursor)
    if (not LAYER.hasVariable(SCALE_TIME_CURSOR)):
        scale = 0.0
        scope = context.getScope().getId()
        results = Crystal.getComputationResults(context, scope, testCase)
        energy = Crystal.getEnergy(context, USED_ENERGY)

        if (results == None or (not results.isComputed())):
            LAYER.setVariable(SCALE_TIME_CURSOR, 1)
            return

        for asset in Crystal.listPhysicalAssets(context):
            if energy in Crystal.listProducedEnergies(context,asset):
                scale += sumAggregate(results.getProduction(asset,energy),timeCursor, aggregateMode)

        LAYER.setVariable(SCALE_TIME_CURSOR, 1+scale/(len(Crystal.listPhysicalAssets(context))+1))

        LAYER.setVariable(SCALE_TIME_CURSOR + str(context), 'ok')

    elif (not LAYER.hasVariable(SCALE_TIME_CURSOR + str(context))):
        scale = 0
        scope = context.getScope().getId()
        results = Crystal.getComputationResults(context, scope, testCase)
        energy = Crystal.getEnergy(context, USED_ENERGY)

        if (results == None or (not results.isComputed())):
            return

        for asset in Crystal.listPhysicalAssets(context):
            if energy in Crystal.listProducedEnergies(context,asset):
                scale += sumAggregate(results.getProduction(asset,energy),timeCursor, aggregateMode)

        LAYER.setVariable(SCALE_TIME_CURSOR, 1+scale/(len(Crystal.listPhysicalAssets(context))+1) + LAYER.getVariable(SCALE_TIME_CURSOR))

        LAYER.setVariable(SCALE_TIME_CURSOR + str(context), 'ok')
