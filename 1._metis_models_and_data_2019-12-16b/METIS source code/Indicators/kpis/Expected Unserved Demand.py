########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Expected Unserved Demand (%)
-----------------------------

Indexed by
	* scope
	* delivery point
	* energy
	* test case

The Expected Unserved Demand is a metric used to measure security of supply. This is the amount of electricity, gas or reserve demand that is expected not to be met by the production means during the year.
It is calculated as the Loss Of Load volumes (LOL) expressed relatively to the corresponding annual demand volumes, in percentage. It can be calculated for each energy independently:

.. math::
	
	\\small EENS_{dp, energy} = \\frac {LOL_{dp, energy}}{demand_{dp, energy}} (\\%)

See the 'Loss of load' KPI for further documentation about the loss of load.

"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = PRODUCED_ENERGIES))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	
	demandAssetsByScope     = getAssetsByScope(context, selectedScopes, includeFinancialAssets=True, includedTechnologies = DEMAND_TYPES)
	lossOfLoadAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets=True, includedTechnologies = LOSS_OF_ENERGY_TYPES)

	demandDict             = getDemandDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, demandAssetsByScope, aggregation = True)
	lossOfLoadDict         = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, lossOfLoadAssetsByScope, aggregation = True)

	for index in lossOfLoadDict:
		if index in demandDict:
			demand = demandDict[index].getSumValue()
			if demand != 0:
				kpiDict[index] = 100 * lossOfLoadDict[index].getSumValue() / demand
	
	return kpiDict

def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = PRODUCED_ENERGIES), getTestCasesIndexing(context)]
	return baseIndexList

IndicatorLabel = "Expected Unserved Demand"
IndicatorUnit = "%"
IndicatorDeltaUnit = "%"
IndicatorDescription = "Expected energy not served as a percentage of demand volume attached to a delivery point"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Loss of load"
IndicatorTags = "Power System, Gas System, Power Markets"
