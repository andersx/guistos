#!/usr/bin/python
from guistos_utils import *






# Begin settings dictionary; (yes, I know Pascal)
settings = {


######################
#### MAIN OPTIONS ####
######################

# Generate config-filename:
"config-filename" 	: "my-file.txt",

# Output directory:
"output-directory"	: "/home/andersx/folds",

# Input PDB-file ...
"pdb-file" 		: "/home/andersx/guistos/1PGB.pdb",
"init-from-pdb"		: True,

# ... or input AA-sequence file:
"aa-file"		: "",

# Simulation length: (iterations per thread!)
"iterations-per-thread"	: 10000000,
"threads"		: 2,
"pdb-dump-interval"	: 10000,

# Random seed: (set to -1 for random or >0 for static (integers only))
"random-seed"		: -1,


#############################
#### MONTE CARLO OPTIONS ####
#############################

# Simulation/optimization type: ("metropolis-hastings"|"simulated-annealing"|"muninn"|"optimization-greedy")
#mc-type" 			: "metropolis-hastings",
"mc-type" 			: "simulated-annealing",
#"mc-type" 			: "muninn",
#"mc-type" 			: "optimization-greedy",

# Monte Carlo Metropolis-Hastings options: (in degrees Kelvin)
#"mc-type-mh-temp"		: 300,
"mc-type-mh-temp"		: 1,

# Simulated annealing options: (in degrees Kelvin)
"mc-type-sa-temp-start"		: 450,
"mc-type-sa-temp-end"		: 1,

# Muninn options (in degrees Kelvin)
"mc-type-muninn-temp-max"	: 1000,
"mc-type-muninn-temp-min"	: 273,


########################
#### ENERGY OPTIONS ####
########################

# CamShift 1.35 MD penalty function
"energy-camshift"	: True,
"energy-camshift-star-file" 	: "/home/andersx/guistos/1PGB.str",

# ProCS energy
"energy-procs"		: False,
"energy-procs-bcs-file"	: "/home/lol",

# MM force field potential energy
"energy-opls"		: True,
"energy-profasi"	: False,


######################
#### MOVE OPTIONS ####
######################

# Select types of backbone-moves:
"bb-moves" 		: "subtle", 			# ("subtle"|"large"|"large-biased"|"large-cs-biased")
#"bb-move-cs-filename"	: "/home/lol",

# Select select type of sidechain-moves:
"sc-moves" 		: "subtle",		# ("subtle"|"subtle-biased"|"large"|"large-biased")

# Whether to bias enemble (=True) for optimization - or conversely unbiased (=False) for pure simulation.
#implicit-energies" 	: True


# End settings dictionary
}


#############################
#### USER DEFINED OUTPUT ####
#############################

#write_config(settings)

cat_config(settings)





