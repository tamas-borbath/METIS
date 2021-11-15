########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Producer surplus (euro)
---------------------------

Indexed by
	* scope
	* reference delivery point
	* test case
	* technology
	* asset name

A producer surplus occurs when the producer is **paid more for a given product than the minimum amount it is willing to pay for its production**. It represents the **benefit the producer receives for selling its product on the market**.

The KPI thus computes the difference between the amount an energy producer receives and the minimum amount the producer is paying for the energy it produces, i.e. the production 
times the marginal cost (the amount the producer receives) minus the production cost and the marginal consumption cost if there is one (the amount the producer has paying).
And to compute the producer revenue, we need to consider all its "primary energy productions" and consumptions (electricity, reserve energies,...), but not the secondary ones (fuel, co2,...).

For each scope :math:`s`, test case :math:`c`, delivery points :math:`d` and technology :math:`T` :

.. math:: \\small productionSurplusKpi_{s, c, d, T} = \\small \\sum_{asset\ a\ |\ refDp(a)==d\ \\\\and\ technology(a)==T} ( \\sum_{time\ step\ t} (\\sum_{primary\ produced\ \\\\energy\ e\ of\ a} production_{s, c, t, a, e} \\times margCost_{s, c, t, e, prodDp(a,e)} - \\sum_{primary\ consumed\ \\\\energy\ e'\ of\ a} consumption_{s, c, t, a, e'} \\times margCost_{s, c, t, e', consumptionDp(a,e')}) 
			\\\\ \\small - productionCost_{s, c, a})

Where :math:`\\small productionCost_{s, c, a}` is the total production cost of the asset for given scope and test case (cf the "Production costs" KPI documentation).

"""


def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):

	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedTestCases      = indexFilter.filterIndexList(2, context.getResultsIndexSet())
	selectedTechnologies   = indexFilter.filterIndexList(3, getTechnologies(context, includedTechnologies = PRODUCTION_TYPES))
	selectedAssets         = indexFilter.filterIndexList(4, getAssets(context, includedTechnologies = PRODUCTION_TYPES))
	
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedAssetsName=selectedAssets, includedTechnologies = selectedTechnologies)

	producerSurplusDict = getProducerSurplusDict(context, selectedScopes, selectedTestCases, selectedDeliveryPoints, selectedAssetsByScope, indexByAsset=True)

	for index in producerSurplusDict:
		kpiDict[index] = producerSurplusDict[index].getSumValue()

	return kpiDict


def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getTestCasesIndexing(context), 
							getTechnologiesIndexing(context, includedTechnologies = PRODUCTION_TYPES),
							getAssetsIndexing(context, includedTechnologies = PRODUCTION_TYPES)]
	return baseIndexList

IndicatorLabel = "Producer surplus"
IndicatorUnit = u"\u20ac"
IndicatorDeltaUnit = u"\u20ac"
IndicatorDescription = "Producer surplus per zone and technology"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Welfare"
IndicatorTags = "Power System, Power Markets"
