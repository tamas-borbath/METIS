########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Scarcity Price Hours (h)
-------------------------

Indexed by
	* scope
	* delivery point
	* energy
	* test case

Return the number of hours where marginal costs of a delivery point is higher than a certain value reflecting scarcity of production capacity at said hours.
	
"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):

	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getZones(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = PRODUCED_ENERGIES))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets=True, includedTechnologies = LOSS_OF_ENERGY_TYPES)

	lossOfLoadPriceDict = getPriceDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope, aggregation = True)
	marginalCostDict    = getMarginalCostDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints)

	for index in marginalCostDict:
		if index in lossOfLoadPriceDict:
			kpiDict[index] = (0.8*lossOfLoadPriceDict[index] - marginalCostDict[index]).getValue().countBelow(0)*timeStepDuration

	return kpiDict

	
def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = PRODUCED_ENERGIES), getTestCasesIndexing(context)]
	return baseIndexList
	

IndicatorLabel = "Scarcity price hours"
IndicatorUnit = u"h"
IndicatorDeltaUnit = u"h"
IndicatorDescription = "Scarcity price hours"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Loss of load"
IndicatorTags = "Power System, Gas System, Power Markets"