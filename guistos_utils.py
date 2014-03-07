# guistos is a 3rd party user interface for Phaistos
# Copyright (C) 2012 Anders Steen Christensen
#
# guistos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# guistos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with guistos.  If not, see <http://www.gnu.org/licenses/>.

#####################
### USER SETTINGS ###
#####################
PHAISTOS_BUILD_ROOT = "/home/andersx/phaistos_stable/phaistos_324/build"

DEFAULT_OUT_DIR = "/home/andersx/folds"

GUISTOS_ROOT_DIR = "/home/andersx/guistos"
#####################
####################




import random
import math

DEFAULT_BETA = 1.67857

def get_main_output(settings):
	if settings["random-seed"] == -1:
		random.seed()
		random_seed = random.randint(1,1024)
	else:
		random_seed = settings["random-seed"]
	config_text = """
############################################################
#                 PHAISTOS v1.0-rc1 (rev. 324)             #
#    A Markov Chain Monte Carlo Simulation Framework       #
#                                                          #
#  Please cite:                                            #
#    Boomsma, Frellsen, Harder, Bottaro, Johansson, Tian   #
#    Stovgaard, Andreetta, Olsson, Valentin, Christensen,  #
#    Borg, Ferkinghoff-Borg, Hamelryck. submitted.         #
#                                                          #
############################################################

###################### guistos OPTIONS ######################
#                                                          #
#           This file was created using guistos.            #
#           Report bugs to andersx@nano.ku.dk              #
#                                                          #
############################################################

######################
#### MAIN OPTIONS ####
######################

### General options ###
seed = """ + str(random_seed) + """
output-directory = """ + settings["output-directory"] + """
procedure-fold = 1

### Starting structure options ###
pdb-file = """ + settings["pdb-file"]

	if settings["aa-file"] != "":
		config_text += """
aa-file = """ + settings["aa-file"]
	config_text += """
init-from-pdb = """ + str(settings["init-from-pdb"]) + """
"""
	return config_text


def get_monte_carlo_output(settings):
	iterations = int(settings["iterations-per-thread"]) * int(settings["threads"])
	config_text = """

#############################
#### MONTE CARLO OPTIONS ####
#############################

### General Monte Carlo options ###
iterations = """ + str(iterations) + """
threads = """ + str(settings["threads"]) + """
procedure-fold-pdb-dump-interval = """ + str(settings["pdb-dump-interval"]) + """
"""
	if settings["mc-type"] == "metropolis-hastings":
		config_text += """
monte-carlo-metropolis-hastings = 1
temperature = """ + str(settings["mc-type-mh-temp"]) + """ 
"""


	elif settings["mc-type"] == "simulated-annealing":
		t_start = float(settings["mc-type-sa-temp-start"])/300.0	## These temperatures are in units of 300 K
		t_end = float(settings["mc-type-sa-temp-end"])/300.0		## These temperatures are in units of 300 K

		config_text += """
monte-carlo-simulated-annealing = 1
monte-carlo-simulated-annealing-temperature-start = """ + str(t_start) + """ 
monte-carlo-simulated-annealing-temperature-end = """ + str(t_end) + """ 
"""


	elif settings["mc-type"] == "muninn":
		beta_max = 300.0/float(settings["mc-type-muninn-temp-min"])
		beta_min = 300.0/float(settings["mc-type-muninn-temp-max"])

		config_text += """
monte-carlo-muninn = 1
monte-carlo-muninn-statistics-log-filename = """ + settings["output-directory"] + "/" + settings["title"] + ".muninn" + """
monte-carlo-muninn-min-beta = """ + str(beta_min) + """
monte-carlo-muninn-max-beta = """ + str(beta_max) 
		if settings["mc-type-muninn-scheme"] == "1/k":
			config_text += """
monte-carlo-muninn-weight-scheme = invk"""

		elif settings["mc-type-muninn-scheme"] == "Multicanonical":
			config_text += """
monte-carlo-muninn-weight-scheme = multicanonical"""

	elif settings["mc-type"] == "optimization-greedy":
		config_text += """
monte-carlo-optimization-greedy = 1
"""
	return config_text

def get_energy_output(settings):
	config_text = """

########################
#### ENERGY OPTIONS ####
########################

energy-clash-fast = 1
"""

	if settings["mc-type"] == "metropolis-hastings":
