########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Consumer Surplus (euro)
-----------------------

Indexed by
	* scope
	* delivery point
	* energy
	* test case

A consumer surplus occurs when the consumer is willing to pay more for a given product than the current market price.

In classic models, consumers' benefit equals the value of loss of load (VoLL), leading to the following formulation:

.. math::

	\\small consumerSurplus_{dp, energy} = \\sum_t (VoLL^{dp, energy} - marginalCost_t^{dp, energy}) \\times demand_t^{dp, energy}
	 
For a given demand, the term :math:`\\small \\sum_t (VoLL.demand_t)` is a constant, which does not affect comparisons between two scenarios (that have the same demand). 
As the VoLL is arbitrary, those comparisons are usually more interesting than absolute values.
The consumer surplus indicator therefore uses the following formula:

.. math::	\\small consumerSurplus_{dp, energy} = \\sum_t - marginalCost_t^{dp, energy} \\times demand_t^{dp, energy}

NB : The KPI should thus only be used in comparison mode (between scenarios) in order to have a proper meaning.

In the formula above, :math:`\\small demand` is the realized demand. 
For non-flexible demand assets, the realized demand equals the raw demand. For flexible demand assets, which may also produce energy, we have :

.. math::	\\small realizedDemand_t^a = consumption_t^a - production_t^a \ ,\\forall \ demand \ asset \ a

In case of loss of load, part of this realized demand was not really matched. But it is included in the formula to substract to the consumer surplus the cost of not matching this demand.

So when properly including flexible demands and the costs of load management, the consumer surplus becomes :

.. math::	\\small consumerSurplus_{dp, energy} = \\sum_{a \ demand \ asset \ with [dpCons, energyCons]==[dp, energy]} production_t^a \\times marginalCost_t^{dpProd, energyProd} - consumption_t^a \\times marginalCost_t^{dpCons, energyCons} - assetCost_t^a


"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	
	tempDict = getConsumerSurplus(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints)
	
	for index in tempDict:
		kpiDict[index] = tempDict[index].getSumValue()
	
	return kpiDict

def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context), getTestCasesIndexing(context)]
	return baseIndexList

IndicatorLabel = "Consumer surplus"
IndicatorUnit = u"\u20ac"
IndicatorDeltaUnit = u"\u20ac"
IndicatorDescription = "Consumer surplus by delivery point"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Welfare"
IndicatorTags = " Power System, Power Markets "

