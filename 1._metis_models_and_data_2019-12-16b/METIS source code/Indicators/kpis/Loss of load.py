########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Loss Of Load (h)
------------------------

Indexed by
	* scope
	* delivery point
	* energy
	* test case

Loss Of Load (LOL), also called Loss Of Load Expectation (LOLE) represents the number of hours per year in which there is a situation of loss of load (i.e. that supply does not meet demand). 
It takes into account the fact that if the LOL is "too large", then additional capacities (power plants or batteries) will be built. See KPI "Loss of load" for more details.

.. math::

	\\small LOL_{zone} = \\sum_t \\mathbf 1_{\\{supply_t < demand_t\\}}

"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = PRODUCED_ENERGIES))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets=True, includedTechnologies = LOSS_OF_ENERGY_TYPES)

	lossOfLoadDict          = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope, aggregation=True)
	
	for index in lossOfLoadDict:
		kpiDict[index] = lossOfLoadDict[index].getValue().countAbove(0.001) * timeStepDuration

	return kpiDict

def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = PRODUCED_ENERGIES), getTestCasesIndexing(context)]
	return baseIndexList

IndicatorLabel = "Loss of load"
IndicatorUnit = "h"
IndicatorDeltaUnit = "h"
IndicatorDescription = "Loss of load expectation per delivery point"
IndicatorParameters = []
IndicatorIcon = "" 
IndicatorCategory = "Results>Loss of load"
IndicatorTags = "Power System, Gas System, Power Markets"
