########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""

This view shows time series, for each energy, of the demand and net demand, both optimized and unoptimized, for this energy at the selected delivery point.
Unoptimized net demand is defined as the difference between unoptimized demand and the must run available capacity.
Optimized net demand is defined as the difference between optimized demand and the must run generation.

"""

from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'/results\kpis\imports\BaseKPI.py')

ViewLabel = "Demand and Net Demand (W)"

# Index labels
UNOPTIMIZED_DEMAND     = "Unoptimized demand"
OPTIMIZED_DEMAND       = "Optimized demand"
UNOPTIMIZED_NET_DEMAND = "Unoptimized net demand"
OPTIMIZED_NET_DEMAND   = "Optimized net demand"
DATA_INDEX_LIST = [UNOPTIMIZED_DEMAND, OPTIMIZED_DEMAND, UNOPTIMIZED_NET_DEMAND, OPTIMIZED_NET_DEMAND]

def get_indexing(context):
	return [
	getScopesIndexing(localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getDeliveryPointsIndexing(context, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getEnergiesIndexing(context, includedEnergies=PRODUCED_ENERGIES, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getTestCasesIndexing(context, localized=False, selectFirst=True, colorizeIndex=True, groupIndexAsGraphs=0),
	BaseIndexDefault("Data", DATA_INDEX_LIST, False, False, True, 0)
	]

def getData(view) :
	context = view.getContext()
	
	# Index filter
	selectedScopes         = view.filterIndexList(0, getScopes())
	selectedDeliveryPoints = view.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = view.filterIndexList(2, getEnergies(context, includedEnergies=PRODUCED_ENERGIES))
	selectedTestCases      = view.filterIndexList(3, getTestCasesWithoutResults(context))
	selectedDataTypes      = view.filterIndexList(4, DATA_INDEX_LIST)
	
	# Asset lists & results computation
	demandAssetsByScope     = getAssetsByScope(context, selectedScopes, includeFinancialAssets = True, includedTechnologies = DEMAND_TYPES)
	renewableAssetsByScope  = getAssetsByScope(context, selectedScopes, includedTechnologies = NON_FLEXIBLE_RES_TYPES)
	
	unoptimizedDemandDict            = getRawDemandDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, demandAssetsByScope, aggregation = True)
	optimizedDemandDict              = getDemandDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, demandAssetsByScope, aggregation = True)
	renewableAvailableCapacitiesDict = getAvailableCapacityDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, renewableAssetsByScope, aggregation = True)
	renewableGenerationDict          = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, renewableAssetsByScope, aggregation = True)

	ret = []
	# Un-optimized demand
	for index in unoptimizedDemandDict:
		# index = (scope, deliveryPoint, energyName, testCase)
		ret += [[list(index)+[UNOPTIMIZED_DEMAND], unoptimizedDemandDict[index] * MW_TO_W_CONVERSION]]
		if index in renewableAvailableCapacitiesDict:
			ret += [[list(index)+[UNOPTIMIZED_NET_DEMAND], (unoptimizedDemandDict[index] - renewableAvailableCapacitiesDict[index]) * MW_TO_W_CONVERSION]]
		else:
			ret += [[list(index)+[UNOPTIMIZED_NET_DEMAND], unoptimizedDemandDict[index] * MW_TO_W_CONVERSION]]
	# Optimized demand
	for index in optimizedDemandDict:
		# index = (scope, deliveryPoint, energyName, testCase)
		ret += [[list(index)+[OPTIMIZED_DEMAND], optimizedDemandDict[index] * MW_TO_W_CONVERSION]]
		if index in renewableGenerationDict:
			ret += [[list(index)+[OPTIMIZED_NET_DEMAND], (optimizedDemandDict[index] - renewableGenerationDict[index]) * MW_TO_W_CONVERSION]]
		else:
			ret += [[list(index)+[OPTIMIZED_NET_DEMAND], optimizedDemandDict[index] * MW_TO_W_CONVERSION]]
	return ret

def getTimeContext(context):
	timeContext = [context.getStartingDate(), context.getTimeStepDuration(), context.getTimeStepCount()]
	return timeContext