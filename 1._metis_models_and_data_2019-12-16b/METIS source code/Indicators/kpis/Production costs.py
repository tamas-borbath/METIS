########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Production costs (euro)
------------------------

Indexed by
	* scope
	* reference delivery point
	* test case
	* technology
	* asset name

The KPI computes the total production costs in a given delivery point and a given technology.

So for each scope :math:`s`, test case :math:`c`, asset :math:`a` and time step :math:`t`, asset costs fall in the various categories below :

.. math:: \\small variableCost_{s, c, t, a} = production_{s, c, t, a, mainEnergy} \\times (productionCost_{s, c, t, a} \\times \\delta_{notActive(BH\_CLUSTER)} + variableCost_{s, c, t, a} \\times \\delta_{isActive(BH\_CLUSTER)})
	
.. math:: \\small runningCapacityCost_{s, c, t, a} = runningCapacityCost_{s, c, t, a} \\times runningBound_{s, c, t, a}
	
.. math:: \\small startUpCost_{s, c, t, a} = startUpIndexedCost_{s, c, t, a} \\times startingCapacity_{s, c, t, a}
	
.. math:: \\small fuelCost_{s, c, t, a} = \\small \\sum_{fuelEnergy} fuelConsumption_{s, c, t, a, fuelEnergy} \\times marginalCost_{s, c, t, fuelEnergy, fuelDP(fuelEnergy, a)}
	
where :math:`\\small fuelDP(fuelEnergy, a)` is the delivery point where the asset :math:`a` consumes the fuel energy :math:`\\small fuelEnergy`
	
.. math:: \\small consumptionCost_{s, c, t, a} = consumption_{s, c, t, a, mainEnergy} \\times consumptionIndexedCost_{s, c, t, a}
	
.. math:: \\small co2EmissionsCost_{s, c, t, a} = co2Emissions_{s, c, t, a, co2Energy} \\times  marginalCost_{s, c, t, co2Energy, co2DP(co2Energy,a)}
	
where :math:`\\small co2DP(co2Energy,a)` is the delivery point where the asset :math:`a` produces the fuel energy :math:`\\small co2Energy`
	
.. math:: \\small storageCost_{s, c, t, a} = storageLevel_{s, c, t, a} \\times storageLevelIndexedCost_{s, c, t, a}
	
For each reserve energy :
	
.. math:: \\small reserveCost_{s, c, t, a, reserveEnergy} = production_{s, c, t, a, reserveEnergy, RUNNING} \\times reserveProdCost_{s, c, t, a, reserveEnergy}
	
.. math:: \\small reserveNotRunningCost_{s, c, t, a} = production_{s, c, t, a, mfrrUp, NOT\_RUNNING} \\times notRunningReserveCost_{s, c, t, a, mfrrUp}
	

So we can define the total **production cost** of an asset as :

.. math:: \\small productionCost_{s, c, a} = \\sum_t variableCost_{s, c, t, a} + runningCapacityCost_{s, c, t, a} + startUpCost_{s, c, t, a} + fuelCost_{s, c, t, a} + consumptionCost_{s, c, t, a} + co2EmissionsCost_{s, c, t, a} + storageCost_{s, c, t, a}

.. math:: \\small + \\sum_{reserveEnergy} reserveCost_{s, c, t, a, reserveEnergy} + reserveNotRunningCost_{s, c, t, a}

NB : All costs of a given asset must always be considered together, since some costs are shared. For instance, the runningCapacityCost is linked to the electricity production as much as to the reserve production.
Therefore, indexing these costs by energy would be misleading.
It is also true for the indexing by delivery points : an asset could produce or consume at several delivery points, but divide its cost on several DP would be misleading and wrong. 
For practicality purposes, we just index this KPI by **reference DP**, each asset having a single reference DP (classically the DP where the asset produces its main energy production).

So for each scope :math:`s`, test case :math:`c`, delivery points :math:`d` and technology :math:`T`, we have :

.. math:: \\small productionCostKpi_{s, c, d, T} = \\sum_{time\ step\ t} \\sum_{asset\ a\ |\ refDp(a)==d\ \\\\and\ technology(a)==T} productionCost_{s, c, a}


"""


def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedTestCases      = indexFilter.filterIndexList(2, context.getResultsIndexSet())
	selectedTechnologies   = indexFilter.filterIndexList(3, getTechnologies(context, includedTechnologies=PRODUCTION_TYPES))
	selectedAssets         = indexFilter.filterIndexList(4, getAssets(context, includedTechnologies=PRODUCTION_TYPES))

	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedAssetsName=selectedAssets, includedTechnologies=selectedTechnologies)
	
	productionCostDict = getProductionCostDict(context, selectedScopes, selectedTestCases, None, selectedDeliveryPoints, selectedAssetsByScope, indexByAsset=True)
	
	for index in productionCostDict:
		kpiDict[index] = productionCostDict[index].getSumValue() * timeStepDuration
	
	return kpiDict


def get_indexing(context):
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getTestCasesIndexing(context), 
							getTechnologiesIndexing(context, excludedTechnologies=TRANSMISSION_TYPES),
							getAssetsIndexing(context, excludedTechnologies=TRANSMISSION_TYPES)]
	return baseIndexList

IndicatorLabel = "Production costs"
IndicatorUnit = u"\u20ac"
IndicatorDeltaUnit = u"\u20ac"
IndicatorDescription = "Production costs per technology attached to a zone"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Production"
IndicatorTags = "Power System, Gas System, Power Markets"
