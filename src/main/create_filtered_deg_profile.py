import sys
import os
import os.path
from os import path
sys.path.append('../../src/main')
import gene_set_handling as GSH

deg_file = sys.argv[1]
filtered_deg_file = sys.argv[2]

deg_dict, deg_list = GSH.deg_file_to_dict_and_list(deg_file, ",", 2, 0.01)
GSH.gene_dict_to_output(deg_dict, filtered_deg_file)

