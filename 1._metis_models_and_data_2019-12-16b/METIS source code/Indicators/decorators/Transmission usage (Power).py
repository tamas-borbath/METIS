########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""
This view shows, for each power interconnection and each direction, the total usage define by the total flow during the length of the context divided by the maximum theoretical flow.
There is one arrow per direction whose size is related to the total usage.

"""

from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'/decoratorUtils.py')

#Need to be redefined for each decorator
transmissionUnit = "%"

def computeValue(context, testCase, energy, results, asset, timeCursor, aggregateMode):
	#Need to be redefined for each decorator
	scopeId = context.getScope().getId()
	transmissionCapacity = getInstalledCapacity(context, scopeId, asset, testCase, results)
	if transmissionCapacity == None or results == None or (not results.isComputed()):
		return None
	if transmissionCapacity > 0 :
		productionTimeSeries = getProduction(results, context, scopeId, asset, energy, testCase)
		if productionTimeSeries is None:
			# L'asset ne produit pas cette energy
			return None
		transmissionUsageTimesSeries = productionTimeSeries / transmissionCapacity
		if aggregateMode == AGGREGATE_MODE_ALL:
			value = transmissionUsageTimesSeries.getMeanValue() * 100
		else:
			value = transmissionUsageTimesSeries.getValueAt(timeCursor) * 100
		return value
	else:
		return 0

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

