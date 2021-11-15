########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""
Indexed by
	* scope
	* delivery point
	* energy
	* test case
	* time

This view shows a time series of the hourly balanced volume of energy (volume of energy exported minus the hourly volume of energy imported), for a selected delivery point.

"""

from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'/results\kpis\imports\BaseKPI.py')

ViewLabel = "Net Position (Wh)"

EXPORTS = 'Exports'
IMPORTS = 'Imports'
selectedData = [EXPORTS, IMPORTS]

def get_indexing(context) :
	baseIndexList = [getScopesIndexing(), getDeliveryPointsIndexing(context), getEnergiesIndexing(context, includedEnergies = {ELECTRICITY, GAS}),
	getTestCasesIndexing(context), getTechnologiesIndexing(context, includeFinancialAssetTypes = True, includedTechnologies=EXPORT_TYPES|IMPORT_TYPES|TRANSMISSION_TYPES)]
	
	return baseIndexList
	

def getData(view) :
	context = view.getContext()
	timeStepDuration = getTimeStepDurationInHours(context)
	
	# Filter Index
	selectedScopes         = getScopes(includedScopes=getScopes())
	selectedDeliveryPoints = getDeliveryPoints(context, includedDeliveryPoints=getDeliveryPoints(context))
	selectedEnergies       = getEnergies(context, includedEnergies={ELECTRICITY, GAS})
	selectedTestCases      = getTestCasesWithoutResults(context, includedTestCases=getTestCasesWithoutResults(context))
	selectedTechnologies   = getTechnologies(context, includeFinancialAssetTypes = True, includedTechnologies=EXPORT_TYPES|IMPORT_TYPES|TRANSMISSION_TYPES)
	
	# Compute KPI
	ret = []
	
	exportAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets = True, includedTechnologies = EXPORT_TYPES|TRANSMISSION_TYPES)
	exportsDict = getConsumptionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, exportAssetsByScope, aggregation=False)

	importAssetsByScope = getAssetsByScope(context, selectedScopes, includeFinancialAssets = True, includedTechnologies = IMPORT_TYPES|TRANSMISSION_TYPES)
	importsDict = getProductionDict(context, selectedScopes, selectedTestCases, selectedEnergies, selectedDeliveryPoints, importAssetsByScope, aggregation=False)
	
	dataDict = {index: (exportsDict[index] * MW_TO_W_CONVERSION * timeStepDuration) for index in exportsDict}
	for index in importsDict:
		if index in dataDict:
			dataDict[index] = (exportsDict[index] - importsDict[index]) * MW_TO_W_CONVERSION * timeStepDuration
		else:
			dataDict[index] = - importsDict[index] * MW_TO_W_CONVERSION * timeStepDuration
	for index in dataDict:
			ret += [[list(index), dataDict[index]]]
	
	return ret
	
def getTimeContext(context):
	timeContext = [context.getStartingDate(), context.getTimeStepDuration(), context.getTimeStepCount()]
	return timeContext
