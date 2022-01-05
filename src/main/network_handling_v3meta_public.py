import sys
import os
import os.path
from os import path
sys.path.append('../../src/main')
sys.path.append('../../src/network')
import network_functions as NF
import gene_set_handling as GSH
import pandas as pd

topology_file = '../../database/hs_ppi_network.high.tsv'
sub_topology_file = '../network/sub_hs_ppi_network.high.tsv'

filtered_deg_file = '../gene_set/aortitis.deg.filter.tsv'
main_output_file = "../network/aortitis.deg.topology.tsv"

deg_list, gene_dict  = GSH.gene_file_to_gene_dict_and_list(filtered_deg_file, "\t", 0)

topology_dict = NF.topology_file_to_dict(topology_file)
sub_topology_dict = NF.create_sub_topology(deg_list, topology_dict)
print ("Info :: Original Topology > %s " % len(topology_dict.keys()))
print ("Info :: Sub Topology > %s " % len(sub_topology_dict.keys()))
NF.topology_dict_to_output(sub_topology_dict, sub_topology_file)

