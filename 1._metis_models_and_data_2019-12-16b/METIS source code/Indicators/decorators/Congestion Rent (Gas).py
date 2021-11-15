########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""

This view shows the congestion rent of each gas interconnector, for both directions.  
There is one arrow per direction whose size is related to its congestion rent.

"""

from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'/gasDecoratorUtils.py')

try:
	LAYER.clearVariables()
except:
	pass

def configurePhysicalAssetRenderable(renderable,physicalAsset):
	context = CONTEXTS.getObjectContext(physicalAsset)
	energy = Crystal.getEnergy(context,GAS)

	if physicalAsset.getType() in TRANSMISSION_TYPES and energy in physicalAsset.get_producedEnergies(context.getPortfolioInterface()):
		latitude = physicalAsset.getLatitude()
		longitude = physicalAsset.getLongitude()
		renderable.setVariable(physicalAsset.getName(),"ok")
		renderable.setLat(latitude)
		renderable.setLon(longitude)
		renderable.setDisplayAnnotation(stringify(physicalAsset))

		updatePhysicalAssetRenderable(renderable, physicalAsset, context.getIndex(1), None)

def updatePhysicalAssetRenderable(renderable,physicalAsset,timeCursor, aggregateMode):

	context = CONTEXTS.getObjectContext(physicalAsset)
	energy = Crystal.getEnergy(context,GAS)
	results = Crystal.getComputationResults(context, TEST_CASE)
	timeStepDuration = getTimeStepDurationInHours(context)
	
	# Only print when Transmission and results
	if not (physicalAsset.getType() in TRANSMISSION_TYPES and energy in physicalAsset.get_producedEnergies(context.getPortfolioInterface())) or results == None or (not results.isComputed()):
		return

	if not LAYER.hasVariable("%s"%(timeCursor)):
		# clear variables on first update
		LAYER.clearVariables()
		LAYER.setVariable("%s"%(timeCursor),"ok")
	
	if not renderable.hasVariable("%s"%(timeCursor)):
		# clear variables on first update
		renderable.clearVariables()
		renderable.setVariable("%s"%(timeCursor),"ok")

	if not LAYER.hasVariable('isReferenceContext'):
		LAYER.setVariable('isReferenceContext', context.getName())
	
	# Clear arrows to avoid multiple arrows per asset / context in compare mode	
	renderable.clearArrows()

	deliveryPointIn = Crystal.listConsumptionDeliveryPoint(context,physicalAsset, energy)[0]
	deliveryPointOut = Crystal.listProductionDeliveryPoint(context,physicalAsset, energy)[0]
	
	# Check order and set dp first as dirst in alphabetical order
	firstDeliveryPoint = deliveryPointIn
	secondDeliveryPoint = deliveryPointOut
	if firstDeliveryPoint.getName() > secondDeliveryPoint.getName():
		firstDeliveryPoint = deliveryPointOut
		secondDeliveryPoint = deliveryPointIn
	
	# If congestion rent has already been computed on this line in this context then return
	if LAYER.hasVariable(context.getName()+'/'+firstDeliveryPoint.getName()+'/'+secondDeliveryPoint.getName()):
		return
		
	# Otherwise create the variable (so that it is not computed twice)
	LAYER.setVariable(context.getName()+'/'+firstDeliveryPoint.getName()+"/"+secondDeliveryPoint.getName(), 'done')
	
	# And create the line while you are at it
	renderable.addArrow(deliveryPointIn, deliveryPointOut, .5, .5, Color.WHITE)
	
	# First compute net flow
	flow = results.getProduction(physicalAsset, energy)
	
	for physicalAssetOther in Crystal.listPhysicalAssets(context):
		if (physicalAssetOther.getType() in TRANSMISSION_TYPES and energy in physicalAssetOther.get_producedEnergies(context.getPortfolioInterface())) and physicalAssetOther.getName() != physicalAsset.getName():
			deliveryPointInOther = Crystal.listConsumptionDeliveryPoint(context, physicalAssetOther, energy)[0]
			deliveryPointOutOther = Crystal.listProductionDeliveryPoint(context, physicalAssetOther, energy)[0]
			
			# If same DPs linked and same directions, simply add
			if deliveryPointInOther == deliveryPointIn and deliveryPointOutOther == deliveryPointOut:
				flow = flow.sum(results.getProduction(physicalAssetOther, energy))
			# If same DPs linked and opposite directions, simply substract
			elif deliveryPointOutOther == deliveryPointIn and deliveryPointInOther == deliveryPointOut: 
				flow = flow.substract(results.getProduction(physicalAssetOther, energy))
	flow = flow.multiply(timeStepDuration)
	
	# Then multiply it by price difference (in-out)
	priceDifference = (results.getDeliveryPointDualValues(deliveryPointOut,energy).substract(results.getDeliveryPointDualValues(deliveryPointIn,energy))).divide(timeStepDuration)
	congestionRent = flow.multiply(priceDifference)

	result = sumAggregate(congestionRent, timeCursor, aggregateMode)
	scale = meanInstalledCapacity(context, results)

	if VIEW_MODE == 'NORMAL':
		sgCircleValue(renderable, result, 'EUR', scale, VIEW_MODE)
		
	elif LAYER.hasVariable(firstDeliveryPoint.getName()+'/'+secondDeliveryPoint.getName()+'firstPassDone'):
		sgCircleValue(renderable, result - LAYER.getVariable(firstDeliveryPoint.getName()+'/'+secondDeliveryPoint.getName()+'firstPassDone'), 'EUR', scale, VIEW_MODE)		
		
		try:
			renderable.getVariables().remove(firstDeliveryPoint.getName()+'/'+secondDeliveryPoint.getName()+'firstPassDone')
		except:
			pass
	
	elif context.getName() <> LAYER.getVariable('isReferenceContext'):
		sgCircleValue(renderable, result, 'EUR', scale, VIEW_MODE)
	
	else:
		LAYER.setVariable(firstDeliveryPoint.getName()+'/'+secondDeliveryPoint.getName()+'firstPassDone', result)
		
def configureFinancialAssetRenderable(renderable,financialAsset):
	pass
	
def updateFinancialAssetRenderable(renderable,financialAsset,timeCursor, aggregateMode) :
	pass

def configureDeliveryPointRenderable(renderable,deliveryPoint):
	updateDeliveryPointRenderable(renderable, deliveryPoint, timeCursorAll, AGGREGATE_MODE_ALL)

def updateDeliveryPointRenderable(renderable, deliveryPoint, timeCursor, aggregateMode):
	context = CONTEXTS.getObjectContext(deliveryPoint)
	results = Crystal.getComputationResults(context, TEST_CASE)

	if 'gas' not in deliveryPoint.getName().lower():
		return
		
	# setDateOnPane(context,timeCursor)
	
	if results == None or (not results.isComputed()):
		LAYER.setOverlayInformation("No results to display")
		return
	elif isNotVisible(deliveryPoint.getName()):
		return
	sgDefaultDeliveryPointLabel(renderable, deliveryPoint)


def configureZoneRenderable(renderable,zone):
	renderable.setPolygon(zone.getNDLGeometry())
	renderable.setShapeBackground(computeUniqueColor(zone.getName(), transparency=80))
	renderable.setShapeForeground(Color.DARK_GRAY)
	renderable.setShape(Renderable.SHAPES.POLYGON)
	renderable.setDisplayAnnotation(zone.getName())
	pass

