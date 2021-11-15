########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Net demand peak (W)
--------------------

Indexed by
	* scope
	* zone
	* energy (electricity, gas)
	* test case

Return the maximum value over the year of the net demand, which is defined as the difference between the realized energy demand and the available capacity of flexible renewable energy at a given delivery point:

.. math::

	\\small netDemandPeak_{testCase, zone} = max_t(demand_t^{testCase, zone} - availableRenewableCapacity_t^{testCase, zone})
"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = {ELECTRICITY, GAS}))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getTestCases()) #This differs from for testCase in context.getResultsIndexSet() which requires to have a computed solution!
	
	demandAssetsByScope     = getAssetsByScope(context, selectedScopes, includeFinancialAssets = True, includedTechnologies = DEMAND_TYPES)
	renewableAssetsByScope  = getAssetsByScope(context, selectedScopes, includedTechnologies = NON_FLEXIBLE_RES_TYPES)
	
	demandsDict                      = getDemandDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, demandAssetsByScope, aggregation = True)
	renewableAvailableCapacitiesDict = getAvailableCapacityDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, renewableAssetsByScope, aggregation = True)

	for index in demandsDict:
		peakDemand = demandsDict[index].getMaxValue() * MW_TO_W_CONVERSION
		if index in renewableAvailableCapacitiesDict.keys():
			kpiDict[index] = (demandsDict[index] - renewableAvailableCapacitiesDict[index]).getMaxValue() * MW_TO_W_CONVERSION
		else:
			kpiDict[index] = peakDemand
	
	return kpiDict

def get_indexing(context):
	baseIndexList = [getScopesIndexing(), context.getDeliveryPointsIndexing(), getEnergiesIndexing(context, includedEnergies = {ELECTRICITY, GAS}), getTestCasesIndexing(context)]
	return baseIndexList

IndicatorLabel = "Net demand peak"
IndicatorUnit = "W"
IndicatorDeltaUnit = "W"
IndicatorDescription = "Net demand peak"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Inputs>Demand"
IndicatorTags = "Power System, Power Markets"