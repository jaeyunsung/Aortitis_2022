#prepare_DESeq2.py							#2020.01.15
#hur.benjamin@mayo.edu
#
#Prepare matrice for DESeq2 analysis
#
#Creates two types of matrix files.
#1. dataframe ( row x column = GeneSymbol x sampleID )
#2. dataframe ( row x column = sampleID x condition )
#
#I might accidently compressed to much information in FL...
#
#Memo: Just to make things easy, prepare the input list in order of 
#
#case
#data 1
#data 2
#control
#data 1
#data 2

if __name__ == '__main__':

	import sys
	import os
	sys.path.insert(1, '/research/labs/surgresearch/jsung/m221138/code')
	#change path if you have different working directory
	import FL
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', dest = 'input_list_file', help='list of input files')
	parser.add_argument('-o', '--output', dest = 'output_prefix', help='prefix of output files')
	args = parser.parse_args()

	input_list_file = args.input_list_file
	output_prefix = args.output_prefix

	FL.after_alignment().file_list_to_DESeq2_ready_matrix(input_list_file, output_prefix)


