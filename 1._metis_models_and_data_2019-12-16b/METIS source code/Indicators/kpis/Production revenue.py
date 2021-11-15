########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Production revenue (euro)
-------------------------

Indexed by
	* scope
	* delivery point
	* energy
	* test case
	* technology
	* asset name

Return the annual revenue received by a given technology in a given delivery point, for the energy it produces.

It is calculated as the sum over the year of the production of the technology times the marginal cost within the considered delivery point:

.. math::

	\\small revenue_{technology, dp} = \\sum_t production_t^{technology, dp}.marginalCost_t^{dp}
	
"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	selectedTechnologies   = indexFilter.filterIndexList(4, getTechnologies(context, includedTechnologies = PRODUCTION_TYPES))
	selectedAssets         = indexFilter.filterIndexList(5, getAssets(context, includedTechnologies = PRODUCTION_TYPES))
	
	selectedAssetsByScope  = getAssetsByScope(context, selectedScopes, includedAssetsName=selectedAssets, includedTechnologies=selectedTechnologies)
	
	producerRevenue = getProductionRevenueDict(context, selectedScopes, selectedTestCases, selectedDeliveryPoints, selectedEnergies, selectedAssetsByScope, aggregation = False, indexByAsset=True)
	for (scope, dp, testCase, techno, assetName, energy) in producerRevenue:
		kpiDict[scope, dp, energy, testCase, techno, assetName] = producerRevenue[scope, dp, testCase, techno, assetName, energy].getSumValue()
	
	return kpiDict

def get_indexing(context):
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context), getTestCasesIndexing(context), 
							getTechnologiesIndexing(context, includedTechnologies = PRODUCTION_TYPES),
							getAssetsIndexing(context, includedTechnologies = PRODUCTION_TYPES)]
	return baseIndexList

IndicatorLabel = "Production revenue"
IndicatorUnit = u"\u20ac"
IndicatorDeltaUnit = u"\u20ac"
IndicatorDescription = "Production revenue per delivery point and technology"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Production"
IndicatorTags = "Power System, Power Markets"