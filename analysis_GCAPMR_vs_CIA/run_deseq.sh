data_file=aortitis_pmr_gca.tsv
meta_file=aortitis_pmr_gca.meta.tsv
output_file=aortitis_pmrgca.deg.tsv
echo "Proceeding >" $data_file $meta_file $output_file

Rscript ../src/RNAseqPipeline_SungLab/deseq2.r $data_file $meta_file $output_file
