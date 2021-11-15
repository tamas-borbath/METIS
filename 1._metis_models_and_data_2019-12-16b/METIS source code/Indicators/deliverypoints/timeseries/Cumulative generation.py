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
	selectedTechnologies = list(PRODUCTION_TYPES) + list(LOSS_OF_ENERGY_TYPES) + [TOTAL_DEMAND, F_DSR, 'Net imports (Transmission)', 'Abroad Gas Imports', 'Abroad LNG Imports']
	return [
	getScopesIndexing(localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getDeliveryPointsIndexing(context, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getEnergiesIndexing(context, includedEnergies=PRODUCED_ENERGIES, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getTestCasesIndexing(context, localized=False, selectFirst=True, colorizeIndex=False, groupIndexAsGraphs=2),
	BaseIndexDefault("Data", selectedTechnologies, False, False, True, 0)
	]

def getData(view) :
	context = view.getContext()
	
	# Index filter
	selectedScopes         = view.filterIndexList(0, getScopes())
	selectedDeliveryPoints = view.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = view.filterIndexList(2, getEnergies(context, includedEnergies=PRODUCED_ENERGIES))
	selectedTestCases      = view.filterIndexList(3, getTestCasesWithResults(context))
	temp_technos = getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies = PRODUCTION_TYPES|LOSS_OF_ENERGY_TYPES) + [F_DSR, 'Net imports (Transmission)', 'Abroad Gas Imports', 'Abroad LNG Imports']
	selectedDataTypes   = set(view.filterIndexList(4, temp_technos)) #Using set to do union operations
	
	# Asset lists & results computation
	prodTechno = PRODUCTION_TYPES | {F_DSR}
	productionTechnologies   = getTechnologies(context, includedTechnologies=selectedDataTypes&prodTechno)
	demandTechnologies       = getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies=DEMAND_TYPES) #Do not consider filters : we only show the total demand
	lossOfEnergyTechnologies = getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies=selectedDataTypes&LOSS_OF_ENERGY_TYPES)
	gasImportTechnologies    = getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies={F_GAS_IMPORTS,F_IMPORT_PIPELINE})
	lngImportTechnologies    = getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies={F_LNG_IMPORTS})
	transmissionTechnologies = getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies=TRANSMISSION_TYPES, excludedTechnologies={F_IMPORT_PIPELINE})
	
	productionAssetsByScope = getAssetsByScope(context, selectedScopes, includedTechnologies = productionTechnologies)
	productionsDict         = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, productionAssetsByScope)
	
	demandAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets = True, includedTechnologies = demandTechnologies)
	demandsDict = getDemandDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, demandAssetsByScope)
	
	lossOfEnergyAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets = True, includedTechnologies = lossOfEnergyTechnologies)
	lossOfEnergyDict          = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, lossOfEnergyAssetsByScope)

	gasImportAssetsByScope = getAssetsByScope(context, selectedScopes, includedTechnologies = gasImportTechnologies)
	gasImportsDict         = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, gasImportAssetsByScope, aggregation=True)

	lngImportAssetsByScope = getAssetsByScope(context, selectedScopes, includedTechnologies = lngImportTechnologies)
	lngImportsDict         = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, lngImportAssetsByScope, aggregation=True)


	transmissionAssetsByScope 	= getAssetsByScope(context, selectedScopes, includedTechnologies = transmissionTechnologies)
	transmissionImportsDict     = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, transmissionAssetsByScope, aggregation=True)
	transmissionExportsDict     = getConsumptionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, transmissionAssetsByScope, aggregation=True)


	netImportsDict = defaultdict(float)

	for index in transmissionImportsDict:
		netImportsDict[index] = ((transmissionImportsDict[index] - transmissionExportsDict[index]) + abs(transmissionImportsDict[index] - transmissionExportsDict[index]))/2


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
					if 'Net imports (Transmission)' in selectedDataTypes:
						index = (scope, deliveryPoint, energyName, testCase)
						if index in netImportsDict:
							netImportsDict[index] = netImportsDict[index] * MW_TO_W_CONVERSION
							ret += [[list(index + ('Net imports (Transmission)',)), netImportsDict[index]]]
					if 'Abroad Gas Imports' in selectedDataTypes:
						index = (scope, deliveryPoint, energyName, testCase)
						if index in gasImportsDict:
							gasImportsDict[index] = gasImportsDict[index] * MW_TO_W_CONVERSION
							ret += [[list(index + ('Abroad Gas Imports',)), gasImportsDict[index]]]
					if 'Abroad LNG Imports' in selectedDataTypes:
						index = (scope, deliveryPoint, energyName, testCase)
						if index in lngImportsDict:
							lngImportsDict[index] = lngImportsDict[index] * MW_TO_W_CONVERSION
							ret += [[list(index + ('Abroad LNG Imports',)), lngImportsDict[index]]]

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
			
		elif indexValue == 'Net imports (Transmission)':
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

