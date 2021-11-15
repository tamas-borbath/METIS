########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""

Indexed by
	* scope
	* test case
	* asset
	* data

This view shows a combination of time series as stacks and lines

Stacks:
 - Production
 - Fixed demand
 - Consumption
 - Fixed supply
 - Bounded supply

Lines:
 - Maximum storage capacity
 - Available storage capacity
 - Storage level
 - Minimal storage level

"""


from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'/results/kpis/imports/BaseKPI.py')
from java.awt import Color

ViewLabel = "Storage view (Wh)"

##############################
# INDEX DEFINITION & RANKING
##############################
#Stacks
productionIndex = "Production"
fixedDemandIndex = "Fixed demand"
consumptionIndex = "Consumption"
fixedSupplyIndex = "Fixed supply"
boundedSupplyIndex = "Bounded supply"
#unchangedStock
stackIndexesRanking = {consumptionIndex:1, boundedSupplyIndex:2, fixedSupplyIndex:3, fixedDemandIndex:4, productionIndex:5}

#Lines
smaxIndex = 'Maximum storage capacity'
availableStorageCapacityIndex = 'Available storage capacity'
storageLevelIndex = 'Storage level'
minStorageLevelIndex = 'Minimal storage level'
nonStackIndexesRanking = {smaxIndex:11, availableStorageCapacityIndex:12, storageLevelIndex:13, minStorageLevelIndex:14}

#All
selectedData = stackIndexesRanking.keys()
selectedData.extend(nonStackIndexesRanking.keys())

indexesRanking = stackIndexesRanking.copy()
indexesRanking.update(nonStackIndexesRanking)

##############################
# JYTHON FUNCTIONS
##############################
def get_indexing(context) :
	return [
	getScopesIndexing(localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getTestCasesIndexing(context, localized=False, selectFirst=True, colorizeIndex=False, groupIndexAsGraphs=2),
	getAssetsIndexing(context, includedTechnologies=STORAGE_TYPES, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2, indexName="Physical Assets"),
	BaseIndexDefault("Data",selectedData, False, False, True, 0),
	getEnergiesIndexing(context, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2)
	]

def getData(view) :
	context = view.getContext()
	# Zero TS used for init and/or ensure we use the algebra and return a DataExpr
	zeroTs = getZeroTs(context)
	
	selectedScopes = getScopes()
	selectedEnergies = getEnergies(context)
	selectedTestCases = context.getTestCases()
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedTechnologies=STORAGE_TYPES)
	
	ret = []
	
	for scope in selectedScopes:
		for testCase in selectedTestCases:
			results = Crystal.getComputationResults(context, scope, testCase)
			
			if results == None or (not results.isComputed()):
				print '[SCRIPT INFO] No results for ' + scope + ' ' + str(testCase)
				continue
			
			for asset in selectedAssetsByScope[scope]:
				assetName = asset.getName()
				if view.filter(scope, testCase, assetName):
					stockEnergy = None
					producedEnergy = asset.getEnergyForParameter(ENERGY_DELIVERY, context)
					consumedEnergy = asset.getEnergyForParameter(ENERGY_PICKUP, context)
					
					#Production
					if producedEnergy != None:
						stockEnergy = producedEnergy
						assetProduction = results.getProduction(asset, producedEnergy)
						ret += [[[scope, testCase,assetName,productionIndex, stockEnergy.getName()], assetProduction * MW_TO_W_CONVERSION]]
					
					#Consumption
					if consumedEnergy != None:
						stockEnergy = consumedEnergy
						assetConsumption = results.getConsumption(asset, consumedEnergy)
						ret += [[[scope, testCase,assetName,consumptionIndex, stockEnergy.getName()], assetConsumption * MW_TO_W_CONVERSION]]
					
					#Storage level
					ret += [[[scope, testCase, assetName, storageLevelIndex, stockEnergy.getName()], results.getAssetStock(asset) * MW_TO_W_CONVERSION]]
					
					#SMAX
					storageCapacity = getInstalledStorageCapacity(context, scope, asset, testCase, results)
					if storageCapacity is not None:
						ret += [[[scope, testCase, assetName, smaxIndex, stockEnergy.getName()], storageCapacity * MW_TO_W_CONVERSION + zeroTs]]
						
					#Storage availability
					availableStorageCapacity = getAvailableStorageCapacity(context, scope, asset, testCase, results)
					if availableStorageCapacity!=None:
						ret += [[[scope, testCase,assetName,availableStorageCapacityIndex, stockEnergy.getName()], availableStorageCapacity * MW_TO_W_CONVERSION + zeroTs]]
					
					#Min level
					minLevel = getMinStorageLevel(context, scope, asset, testCase, results)
					if minLevel is not None:
						ret += [[[scope, testCase,assetName,minStorageLevelIndex, stockEnergy.getName()], minLevel * MW_TO_W_CONVERSION + zeroTs]]
					
					#TODO : include boundedSupply, fixedSupply, fixedDemand,...
	
	return ret

def getTimeContext(context):
	timeContext = [context.getStartingDate(), context.getTimeStepDuration(), context.getTimeStepCount()]
	return timeContext

##############################
# OPTIONNAL FUNCTIONS
# Default versions of this functions will be used if necessary
##############################
def isLineStacked(index) :
	"""
	Returns true if the data identified by this (multi)index should be stacked when using the Graph option "Stacked chart" and "Line type:Script"
	"""
	return any(key in index for key in stackIndexesRanking)

def indexCompare(numIndex,indexValue1,indexValue2):
	"""
	Comparator used to order indexes by comparing them two by two (when using the scripted order on this index type)
	numIndex is the index type ID (Scopes are 0, Test cases are 1,... eg)
	indexValue1 and indexValue2 are two index of the same type (two energies, or two technologies eg)
	"""
	if indexValue1 in indexesRanking and indexValue2 in indexesRanking:
		# Using the indexesRanking dict to order data types
		return indexesRanking[indexValue1] - indexesRanking[indexValue2]
	else:
		return 0 # No order defined, all indexes are at the same level --> return 0


def colorizer(curve_label): 
	"""
	The function takes a label associated to a curve as an input and returns the color of the curve. 
	"""
	if productionIndex.lower() in curve_label.lower(): 
		return Color(79,191,57)
	elif fixedDemandIndex.lower() in curve_label.lower():
		return Color(133,182,134)
	elif consumptionIndex.lower() in curve_label.lower():
		return Color(30,57,191)
	elif fixedSupplyIndex.lower() in curve_label.lower():
		return Color(0,128,192)
	elif boundedSupplyIndex.lower() in curve_label.lower():
		return Color(85,200,255)
	elif smaxIndex.lower() in curve_label.lower():
		return Color(0,0,0)
	elif availableStorageCapacityIndex.lower() in curve_label.lower():
		return Color(98,0,196)
	elif minStorageLevelIndex.lower() in curve_label.lower():
		return Color(0,0,200)
	elif storageLevelIndex.lower() in curve_label.lower():
		return Color(191,79,57)
	return Color(0,0,0)