#					Beta = 1 /kB T, kB [kcal/(mol*K)] = 1.9872159 * 10^-3
		boltzmann_weight = 1.0/(0.0019872159 * float(settings["mc-type-mh-temp"]) )
	else:
		boltzmann_weight = DEFAULT_BETA

	if settings["energy-profasi"] == True:
		config_text += """
energy-profasi-local-cached = 1
energy-profasi-local-cached-weight = """ + str(boltzmann_weight) + """

energy-profasi-local-sidechain-cached = 1
energy-profasi-local-sidechain-cached-weight = """ + str(boltzmann_weight) + """

energy-profasi-excluded-volume-cached = 1
energy-profasi-excluded-volume-cached-weight = """ + str(boltzmann_weight) + """

energy-profasi-excluded-volume-local-cached = 1
energy-profasi-excluded-volume-local-cached-weight = """ + str(boltzmann_weight) + """

energy-profasi-hydrogen-bond-improved = 1
energy-profasi-hydrogen-bond-improved-weight = """ + str(boltzmann_weight) + """
energy-profasi-hydrogen-bond-improved-use-ideal-distances = true

energy-profasi-hydrophobicity-cached = 1
energy-profasi-hydrophobicity-cached-weight = """ + str(boltzmann_weight) + """

energy-profasi-sidechain-charge-cached = 1
energy-profasi-sidechain-charge-cached-weight = """ + str(boltzmann_weight) + """

energy-profasi-proline-phi-torsion = 1
energy-profasi-proline-phi-torsion-weight = """ + str(boltzmann_weight) + """
"""

	if settings["energy-opls"] == True:
		config_text += """
energy-opls-angle-bend-cached = 1
energy-opls-angle-bend-cached-weight = """ + str(boltzmann_weight) + """
energy-opls-torsion = 1
energy-opls-torsion-weight = """ + str(boltzmann_weight) + """
energy-opls-bond-stretch = 1
energy-opls-bond-stretch-weight = """ + str(boltzmann_weight) + """
energy-opls-non-bonded-cached = 1
energy-opls-non-bonded-cached-weight = """ + str(boltzmann_weight) + """
"""

	if settings["energy-procs"] == True:
		config_text += """
energy-procs = 1
energy-procs-bcs-filename = """ + settings["energy-procs-bcs-file"] + """
energy-procs-weight = 1.0
"""

	if settings["energy-camshift"] == True:
		config_text += """
energy-camshift-cached = 1
energy-camshift-cached-star-filename = """ + settings["energy-camshift-star-file"] + """
energy-camshift-cached-weight = """ + str(boltzmann_weight) + """
"""
	

	return config_text

