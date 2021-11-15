########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Curtailment (Wh)
----------------------------------

Indexed by
	* scope
	* delivery point
	* energy
	* test case
	* technology
	* asset name

Return the sum of annual volumes of production that is curtailed and annual volumes of production that is not used, per technology.
It is calculated as the difference between the possible RES production (i.e. the installed capacity times the availability) and the actual RES production, per delivery point, per technology:

.. math::

	\\small curtailment_{technology} = \\sum_{RES asset} (\\sum_t  installedCapacity_{t, asset}^{technology}*availability_{t, asset}^{RES asset} - \\sum_t production_{t, asset}^{technology})

"""


def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = PRODUCED_ENERGIES))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	selectedTechnologies   = indexFilter.filterIndexList(4, getTechnologies(context, includedTechnologies=FLEXIBLE_RES_TYPES|CURTAILABLE_TYPES))
	selectedAssets         = indexFilter.filterIndexList(5, getAssets(context, includeFinancialAssets=True, includedTechnologies=FLEXIBLE_RES_TYPES|CURTAILABLE_TYPES))

	productionCurtailmentAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets = True, includedAssetsName=selectedAssets, includedTechnologies = FLEXIBLE_RES_TYPES, excludedBehaviors=[BH_MUST_RUN])
	consumptionCurtailmentAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets = True, includedAssetsName=selectedAssets, includedTechnologies = CURTAILABLE_TYPES)
	
	productionCurtailmentDict = getCurtailmentDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, productionCurtailmentAssetsByScope, aggregation = False, indexByAsset=True)

	for index in productionCurtailmentDict:
		productionCurtailment = productionCurtailmentDict[index].getSumValue() * timeStepDuration
		kpiDict[index] = productionCurtailment * MW_TO_W_CONVERSION

	consumptionCurtailmentDict = getConsumptionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, consumptionCurtailmentAssetsByScope, aggregation=False, indexByAsset=True)

	for index in consumptionCurtailmentDict:
		consumptionCurtailment = consumptionCurtailmentDict[index].getSumValue() * timeStepDuration
		kpiDict[index] = consumptionCurtailment * MW_TO_W_CONVERSION #+ ("Other Technologies",)

	return kpiDict

def get_indexing(context):
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = PRODUCED_ENERGIES), getTestCasesIndexing(context), 
							getTechnologiesIndexing(context, includeFinancialAssetTypes=True, includedTechnologies = FLEXIBLE_RES_TYPES|CURTAILABLE_TYPES),
							getAssetsIndexing(context, includeFinancialAssets=True, includedTechnologies=FLEXIBLE_RES_TYPES|CURTAILABLE_TYPES)]
	return baseIndexList

IndicatorLabel = "Curtailment"
IndicatorUnit = "Wh"
IndicatorDeltaUnit = "Wh"
IndicatorDescription = "Energy curtailment and renewable energy not used"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Curtailment"
IndicatorTags = "Power System, Power Markets"
