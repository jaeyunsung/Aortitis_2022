class access_data:

	#if you have your own data.locations file, modify this directory
	data_profile = '/research/labs/surgresearch/jsung/m221138/code/data.locations'
	data_profile_readlines = open(data_profile,'r').readlines()

	def search_module(self, data_type):
		data_profile_readlines = self.data_profile_readlines

		for i in range(len(data_profile_readlines)):
			read = data_profile_readlines[i]
			read = read.replace('\n','')
			token = read.split('\t')
			if token[0] == data_type:
				dir_of_interest = token[1]
				break
		return dir_of_interest

	def get_dir(self, data_type):
		dir_of_interest = self.search_module(data_type)
		return dir_of_interest


class after_alignment:

	def time_stamp(self, memo):
		#Just for debug purpose
		from datetime import datetime
		dateTimeObj = datetime.now()
		timeObj = dateTimeObj.time()
		print('%s:%s:%s | %s' % (timeObj.hour, timeObj.minute, timeObj.second, memo))

	def file_list_to_DESeq2_ready_matrix(self, data_file, output_prefix):

		self.time_stamp('START')
		condition_dict, file_dir = self.list_to_file_dict(data_file)
		profile_dict, gene_list = self.file_dict_to_profile_dict(condition_dict, file_dir)
		self.create_DESeq2_ready_output(profile_dict, condition_dict, gene_list, output_prefix)


	def list_to_file_dict(self, data_file):

		self.time_stamp('Collecting Files')
		data_dict = {}
		data_file = open(data_file,'r')
		data_file_readlines = data_file.readlines()

		control_flag = 0
		case_flag = 0

		for i in range(len(data_file_readlines)):
			read = data_file_readlines[i]
			read = read.replace('\n','')

			if i == 0:
				file_dir = read
			else:
				if '#control' in read:
					case_flag = 0
					control_flag = 1
				if '#case' in read:
					case_flag = 1
					control_flag = 0
				try:
					if '#' not in read[0]:
						if case_flag == 1:
							try: data_dict['case'].append(read)
							except KeyError: data_dict['case'] = [read]

						if control_flag == 1:
							try: data_dict['control'].append(read)
							except KeyError: data_dict['control'] = [read]
				except IndexError:
					print ("[Notice] Input file list has some blank lines")
					print ("[Notice] If this is not the case, we do not know whats going on")

		data_file.close()
		return data_dict, file_dir

	def file_dict_to_profile_dict(self, data_dict, file_dir):

		self.time_stamp('Indexing file information to dict')
		print ('This might take some time')
		profile_dict = {}
		gene_list = []

		for condition in list(data_dict.keys()):
			for sample_name in data_dict[condition]:

				print ('Proceeding | %s' % sample_name)

				sample_file = '%s/%s/%sReadsPerGene.out.tab' % (file_dir, sample_name, sample_name)
				sample_file_open = open(sample_file,'r')
				sample_file_readlines = sample_file_open.readlines()

				#START: Actual, ReadsPerGene.out.tab file
				for i in range(len(sample_file_readlines)):
					if i > 3:
					#Note that ReadsPerGene contains statistics of mapping for 4 lines
						read = sample_file_readlines[i]
						read = read.replace('\n','')
						token = read.split('\t')
						gene = token[0]

						if gene not in gene_list:
							gene_list.append(gene)

						raw_count = token[1]
						profile_dict[gene, sample_name] = raw_count
				#END: Actual, ReadsPerGene.out.tab file

		return profile_dict, gene_list

	def create_DESeq2_ready_output(self, profile_dict, condition_dict, gene_list, output_prefix):

		self.time_stamp('Creating Output')
		output_txt = open(output_prefix + ".tsv",'w')
		output_meta_txt = open(output_prefix + ".meta.tsv",'w')

		#[1] write header of output_txt
		#[2] write meta information of output_meta_txt
		output_meta_txt.write('sample_name\tcondition\n')
		output_txt.write('GeneSymbol')
		print (condition_dict)
		for condition in list(condition_dict.keys()):
			sample_list = condition_dict[condition]
			for sample_name in sample_list:
				output_meta_txt.write('%s\t%s\n' % (sample_name, condition))
				output_txt.write('\t%s' % sample_name)
		output_txt.write('\n')

		for gene in gene_list:
			output_txt.write(gene)

			for condition in list(condition_dict.keys()):
				sample_list = condition_dict[condition]
				for sample_name in sample_list:
					raw_count = profile_dict[gene, sample_name]
					output_txt.write('\t%s' % raw_count)
			output_txt.write('\n')

		print ("[Notice] DONE!")
		output_txt.close()


if __name__ == "__main__":
	import sys
	import os
	print ("This script is not meant to be run")
else:
	print ("Loading FL")


