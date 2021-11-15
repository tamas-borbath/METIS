########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Production (Wh)
----------------

Indexed by
	* scope
	* delivery point
	* energy
	* test case
	* technology
	* asset name

Total energy production in a given delivery point, for a given energy and a given technology:

.. math::

	\\small production_{dp, techno, energy} = \\sum_t production_{t, dp, techno, energy}

"""


def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = PRODUCED_ENERGIES))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	selectedTechnologies   = indexFilter.filterIndexList(4, getTechnologies(context, excludedTechnologies=TRANSMISSION_TYPES))
	selectedAssets         = indexFilter.filterIndexList(5, getAssets(context, excludedTechnologies=TRANSMISSION_TYPES))
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedAssetsName=selectedAssets, includedTechnologies = selectedTechnologies)
	
	productionDict = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope, indexByAsset=True)

	for index in productionDict:
		kpiDict[index] = productionDict[index].getSumValue() * timeStepDuration * MW_TO_W_CONVERSION
	
	return kpiDict

def get_indexing(context):
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = PRODUCED_ENERGIES), getTestCasesIndexing(context), 
							getTechnologiesIndexing(context, excludedTechnologies=TRANSMISSION_TYPES),
							getAssetsIndexing(context, excludedTechnologies=TRANSMISSION_TYPES)]
	return baseIndexList

IndicatorLabel = "Production"
IndicatorUnit = "Wh"
IndicatorDeltaUnit = "Wh"
IndicatorDescription = "Total production per delivery point and technology"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Production"
IndicatorTags = "Power System, Gas System, Power Markets"
