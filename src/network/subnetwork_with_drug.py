#3meta_subnetwork_with_drug.py
#
#From parsed subnetwork (PPI mapped-DEG network ; largest connected component) 
#connect known diseases 

import pandas as pd
import sys
sys.path.insert(1, "../../src/main")
import gene_set_handling as GSH

#io
#disease_db_file = "../../../database/all_gene_disease_associations.tsv"
disease_db_file = sys.argv[1]
disease_db_df = pd.read_csv(disease_db_file,sep="\t")

#subcluster_topology_file = "../../analysis_with3meta/network/sub_hs_ppi_subcluster.topology.tsv"
subcluster_topology_file = sys.argv[2]
subcluster_topology_df = pd.read_csv(subcluster_topology_file,sep="\t")

#subcluster_gene_file = "../../analysis_with3meta/network/sub_hs_ppi_subcluster_gene.list"
subcluster_gene_file = sys.argv[3]
gene_list = GSH.gene_file_to_gene_list(subcluster_gene_file,"\t",0)

output_file = sys.argv[4]

r, c = subcluster_topology_df.shape
subcluster_topology_dict = {}
drug_list = []

for i in range(r):
	source = subcluster_topology_df.iloc[i][0]
	target = subcluster_topology_df.iloc[i][1]

	try: subcluster_topology_dict[source].append(target)
	except KeyError: subcluster_topology_dict[source] = [target]

r, c = disease_db_df.shape

for i in range(r):
	gene = disease_db_df.iloc[i][3]
	drug = disease_db_df.iloc[i][4]

	if gene in gene_list:
		drug_list.append(drug)
		try: subcluster_topology_dict[gene].append(drug)
		except KeyError: subcluster_topology_dict[gene] = [drug]

print ("Total parsed drug: %s" % len(drug_list))
drug_list = list(set(drug_list))
print ("uniq drug: %s" % len(drug_list))


temp_dict = {}

#output
output_txt = open(output_file,'w')
#output_txt.write("source\ttarget\n")
for source in list(subcluster_topology_dict.keys()):
	if source in gene_list:
		for target in subcluster_topology_dict[source]:
			if target in drug_list:
				drug = target
				target = '%s_drug' % (source)
				try: temp_dict[source].append(drug)
				except KeyError: temp_dict[source] = [drug]
			output_txt.write("%s\t%s\n" % (source, target))
output_txt.close()

output_file = output_file.split('.tsv')[0]
output_txt = open('%s%s' % (output_file,'.drug_info.tsv'),'w')
for gene in list(temp_dict.keys()):
	output_txt.write('%s\t%s' % (gene, len(temp_dict[gene])))
	for drug in temp_dict[gene]:
		output_txt.write('\t%s' % drug)
	output_txt.write('\n')
output_txt.close()

