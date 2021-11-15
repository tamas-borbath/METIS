########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

extends("BaseKPI.py")

"""
Exports and imports (Wh)
-------------------------

Indexed by
	* scope
	* delivery point
	* energy (electricity or gas)
	* test case
	* technology
	* asset name
	* data type (exports or imports)

Return the annual volumes of energy imported and exported by a given delivery point.

"""

EXPORTS = 'Exports'
IMPORTS = 'Imports'
selectedData = [EXPORTS, IMPORTS]

def computeIndicator(context, indexFilter, paramsIndicator, kpiDict):
	
	timeStepDuration = getTimeStepDurationInHours(context)
	
	selectedScopes         = indexFilter.filterIndexList(0, getScopes())
	selectedDeliveryPoints = indexFilter.filterIndexList(1, getDeliveryPoints(context))
	selectedEnergies       = indexFilter.filterIndexList(2, getEnergies(context, includedEnergies = {ELECTRICITY, GAS}))
	selectedTestCases      = indexFilter.filterIndexList(3, context.getResultsIndexSet())
	selectedTechnologies   = indexFilter.filterIndexList(4, getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies=EXPORT_TYPES|IMPORT_TYPES|TRANSMISSION_TYPES))
	selectedAssets         = indexFilter.filterIndexList(5, getAssets(context, includeFinancialAssets = True, includedTechnologies=EXPORT_TYPES|IMPORT_TYPES|TRANSMISSION_TYPES))
	selectedIdxData        = indexFilter.filterIndexList(6, selectedData)
	
	if EXPORTS in selectedIdxData:
		exportAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets = True, includedAssetsName=selectedAssets, includedTechnologies = EXPORT_TYPES|TRANSMISSION_TYPES)
		exportsDict = getConsumptionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, exportAssetsByScope, aggregation=False, indexByAsset=True)
		for index in exportsDict:
			kpiDict[index + (EXPORTS,)] = exportsDict[index].getSumValue() * timeStepDuration * MW_TO_W_CONVERSION
	
	if IMPORTS in selectedIdxData:
		importAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets = True, includedAssetsName=selectedAssets, includedTechnologies = IMPORT_TYPES|TRANSMISSION_TYPES)
		importsDict = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, importAssetsByScope, aggregation=False, indexByAsset=True)
		for index in importsDict:
			kpiDict[index + (IMPORTS,)] = importsDict[index].getSumValue() * timeStepDuration * MW_TO_W_CONVERSION
	
	return kpiDict


def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = {ELECTRICITY, GAS}), getTestCasesIndexing(context), 
							getTechnologiesIndexing(context, includeFinancialAssetTypes = True, includedTechnologies=EXPORT_TYPES|IMPORT_TYPES|TRANSMISSION_TYPES), 
							getAssetsIndexing(context, includeFinancialAssets = True, includedTechnologies=EXPORT_TYPES|IMPORT_TYPES|TRANSMISSION_TYPES), 
							BaseIndexDefault("Data type", selectedData, False, False, True, 0)]
	return baseIndexList

IndicatorLabel = "Exports and imports"
IndicatorUnit = "Wh"
IndicatorDeltaUnit = "Wh"
IndicatorDescription = "Annual export and import energy volume for a delivery point"
IndicatorParameters = []
IndicatorIcon = ""
IndicatorCategory = "Results>Exchanges"
IndicatorTags = "Power System, Gas System, Power Markets"
