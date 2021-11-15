########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Installed capacities (W)
-------------------------

Indexed by
	* scope
	* delivery point
	* energy (electricity or gas)
	* test case
	* technology
	* asset name

Return the installed capacity of a given technology, for a given delivery point and a given test case.

"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies={ELECTRICITY, GAS}))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getTestCases()) #This differs from for testCase in context.getResultsIndexSet() which requires to have a computed solution!
	selectedTechnologies   = indexFilter.filterIndexList(4, getTechnologies(context, includedTechnologies = PRODUCTION_TYPES))
	selectedAssets         = indexFilter.filterIndexList(5, getAssets(context, includedTechnologies = PRODUCTION_TYPES))
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedAssetsName=selectedAssets, includedTechnologies=selectedTechnologies)

	capacitiesDict = getInstalledCapacityDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope, indexByAsset=True)

	for index in capacitiesDict:
		kpiDict[index] = capacitiesDict[index].getMeanValue() * MW_TO_W_CONVERSION
	
	return kpiDict

def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = {ELECTRICITY, GAS}), getTestCasesIndexing(context), 
							getTechnologiesIndexing(context, includedTechnologies = PRODUCTION_TYPES),
							getAssetsIndexing(context, includedTechnologies = PRODUCTION_TYPES)]
	return baseIndexList

IndicatorLabel = "Installed capacities"
IndicatorUnit = "W"
IndicatorDeltaUnit = "W"
IndicatorDescription = "Installed capacities per delivery point and per technology"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Inputs>Production"
IndicatorTags = "Power System, Gas System, Power Markets"