def get_bb_move_output(settings):
	if settings["bb-moves"] == "small":
		if settings["energy-profasi"] == True:
			dbn_weight = 0.05
			crisp_weight = 0.0
			semi_local_weight = 0.20
		elif settings["energy-opls"] == True:
			dbn_weight = 0.05
			crisp_weight = 0.15
			semi_local_weight = 0.05
		else:
			print "PROGRAM ERROR: No force field selected for backbone-move optimization."
			exit(0)
	elif settings["bb-moves"] == "medium" or settings["bb-moves"] == "cs-medium":
		if settings["energy-profasi"] == True:
			dbn_weight = 0.25
			crisp_weight = 0.0
			semi_local_weight = 0.20
		elif settings["energy-opls"] == True:
			dbn_weight = 0.25
			crisp_weight = 0.15
			semi_local_weight = 0.05
		else:
			print "PROGRAM ERROR: No force field selected for backbone-move optimization."
			exit(0)
	elif settings["bb-moves"] == "large" or settings["bb-moves"] == "cs-large":
		if settings["energy-profasi"] == True:
			dbn_weight = 0.375
			crisp_weight = 0.0
			semi_local_weight = 0.375
		elif settings["energy-opls"] == True:
			dbn_weight = 0.375
			crisp_weight = 0.25
			semi_local_weight = 0.125
		else:
			print "PROGRAM ERROR: No force field selected for backbone-move optimization."
			exit(0)
	else:
		print "PROGRAM ERROR: No allowed bb-move selected."
		exit(0)

	config_text = """### semilocal ###
move-semilocal = 1
move-semilocal-debug = 0
move-semilocal-weight = """ + str(semi_local_weight) + """
move-semilocal-move-length-min = 4
move-semilocal-move-length-max = 4
move-semilocal-regions = [(-2147483648,2147483647)]
move-semilocal-only-internal-moves = false
move-semilocal-sample-omega = false
move-semilocal-sample-bond-angle = false
move-semilocal-constraint-a = 300
move-semilocal-constraint-b = 10
move-semilocal-omega-scaling = 8
move-semilocal-bond-angle-scaling = 8
move-semilocal-skip-proline-phi = false
"""

	if settings["energy-opls"] == True:
		config_text +="""
### CRISP ### 
move-crisp = 1
move-crisp-debug = 0
move-crisp-weight = """ + str(crisp_weight) + """
move-crisp-move-length-min = 5
move-crisp-move-length-max = 5
move-crisp-regions = [(-2147483648,2147483647)]
move-crisp-std-dev-bond-angle = 0.5
move-crisp-std-dev-phi-psi = 4
move-crisp-std-dev-omega = 0.5
move-crisp-only-internal-moves = false
move-crisp-sample-omega = false
"""
	if settings["bb-moves"] not in ["cs-medium", "cs-large"]:
		config_text +="""
### DBN ###
move-backbone-dbn = 1
move-backbone-dbn-debug = 0
move-backbone-dbn-weight = """ + str(dbn_weight) + """
move-backbone-dbn-move-length-min = 1
move-backbone-dbn-move-length-max = 7
move-backbone-dbn-regions = [(-2147483648,2147483647)]
move-backbone-dbn-resample-mode = resample-all
move-backbone-dbn-implicit-energy = """ + str(settings["implicit-energies"]) + """
move-backbone-dbn-dbn-consistency-window-size = 10
move-backbone-dbn-dbn-bias-window-size = 10
"""
	else:
		config_text += """
###
### SOME SETTINGS FOR TORUS-DBN-CS
###
"""

	if settings["pdb-file"] != "":
		config_text += "backbone-dbn-torus-initial-pdb-file = " + settings["pdb-file"]
	elif settings["aa-file"] != "":
		config_text += "backbone-dbn-torus-initial-aa-file = " + settings["aa-file"]
	else:
		print "PROGRAM ERROR: Couldn't configure backbone-dbn init-file."
		exit(0)

	return config_text




def get_sc_move_output(settings):
        if settings["sc-moves"] == "small":
		basilisk_weight = 0.25
		basilisk_local_weight = 0.25
		uniform1_weight = 0.125
		uniform2_weight = 0.125
        elif settings["sc-moves"] == "medium":
		basilisk_weight = 0.20
		basilisk_local_weight = 0.1
		uniform1_weight = 0.125
		uniform2_weight = 0.125
        elif settings["sc-moves"] == "large":
		basilisk_weight = 0.1
		basilisk_local_weight = 0.05
		uniform1_weight = 0.1
		uniform2_weight = 0.1
	else:
                print "PROGRAM ERROR: Bug in mc-move selection."
                exit(0)

	config_text = """

### Sidechain move Basilisk ###
move-sidechain-basilisk = 1
move-sidechain-basilisk-debug = 0
move-sidechain-basilisk-weight = """ + str(basilisk_weight) + """
move-sidechain-basilisk-move-length-min = 1
move-sidechain-basilisk-move-length-max = 1
move-sidechain-basilisk-regions = [(-2147483648,2147483647)]
move-sidechain-basilisk-model-filename = "basilisk.dbn"
move-sidechain-basilisk-ignore-bb = false
move-sidechain-basilisk-reject-broken-prolines = true
move-sidechain-basilisk-sample-hydrogen-chis = false
move-sidechain-basilisk-sample-hydrogen-chis-normal = true
move-sidechain-basilisk-sample-hydrogen-chis-sigma = 0.0035
move-sidechain-basilisk-implicit-energy = """ + str(settings["implicit-energies"]) + """
move-sidechain-basilisk-mocapy-dbn-dir = """ +  PHAISTOS_BUILD_ROOT + "/data/mocapy_dbns" + """

## Sidechain move - Basilisk local ###
move-sidechain-basilisk-local = 1
move-sidechain-basilisk-local-debug = 0
move-sidechain-basilisk-local-weight = """ + str(basilisk_local_weight) + """
move-sidechain-basilisk-local-move-length-min = 1
move-sidechain-basilisk-local-move-length-max = 1
move-sidechain-basilisk-local-regions = [(-2147483648,2147483647)]
move-sidechain-basilisk-local-model-filename = "basilisk.dbn"
move-sidechain-basilisk-local-implicit-energy = """ + str(settings["implicit-energies"]) + """
move-sidechain-basilisk-local-mocapy-dbn-dir = """ +  PHAISTOS_BUILD_ROOT + "/data/mocapy_dbns" + """

### Local sidechain move ###
move-sidechain-local = 2
move-sidechain-local-debug = 0
move-sidechain-local-weight = """ + str(uniform1_weight) + """
move-sidechain-local-move-length-min = 1
move-sidechain-local-move-length-max = 1
move-sidechain-local-regions = [(-2147483648,2147483647)]
move-sidechain-local-sigma-major-dofs = 0.1
move-sidechain-local-sigma-minor-dofs = 0.00349066
move-sidechain-local-sample-major-dofs = true
move-sidechain-local-sample-minor-dofs = true
move-sidechain-local-mode = constrain-one-endpoint
move-sidechain-local-lagrange-multiplier = 200
move-sidechain-local-skip-proline = false
move-sidechain-local-1-debug = 0
move-sidechain-local-1-weight = """ + str(uniform2_weight) + """
move-sidechain-local-1-move-length-min = 1
move-sidechain-local-1-move-length-max = 1
move-sidechain-local-1-regions = [(-2147483648,2147483647)]
move-sidechain-local-1-sigma-major-dofs = 0.1
move-sidechain-local-1-sigma-minor-dofs = 0.00349066
move-sidechain-local-1-sample-major-dofs = true
move-sidechain-local-1-sample-minor-dofs = true
move-sidechain-local-1-mode = constrain-one-endpoint
move-sidechain-local-1-lagrange-multiplier = 500000
move-sidechain-local-1-skip-proline = false
"""
	return config_text



