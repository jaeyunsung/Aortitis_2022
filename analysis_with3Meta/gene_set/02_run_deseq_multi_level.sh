data_file=aortitis.tsv
meta_file=aortitis.meta.tsv
output_file=aortitis.deg.tsv
echo "Proceeding >" $data_file $meta_file $output_file

#Rscript ../../src/RNAseqPipeline_SungLab/deseq2_multi_level.r $data_file $meta_file $output_file
Rscript ../../src/RNAseqPipeline_SungLab/deseq2.r $data_file $meta_file $output_file
