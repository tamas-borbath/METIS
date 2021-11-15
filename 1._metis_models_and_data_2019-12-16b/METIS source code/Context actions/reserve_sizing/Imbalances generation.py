########################################################
# Copyright (c) 2015-2017 by European Commission.      #
# All Rights Reserved.                                 #
########################################################


"""

 This script is part of the process to generate demand values for the 4 types of reserve.
 External reserve demand values can alternatively be imported in each asset of type Reserve demand.

 To generate values, first set the sizing options in the following model objects :
    - Reserve sizing (annual or hourly)
	- National reserve symmetry requirement (up down)
	- Europe regional cooperation
 Then run the following context actions in this order :
    - Imbalances generation
	- Outages generation (optional)
	- Reserve sizing
 
 This script uses files from the METIS database that contain historical imbalances components.
 These were generated for the EUCO27 scenario and for a set of zones. 
 
 If there are missing files, the list of countries and test cases for which it will be impossible to generate imbalances is returned in the command window.
 When prompted, the user can decide to compute the imbalances for the rest.
 This script writes the generated imbalances in the data directory so that they can be read by the reserve sizing script.
 
 The reserve sizing methodology is described in appendix 7 of the Power system module documentation on the METIS web page.
 
"""


from com.artelys.CrystalEditor.scripting import Crystal
from com.artelys.platform.gui.dialogs import CrystalOptionDialog
from com.artelys.platform.config import Constantes
from datetime import datetime, timedelta
import csv
import imp
import os

