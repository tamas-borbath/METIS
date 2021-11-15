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

This view shows the fuel consumption of the asset, in W. It considers whether fleet mode and cluster mode, and displays the appropriate results.

Stacks:
 - (Cluster mode only) Fuel consumption from energy making
 - (Cluster mode only) Fuel consumption from running capacity

Lines:
 - Fuel consumption
 - Absolute minimal fuel consumption (0 in cluster mode, as the running capaciy has no lower boundary)
 - Absolute maximal fuel consumption calculated from installed capacity
 - Absolute maximal fuel consumption calculated from available capacity

"""

from com.artelys.platform.config import Constantes

execfile(Constantes.REP_SCRIPTS+'/results/kpis/imports/BaseKPI.py')
from java.awt import Color

ViewLabel = "Consumption view (Fuel) (W)"


##############################
# INDEX DEFINITION & RANKING
##############################
#Stacks
runningCapaFuelConsIndex = "Running capacity fuel consumption"
energyMakingFuelConsIndex = "Energy making fuel consumption"
stackIndexesRanking = {runningCapaFuelConsIndex:1,energyMakingFuelConsIndex:2}

#Lines
minimalFuelConsIndex = 'Minimal fuel consumption'
fuelConsIndex = 'Fuel consumption'
maxFuelConsFromAvailableCapaIndex = 'Maximal fuel consumption from available capacity'
maxFuelConsFromInstalledCapaIndex = 'Maximal fuel consumption from installed capacity'
nonStackIndexesRanking = {minimalFuelConsIndex:11,fuelConsIndex:12,maxFuelConsFromAvailableCapaIndex:13,maxFuelConsFromInstalledCapaIndex:14}

#All
selectedData = stackIndexesRanking.keys()
selectedData.extend(nonStackIndexesRanking.keys())

indexesRanking = stackIndexesRanking.copy()
indexesRanking.update(nonStackIndexesRanking)

##############################
# JYTHON FUNCTIONS
##############################

def get_indexing(context):
	return [
	getScopesIndexing(localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getTestCasesIndexing(context, localized=False, selectFirst=True, colorizeIndex=False, groupIndexAsGraphs=2),
	getAssetsIndexing(context, includedTechnologies=PRODUCTION_TYPES, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2, indexName="Physical Assets"),
	BaseIndexDefault("Data",selectedData, False, False, True, 0)
	]

def getData(view) :
	context = view.getContext()
	zeroTs = getZeroTs(context)
	
	selectedScopes = getScopes()
	selectedTestCases = context.getTestCases()
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includedTechnologies=PRODUCTION_TYPES)
	
	ret = []
	for scope in selectedScopes:
		for testCase in selectedTestCases:
			results = Crystal.getComputationResults(context, scope, testCase)
			
			if results == None or (not results.isComputed()):
				print '[SCRIPT INFO] No results for ' + scope + ' ' + str(testCase)
				continue
			
			for asset in selectedAssetsByScope[scope]:
				assetName = asset.getName()
				if not view.filter(scope,testCase, assetName):
					continue # Indexes not selected
				
				# Fuel behavior active
				if asset.isActiveBehavior(BH_FUEL, scope):
					fuelPickup = asset.getEnergyForParameter(FUEL_PICKUP, context)
					consumedFuel = results.getConsumption(asset, fuelPickup)
					if consumedFuel != None:
						# Timeserie of total fuel consumption
						ret += [[[scope,testCase,assetName,fuelConsIndex],consumedFuel * MW_TO_W_CONVERSION]]
						
					# Cluster mode
					if asset.isActiveBehavior(BH_CLUSTER, scope):
						mainProducedEnergy = asset.getEnergyForParameter(ENERGY_DELIVERY, context)
						# Consumption from keeping the capacity turned on
						runningCapaFuelCons = getRunningCapaFuelConsumptionParameter(context, scope, asset, testCase)
						runningCapa = getRunningBound(results, asset, mainProducedEnergy)
						if runningCapa != None and runningCapaFuelCons != None:
							ret += [[[scope,testCase,assetName,runningCapaFuelConsIndex],runningCapa * runningCapaFuelCons * MW_TO_W_CONVERSION]]
						# Consumption from delevering energy
						heatRate = getProductionHeatRateParameter(context, scope, asset, testCase)
						energyDelivery = results.getProduction(asset, mainProducedEnergy)
						if energyDelivery != None and heatRate != None:
							ret += [[[scope,testCase,assetName,energyMakingFuelConsIndex],energyDelivery * heatRate * MW_TO_W_CONVERSION]]
						# Calculation of conversion factor for calculating minimal and maximal fuel consumption
						if heatRate != None and runningCapaFuelCons != None:
							factor = ( heatRate + runningCapaFuelCons )
						else:
							factor = None
						# Absolute minimal production with cluster mode is 0 because the started capacity has no lower boundary
						minimalGeneration = 0.0

					# Fleet mode
					else:
						# Calculation of conversion factor for calculating minimal and maximal fuel consumption
						fuelYield = getFuelYieldParameter(context, scope, asset, testCase)
						if fuelYield != None:
							factor = 1.0 / fuelYield
						else:
							factor = None
						# Minimal production with fleet mode
						minimalGeneration = getMinLoadBound(context, scope, asset, testCase, results)
						
					# Absolute minimal consumption
					if minimalGeneration != None and factor != None:
						ret += [[[scope,testCase,assetName,minimalFuelConsIndex],minimalGeneration * factor * MW_TO_W_CONVERSION + zeroTs]]
					# Absolute maximal consumption from installed capacity
					installedCapa = getInstalledCapacity(context, scope, asset, testCase, results)
					if installedCapa != None and factor != None:
						ret += [[[scope,testCase,assetName,maxFuelConsFromInstalledCapaIndex],installedCapa * factor * MW_TO_W_CONVERSION + zeroTs]]
					# Absolute maximal consumption from available capacity
					availableCapacity = getAvailableCapacity(context, scope, asset, testCase, results)
					if availableCapacity != None and factor != None:
						ret += [[[scope,testCase,assetName,maxFuelConsFromAvailableCapaIndex],availableCapacity * factor * MW_TO_W_CONVERSION + zeroTs]]
					
				# Fuel behavior inactive
				else:
					print '[SCRIPT INFO] No fuel results for ' + scope + ' ' + str(testCase) + ' : Fuel behavior is inactive'
					continue
				
	return ret

def getTimeContext(context) :
	timeContext = [ context.getStartingDate() , context.getTimeStepDuration() , context.getTimeStepCount()]
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
	if runningCapaFuelConsIndex.lower() in curve_label.lower(): 
		return Color(191,119,57)
	elif energyMakingFuelConsIndex.lower() in curve_label.lower():
		return Color(133,182,134)
	elif minimalFuelConsIndex.lower() in curve_label.lower():
		return Color(72,120,73)
	elif fuelConsIndex.lower() in curve_label.lower():
		return Color(0,128,192)
	elif maxFuelConsFromAvailableCapaIndex.lower() in curve_label.lower():
		return Color(85,200,255)
	elif maxFuelConsFromInstalledCapaIndex.lower() in curve_label.lower():
		return Color(0,0,0)
	return Color(0,0,0)
