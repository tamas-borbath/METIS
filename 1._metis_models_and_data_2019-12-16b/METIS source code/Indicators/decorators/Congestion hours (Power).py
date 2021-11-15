########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""

This view shows the amount of hours during which the interconnector was congested, in both directions.  
There is one arrow per direction whose size is related to its congestion time.

"""

from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'/decoratorUtils.py')

#Need to be redefined for each decorator
transmissionUnit = "h" 

def computeValue(context, testCase, energy, results, asset, timeCursor, aggregateMode):
	#Need to be redefined for each decorator
	scopeId = context.getScope().getId()
	transmissionCapacity = getInstalledCapacity(context, scopeId, asset, testCase, results)
	if transmissionCapacity == None or results == None or (not results.isComputed()):
		return None
	if transmissionCapacity <= 0 :
		return 0
	else:
		productionTimeSeries = getProduction(results, context, scopeId, asset, energy, testCase)
		if productionTimeSeries is None:
			# L'asset ne produit pas cette energy
			return None
		availabilityTimeSeries = getAvailability(context, scopeId, asset, testCase)
		transmissionUsageDataExpr = productionTimeSeries/(transmissionCapacity * availabilityTimeSeries)
		# if the flow at a time step is close to the maximal capacity, the line is saturated :
		transmissionUsageTimesSeries = transmissionUsageDataExpr.getValue()
		if aggregateMode == AGGREGATE_MODE_ALL:
			value = transmissionUsageTimesSeries.countAbove(0.999)
		else:
			value = int(transmissionUsageTimesSeries.getValueAt(timeCursor) > 0.999)
		return value


def configurePhysicalAssetRenderable(renderable, physicalAsset):
	context = CONTEXTS.getObjectContext(physicalAsset)
	assetName = physicalAsset.getName()
	
	if physicalAsset.getType() in TRANSMISSION_TYPES:
		if (not renderable.hasVariable(assetName)):
			renderable.setVariable(assetName, "ok")
			# setAssetBasicRenderable(context, renderable, asset, displayInactiveParameters=False, displayResults=False)
			
			LAYER.setVariable(assetName + "p", ARROW_INITIAL_POSITION)
		updatePhysicalAssetRenderable(renderable, physicalAsset, timeCursor=context.getIndex(0), aggregateMode=AGGREGATE_MODE_ALL)

def updatePhysicalAssetRenderable(renderable, physicalAsset, timeCursor, aggregateMode):
	if physicalAsset.getType() in TRANSMISSION_TYPES:
		context = CONTEXTS.getObjectContext(physicalAsset)
		energy  = Crystal.getEnergy(context, ELECTRICITY)
		if energy == None:
			return
		scope     = context.getScope().getId()
		testCase  = TEST_CASE
		results   = Crystal.getComputationResults(context, scope, testCase)
		updateTransmissionAssetRenderable(renderable, context, testCase, energy, results, physicalAsset, timeCursor, aggregateMode)

def configureFinancialAssetRenderable(renderable, financialAsset):
	pass 

def configureDeliveryPointRenderable(renderable, deliveryPoint):
	setDeliveryPointShape(renderable, deliveryPoint)
	# setDeliveryPointLabel(renderable, deliveryPoint)
	pass

def configureZoneRenderable(renderable, zone):
	setZoneShape(renderable,zone)
	setZoneLabel(renderable,zone)
	pass

