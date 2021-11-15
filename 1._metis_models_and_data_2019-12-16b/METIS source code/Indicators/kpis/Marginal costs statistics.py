########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Marginal costs statistics (euro/MWh)
-------------------------------------

Indexed by
	* scope
	* delivery point
	* energy (electricity, reserve or gas)
	* test case
	* statistics (min, max, average or demand average)

Computes the minimum, maximum and average value of the marginal cost over the year for a given delivery point and energy.

The KPI also computes the demand weighted (demand average) marginal cost:

.. math::

	\\small demandWeightedMarginalCost_{zone, energy} = \\frac{\\sum_t marginalCost_t^{zone, energy}.demand_t^{zone, energy}}{\\sum_t demand_t^{zone, energy}} 

The marginal cost of a given energy and a given delivery point is the variable cost of the production unit that was last called (after the costs of the different technologies were ordered in increasing order) to meet the energy demand in the delivery point.

"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):

	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = PRODUCED_ENERGIES))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets=True, includedTechnologies = DEMAND_TYPES)
	
	demandDict = getDemandDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope, aggregation = True)
	marginalCostDict = getMarginalCostDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints)

	for index in marginalCostDict:
		kpiDict[index + ("Min",)] = marginalCostDict[index].getMinValue() / timeStepDuration
		kpiDict[index + ("Max",)] = marginalCostDict[index].getMaxValue() / timeStepDuration
		kpiDict[index + ("Average",)] = marginalCostDict[index].getMeanValue() / timeStepDuration
		if index in demandDict and demandDict[index].getSumValue() > 0:
			kpiDict[index + ("Demand average",)] = (marginalCostDict[index]*demandDict[index]).getSumValue() / (timeStepDuration*demandDict[index]).getSumValue()

	return kpiDict

	
def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), context.getDeliveryPointsIndexing(), getEnergiesIndexing(context, includedEnergies = PRODUCED_ENERGIES), getTestCasesIndexing(context), BaseIndexDefault("Statistics",["Min", "Max", "Average", "Demand average"], False, False, True, 0)]
	return baseIndexList
	

IndicatorLabel = "Marginal costs statistics"
IndicatorUnit = u"\u20ac/MWh"
IndicatorDeltaUnit = u"\u20ac/MWh"
IndicatorDescription = "Marginal costs statistics (min, max and average)"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Marginal Costs"
IndicatorTags = "Power System, Gas System, Power Markets"