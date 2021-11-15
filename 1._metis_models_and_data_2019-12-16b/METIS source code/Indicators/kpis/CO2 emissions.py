########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################


extends("BaseKPI.py")

"""
CO2 emissions (t)
--------------------

Indexed by
	* scope
	* delivery point
	* test case
	* technology
	* asset name

Return the annual volumes of CO2 emissions (tons) associated to the energy (electricity + reserve) production relative to a given technology

It is calculated as the sum over the hours, over the assets and over the energies, of the CO2 emissions/MWh per asset multiplied by the volume of produced energy:

.. math::

	\\small CO2Emissions_{dp, techno, energy} = \\sum_{t,assets} CO2perMWh_{t, dp, techno, energy}*producedEnergy_{t, dp, techno, energy}

CO2 emissions due the reserve activation (balancing) are not calculated by this KPI.
"""


def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)

	selectedScopes          = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints  = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies        = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies={CO2}))
	selectedTestCases       = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	selectedTechnologies    = indexFilter.filterIndexList(4, getTechnologies(context, includedTechnologies=CO2_TYPES))
	selectedAssets          = indexFilter.filterIndexList(5, getAssets(context, includedTechnologies=CO2_TYPES))
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedAssetsName=selectedAssets, includedTechnologies = selectedTechnologies)
	
	productionDict = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, selectedAssetsByScope, indexByAsset=True)
	
	for index in productionDict:
		kpiDict[index] = productionDict[index].getSumValue() * timeStepDuration
	
	return kpiDict

def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = {CO2}), getTestCasesIndexing(context), 
							getTechnologiesIndexing(context, includedTechnologies = CO2_TYPES),
							getAssetsIndexing(context, includedTechnologies = CO2_TYPES)]
	return baseIndexList
	

IndicatorLabel = "CO2 emissions"
IndicatorUnit = "t"
IndicatorDeltaUnit = "t"
IndicatorDescription = "Gross CO2 emissions attached to a delivery point"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>CO2"
IndicatorTags = "Power System, Gas System, Power Markets"

