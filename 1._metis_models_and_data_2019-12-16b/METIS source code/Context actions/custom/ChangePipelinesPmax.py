########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################

"""
This action imports Pmax values for a list of pipelines in the current context.
Values must be defined in the changePipelinesPmax.csv file in the client/Standard/data folder.

"""
from com.artelys.CrystalEditor.scripting import Crystal
from com.artelys.platform.gui.dialogs import CrystalOptionDialog
from com.artelys.platform.config import Constantes
import csv
import os
execfile(Constantes.REP_SCRIPTS+'/CommonUtils.py')

def onExecute(action, event):  
    changePipelinesPmax(action, event)

def changePipelinesPmax(action, event):
    # Context retrieval -------------------------------------
    sourceContext = action.getSourceContext()
    energy = Crystal.getEnergy("gas")
    GWtoMW = 1000

    #open csvfile
    csvFileName = Constantes.REP_DATA + 'changePipelinesPmax.csv'
    CrystalOptionDialog.showConfirmDialog(None, "Changing pipeline pmax according to data from " + csvFileName +
        "\nPlease note that csv delimiter must be ';' and decimal mark must be ','" +
        "\nUnit for capacities is GW, and will be converted into MW in METIS" +
        "\nThe csv must start with a header line, and then each line should be as follows:" +
        "\n  zoneIn | zoneOut | newValue", "", CrystalOptionDialog.CLOSED_OPTION)
    with open(csvFileName, 'rb') as csvfile:
        csvReader = csv.reader(csvfile,  delimiter=';')

        transmissionDict = {}

        ignoreFirstLine = True
        for row in csvReader:
            if ignoreFirstLine:
                ignoreFirstLine = False
                continue

            if row[2] == '':
                continue

            zoneIn = row[0]
            zoneOut = row[1]
            newValue = float(row[2].replace(',', '.'))

            if (zoneIn,zoneOut) not in transmissionDict:
                transmissionDict[zoneIn,zoneOut] = newValue
            else:
                raise ValueError('Multiple values for transmission from ' + zoneIn + ' to ' + zoneOut + ' are defined in the csv file. Please remove unwanted values')

        #Change transmission pmax according to the value in the csv
        changedTransmissionsList = []
        for asset in getAssets(sourceContext, includedTechnologies = ["Pipeline"]):
            dpIn = getConsumptionDeliveryPoint(sourceContext,asset,energy)
            dpOut = getProductionDeliveryPoint(sourceContext,asset,energy)
            zoneIn = dpIn.getZones()[0].getName()
            zoneOut = dpOut.getZones()[0].getName()

            if (zoneIn, zoneOut) in transmissionDict:
                newPmax = transmissionDict[zoneIn, zoneOut] * GWtoMW
                asset.setData('_pmax', newPmax)
                changedTransmissionsList.append(zoneIn + "->" + zoneOut + " : " + str(newPmax) + " MW")

        for elt in changedTransmissionsList:
            print elt

        CrystalOptionDialog.showConfirmDialog(None, "Pmax value changed for " + str(len(changedTransmissionsList)) + " transmissions.\nSee console logs for details", "", CrystalOptionDialog.CLOSED_OPTION)

askOnResults = False
askOnParametersChange = False
askOnDelete = False
askOnStructureChange = False