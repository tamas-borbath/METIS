########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Net Production (Wh)
--------------------

Indexed by
	* scope
	* delivery point
	* energy
	* test case
	* technology
	* asset name

Return the total energy production in a given delivery point, a given energy and a given technology minus the consumption on the same period.

.. math::

	\\small production_{dp, energy, techno} = \\sum_t (production_{t, dp, energy, techno} - consumption_{t, dp, energy, techno})

"""


def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = PRODUCED_ENERGIES))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	selectedTechnologies   = indexFilter.filterIndexList(4, getTechnologies(context, includedTechnologies=PRODUCTION_TYPES, excludedTechnologies=TRANSMISSION_TYPES))
	selectedAssets         = indexFilter.filterIndexList(5, getAssets(context, includedTechnologies=PRODUCTION_TYPES, excludedTechnologies=TRANSMISSION_TYPES))
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedAssetsName=selectedAssets, includedTechnologies = selectedTechnologies)
	
	productionDict = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope, indexByAsset=True)
	consumptionDict = getConsumptionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope, indexByAsset=True)

	for index in productionDict:
		kpiDict[index] = productionDict[index].getSumValue() * timeStepDuration * MW_TO_W_CONVERSION
		if index in consumptionDict:
			kpiDict[index] -= consumptionDict[index].getSumValue() * timeStepDuration * MW_TO_W_CONVERSION
	
	return kpiDict

def get_indexing(context):
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = PRODUCED_ENERGIES), getTestCasesIndexing(context), 
							getTechnologiesIndexing(context, includedTechnologies=PRODUCTION_TYPES, excludedTechnologies=TRANSMISSION_TYPES),
							getAssetsIndexing(context, includedTechnologies=PRODUCTION_TYPES, excludedTechnologies=TRANSMISSION_TYPES)]
	return baseIndexList

IndicatorLabel = "Net Production"
IndicatorUnit = "Wh"
IndicatorDeltaUnit = "Wh"
IndicatorDescription = "Total production per delivery point"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Production"
IndicatorTags = "Power System, Gas System, Power Markets"
