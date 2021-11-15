########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Load payment (euro)
--------------------

Indexed by
	* scope
	* delivery point
	* energy
	* test case

The load payment corresponds to the price consumers must pay for the energy consumed over the year, in a given delivery point. It is calculated as the sum, over the year, of the hourly marginal cost of the delivery point
for the corresponding energy times the hourly demand for this energy in the delivery point.

For a given energy, the load payment differs depending on the scope, the load payment is computed as follows:

.. math:: \\small loadPayment_{dp, energy} = \\sum_t marginalCost_t^{dp, energy}*demand_t^{dp, energy}

"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):

	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = PRODUCED_ENERGIES))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet()) 
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets=True, includedTechnologies = DEMAND_TYPES)

	marginalCostDict      = getMarginalCostDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints)
	consumptionDict       = getConsumptionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope, aggregation=True)

	for index in marginalCostDict:
		kpiDict[index] = (marginalCostDict[index] * consumptionDict[index]).getSumValue()

	return kpiDict

	
def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = PRODUCED_ENERGIES), getTestCasesIndexing(context)]
	return baseIndexList
	

IndicatorLabel = "Load payment"
IndicatorUnit = u"\u20ac"
IndicatorDeltaUnit = u"\u20ac"
IndicatorDescription = "Load payment"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Marginal Costs"
IndicatorTags = " Power System, Power Markets "