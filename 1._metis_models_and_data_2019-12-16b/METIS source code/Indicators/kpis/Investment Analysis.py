########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Investment Analysis (euro)
---------------------------

Indexed by
	* scope
	* energy
	* test case
	* production asset

The Investment Analysis calculates the economic profitability of a given production asset in a given delivery point, defined as the difference between the producer surplus and the investment costs for this specific asset.

The producer surplus is calculated as the benefit the producer receives for selling its product on the market.
The investment costs is the sum of the Capital Expenditure (CAPEX) and Fixed Operating Cost (FOC):

.. math::

	\\small investmentAnalysis_{asset} = \\small \\sum_t producerSurplus_{t, asset} - investmentCosts_{asset}

with:

.. math::

	\\small investmentCosts_{asset} = \small \\sum_t installedCapacity^{asset}*(CAPEX^{asset} + FOC^{asset})

and:

.. math::

	\\small producerSurplus_{asset} = \small \\sum_t (production_{t, asset}.marginalCost_{t, dp, energy}) - productionCost_{asset}

"""


def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):

	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedTestCases      = indexFilter.filterIndexList(1, context.getResultsIndexSet())
	selectedAssets         = indexFilter.filterIndexList(2, getAssets(context, includedTechnologies = PRODUCTION_TYPES))
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedAssetsName = selectedAssets)

	producerSurplusDict = getProducerSurplusByAssetDict(context, selectedScopes, selectedTestCases, selectedAssetsByScope)
	capexDict = getCapexByAssetDict(context, selectedScopes, selectedTestCases, selectedAssetsByScope)
	focDict = getFocByAssetDict(context, selectedScopes, selectedTestCases, selectedAssetsByScope)

	for index in producerSurplusDict:
		kpiDict[index] = (producerSurplusDict[index]).getSumValue() - (capexDict[index] + focDict[index]).getMeanValue()

	return kpiDict


def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), getTestCasesIndexing(context), getAssetsIndexing(context, includedTechnologies = PRODUCTION_TYPES)]
	return baseIndexList

IndicatorLabel = "Investment Analysis"
IndicatorUnit = u"\u20ac"
IndicatorDeltaUnit = u"\u20ac"
IndicatorDescription = "Difference between the Surplus and the investment costs for a given production asset"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Welfare"
IndicatorTags = "Power System, Power Markets"
