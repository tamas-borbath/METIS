########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Welfare (euro)
---------------

Indexed by
	* scope
	* delivery point
	* test case
	
The welfare for a given delivery point is the sum of its consumer surplus, its producer surplus, the border exchange surplus and half of the congestion rent for power transmission lines connected to the delivery point:

.. math:: \\small welfare_{scope, dp, tc} = consumerSurplus_{scope, dp, tc} + producerSurplus_{scope, dp, tc} + exchangeSurplus_{scope, dp, tc} + \\frac{1}{2} \\sum_{transmission\ t \\in dp} congestionRent_{scope, t, tc}


"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedTestCases      = indexFilter.filterIndexList(2, context.getResultsIndexSet())
	
	productionAssetsByScope   = getAssetsByScope(context, selectedScopes, includedTechnologies = PRODUCTION_TYPES)
	transmissionAssetsByScope = getAssetsByScope(context, selectedScopes, includedTechnologies = TRANSMISSION_TYPES)
	flexibleAssetsByScope     = getAssetsByScope(context, selectedScopes, includedTechnologies = FLEXIBLE_EXPORT_TYPES|FLEXIBLE_IMPORT_TYPES)
	
	# All energies : filter on techno (and interface) only
	selectedEnergies = Crystal.listEnergies(context)
	
	marginalCostDict        = getMarginalCostDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints)

	producerSurplusDict = getProducerSurplusDict(context, selectedScopes, selectedTestCases, selectedDeliveryPoints, productionAssetsByScope, aggregation=True)

	exchangeSurplusDict = getExchangeSurplusDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, flexibleAssetsByScope, aggregation=True)
	
	consumerSurplusDict = getConsumerSurplus(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints)
	
	#Init
	for (scope, dpName, energy, testCase) in marginalCostDict:
		kpiDict[scope, dpName, testCase] = 0

	#Congestion Rent
	congestionRentDict = getCongestionRentByDP(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, transmissionAssetsByScope)
	for (scope, dpName, energy, testCase) in congestionRentDict:
		kpiDict[scope, dpName, testCase] += congestionRentDict[scope, dpName, energy, testCase].getSumValue()

	#Surplus
	for index in marginalCostDict:
		indexKpi = (index[0], index[1], index[3])
		#Consumer
		if index in consumerSurplusDict:
			kpiDict[indexKpi] += consumerSurplusDict[index].getSumValue()
		#Exchanges
		if index in exchangeSurplusDict:
			kpiDict[indexKpi] += exchangeSurplusDict[index].getSumValue()
	
	for indexKpi in producerSurplusDict:
		#Producer
		kpiDict[indexKpi] += producerSurplusDict[indexKpi].getSumValue()

	return kpiDict

def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getTestCasesIndexing(context)]
	return baseIndexList

IndicatorLabel = "Welfare"
IndicatorUnit = u"\u20ac"
IndicatorDeltaUnit = u"\u20ac"
IndicatorDescription = "Welfare attached to a delivery point"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Welfare"
IndicatorTags = "Power System, Power Markets"

