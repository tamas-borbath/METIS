########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""

This view shows, for each gas interconnection and each direction, the corresponding transmission capacity.
There is one arrow per direction whose size is related to the transmission capacity.

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
	
	# Only print when Transmission
	if not physicalAsset.getType() in TRANSMISSION_TYPES:
		return
		
	# Only print when proper energy is considered
	if energy not in Crystal.listConsumedEnergies(context, physicalAsset):
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
	
	# And create the line while you are at it
	renderable.addArrow(deliveryPointIn, deliveryPointOut, .5, .5, Color.WHITE)
	
	# First compute net flow
	scopeId = context.getScope().getId()
	capacity = getInstalledCapacity(context, scopeId, physicalAsset, TEST_CASE, results)
	
	if capacity==None or capacity <= 1 :
		return
	meanCapa = capacity
	if isinstance(meanCapa,RegularTimeSerie):
		meanCapa = capacity.getMeanValue()
	elif isinstance(meanCapa,DataExpressionBinarySerie):
		meanCapa = capacity.getValue().getMeanValue()
	scale = meanInstalledCapacity(context, results)

	if VIEW_MODE == 'NORMAL':
		sgCircleValue(renderable, meanCapa, '', scale, VIEW_MODE)
		renderable.setShapeBackground(Color.WHITE)
		
	elif LAYER.hasVariable(deliveryPointIn.getName()+'/'+deliveryPointOut.getName()+'firstPassDone'):
		sgCircleValue(renderable, meanCapa - LAYER.getVariable(deliveryPointIn.getName()+'/'+deliveryPointOut.getName()+'firstPassDone'), 'MW', scale, VIEW_MODE)
		
		try:
			renderable.getVariables().remove(deliveryPointIn.getName()+'/'+deliveryPointOut.getName()+'firstPassDone')
		except:
			pass
	
	elif context.getName() <> LAYER.getVariable('isReferenceContext'):
		sgCircleValue(renderable, meanCapa, 'MW', scale, VIEW_MODE)
	
	else:
		LAYER.setVariable(deliveryPointIn.getName()+'/'+deliveryPointOut.getName()+'firstPassDone', meanCapa)
		
def configureFinancialAssetRenderable(renderable,financialAsset):
	pass
	
def updateFinancialAssetRenderable(renderable,financialAsset,timeCursor, aggregateMode) :
	pass

def configureDeliveryPointRenderable(renderable,deliveryPoint):
	updateDeliveryPointRenderable(renderable, deliveryPoint, timeCursorAll, AGGREGATE_MODE_ALL)

def updateDeliveryPointRenderable(renderable, deliveryPoint, timeCursor, aggregateMode):
	context = CONTEXTS.getObjectContext(deliveryPoint)
	results = Crystal.getComputationResults(context, TEST_CASE)	
	
	# setDateOnPane(context,timeCursor)

	if 'gas' not in deliveryPoint.getName().lower() and 'lng' not in deliveryPoint.getName().lower() :
		return
	
	if results == None or (not results.isComputed()):
		LAYER.setOverlayInformation("No results to display")
		return
	elif isNotVisible(deliveryPoint.getName()) or "lng" in deliveryPoint.getName() or "AL" in deliveryPoint.getName():
		return
	sgDefaultDeliveryPointLabel(renderable, deliveryPoint)


def configureZoneRenderable(renderable,zone) :
	renderable.setPolygon(zone.getNDLGeometry())
	renderable.setShapeBackground(computeUniqueColor(zone.getName(), transparency=80))
	renderable.setShapeForeground(Color.DARK_GRAY)
	renderable.setShape(Renderable.SHAPES.POLYGON)
	renderable.setDisplayAnnotation(zone.getName())
	pass