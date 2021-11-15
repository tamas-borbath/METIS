########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Congestion Rent (euro)
-----------------------

Indexed by
	* energy
	* transmission line
	* test case

The congestion rent is the benefit made when transferring energy from a zone to another. 
The congestion rent of a transmission line from zone :math:`Z_1` to zone :math:`Z_2` is defined as the cost saved from using a production from another zone to meet a local demand:

.. math::

	 \\small congestionRent_{Z_1 -> Z_2} = \\sum_t (marginalCost_t^{Z_2} - marginalCost_t^{Z_1}).exchangedPower_t^{Z_1 -> Z_2}

It is called congestion rent, because at time steps when a line is not saturated, marginal costs in the two extremities of the line converge and the surplus is 0.
In other words, the rent is only derived from congestions.

Since the result is given for each transmission, and that transmissions are directional (e.g. transmision :math:`Z_1 -> Z_2` is different from transmision :math:`Z_2 -> Z_1`), one must sum the results given
for each direction in order to have the total congestion rent associated to a transmission between two zones:

.. math::

	 \\small congestionRent_{Z_1, Z_2} = congestionRent_{Z_1 -> Z_2} + congestionRent_{Z_2 -> Z_1}

"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)

	selectedScopes        = indexFilter.filterIndexList(0, getScopes())
	selectedEnergies      = indexFilter.filterIndexList(1, getEnergies(context, includedEnergies = {ELECTRICITY, GAS}))
	selectedTestCases     = indexFilter.filterIndexList(2, context.getResultsIndexSet())
	selectedAssets        = indexFilter.filterIndexList(3, getAssets(context, includedTechnologies = TRANSMISSION_TYPES))
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedAssetsName = selectedAssets)
	
	congestionRentDict = getCongestionRentDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedAssetsByScope)

	for index in congestionRentDict:
		kpiDict[index] = congestionRentDict[index].getSumValue()
	
	return kpiDict

def get_indexing(context):
	baseIndexList = [getScopesIndexing(), getEnergiesIndexing(context, includedEnergies = {ELECTRICITY, GAS}), getTestCasesIndexing(context), getAssetsIndexing(context, includedTechnologies = TRANSMISSION_TYPES)]
	return baseIndexList

IndicatorLabel = "Congestion rent"
IndicatorUnit = u"\u20ac"
IndicatorDeltaUnit = u"\u20ac"
IndicatorDescription = "Congestion rent attached to a transmission"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Welfare"
IndicatorTags = " Power System "
