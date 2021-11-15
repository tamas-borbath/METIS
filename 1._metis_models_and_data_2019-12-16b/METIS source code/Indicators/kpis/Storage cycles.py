########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Storage cycles (cycles)
-----------------------------

Indexed by
	* scope
	* delivery point
	* energy (electricity)
	* test case

For a given delivery point, computes the equivalent number of full discharge cycles of all the cycling storage units within the delivery point, based on their annual production and their production capacity.

"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = {ELECTRICITY, GAS}))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedTechnologies = CYCLE_STORAGE_TYPES)
	
	productionDict = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope)
	capacitiesDict = getStorageCapacityDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope)

	for index in productionDict:
		if index in capacitiesDict:
			capacity = capacitiesDict[index].getMeanValue()
			if capacity != 0:
				kpiDict[index] = productionDict[index].getSumValue() * timeStepDuration / capacity

	return kpiDict

def get_indexing(context):
	baseIndexList = [getScopesIndexing(),  getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = {ELECTRICITY, GAS}), getTestCasesIndexing(context)]
	return baseIndexList

IndicatorLabel = "Storage cycles"
IndicatorUnit = ""
IndicatorDeltaUnit = ""
IndicatorDescription = "Number of full storage cycles per delivery point"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Production"
IndicatorTags = "Power System, Power Markets"