########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Consumption (Wh)
------------------

Indexed by
	* scope
	* delivery point
	* energy (including fuels)
	* test case
	* technology
	* asset name

Return the annual volumes of energy demand for a given technology or contract.
We here consider the flexible demand after optimization (using the consumption of the corresponding assets).

"""

TECHNO_TO_CONSIDER = DEMAND_TYPES|PRODUCTION_TYPES|{F_GAS_CONSUMPTION}

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies=PRODUCED_ENERGIES))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	selectedTechnologies   = indexFilter.filterIndexList(4, getTechnologies(context, includeFinancialAssetTypes=True, includedTechnologies=TECHNO_TO_CONSIDER))
	selectedAssets         = indexFilter.filterIndexList(5, getAssets(context, includeFinancialAssets=True, includedTechnologies=TECHNO_TO_CONSIDER))
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets=True, includedAssetsName=selectedAssets, includedTechnologies = selectedTechnologies)
	
	consumptionDict = getConsumptionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope, indexByAsset=True)
	
	for index in consumptionDict:
		kpiDict[index] = consumptionDict[index].getSumValue() * timeStepDuration * MW_TO_W_CONVERSION

	return kpiDict

def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies=PRODUCED_ENERGIES), getTestCasesIndexing(context), 
							getTechnologiesIndexing(context, includeFinancialAssetTypes=True, includedTechnologies=TECHNO_TO_CONSIDER),
							getAssetsIndexing(context, includeFinancialAssets=True, includedTechnologies=TECHNO_TO_CONSIDER)]
	return baseIndexList

IndicatorLabel = "Consumption"
IndicatorUnit = "Wh"
IndicatorDeltaUnit = "Wh"
IndicatorDescription = "Total consumption per technology"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results"
IndicatorTags = " Power System, Gas System, Power Markets "