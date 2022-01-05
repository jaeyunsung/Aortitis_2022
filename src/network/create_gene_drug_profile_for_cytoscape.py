#clean duplicate edges		2021.04.18

import networkx as nx
import sys

ppi_graph_file = sys.argv[1]
drug_info_file = sys.argv[2]
profile_output = sys.argv[3]

print (ppi_graph_file)
print (drug_info_file)
print (profile_output)

#drug info to dict
drug_info_dict = {}
drug_info_open = open(drug_info_file,'r')
drug_info_readlines = drug_info_open.readlines()
for i in range(len(drug_info_readlines)):
	read = drug_info_readlines[i]
	read = read.replace('\n','')
	token = read.split('\t')
	gene = token[0]
	n_drug = token[1]
	drug_info_dict['%s_drug' % gene] = n_drug


#do graph things
my_graph = nx.Graph()
data_edge = nx.read_edgelist(ppi_graph_file)
my_graph.add_edges_from(data_edge.edges())

print ("Current Network's number of nodes:")
print ("nodes:" ,len(list(my_graph.nodes)))
print ("edges:", len(list(my_graph.edges)))


#output
node_list = list(my_graph.nodes)
output_txt = open(profile_output, 'w')
output_txt.write('node\tn_edges\tisgene\n')

for node in node_list:
	if node != 'source' and node != 'target':
		if 'drug' in node:
			isgene = 0
		else:
			isgene = 1
		edge_size = len(my_graph.edges(node))
		if node in list(drug_info_dict.keys()):
			edge_size = drug_info_dict[node]
		output_txt.write('%s\t%s\t%s\n' % (node,edge_size, isgene))
output_txt.close()

