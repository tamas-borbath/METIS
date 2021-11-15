########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Marginal costs (euro/MWh)
-------------------------

Indexed by:
	* scope
	* delivery point
	* energy (electricity, reserve or gas)
	* test case

The marginal cost of a given energy and a given delivery point is the variable cost of the production unit that was last called (after the costs of the different technologies were ordered in increasing order) to meet the energy demand in the delivery point.

This KPI computes the average value of the marginal cost over the year for a given delivery point and energy. Additional statistics can be calculated in *Marginal costs statistics* KPI

"""


def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = PRODUCED_ENERGIES))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())

	marginalCostDict = getMarginalCostDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints)

	for index in marginalCostDict:
		kpiDict[index] = marginalCostDict[index].getMeanValue() / timeStepDuration

	
	return kpiDict

	
def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = PRODUCED_ENERGIES), getTestCasesIndexing(context)]
	return baseIndexList
	

IndicatorLabel = "Marginal costs"
IndicatorUnit = u"\u20ac/MWh"
IndicatorDeltaUnit = u"\u20ac/MWh"
IndicatorDescription = "Marginal cost attached to a delivery point"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Marginal Costs"
IndicatorTags = "Power System, Gas System, Power Markets"