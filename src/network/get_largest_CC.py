#get_largest_CC.py			2020.12.16
import networkx as nx
import sys
import os

ppi_graph_file = sys.argv[1]
subgraph_file = sys.argv[2]
sub_topology_file = sys.argv[3]

my_graph = nx.Graph()

data_edge = nx.read_edgelist(ppi_graph_file)
my_graph.add_edges_from(data_edge.edges())

print ("Current Network's number of nodes:")
print (len(list(my_graph.nodes)))

largest_cc = max(nx.connected_components(my_graph), key=len)
subgraph_gene_list = list(largest_cc)

print ("Number of nodes in largest connected components:")
print (len(subgraph_gene_list))

output_txt = open(subgraph_file, 'w')
for gene in subgraph_gene_list:
	output_txt.write("%s\n" % gene)
output_txt.close()

output_txt = open(sub_topology_file, 'w')

for node in subgraph_gene_list:
	edge_list = my_graph.edges(node)
	for edge_info in edge_list:
		source_node = edge_info[0]
		target_node = edge_info[1]
		output_txt.write("%s\t%s\n" % (source_node, target_node))
output_txt.close()
