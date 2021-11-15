########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Border exchange surplus (euro)
-------------------------------

Indexed by
	* scope
	* delivery point
	* main energy
	* test case
	* technology
	* asset name

This KPI will return No data on power contexts and gas contexts without import or export contracts as it only applies to gas import and export contracts.

A border exchange surplus is defined as the surplus of model outsiders, that is all actors which are not explicitly represented but are aggregated into flexible import/export assets. 
Flexible imports and exports are optimized during simulations along with the other supplies and consumptions: imports (respectively exports) level at each time step depend on the import costs (respectively export earnings) on one hand and the endogenous marginal supply cost on the other hand. 
The border exchange surplus represents the benefit that an outside actor receives for selling its product on the modeled network (for flexible imports) or from buying it from the network (for flexible exports).

The KPI thus computes the following:

For a flexible import asset:

.. math::

	\\small borderExchangeSurplus_{dp, energy, asset} = \\small \\sum_t (prod_t^{dp, energy, techno}.(margCost_t^{dp, energy} - importPrice^{dp, energy, techno})


For a flexible export asset:

.. math::

	\\small borderExchangeSurplus_{dp, energy, asset} = \\small \\sum_t (prod_t^{dp, energy, techno}.(exportPrice^{dp, energy, techno} - margCost_t^{dp, energy}

"""



def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = {ELECTRICITY, GAS}))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	selectedTechnologies   = indexFilter.filterIndexList(4, getTechnologies(context, includedTechnologies = FLEXIBLE_EXPORT_TYPES|FLEXIBLE_IMPORT_TYPES))
	selectedAssets         = indexFilter.filterIndexList(5, getAssets(context, includedTechnologies = FLEXIBLE_EXPORT_TYPES|FLEXIBLE_IMPORT_TYPES))

	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedAssetsName=selectedAssets, includedTechnologies = selectedTechnologies)
	
	exchangeSurplusDict = getExchangeSurplusDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope)

	for index in exchangeSurplusDict:
		kpiDict[index] = exchangeSurplusDict[index].getSumValue()
	
	return kpiDict

def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = {ELECTRICITY, GAS}), getTestCasesIndexing(context), 
							getTechnologiesIndexing(context, includedTechnologies = FLEXIBLE_EXPORT_TYPES|FLEXIBLE_IMPORT_TYPES),
							getAssetsIndexing(context, includedTechnologies = FLEXIBLE_EXPORT_TYPES|FLEXIBLE_IMPORT_TYPES)]
	return baseIndexList

IndicatorLabel = "Border exchange surplus"
IndicatorUnit = u"\u20ac"
IndicatorDeltaUnit = u"\u20ac"
IndicatorDescription = "Surplus of an outside actor from supplying"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Welfare"
IndicatorTags = " Power System, Power Markets "

