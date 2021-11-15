########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""

This view shows, in hours and for each interconnector, the amount of time during which the marginal price for generating electricity in the input country is higher by more than 1€/MWh then the one in the output country.
There is one arrow per direction whose size is related to its amount of price divergence hours as defined.

"""

from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'/decoratorUtils.py')

#Need to be redefined for each decorator
transmissionUnit = "h"

def computeValue(context, testCase, energy, results, asset, timeCursor, aggregateMode):
	#Need to be redefined for each decorator
	if results == None or (not results.isComputed()):
		return None
	divergenceTolerance = 1
	timeStepCount =  context.getTimeStepCount()
	timeStepDuration = getTimeStepDurationInHours(context)
	
	consumptionDp = getConsumptionDeliveryPoint(context, asset, energy)
	productionDp  = getProductionDeliveryPoint(context, asset, energy)
	if consumptionDp is None or productionDp is None :
		print '[ERROR] Transmission ' + asset.getName() + ' should have one production delivery point and one consumption delivery point for energy ' + str(energy)
		return None
	
	priceDifference = results.getDeliveryPointDualValues(productionDp, energy).substract(results.getDeliveryPointDualValues(consumptionDp, energy))
	
	if aggregateMode == AGGREGATE_MODE_ALL:
		value = int(timeStepCount - priceDifference.countBelowEps(0, divergenceTolerance) * timeStepDuration)
	else:
		value = int(int(abs(priceDifference.getValueAt(timeCursor)) > divergenceTolerance) * timeStepDuration)
	
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

