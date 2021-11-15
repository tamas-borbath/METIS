########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""

This view shows, for each power interconnection and each direction, the corresponding total flow during the length of the context.
There is one arrow per direction whose size is related to the total flow in that direction.

"""

from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'/decoratorUtils.py')

#Need to be redefined for each decorator
transmissionUnit = "Wh"

def computeValue(context, testCase, energy, results, asset, timeCursor, aggregateMode):
	#Need to be redefined for each decorator
	if results == None or (not results.isComputed()):
		return None
	
	scopeId = context.getScope().getId()
	productionTimeSeries = getProduction(results, context, scopeId, asset, energy, testCase)
	if productionTimeSeries == None :
		return #No production for this asset and energy
	
	timeStepDuration = getTimeStepDurationInHours(context)
	if aggregateMode == AGGREGATE_MODE_ALL:
		value = productionTimeSeries.getSumValue() * timeStepDuration * MW_TO_W_CONVERSION
	else:
		value = productionTimeSeries.getValueAt(timeCursor) * timeStepDuration * MW_TO_W_CONVERSION
	
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

