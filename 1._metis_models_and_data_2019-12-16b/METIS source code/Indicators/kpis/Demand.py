########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Demand (Wh)
------------

Indexed by
	* scope
	* delivery point
	* test case
	* energy
	* demand type
	* asset name

Return the annual volumes of energy demand for a given technology or contract.
We here consider the flexible demand after optimization (using the consumption of the corresponding assets).
For asset "Electric Vehicles" with behavior Vehicule to grid, the demand is the difference between consumption and generation of the vehicles.

"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies=PRODUCED_ENERGIES))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getTestCases()) #This differs from for testCase in context.getResultsIndexSet() which requires to have a computed solution!
	selectedTechnologies   = indexFilter.filterIndexList(4, getTechnologies(context, includeFinancialAssetTypes=True, includedTechnologies=DEMAND_TYPES))
	selectedAssets         = indexFilter.filterIndexList(5, getAssets(context, includeFinancialAssets=True, includedTechnologies=DEMAND_TYPES))

	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets=True, includedAssetsName=selectedAssets, includedTechnologies=selectedTechnologies)

	demandDict = getDemandDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope, indexByAsset=True)
	
	for index in demandDict:
		kpiDict[index] = demandDict[index].getSumValue() * timeStepDuration * MW_TO_W_CONVERSION
	
	return kpiDict


def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies=PRODUCED_ENERGIES), getTestCasesIndexing(context), 
							getTechnologiesIndexing(context, includeFinancialAssetTypes=True, includedTechnologies=DEMAND_TYPES),
							getAssetsIndexing(context, includeFinancialAssets=True, includedTechnologies=DEMAND_TYPES)]
	return baseIndexList

IndicatorLabel = "Demand"
IndicatorUnit = "Wh"
IndicatorDeltaUnit = "Wh"
IndicatorDescription = "Total optimized demand (substracting load curtailment and V2G production)"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Inputs>Demand"
IndicatorTags = "Power System, Gas System, Power Markets"