########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""

Indexed by
	* scope
	* test case
	* asset

This view shows the result of the financial asset, as a time series

"""

from com.artelys.platform.config import Constantes
execfile(Constantes.REP_SCRIPTS+'/results/kpis/imports/BaseKPI.py')


ViewLabel = "Contract view (W)"


def get_indexing(context) :
	return [
	getScopesIndexing(localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2),
	getTestCasesIndexing(context, localized=False, selectFirst=True, colorizeIndex=False, groupIndexAsGraphs=2),
	getAssetsIndexing(context, includePhysicalAssets=False, includeFinancialAssets=True, localized=False, selectFirst=False, colorizeIndex=False, groupIndexAsGraphs=2, indexName="Financial Assets")
	]

def getData(view) :
	context = view.getContext()
	
	selectedScopes = getScopes()
	selectedTestCases = context.getTestCases()
	selectedAssetsByScope = getAssetsByScope(context, selectedScopes, includePhysicalAssets=False, includeFinancialAssets=True) #Select financial assets only
	
	ret = []
	for scope in selectedScopes:
		for testCase in selectedTestCases:
			results = Crystal.getComputationResults(context, scope, testCase)
			
			if results == None or (not results.isComputed()):
				print '[SCRIPT INFO] No results for ' + scope + ' ' + str(testCase)
				continue
			
			for asset in selectedAssetsByScope[scope]: #Financial assets only
				assetName = asset.getName()
				if view.filter(scope, testCase, assetName):
					ret += [[[scope, testCase, assetName], results.getVolume(asset) * MW_TO_W_CONVERSION]]
	
	return ret

def getTimeContext(context):
	timeContext = [context.getStartingDate(), context.getTimeStepDuration(), context.getTimeStepCount()]
	return timeContext