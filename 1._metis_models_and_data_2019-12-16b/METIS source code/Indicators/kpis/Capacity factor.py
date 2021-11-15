########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################


extends("BaseKPI.py")

"""
Capacity factor (%)
-------------------

Indexed by
	* scope
	* delivery point
	* energy (electricity or gas)
	* test case
	* technology

Return the capacity factor, which is the mean annual usage of a given technology relative to its installed capacity in a given delivery point:

.. math::

	 \\small capacityFactor_{technology, dp} = \\frac{mean_t(production_t^{technology, dp})}{installedCapacity^{technology, dp}}

"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = {ELECTRICITY, GAS}))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	selectedTechnologies   = indexFilter.filterIndexList(4, getTechnologies(context, includedTechnologies = PRODUCTION_TYPES))
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedTechnologies = selectedTechnologies)
	
	productionsDict = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope)
	capacitiesDict  = getInstalledCapacityDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope)

	for index in productionsDict:
		if index in capacitiesDict:
			capacity = capacitiesDict[index].getValue()
			if capacity > 0:
				kpiDict[index] = 100 * (productionsDict[index]/capacitiesDict[index]).getMeanValue()

	return kpiDict

def get_indexing(context):
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = {ELECTRICITY, GAS}), getTestCasesIndexing(context), getTechnologiesIndexing(context, includedTechnologies = PRODUCTION_TYPES)]
	return baseIndexList

IndicatorLabel = "Capacity factor"
IndicatorUnit = "%"
IndicatorDeltaUnit = "%"
IndicatorDescription = "Capacity factor attached to a technology"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Production"
IndicatorTags = " Power System, Gas System, Power Markets "