def get_move_output(settings):
	config_text = """

######################
#### MOVE OPTIONS ####
######################

"""
	config_text += get_bb_move_output(settings)
	config_text += get_sc_move_output(settings)

	return config_text



def collect_output(settings):

	output  = get_main_output(settings)
	output += get_monte_carlo_output(settings)
	output += get_energy_output(settings)
	output += get_move_output(settings)
	output += "\n################### PHAISTOS OPTIONS END ###################"
	return output



def write_config(settings):
	print settings

def cat_config(settings):

	output = collect_output(settings)
	print output


# Default settings
guistos_default_settings = {


######################
#### MAIN OPTIONS ####
######################

# GUI Specific:
"title"			: "default",
"spectroscopy"		: "None",
"input-file"		: "",

# Generate config-filename:
"config-filename" 	: "default.config",

# Output directory:
"output-directory"	: DEFAULT_OUT_DIR + "/default",

# Input PDB-file ...
"pdb-file" 		: "",
"init-from-pdb"		: False,
"init-from-pdb-py-var"	: False,

# ... or input AA-sequence file:
"aa-file"		: "",

# Simulation length: (iterations per thread!)
"iterations-per-thread"	: 10000000,
"threads"		: 1,
"pdb-dump-interval"	: 10000,

# Random seed: (set to -1 for random or >0 for static (integers only))
"random-seed"		: -1,


#############################
#### MONTE CARLO OPTIONS ####
#############################

# Simulation/optimization type: ("metropolis-hastings"|"simulated-annealing"|"muninn"|"optimization-greedy")
"mc-type" 			: "metropolis-hastings",

# Monte Carlo Metropolis-Hastings options: (in degrees Kelvin)
"mc-type-mh-temp"		: 300,

# Simulated annealing options: (in degrees Kelvin)
"mc-type-sa-temp-start"		: 450,
"mc-type-sa-temp-end"		: 100,

# Muninn options (in degrees Kelvin)
"mc-type-muninn-temp-max"	: 600,
"mc-type-muninn-temp-min"	: 100,
"mc-type-muninn-scheme"		: "1/k", #("1/k"|"multicanonical")


########################
#### ENERGY OPTIONS ####
########################

# CamShift 1.35 MD penalty function
"energy-camshift"	: False,
"energy-camshift-star-file" 	: "",

# ProCS energy
"energy-procs"		: False,
"energy-procs-bcs-file"	: "",

# MM force field potential energy
"energy-opls"		: True,
"energy-profasi"	: False,


######################
#### MOVE OPTIONS ####
######################

# Select types of backbone-moves:
"bb-moves" 		: "small",
#"bb-move-cs-filename"	: "/home/lol",

# Select select type of sidechain-moves:
"sc-moves" 		: "small",

# Whether to bias enemble (=True) for optimization - or conversely unbiased (=False) for pure simulation.
"implicit-energies" 	: True


# End settings dictionary
}



