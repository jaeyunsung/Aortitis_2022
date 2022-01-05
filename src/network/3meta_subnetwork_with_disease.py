#3meta_subnetwork_with_disease.py
#
#From parsed subnetwork (PPI mapped-DEG network ; largest connected component) 
#connect known diseases 

import pandas as pd
import sys
sys.path.insert(1, "../../src/machine_learning/")
sys.path.insert(1, "../../src/main/")
import gene_set_handling as GSH


#io
disease_db_file = "../../database/all_gene_disease_associations.tsv"
disease_db_df = pd.read_csv(disease_db_file,sep="\t")

subcluster_topology_file = "../../analysis_with3meta/network/sub_hs_ppi_subcluster.topology.tsv"
subcluster_topology_df = pd.read_csv(subcluster_topology_file,sep="\t")

subcluster_gene_file = "../../analysis_with3meta/network/sub_hs_ppi_subcluster_gene.list"
gene_list = GSH.gene_file_to_gene_list(subcluster_gene_file,"\t",0)

r, c = subcluster_topology_df.shape
subcluster_topology_dict = {}
disease_list = []

for i in range(r):
	source = subcluster_topology_df.iloc[i][0]
	target = subcluster_topology_df.iloc[i][1]

	try: subcluster_topology_dict[source].append(target)
	except KeyError: subcluster_topology_dict[source] = [target]

r, c = disease_db_df.shape

for i in range(r):

	if i % 10000 == 0:
		print ("%s/%s" % (i, r))

	gene = disease_db_df.iloc[i][1]
	disease_name = disease_db_df.iloc[i][5]
	disease_type = disease_db_df["diseaseType"][i]
	score = disease_db_df["score"][i]
	
	if score > 0.4: 
	#if score > 0.7: 
	#if score > 0.3: 
	#Note: https://www.disgenet.org/static/disgenet_ap1/files/current/DisGeNET_Cytoscape_v6.2.pdf
	#Tutorial used 0.4 and 0.3 cutoffs.
		if gene in gene_list:
			disease_list.append(disease_name)
			try: subcluster_topology_dict[gene].append(disease_name)
			except KeyError: subcluster_topology_dict[gene] = [disease_name]

print ("Total parsed diseases: %s" % len(disease_list))
disease_list = list(set(disease_list))
print ("uniq disease: %s" % len(disease_list))

#output
output_file = "/Users/m221138/NGS_KennethWarrington/analysis_with3meta/network/subcluster_gene_disease_topology.tsv"
output_txt = open(output_file,'w')
output_txt.write("source\ttarget\n")
for source in list(subcluster_topology_dict.keys()):
	if source in gene_list:
		for target in subcluster_topology_dict[source]:
			output_txt.write("%s\t%s\n" % (source, target))
output_txt.close()


