#gene_set_handling.py        20.11.03


def deg_file_to_dict_and_list(deg_file, delimiter, abs_log2_threshold, padj_threshold):
#Requirements before entering this function
#DESeq2 outputs
#Currently "Specified" to handle Vasculitis project

	print ("Info :: abs log2 threshold > %s" % abs_log2_threshold)
	print ("Info :: adj p-value threshold > %s" % padj_threshold)

	deg_dict = {}
	deg_list = []

	deg_df = pd.read_csv(deg_file, sep = delimiter, header=0)
	r, c = deg_df.shape

	for i in range(r):
		gene = deg_df.iloc[i][0]
		log2fc = float(deg_df.iloc[i][2])
		abs_log2fc = float(abs(deg_df.iloc[i][2]))
		padj = float(deg_df.iloc[i][6])

		if abs_log2fc > float(abs_log2_threshold):
			if padj < float(padj_threshold):
				deg_dict[gene] = [log2fc, padj]
				deg_list.append(gene)

	print ("Info :: Total Number of DEGS > %s " % len(deg_list))

	deg_list = list(deg_list)

	return deg_dict, deg_list

def gene_dict_to_output(deg_dict, output_file):

	output_txt = open(output_file,'w')
	output_txt.write("gene\tlog2fc\tpadj\n")

	for gene in list(deg_dict.keys()):

		log2fc = deg_dict[gene][0]
		padj = deg_dict[gene][1]

		output_txt.write("%s\t%s\t%s\n" % (gene, log2fc, padj))

	output_txt.close()

def gene_file_to_gene_list(input_file, delimiter, focus_column):
#intentioned to...
#Requirements: convert_genesymbol_to_entrezid.R
#Preprocess for function > api_geneset_enrichment
	
	input_df = pd.read_csv(input_file, sep = delimiter, header=None, dtype=str)
	gene_list = input_df.iloc[:,focus_column]
	gene_list = list(gene_list)

	return gene_list

def sample_class_information_to_dict(input_file, delimiter):

	input_df = pd.read_csv(input_file, sep = delimiter, header=None, dtype=str)
	r, c = input_df.shape
	print (input_df)
	print (r,c)
	sample_dict = {}

	for i in range(r):
		sampleID = input_df.iloc[i,0]
		sample_class = input_df.iloc[i,1]
		sample_dict[sampleID] = sample_class

	return sample_dict


def gene_file_to_gene_dict_and_list(input_file, delimiter, focus_column):
#intentioned to...
#Requirements: convert_genesymbol_to_entrezid.R
#Preprocess for function > api_geneset_enrichment
	
	input_df = pd.read_csv(input_file, sep = delimiter, header=0, dtype=str)
	gene_list = list(input_df.iloc[:,focus_column])
	gene_dict = {}
	r, c = input_df.shape

	for i in range(r):
		gene = input_df.iloc[i][0]
		fc = input_df.iloc[i][1]
		gene_dict[gene] = fc

	return gene_list, gene_dict

def sample_metafile_to_info_dict(input_file, delimiter):

	input_df = pd.read_csv(input_file, sep = delimiter, header=0, dtype=str)
	r, c = input_df.shape

	kfold_sample_dict = {}
	sample_class_dict = {}

	for i in range(r):
		
		sampleID = input_df.iloc[i][0]
		kfold = input_df.iloc[i][4]

		if input_df.iloc[i][1] == "case":
			sample_class = 1
		if input_df.iloc[i][1] == "control":
			sample_class = 0
		
		sample_class_dict[sampleID] = sample_class
		
		try: kfold_sample_dict[kfold].append(sampleID)
		except KeyError: kfold_sample_dict[kfold] = [sampleID]

	return kfold_sample_dict, sample_class_dict

def sample_metafile_to_info_dict_v2(input_file, delimiter):

	input_df = pd.read_csv(input_file, sep = delimiter, header=0, dtype=str)
	r, c = input_df.shape

	kfold_sample_dict = {}
	sample_class_dict = {}

	for i in range(r):
		
		sampleID = input_df.iloc[i][0]
		kfold = input_df.iloc[i][5]

		if input_df.iloc[i][1] == "case" or int(input_df.iloc[i][1]) == 1:
			sample_class = 1
		if input_df.iloc[i][1] == "control" or int(input_df.iloc[i][1]) == 0:
			sample_class = 0
		
		sample_class_dict[sampleID] = sample_class
		
		try: kfold_sample_dict[kfold].append(sampleID)
		except KeyError: kfold_sample_dict[kfold] = [sampleID]

	return kfold_sample_dict, sample_class_dict




def api_geneset_enrichment(gene_list, annot_type):
#Note: specific options are fixed

	base_url = "http://david.abcc.ncifcrf.gov/api.jsp?"
	gene_symbol = "type=ENTREZ_GENE_ID&ids="
	tool = "&tool=term2term"

	if annot_type == "goterm":
		annot = "&annot=GOTERM_BP_FAT,GOTERM_CC_FAT,GOTERM_MF_FAT"
	if annot_type == "pathway":
		annot = "&annot=BIOCARTA,KEGG_PATHWAY"
	if annot_type == "disease":
		annot = "&annot=GENETIC_ASSOCIATION_DB_DISEASE,OMIM_DISEASE"

	gene_list_str = ""
	gene_list_str += gene_list[0]
	for i in range(1, len(gene_list)):
		gene = gene_list[i]
		gene_list_str += ",%s" % gene
		
	api_str = base_url + gene_symbol + gene_list_str + tool + annot

	return api_str


if __name__ == "__main__":
    print ('This is not meant to be run')
else:
    import pandas as pd
    print ("LOADING :: gene_set_handling")
