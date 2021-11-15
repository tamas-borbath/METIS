########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Loss of load cost (euro)
-------------------------

Indexed by
	* scope
	* delivery point
	* energy
	* test case

The loss of load cost is the cost associated to loss of load (LoL) in an energy system.
In classic models, this cost is directly indexed on the value of loss of load (VoLL), which is the amount customers would be willing to pay in order to avoid a disruption in their electricity service.
This leads to the following formulation:

.. math::

	\\small LoLcost_{dp} = \\sum_t VoLL^{dp}.LoL_t^{dp}

"""


def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = PRODUCED_ENERGIES))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets=True, includedTechnologies = LOSS_OF_ENERGY_TYPES)

	lossOfLoadDict          = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope, aggregation=True)
	lossOfLoadPriceDict     = getPriceDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope, aggregation = True)

	for index in lossOfLoadDict:
		kpiDict[index] = (lossOfLoadDict[index]*lossOfLoadPriceDict[index]).getSumValue()

	return kpiDict

def get_indexing(context):
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = PRODUCED_ENERGIES), getTestCasesIndexing(context)]
	return baseIndexList
	

IndicatorLabel = "Loss of load cost"
IndicatorUnit = u"\u20ac"
IndicatorDeltaUnit = u"\u20ac"
IndicatorDescription = "Loss of load cost attached to a delivery point"
IndicatorParameters = []
IndicatorIcon = "" 
IndicatorCategory = "Results>Loss of load"
IndicatorTags = "Power System, Gas System, Power Markets"
