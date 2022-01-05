#trimmomatic.py							#2020.10.20 ver
#hur.benjamin@mayo.edu
#
#Important files: /research/labs/surgresearch/jsung/m221138/code/data.locations
#
#considered to trim fastq files that have TruSeq adaptors:Hiseq, Novaseq
#read the manual of trimmomatic before modifying this code
#http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/TrimmomaticManual_V0.32.pdf

if __name__ == '__main__':

	import sys
	import os
	sys.path.insert(1, '/research/labs/surgresearch/jsung/m221138/NGS_KennethWarrington_v2/src/RNAseqPipeline_SungLab')
	#change path if FL is located elsewhere
	import FL
	import argparse

	#Browse data.locations, 
	#get the directory of ref
	#get the directory that will store indexing file 
	#  > Note that the index files should be stored at the same directory of the reference genome
	#get the directory of the gtf file
	adapter_info  = FL.access_data().get_dir('adapter_info')
	trim_jar  = FL.access_data().get_dir('trim_jar')

	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--fastqlist', dest = 'input_file', help='list of fastqs delimiter ","')
	args = parser.parse_args()
	input_file = args.input_file

	if input_file == None:
		print ("[Error] No input")
		quit()

	input_file_open = open(input_file,'r')
	input_file_readlines = input_file_open.readlines()

	for i in range(len(input_file_readlines)):

		read = input_file_readlines[i]
		read = read.replace('\n','')

		if i == 0:
			file_dir = read + '/'

		else:
			token = read.split(',')
			PE_a_in = token[0]
			PE_b_in = token[1]

			#a = front strand, p = paired, u = unpaired
			#i.e: ae = front strand with paired
			PE_ap_out = PE_a_in.replace('.fastq.gz','') + '.P1.fastq.gz'
			PE_au_out = PE_a_in.replace('.fastq.gz','') + '.U1.fastq.gz'

			#b = reverse strand, p = paired, u = unpaired
			PE_bp_out = PE_b_in.replace('.fastq.gz','') + '.P2.fastq.gz'
			PE_bu_out = PE_b_in.replace('.fastq.gz','') + '.U2.fastq.gz'

			cmd = 'java -jar %s PE -threads 4 %s %s %s %s %s %s ILLUMINACLIP:%s:2:30:10' % (trim_jar, file_dir + PE_a_in, file_dir + PE_b_in, PE_ap_out, PE_au_out, PE_bp_out, PE_bu_out, adapter_info)

			#your CL would look like this
			print (">>> %s" % i)
			print (cmd)
			#run
			os.system(cmd)


