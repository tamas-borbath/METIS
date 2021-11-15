########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Reserve Sizing (W)
-------------------

Indexed by
	* scope
	* delivery point
	* reserve energy
	* test case
	
Return reserve requirements per delivery point in W (annual average values instead of annual volumes).


"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies=RESERVE_ENERGIES))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getTestCases()) #This differs from for testCase in context.getResultsIndexSet() which requires to have a computed solution!
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets=True, includedTechnologies = DEMAND_TYPES)
	
	demandDict = getDemandDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope, aggregation = True)

	for index in demandDict:
		kpiDict[index] = demandDict[index].getMeanValue() * MW_TO_W_CONVERSION
	
	return kpiDict

def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies=RESERVE_ENERGIES), getTestCasesIndexing(context)]
	return baseIndexList

IndicatorLabel = "Reserve sizing"
IndicatorUnit = "W"
IndicatorDeltaUnit = "W"
IndicatorDescription = "Average reserve demand attached to a delivery point"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Inputs>Demand"
IndicatorTags = "Power System, Power Markets"