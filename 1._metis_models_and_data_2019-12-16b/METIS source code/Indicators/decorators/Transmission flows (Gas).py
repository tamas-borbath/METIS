########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""

This view shows, for each gas interconnection and each direction, the corresponding total flow during the length of the context.
There is one arrow per direction whose size is related to the total flow in that direction.

"""

from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'/gasDecoratorUtils.py')

def computeScale(context,test_case,timeCursor, aggregateMode):
	energy = Crystal.getEnergy(context, GAS)
	scale = 0.0
	iteration = 0
	
	results = Crystal.getComputationResults(context, TEST_CASE)
	if (results <> None):
		for assetType in IMPORT_TYPES:
			for contract in Crystal.listFinancialAssetsByType(context, assetType):
				if contract.getEnergy() == energy:
					scale+=sumAggregate(results.getVolume(contract),timeCursor,aggregateMode)
					iteration += 1

		for assetType in EXPORT_TYPES:
			for contract in Crystal.listFinancialAssetsByType(context, assetType):
				if contract.getEnergy() == energy:
					scale+=sumAggregate(results.getVolume(contract),timeCursor,aggregateMode)
					iteration += 1

		for assetType in TRANSMISSION_TYPES:
			for asset in Crystal.listPhysicalAssetsByType(context, assetType):
				if energy in asset.get_producedEnergies(context.getPortfolioInterface()):
					scale += sumAggregate(results.getProduction(asset, energy),timeCursor,aggregateMode)
					iteration += 1

	LAYER.setVariable('scale', scale / (1 + iteration))

def configurePhysicalAssetRenderable(renderable,physicalAsset):
	context = CONTEXTS.getObjectContext(physicalAsset)
	energy = Crystal.getEnergy(context,GAS)
	
	if physicalAsset.getType() in TRANSMISSION_TYPES and energy in physicalAsset.get_producedEnergies(context.getPortfolioInterface()):
		if (not renderable.hasVariable(physicalAsset.getName())) :
			latitude = physicalAsset.getLatitude()
			longitude = physicalAsset.getLongitude()
			renderable.setVariable(physicalAsset.getName(),"ok")
			renderable.setLat(latitude)
			renderable.setLon(longitude)
			renderable.setDisplayAnnotation(stringify(physicalAsset))
			
			arrowPosition = 0.2
			LAYER.setVariable(physicalAsset.getName() + "c", arrowPosition)
			LAYER.setVariable(physicalAsset.getName() + "p", arrowPosition)
	
			updatePhysicalAssetRenderable(renderable,physicalAsset, timeCursorAll, AGGREGATE_MODE_ALL)

def updatePhysicalAssetRenderable(renderable, physicalAsset, timeCursor, aggregateMode):
	context = CONTEXTS.getObjectContext(physicalAsset)
	energy = Crystal.getEnergy(context, GAS)
	timeStepDurationInHours = getTimeStepDurationInHours(context)
	results = Crystal.getComputationResults(context, TEST_CASE)

	if not (physicalAsset.getType() in TRANSMISSION_TYPES and energy in physicalAsset.get_producedEnergies(context.getPortfolioInterface())) or (results == None or (not results.isComputed())):
		return
	
	computeScale(context,TEST_CASE,timeCursor, aggregateMode)

	if not renderable.hasVariable("%s"%(timeCursor)) :
		# clear variables on first update
		renderable.clearVariables()
		renderable.setVariable("%s"%(timeCursor),"ok")
		# advance arrow position to simulate a flow
		LAYER.setVariable(physicalAsset.getName()+"c", ((LAYER.getVariable(physicalAsset.getName()+"c")*100+5) % 100)/100)
		LAYER.setVariable(physicalAsset.getName()+"p", ((LAYER.getVariable(physicalAsset.getName()+"p")*100+5) % 100)/100)
	
	# Clear arrows to avoid multiple arrows per asset / context in compare mode	
	renderable.clearArrows()
	
	# iterate through asset productions
	production = sumAggregate(results.getProduction(physicalAsset, energy), timeCursor, aggregateMode) * timeStepDurationInHours
	if production > 0:
		width = min(10, 4 * production / LAYER.getVariable("scale"))
	else:
		width = 0
		
	color = sg_color[0]
	# difference mode
	if (renderable.hasVariable(physicalAsset.getName()+"wp")) :
		width =(width - renderable.getVariable(physicalAsset.getName()+"wp"))
		color = differenceColorizer(width)
	else :
		renderable.setVariable(physicalAsset.getName()+"wp",width)
		
	deliveryPointIn = Crystal.listConsumptionDeliveryPoint(context,physicalAsset, energy)[0]
	deliveryPointOut = Crystal.listProductionDeliveryPoint(context,physicalAsset, energy)[0]
	# draw production arrows
	
	capacity = getInstalledCapacity(context, context.getScope().getId(), physicalAsset, TEST_CASE, results)
	if capacity is not None:
		congestion = results.getProduction(physicalAsset, energy) - capacity
		meanCapa = capacity
		if isinstance(meanCapa,RegularTimeSerie):
			meanCapa = capacity.getMeanValue()
		elif isinstance(meanCapa,DataExpressionBinarySerie):
			meanCapa = capacity.getValue().getMeanValue()
		numberOfHours = congestion.getValue().countAbove(-0.05 * meanCapa) * timeStepDurationInHours
		if numberOfHours > 504: # production > 0.8 * meanCapa * 8760 or
			color = Color.RED
		renderable.addArrow(deliveryPointIn, deliveryPointOut, abs(width),  0.2 + LAYER.getVariable(physicalAsset.getName()+"p") * 0.6, color)

	pass

def configureFinancialAssetRenderable(renderable,financialAsset):
	context = CONTEXTS.getObjectContext(financialAsset)
	energy = Crystal.getEnergy(context,GAS)
	
	if (financialAsset.getType() in IMPORT_TYPES or financialAsset.getType() in EXPORT_TYPES) and financialAsset.getEnergy() == energy:
		if (not renderable.hasVariable(financialAsset.getName())) :
			context = CONTEXTS.getObjectContext(financialAsset)
			renderable.setVariable(financialAsset.getName(),"ok")
			latitude = financialAsset.getLatitude()
			longitude = financialAsset.getLongitude()
			renderable.setLat(latitude)
			renderable.setLon(longitude)
			renderable.setDisplayAnnotation(stringify(financialAsset))
			renderable.setIcon(LAYER.getDefaultIcon(financialAsset))
			iconeSize = 32
			renderable.setIconWidth(iconeSize)
			renderable.setIconHeight(iconeSize)
			
			renderable.clearArrows()
			arrowPosition = 0.2
			LAYER.setVariable(financialAsset.getName(), arrowPosition)
			
			updateFinancialAssetRenderable(renderable,financialAsset,context.getIndex(1),None)
	
def updateFinancialAssetRenderable(renderable,financialAsset,timeCursor, aggregateMode) :

	context = CONTEXTS.getObjectContext(financialAsset)
	energy = Crystal.getEnergy(context, GAS)
	timeStepDuration = getTimeStepDurationInHours(context)
	results = Crystal.getComputationResults(context, TEST_CASE)
	computeScale(context,TEST_CASE,timeCursor, aggregateMode)

	if (results == None or (not results.isComputed())) or not ((financialAsset.getType() in IMPORT_TYPES or financialAsset.getType() in EXPORT_TYPES) and financialAsset.getEnergy() == energy):
		return
	
	
	if not renderable.hasVariable("%s"%(timeCursor)) :
		# clear variables on first update
		renderable.clearVariables()
		renderable.setVariable("%s"%(timeCursor),"ok")
		# advance arrow position to simulate a flow
		LAYER.setVariable(financialAsset.getName(), ((LAYER.getVariable(financialAsset.getName())*100+5) % 100)/100)
		
	renderable.clearArrows()
	volume = math.fabs(sumAggregate(results.getVolume(financialAsset), timeCursor, aggregateMode)) * timeStepDuration
	if volume > 0:
		width = min(10, 4 * volume / LAYER.getVariable("scale"))
	else:
		width = 0


	if (renderable.hasVariable(financialAsset.getName()+"wv")) :
		width = width - renderable.getVariable(financialAsset.getName()+"wv")
	else :
		renderable.setVariable(financialAsset.getName()+"wv",width)
			
		
	if financialAsset.isBuyContract():
		for deliveryPointIn in Crystal.listDeliveryPoints(context, financialAsset):
			renderable.addArrow(financialAsset,deliveryPointIn, abs(width), 0.2 + LAYER.getVariable(financialAsset.getName()) * 0.6, Color.WHITE if VIEW_MODE=="NORMAL" else differenceColorizer(width))
	else:
		for deliveryPointOut in Crystal.listDeliveryPoints(context, financialAsset):
			renderable.addArrow(deliveryPointOut,financialAsset,abs(width), 0.2 + LAYER.getVariable(financialAsset.getName()) * 0.6, Color.WHITE if VIEW_MODE=="NORMAL" else differenceColorizer(width))

	
def configureDeliveryPointRenderable(renderable,deliveryPoint):
	updateDeliveryPointRenderable(renderable, deliveryPoint, timeCursorAll, AGGREGATE_MODE_ALL)

def updateDeliveryPointRenderable(renderable, deliveryPoint, timeCursor, aggregateMode):
	context = CONTEXTS.getObjectContext(deliveryPoint)
	results = Crystal.getComputationResults(context, TEST_CASE)	
	
	# setDateOnPane(context,timeCursor)
	
	if results == None or (not results.isComputed()):
		LAYER.setOverlayInformation("No results to display")
		return
	elif isNotVisible(deliveryPoint.getName()):
		return
	elif 'co2' in deliveryPoint.getName() or 'lng' in deliveryPoint.getName():
		return
	if (not renderable.hasVariable(deliveryPoint.getName())) :
		renderable.setVariable(deliveryPoint.getName(),"ok")
		sgDefaultDeliveryPointLabel(renderable, deliveryPoint)
	else :
		renderable.setShapeBackground(Color.PINK)


def configureZoneRenderable(renderable,zone) :
	renderable.setPolygon(zone.getNDLGeometry())
	renderable.setShapeBackground(computeUniqueColor(zone.getName(), transparency=80))
	renderable.setShapeForeground(Color.DARK_GRAY)
	renderable.setShape(Renderable.SHAPES.POLYGON)
	renderable.setDisplayAnnotation(zone.getName())
	pass
def stringify(object):
	retString = "<table>"
	retString += "<thead><tr>"
	retString += "<th colspan='2'><img src='file:///"+LAYER.getDefaultIcon(object)+"'/>"+object.getName() +"</th>"
	retString += "</tr></thead>"
	retString += "<tbody>"
	for dataId in	object.getAssetDataSortedByXML().keySet() :
		retString += "<tr>"
		retString += "<td><i>" + object.getDataLabel(dataId) + "</i></td>"
		retString += "<td>%s</td>" % (object.get_assetData().get(dataId))
		retString += "</tr>"
	retString += "</tbody>"
	retString += "</table>"
	return retString

