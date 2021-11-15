########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################


"""

This view shows, for each energy, a temporal cumulative view showing how the energy demand is divided by technology at this delivery point.
The demands are here shown after optimization (using the consumption of the corresponding assets).
For asset "Electric Vehicles" with behavior Vehicule to grid, the demand is the difference between consumption and generation of the vehicles.

"""


from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'/results\kpis\imports\BaseKPI.py')

ViewLabel = "Cumulative demand (W)"

indexValues = {}
# CUMULATIVE LABELS
TOTAL_DEMAND = "Total demand"

def get_indexing(context) :
	assetList = getAssets(context, includeFinancialAssets=True, includedTechnologies=DEMAND_TYPES)
	assetNameList = [asset.getName() for asset in assetList]
	return [
	getScopesIndexing(localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getDeliveryPointsIndexing(context, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getEnergiesIndexing(context, includedEnergies=PRODUCED_ENERGIES, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getTestCasesIndexing(context, localized=False, selectFirst=True, colorizeIndex=False, groupIndexAsGraphs=2),
	BaseIndexDefault("Technologies", getTechnologies(context, includeFinancialAssetTypes=True, includedTechnologies=DEMAND_TYPES) + [TOTAL_DEMAND], False, False, True, 0),
	BaseIndexDefault("Assets", assetNameList + [TOTAL_DEMAND], False, False, True, 0)
	]

def getData(view) :
	context = view.getContext()
	assetList = getAssets(context, includeFinancialAssets=True, includedTechnologies=DEMAND_TYPES)
	assetNameList = [asset.getName() for asset in assetList]
	
	# Index filter
	selectedScopes         = view.filterIndexList(0, getScopes())
	selectedDeliveryPoints = view.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = view.filterIndexList(2, getEnergies(context, includedEnergies=PRODUCED_ENERGIES))
	selectedEnergyNames = [energy.getName() for energy in selectedEnergies]
	selectedTestCases      = view.filterIndexList(3, getTestCasesWithResults(context))
	selectedTechnologies   = view.filterIndexList(4, getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies = DEMAND_TYPES) + [TOTAL_DEMAND])
	selectedAssets         = view.filterIndexList(5, assetNameList + [TOTAL_DEMAND])
	
	# Compute data
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets = True, includedTechnologies=DEMAND_TYPES) #We need all Demand assets to have a consistent total demand
	
	demandDict = getDemandDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope, indexByAsset=True)
	
	ret = []
	totalDemandDict = defaultdict(lambda: getZeroTs(context))
	for (scope, deliveryPoint, energyName, testCase, technology, assetName) in demandDict:
		if scope in selectedScopes and deliveryPoint in selectedDeliveryPoints and energyName in selectedEnergyNames and testCase in selectedTestCases: #Nec ?
			# Demand curves by techno
			index = (scope, deliveryPoint, energyName, testCase, technology, assetName)
			demandTs = demandDict[index] * MW_TO_W_CONVERSION
			if technology in selectedTechnologies and assetName in selectedAssets:
				ret += [[list(index), demandTs]]
			# Total demand curve
			totalIndex = (scope, deliveryPoint, energyName, testCase, TOTAL_DEMAND, TOTAL_DEMAND)
			totalDemandDict[totalIndex] = totalDemandDict[totalIndex] + demandTs
	
	# Add Total demand curve to results
	if TOTAL_DEMAND in selectedTechnologies and TOTAL_DEMAND in selectedAssets:
		totalDemandDict = dict(totalDemandDict)
		for index in totalDemandDict:
			ret += [[list(index), totalDemandDict[index]]]

	return ret

def getTimeContext(context) :
	timeContext = [ context.getStartingDate() , context.getTimeStepDuration() , context.getTimeStepCount() ]
	return timeContext 


def isLineStacked(index) :
	if TOTAL_DEMAND in index:
		return False
	return True

