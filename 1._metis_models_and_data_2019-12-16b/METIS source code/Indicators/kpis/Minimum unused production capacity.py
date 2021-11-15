########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Minimum unused production capacity (Wh)
----------------------------------------

Indexed by
	* scope
	* delivery point
	* energy
	* test case
	* technology

Minimal margin between available capacity and energy production for a given delivery point, for a given energy and a given technology:

.. math::

	\\small minMargin_{dp, techno, energy} = \\min_t availability_{t, dp, techno, energy} \times pmax_{t, dp, techno, energy} - production_{t, dp, techno, energy}

"""

TOTAL_LABEL = "Total of selected technologies"

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = PRODUCED_ENERGIES))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	selectedTechnologies   = indexFilter.filterIndexList(4, getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies=PRODUCTION_TYPES) + [TOTAL_LABEL])
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets=True, includedTechnologies = selectedTechnologies)
	
	availCapacitiesDict = getAvailableCapacityDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope)
	productionDict = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope)
	
	totalDict = defaultdict(lambda: getZeroTs(context))
	for index in availCapacitiesDict:
		# Margin by techno
		marginTs = availCapacitiesDict[index] - productionDict[index]
		kpiDict[index] = marginTs.getMinValue() * MW_TO_W_CONVERSION
		# Total demand
		scope, dpName, energy, testCase, techno = index
		indexTotal = (scope, dpName, energy, testCase, TOTAL_LABEL)
		totalDict[indexTotal] = totalDict[indexTotal] + marginTs
	
	if TOTAL_LABEL in selectedTechnologies:
		for index in totalDict:
			kpiDict[index] = totalDict[index].getMinValue() * MW_TO_W_CONVERSION
	
	
	return kpiDict

def get_indexing(context):
	demandTechnologies = getTechnologies(context, includeFinancialAssetTypes=True, includedTechnologies=PRODUCTION_TYPES)
	selectedTechnologies = demandTechnologies + [TOTAL_LABEL]
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = PRODUCED_ENERGIES), getTestCasesIndexing(context), 
						BaseIndexDefault("Data", selectedTechnologies, False, False, True, 0)]
	return baseIndexList

IndicatorLabel = "Minimum unused production capacity"
IndicatorUnit = "Wh"
IndicatorDeltaUnit = "Wh"
IndicatorDescription = "Minimum unused production capacity per delivery point and technology"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Production"
IndicatorTags = "Power System, Gas System, Power Markets"