def onExecute(action, event):
	context = action.getDestinationContext()
	if context != action.getSourceContext():
		Crystal.showErrorDialog("Cannot execute script: source and destination contexts are different!")
		return

	ret = CrystalOptionDialog.showConfirmDialog(None, "Do you want to launch imbalances generation?", "Imbalances generation?", CrystalOptionDialog.YES_NO_OPTION)
	if ret != 0: return
	CrystalOptionDialog.showConfirmDialog(None, "Imbalances generation is being launched, see log for details", "", CrystalOptionDialog.CLOSED_OPTION)

	###########################################  ACCESS TO PARAMETERS AND CHECK THAT ALL THE FILES EXIST  ###########################################
	#  First the parameters are accessed.
	#  parameters.py contains all the parameters (name of assets, csv files, etc.) useful for the calculations.
	if os.path.isfile(Constantes.REP_CONF_XML + 'CrystalModule/internal/parameters.py'):
		script = imp.load_source("parameters", Constantes.REP_CONF_XML + 'CrystalModule/internal/parameters.py')
	else:
		Crystal.showErrorDialog('Missing file. Process is aborted.')
		Crystal.logInfo('Missing file parameters.py in ' + str(Constantes.REP_CONF_XML + '/CrystalModule/internal'))
	parameters = script.readParameters(context)
	if len(parameters) == 0:
		Crystal.showErrorDialog("Process is aborted.")
		return
	Crystal.logInfo(parameters['path_to_imbalances_csv'])
	Crystal.logInfo(parameters['imbalances_csv_name'])
	
	#  list climatic year gives the number of historical climatic years used for the calculation.
	#  It should contain 10 years.
	list_climatic_year = parameters['list_climatic_year']
	
	# testCases is a list containing the list of testCases of the context.
	testCases = context.getTestCases()
	
	#  Then there is a file to check whether:
	#                        	- all the files needed for the imbalance generation exist.
	#							- imbalances files already exist or not.
	#                           - all the scripts needed for the calculation exist.
	#  First it is checked that the files exists.
	if os.path.isfile(parameters['path_to_check_file_existence']):
		check = imp.load_source(parameters['file_name_check_file_existence'], parameters['path_to_check_file_existence'])
	else:
		Crystal.logInfo('Please check that the file ' + parameters['file_name_check_file_existence'] +  ' exists in ' + parameters['path_to_check_file_existence'])
		Crystal.showErrorDialog('Missing file. Process is aborted.')

	#  Then it is checked that all the scripts needed for the calculation exist. If there is a missing script, the process is aborted.
	should_process_be_aborted = check.check_if_scripts_exist(parameters)
	if should_process_be_aborted == True:
		return
	
	#  It will be checked that all the files needed for the imbalance calculation exist.
	#  But to do so the user inputs are needed.
	#  So first, user inputs are accessed.
	functions = imp.load_source(parameters['file_name_functions_for_reserve_sizing'], parameters['path_to_functions_for_reserve_sizing'])
	userInput = functions.getUserInput(context, parameters)
	
	#  in case of missing model objects or data, the process is stopped and the user is warned.
	isProcessAborted = userInput['aborted']
	if isProcessAborted == True:
		Crystal.showErrorDialog('There is a problem with the model objects.' + ' See log for details')
		Crystal.showErrorDialog('Process is aborted')
		return

	#  boolean_aggregation: is there aggregation or not.
	#  list_countries: list of counntries for which the calculation is going to be performed.
	#  dict_aggregation: in case of aggregation, a dict containing the name of the areas being aggregated and the countries aggregated together.
	#  For instance: {'Iberia': ['ES', 'PT']}
	#  mean_demand : mean_demand per testCase and per country, scaled in case of aggregation.
	#  dict_PV_fleet: installed PV capacity per country, scaled in case of aggregation.
	#  dict_wind_off_fleet: installed wind offshore capacity, scaled in case of aggregation.
	#  dict_wind_on_fleet: installed wind onshore capacity, scaled in case of aggregation.
	#  forecast_horizon_parameter: forecast horizon to be used for the imbalance calculation.
	boolean_aggregation = userInput['boolean_aggregation'] 
	list_countries = userInput['list_countries']
	dict_aggregation = userInput['dict_aggregation'] 
	mean_demand = userInput['mean_demand'] 
	dict_PV_fleet = userInput['dict_PV_fleet']
	dict_wind_off_fleet= userInput['dict_wind_off_fleet']
	dict_wind_on_fleet = userInput['dict_wind_on_fleet']
	mean_demand = userInput['mean_demand']
	forecast_horizon_parameter = userInput['forecast_horizon_parameter']
	
	#  Then thest to see if all the files needed for the imbalance calculation exist can be performed.
	#  Returns a list containing the countries for which there lacks data.
	#  Then it is asked to the user whether it is ok to calculate the imbalances anyways.
	list_countries_no_imbalances = check.check_if_files_for_imbalances_exist(list_countries, parameters, forecast_horizon_parameter, dict_wind_on_fleet, dict_wind_off_fleet, dict_PV_fleet)
	if len(list_countries_no_imbalances) != 0:
		ret = CrystalOptionDialog.showConfirmDialog(None, "No imbalance can be generated for the following countries due to a lack of data: " + str(list_countries_no_imbalances) +  " (see log for details). Launch the calculation anyways ?", "Imbalances generation?", CrystalOptionDialog.YES_NO_OPTION)
	if ret != 0: return

	#  Fianlly, test to see if file containing imbalances already exists (imbalances without outages).
	#  If that is the case, the question is asked whether to recompute the imbalances or not.
	erase_boolean = check.check_if_repository_exists(parameters['imbalances_repository_name'], parameters['path_to_imbalances_csv'], context)

	#  if erase_boolean is equal to 0, then the user must change the repository name in order to be able to launch the reserve sizing.
	if erase_boolean == 0: return
	
	######################################   WARNING ABOUT DATA USED FOR IMBALANCES  ###################################### 
	#  Imbalance components that are used for the imbalance generation process were created based on a certain set of data.
	#  So the user has to be warned that potentially the imbalances that are going to be created do not match exactly the data it is using.
	Crystal.showErrorDialog('Imbalances generation in METIS is based upon PRIMES EUCO27 scenario data. The imbalances you are about to generate will be resized according to data from the current scenario, but inconsistency may appear if load or availability profiles are significantly different.')

	###########################################   BEGINNING OF THE CALCULATION  ########################################### 
	#  Finally, the calculation is launched.
	#  Imbalances are calculated and written as csv in a directory. One csv per testCase and per country.
	path = parameters['path_to_imbalances_csv']
	file_name = parameters['imbalances_csv_name']
	script_imbalances = imp.load_source(parameters['file_name_for_imbalances_generation'], parameters['path_to_file_for_imbalances_generation'])
	script_imbalances.imbalances_to_csv(list_countries, list_climatic_year, dict_PV_fleet, dict_wind_off_fleet, dict_wind_on_fleet, testCases, context, parameters, forecast_horizon_parameter, list_countries_no_imbalances, path, file_name, dict_aggregation, mean_demand)
	CrystalOptionDialog.showConfirmDialog(None, "Imbalances generation process is over.", "", CrystalOptionDialog.CLOSED_OPTION)
