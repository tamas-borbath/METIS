########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Share of production in national demand (%)
-------------------------------------------

Indexed by
	* scope
	* delivery point
	* energy
	* test case
	* technology
	* asset name

Return, for each technology and for each energy, the share (in %) of the energy demand procured by the technology. 

.. math::

	\\small share_{dp, technology, energy} = \\frac{\\sum_t production_{t}^{dp, technology, energy}}{\\sum_t demand_{t}^{dp, energy}}

Because of transmissions, the result can be greater than 100% (if the delivery point is a net exporter) or lower than 100% (if the delivery point is a net importer).

"""


def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, PRODUCED_ENERGIES))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	selectedTechnologies   = indexFilter.filterIndexList(4, getTechnologies(context, excludedTechnologies = TRANSMISSION_TYPES))
	selectedAssets         = indexFilter.filterIndexList(5, getAssets(context, excludedTechnologies = TRANSMISSION_TYPES))
	
	productionAssetsByScope = getAssetsByScope(context, selectedScopes, includedAssetsName=selectedAssets, includedTechnologies = selectedTechnologies)
	demandAssetsByScope     = getAssetsByScope(context, selectedScopes, includeFinancialAssets=True, includedTechnologies = DEMAND_TYPES)
	
	productionDict = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, productionAssetsByScope, indexByAsset=True)
	demandDict     = getDemandDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, demandAssetsByScope, aggregation = True)
	
	for index in productionDict:
		demandIndex = index[:-2]
		if demandIndex in demandDict and demandDict[demandIndex].getSumValue() > 0:
			kpiDict[index] = productionDict[index].getSumValue() / demandDict[demandIndex].getSumValue() * 100
		else:
			kpiDict[index] = 0
	
	return kpiDict

def get_indexing(context):
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = PRODUCED_ENERGIES), getTestCasesIndexing(context), 
							getTechnologiesIndexing(context, excludedTechnologies = TRANSMISSION_TYPES),
							getAssetsIndexing(context, excludedTechnologies = TRANSMISSION_TYPES)]
	return baseIndexList
    

IndicatorLabel = "Share of production per technology as part of national demand"
IndicatorUnit = "%"
IndicatorDeltaUnit = "%"
IndicatorDescription = "Share of production per technology as part of national demand"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Production"
IndicatorTags = "Power System, Gas System, Power Markets"
