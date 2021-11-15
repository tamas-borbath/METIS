########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Total costs (euro)
------------------

Indexed by:
    * scope
    * delivery point
    * test case

Return the total costs associated to satisfying the demand (for electricity and reserve), for a given delivery point and scope, as the sum of the production costs, the loss of load costs, 
the loss of reserve costs and the curtailment costs:

.. math:: \\small totalCosts{dp,scope} 	& = \\small productionCost_t^{scope,dp} + \\small lossOfLoadCost^{scope,dp} \\\\
											& + \\small lossOfReserveCost^{scope,dp} + \\small CurtailmentCost^{scope,dp} 

"""

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedTestCases      = indexFilter.filterIndexList(2, context.getResultsIndexSet())
	selectedEnergies = getEnergies(context) #All energies
	
	productionAssetsByScope = getAssetsByScope(context, selectedScopes, includedTechnologies = PRODUCTION_TYPES)
	lossOfLoadAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets=True, includedTechnologies = LOSS_OF_ENERGY_TYPES)
	consumptionCurtailmentAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets = True, includedTechnologies = CURTAILABLE_TYPES)
	
	productionCostDict             = getProductionCostDict(context, selectedScopes, selectedTestCases, None, selectedDeliveryPoints, productionAssetsByScope, aggregation=True)
	lossOfLoadDict                 = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, lossOfLoadAssetsByScope, aggregation=True)
	lossOfLoadPriceDict            = getPriceDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, lossOfLoadAssetsByScope, aggregation=True)
	consumptionCurtailmentCostDict = getConsumptionCostDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, consumptionCurtailmentAssetsByScope, aggregation=True)

	# Init 
	for scope, dp, testCase in itertools.product(selectedScopes, selectedDeliveryPoints, selectedTestCases):
		kpiDict[scope, dp, testCase] = 0
		
	#Prod costs
	for index in productionCostDict:
		kpiDict[index] += productionCostDict[index].getSumValue()
	
	# LOL & curtailment costs : all energies summed
	for index in lossOfLoadDict:
		scope, dp, energy, tc = index
		indexKpi = (scope, dp, tc)
		kpiDict[indexKpi] += (lossOfLoadDict[index] * lossOfLoadPriceDict[index]).getSumValue()
		if index in consumptionCurtailmentCostDict:
			kpiDict[indexKpi] += consumptionCurtailmentCostDict[index].getSumValue()
	
	return kpiDict

def get_indexing(context):
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getTestCasesIndexing(context)]
	return baseIndexList

IndicatorLabel = "Total costs"
IndicatorUnit = u"\u20ac"
IndicatorDeltaUnit = u"\u20ac"
IndicatorDescription = "Sum of the production costs, the loss of load/reserve costs and the curtailment costs"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results"
IndicatorTags = "Power System, Power Markets"
