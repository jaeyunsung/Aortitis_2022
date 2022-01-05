#network_functions.py        20.11.03

def topology_file_to_dict(topology_file):

	print ("Function :: topology_file_to_dict > This might take time.")
	topology_dict = {}
	topology_df = pd.read_csv(topology_file, sep="\t", header=0)
	r, c = topology_df.shape

	for i in range(r):
		source_node = topology_df.iloc[i][0]
		target_node = topology_df.iloc[i][1]

		try: topology_dict[source_node].append(target_node)
		except KeyError: topology_dict[source_node] = [target_node]

	return topology_dict


def create_sub_topology(feature_list, topology_dict):
#Requirements before entering this function: 
#[1] topology_dict created from FUNCTION: self.topology_file_to_dict
#[2] feature_list created from FUNCTION: main.feature_file_to_list

	print ("Function :: create_sub_topology")
	sub_topology_dict = {}
	print ("Info :: Feature list size > %s" % len(feature_list))
	print (feature_list)

	for source_node in list(topology_dict.keys()):
		if source_node in feature_list:
			print ("STEP1:YES")
			for target_node in topology_dict[source_node]:
				if target_node in feature_list:
					print ("STEP2:YES")

					try: sub_topology_dict[source_node].append(target_node)
					except KeyError: sub_topology_dict[source_node] = [target_node]


	print ("Info :: Total No. source nodes  in original topology > %s " % len(list(topology_dict.keys())))
	print ("Info :: Total No. source nodes in SUB topology > %s " % len(list(sub_topology_dict.keys())))
	print (list(sub_topology_dict.keys()))

	return sub_topology_dict

def create_sub_topology_jae_request(feature_list, topology_dict):
#2021.04.20 Jae request to observe
#graphs such as: DEG - not DEG - DEG

#Requirements before entering this function: 
#[1] topology_dict created from FUNCTION: self.topology_file_to_dict
#[2] feature_list created from FUNCTION: main.feature_file_to_list

	sub_topology_dict = {}

	print ("Function :: create_sub_topology_jae_request")
	print ("Info :: Feature list size > %s" % len(feature_list))
	#print (feature_list)

	#Concept
	#find DEG-DEG, nonDEG
		#create temp_topology_dict[DEG] = [DEG nonDEG]
	#find nonDEG-DEG
		#create temp_topology_dict[nonDEG] = [DEG non DEG]
	#remove DEG-nonDEG-nonDEG

	uniq_node_list = []
	temp_topology_dict = {}
	
	#find DEG-DEG, nonDEG
	count = 0
	for source_node in list(topology_dict.keys()):
		if source_node in feature_list:
			for target_node in topology_dict[source_node]:
				count += 1
				try: temp_topology_dict[source_node].append(target_node)
				except KeyError: temp_topology_dict[source_node] = [target_node]


	print ('DEG-DEG, DEG-nonDEG edges:', count)

	#find nonDEG-DEG
	count = 0
	for source_node in list(topology_dict.keys()):
		if source_node not in feature_list:
			for target_node in topology_dict[source_node]:
				if target_node in feature_list:
					count += 1
					try: temp_topology_dict[source_node].append(target_node)
					except KeyError: temp_topology_dict[source_node] = [target_node]

	print ('nonDEG-DEG edges:', count)

	#create sub_topology_dict
	for source_node in list(temp_topology_dict.keys()):
		if source_node in feature_list:
			for target_node in topology_dict[source_node]:
				if target_node in feature_list: #DEG-DEG
					uniq_node_list.append(source_node)
					uniq_node_list.append(target_node)
					edge_info_to_dict(source_node, target_node, sub_topology_dict)

				if target_node not in feature_list: #DEG-nonDEG-DEG
					target_node_target_list = temp_topology_dict[target_node]
					common_count = len(set(target_node_target_list) & set(feature_list))
					if common_count >  0:
						uniq_node_list.append(source_node)
						uniq_node_list.append(target_node)
						edge_info_to_dict(source_node, target_node, sub_topology_dict)
					else:
						None
		#nonDEG-DEG
		if source_node not in feature_list:
			source_node_target_list = temp_topology_dict[source_node]
			common_count = len(set(source_node_target_list) & set(feature_list))
			if common_count > 0:
				for target_node in temp_topology_dict[source_node]:
					if target_node in feature_list:
						uniq_node_list.append(source_node)
						uniq_node_list.append(target_node)
						edge_info_to_dict(source_node, target_node, sub_topology_dict)

	
	print ("Info :: Total No. source nodes  in original topology > %s " % len(list(topology_dict.keys())))
	print ("Info :: Total No. source nodes in SUB topology > %s " % len(list(sub_topology_dict.keys())))
	print ("uniq nodes: %s " % (len(list(set(uniq_node_list)))))
	print (list(sub_topology_dict.keys()))

	return sub_topology_dict

def edge_info_to_dict(source, target, topology_dict):
	try: topology_dict[source].append(target)
	except KeyError: topology_dict[source] = [target]

	return topology_dict


def topology_dict_to_output(topology_dict, output_file):
#Requirements before entering this function: 
#topology_dict created from FUNCTION: self.topology_file_to_dict

	print ("Function :: topology_dict_to_output")
	output_txt = open(output_file, 'w')

#	output_txt.write("source_node\ttarget_node\n")
	for source_node in list(topology_dict.keys()):
		for target_node in topology_dict[source_node]:
			output_txt.write("%s\t%s\n" % (source_node, target_node))

	output_txt.close()
	print ("Info :: topology output creation complete")
	print ("Info :: > %s < " % output_file)


if __name__ == "__main__":
	print ('This is not meant to be run')

else:
	import pandas as pd
	print ("LOADING :: network_functions")
