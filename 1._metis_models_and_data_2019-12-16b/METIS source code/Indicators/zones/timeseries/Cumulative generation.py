########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""

This view shows a temporal cumulative view, for each energy, of the generation at the selected delivery point for each generation technology at every time step as well at the demand level.

"""

from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'/results\kpis\imports\BaseKPI.py')

ViewLabel = "Cumulative generation (W)"

# CUMULATIVE LABELS
TOTAL_DEMAND = "Total demand"

indexValues = {}

def get_indexing(context) :
	productionTechnologies   = getTechnologies(context, includedTechnologies = PRODUCTION_TYPES)
	lossOfEnergyTechnologies = getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies = LOSS_OF_ENERGY_TYPES)
	selectedTechnologies = productionTechnologies + lossOfEnergyTechnologies + [TOTAL_DEMAND, F_DSR, 'Net imports']
	return [
	getScopesIndexing(localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getZonesIndexing(context, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getEnergiesIndexing(context, includedEnergies=PRODUCED_ENERGIES, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getTestCasesIndexing(context, localized=False, selectFirst=True, colorizeIndex=False, groupIndexAsGraphs=2),
	BaseIndexDefault("Data", selectedTechnologies, False, False, True, 0)
	]

def getData(view) :
	context = view.getContext()
	
	# Index filter
	selectedScopes         = view.filterIndexList(0, getScopes())
	selectedZones          = view.filterIndexList(1, getZones(context))
	selectedEnergies       = view.filterIndexList(2, getEnergies(context, includedEnergies=PRODUCED_ENERGIES))
	selectedTestCases      = view.filterIndexList(3, getTestCasesWithResults(context))
	temp_technos = getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies = PRODUCTION_TYPES|LOSS_OF_ENERGY_TYPES) + [TOTAL_DEMAND, F_DSR, 'Net imports']
	selectedDataTypes   = set(view.filterIndexList(4, temp_technos)) #Using set to do union operations
	
	selectedDeliveryPoints = getDpSetFromZoneList(context, selectedZones)
	
	# Asset lists & results computation
	prodTechno = PRODUCTION_TYPES | {F_DSR}
	productionTechnologies   = getTechnologies(context, includedTechnologies=selectedDataTypes&prodTechno)
	demandTechnologies       = getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies=DEMAND_TYPES) #Do not consider filters : we only show the total demand
	lossOfEnergyTechnologies = getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies=selectedDataTypes&LOSS_OF_ENERGY_TYPES)
	importTechnologies 		 = getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies=IMPORT_TYPES)
	exportTechnologies 		 = getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies=EXPORT_TYPES)
	

	productionAssetsByScope = getAssetsByScope(context, selectedScopes, includedTechnologies = productionTechnologies)
	productionsDict         = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, productionAssetsByScope)
	
	demandAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets = True, includedTechnologies = demandTechnologies)
	demandsDict         = getDemandDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, demandAssetsByScope)
	
	lossOfEnergyAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets = True, includedTechnologies = lossOfEnergyTechnologies)
	lossOfEnergyDict          = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, lossOfEnergyAssetsByScope)

	importAssetsByScope = getAssetsByScope(context, selectedScopes, includedTechnologies = importTechnologies)
	importsDict         = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, importAssetsByScope, aggregation=True)	

	exportAssetsByScope = getAssetsByScope(context, selectedScopes, includedTechnologies = exportTechnologies)
	exportsDict         = getConsumptionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, exportAssetsByScope, aggregation=True)	

	netImportsDict = defaultdict(float)

	for index in importsDict:
		netImportsDict[index] = ((importsDict[index] - exportsDict[index]) + abs(importsDict[index] - exportsDict[index]))/2
	
	productionsDictZone = getZoneDictFromDpDict(context, productionsDict, 1)
	demandsDictZone = getZoneDictFromDpDict(context, demandsDict, 1)
	lossOfEnergyDictZone = getZoneDictFromDpDict(context, lossOfEnergyDict, 1)

	ret = []
	
	for scope in selectedScopes:
		for testCase in selectedTestCases:
			results = Crystal.getComputationResults(context, scope, testCase)
			if results == None or (not results.isComputed()):
				print '[SCRIPT INFO] No results for ' + scope + ' ' + str(testCase)
				continue
			
			for deliveryPoint in selectedDeliveryPoints:
				for energy in selectedEnergies:
					energyName = energy.getName()
					# Productions
					for technology in productionTechnologies:
						index = (scope, deliveryPoint, energyName, testCase, technology)
						if index in productionsDict:
							productionsDict[index] = productionsDict[index] * MW_TO_W_CONVERSION
							ret += [[list(index), productionsDict[index]]]
					# Total demand
					demandIndex = (scope, deliveryPoint, energyName, testCase, TOTAL_DEMAND)
					demandTs = None
					for technology in demandTechnologies:
						index = (scope, deliveryPoint, energyName, testCase, technology)
						if index in demandsDict:
							if demandTs is None:
								demandTs = demandsDict[index] * MW_TO_W_CONVERSION
							else:
								demandTs = demandTs + demandsDict[index] * MW_TO_W_CONVERSION
					if demandTs is not None:
						ret += [[list(demandIndex), demandTs]]
					# LoL
					for technology in lossOfEnergyTechnologies:
						index = (scope, deliveryPoint, energyName, testCase, technology)
						if index in lossOfEnergyDict:
							lossOfEnergyDict[index] = lossOfEnergyDict[index] * MW_TO_W_CONVERSION
							ret += [[list(index), lossOfEnergyDict[index]]]
					# Other
					if 'Net imports' in selectedDataTypes:
						index = (scope, deliveryPoint, energyName, testCase)
						if index in netImportsDict:
							netImportsDict[index] = netImportsDict[index] * MW_TO_W_CONVERSION
							ret += [[list(index + ('Net imports',)), netImportsDict[index]]]
	
	return ret

def getTimeContext(context) :
	timeContext = [ context.getStartingDate() , context.getTimeStepDuration() , context.getTimeStepCount() ]
	return timeContext 

def isLineStacked(index) :
	if TOTAL_DEMAND in index:
		return False
	return True

#TODO: Refine this function when it will be possible to retrieve information (like the scope) from the view
def getIndexPrice(indexValue):
	if indexValue in indexValues.keys():
		return indexValues[indexValue]
	else:
		context  = Crystal.getStaticContext()
		scope    = context.getScope().getId()
		testCase = list(context.getTestCases())[0]
		if indexValue in getTechnologies(context, excludedTechnologies = TRANSMISSION_TYPES|DEMAND_TYPES|CYCLE_STORAGE_TYPES):
			price = getTechnologyProductionCostPerMWH(context, scope, testCase, indexValue)
			if price == None:
				price = 30
			
		elif indexValue == 'Net imports':
			price = 300
		elif indexValue in getTechnologies(context, includedTechnologies = CYCLE_STORAGE_TYPES):
			price = 500
		elif indexValue in getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies = LOSS_OF_ENERGY_TYPES):
			price = 15000
		elif indexValue in getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies = DEMAND_TYPES):
			price = 0
		else:
			price = 0
		indexValues.update({indexValue: price})
		return price

#TODO: Refine this function when it will be possible to retrieve information (like the scope) from the view
def indexCompare(numIndex,indexValue1,indexValue2):
	price1 = getIndexPrice(indexValue1)
	price2 = getIndexPrice(indexValue2)
	return int(price1-price2)

