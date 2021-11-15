########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""
Before using this action, two contexts must be present in the study :
- the current context where the action is launched, with results in the SIMULATION scope
- another context with the same assets but a subset of countries and no results
This new context should be selected as linked (or destination) context.

This action will create fixed import/export contracts in the destination context to model exchanges from and to countries outside this subset, 
according to transmissions exchanges results from the current context.

For example, if the current context has three countries DE,AT,CH and the destination context has the subset DE,AT then exchanges 
between CH and DE, and between CH an AT, are represented in the destination context with import/export contracts whose timeseries are
extracted from results of transmissions exchanges from the current context.

Please note that the destination context should have the same data than the current context to get consistent results.
If no results exist in the current context, import and contract assets are still created, but with a default timeseries set to 0.

"""

from com.artelys.CrystalEditor.scripting import Crystal
from com.artelys.platform.gui.dialogs import CrystalOptionDialog
from com.artelys.platform.config import Constantes

execfile(Constantes.REP_SCRIPTS+'/CommonUtils.py')
execfile(Constantes.REP_SCRIPTS+'/CommonGetters.py')
# Import DefaultVar_scripting
execfile(Constantes.getLibraryMappings("DefaultVar"))
execfile(Constantes.getLibraryMappings("CommonFilters"))

def onExecute(action, event):  
	freezeTransmissions(action, event)

def freezeTransmissions(action, event):
	# Context retrieval -------------------------------------
	sourceContext = action.getSourceContext()
	destinationContext = action.getDestinationContext()
	if sourceContext == None:
		Crystal.showErrorDialog("Cannot execute script: source context cannot be None!")
		return
	if destinationContext == None:
		Crystal.showErrorDialog("Cannot execute script: destination context cannot be None!")
		return
	if sourceContext == destinationContext:
		Crystal.showErrorDialog("Cannot execute script: destination context should not be the same as source context!")
		return
	
	transmissionsEndMessage = createImportExportContracts(Crystal.getEnergy(ELECTRICITY), [F_TRANSMISSION], sourceContext, destinationContext, "SIMULATION")

	strMsg = "End of freezeTransmissions action.\n\n" + transmissionsEndMessage
	CrystalOptionDialog.showConfirmDialog(None, strMsg, "", CrystalOptionDialog.CLOSED_OPTION)
	
def createImportExportContracts(energy,assetTypes,sourceContext,destinationContext, scopeWithResults):
	def importContractName(dpNameIn, dpNameOut, energyName):
		return energy.getName() + "_import_from_" + dpNameIn + "_to_" + dpNameOut

	def exportContractName(dpNameIn, dpNameOut, energyName):
		return energy.getName() + "_export_from_" + dpNameIn + "_to_" + dpNameOut
	
	listDpNamesDestinationContext = getDeliveryPoints(destinationContext)
	resetTo0imports = {dpName:True for dpName in listDpNamesDestinationContext}
	resetTo0exports = {dpName:True for dpName in listDpNamesDestinationContext}

	zonesWithFrozenTransmissions = []

	for asset in getAssets(sourceContext, includedTechnologies = assetTypes):
		consumptionDpList = getConsumptionDeliveryPoints(sourceContext, asset, energy)
		productionDpList  = getProductionDeliveryPoints(sourceContext, asset, energy)
		if len(consumptionDpList) != 1 or len(productionDpList) != 1:
			raise ValueError('[ERROR] '+asset.getName()+' in source context should have one production delivery point and one consumption delivery point')

		dpNameIn = consumptionDpList[0].getName()
		dpNameOut = productionDpList[0].getName()

		if ((dpNameIn in listDpNamesDestinationContext) and (dpNameOut not in listDpNamesDestinationContext)):
			zonesWithFrozenTransmissions.append(dpNameIn)
			exportAssetForThisZone = None		
			for exportAsset in getAssets(destinationContext,includeFinancialAssets = True, includedTechnologies = [F_EXPORT_CONTRACT]):
				exportDpNameIn = getConsumptionDeliveryPoints(sourceContext, asset, energy)[0].getName()
				if dpNameIn == exportDpNameIn:
					if exportAsset.getName() == exportContractName(dpNameIn, "otherCountries", energy.getName()):
						exportAssetForThisZone = exportAsset
						randomValue = exportAsset.getData("_exports")
						if resetTo0exports[dpNameIn]:
							randomValue.setValue(0)
							resetTo0exports[dpNameIn] = False
						break
			if exportAssetForThisZone == None:
				exportAssetForThisZone = Crystal.createContract(destinationContext,F_EXPORT_CONTRACT,exportContractName(dpNameIn, "otherCountries", energy.getName()),energy.getName(),[dpNameIn])
				randomValue = Crystal.createRandomValue(destinationContext, "Exports_"+energy.getName()+"_"+dpNameIn)
				exportAssetForThisZone.setData("_exports",randomValue)
					
			for tc in destinationContext.getTestCases():
				results = Crystal.getComputationResults(sourceContext, scopeWithResults, tc)
				if results != None:
					consumptionTimeSeries = results.getConsumption(asset, energy)
					realization = randomValue.getRealization(tc)
					for t in range(destinationContext.getTimeStepCount()):
						realization.setValueAt(t,realization.getValueAt(t)+consumptionTimeSeries.getValueAt(t))
				
		elif ((dpNameIn not in listDpNamesDestinationContext) and (dpNameOut in listDpNamesDestinationContext)):
			zonesWithFrozenTransmissions.append(dpNameOut)
			importAssetForThisZone = None						
			for importAsset in getAssets(destinationContext,includeFinancialAssets = True, includedTechnologies = [F_IMPORT_CONTRACT]):
				importDpNameOut = getProductionDeliveryPoints(sourceContext, asset, energy)[0].getName()
				if dpNameOut == importDpNameOut:
					if importAsset.getName() == importContractName("otherCountries", dpNameOut, energy.getName()):
						importAssetForThisZone = importAsset
						randomValue = importAsset.getData("_imports")
						if resetTo0imports[dpNameOut]:
							randomValue.setValue(0)
							resetTo0imports[dpNameOut] = False
						break
			if importAssetForThisZone == None:
				importAssetForThisZone = Crystal.createContract(destinationContext,F_IMPORT_CONTRACT,importContractName("otherCountries", dpNameOut, energy.getName()),energy.getName(),[dpNameOut])
				randomValue = Crystal.createRandomValue(destinationContext, "Imports_"+energy.getName()+"_"+dpNameOut)
				importAssetForThisZone.setData("_imports",randomValue)
			

			for tc in destinationContext.getTestCases():
				results = Crystal.getComputationResults(sourceContext, scopeWithResults, tc)
				if results != None:
					productionTimeSeries = results.getProduction(asset, energy)
					realization = randomValue.getRealization(tc)
					for t in range(destinationContext.getTimeStepCount()):
						realization.setValueAt(t,realization.getValueAt(t)+productionTimeSeries.getValueAt(t))
	
	# return a message to list in which countries import and export contracts have been created
	zonesWithFrozenTransmissions = set(zonesWithFrozenTransmissions)
	if len(zonesWithFrozenTransmissions) != 0:
		endMessage = "- " + energy.getName() + " import and export contracts have been created for countries " + ",".join(zonesWithFrozenTransmissions) + " in destination context " + destinationContext.getName() + "\n"
	else:
		endMessage = ""
	return endMessage
			
askOnResults = False
askOnParametersChange = False
askOnDelete = False
askOnStructureChange = False
