########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Curtailment cost (euro)
---------------------------------------

Indexed by
	* scope
	* delivery point
	* energy (electricity or gas)
	* test case
	* technology
	* asset name

The curtailement cost represents the cost, for the system, associated to curtailing or not using RES energy production. 
The KPI thus computes the total cost associated to the sum of annual volumes of Renewable Energy Sources (RES) production that is curtailed and annual volumes of RES production that is not used, per technology.

This cost is calculated by multplying the volume of RES production that is curtailed by the value for the system associated to this RES production, which, in the case of RES assets, 
is the difference between the incentives and the production cost.

The formula used is thus the following:

.. math::

	\\small curtailmentCost_{RES technology} = \\small \\sum_t  installedCapa_{t}^{RES technology}*availability_{t}^{RES technology} - \\small \\sum_t prod_{t}^{RES technology})* \\small RESproductionValue^{RES technology}

Where:

.. math::

	\\small RESproductionValue_{RES technology} = incentive_{RES technology} - productionCost_{RES technology}

Results are given for electricity and gas production
	
"""


def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = PRODUCED_ENERGIES))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	selectedTechnologies   = indexFilter.filterIndexList(4, getTechnologies(context, includeFinancialAssetTypes=True, includedTechnologies=FLEXIBLE_RES_TYPES|CURTAILABLE_TYPES))
	selectedAssets         = indexFilter.filterIndexList(5, getAssets(context, includeFinancialAssets=True, includedTechnologies=FLEXIBLE_RES_TYPES|CURTAILABLE_TYPES))

	prodCurtailmentAssetsByScope  = getAssetsByScope(context, selectedScopes, includedAssetsName=selectedAssets, includeFinancialAssets = True, includedTechnologies = FLEXIBLE_RES_TYPES, excludedBehaviors=[BH_MUST_RUN])
	consumptionCurtailmentAssetsByScope = getAssetsByScope(context, selectedScopes, includedAssetsName=selectedAssets, includeFinancialAssets = True, includedTechnologies = CURTAILABLE_TYPES)
	
	productionCurtailmentCostDict = getCurtailmentCostDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, prodCurtailmentAssetsByScope, aggregation=False, indexByAsset=True)

	for index in productionCurtailmentCostDict:
		productionCurtailmentCost = productionCurtailmentCostDict[index].getSumValue() * timeStepDuration
		kpiDict[index] = productionCurtailmentCost

	consumptionCurtailmentCostDict = getConsumptionCostDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, consumptionCurtailmentAssetsByScope, aggregation=False, indexByAsset=True)
	
	for index in consumptionCurtailmentCostDict:
		consumptionCurtailment = consumptionCurtailmentCostDict[index].getSumValue() * timeStepDuration
		kpiDict[index] = consumptionCurtailment

	return kpiDict

def get_indexing(context):
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = PRODUCED_ENERGIES), getTestCasesIndexing(context), 
							getTechnologiesIndexing(context, includeFinancialAssetTypes=True, includedTechnologies = FLEXIBLE_RES_TYPES|CURTAILABLE_TYPES),
							getAssetsIndexing(context, includeFinancialAssets=True, includedTechnologies=FLEXIBLE_RES_TYPES|CURTAILABLE_TYPES)]
	return baseIndexList

IndicatorLabel = "Curtailment cost"
IndicatorUnit = u"\u20ac"
IndicatorDeltaUnit = u"\u20ac"
IndicatorDescription = "Curtailment cost and costs of renewable energy not used"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Curtailment"
IndicatorTags = "Power System, Power Markets"
