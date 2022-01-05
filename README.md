Global Transcriptomic Profiling Identifies Differential Gene expression Signatures between Inflammatory and Non-inflammatory Aortic Aneurysms
=========================

DOI : TBD

Benjamin Hur, Matthew J. Koster, Jin Sung Jang, Cornelia M. Weyand, Kenneth J. Warrington, and Jaeyun Sung

Contact: hur.benjamin@mayo.edu
Corresponding Author : sung.jaeyun@mayo.edu

## Analysis associated with inflammatory and non-inflammatory aortic aneurysms.


#### Differentially expressed genes and volcano plot

>analysis_with3Meta/gene_set/01_run_deseq_multi_level.sh

>analysis_with3Meta/gene_set/02_geneset.sh

>analysis_with3Meta/gene_set/03_draw_vocano.sh

Note: DESeq2 (v1.26.0) was used during the analysis. Please note that we identified different DEG results compared to (v1.30)

#### Pharmacogenomic network construction

>analysis_with3Meta/network/01_run.sh

>analysis_with3Meta/network/02_parse_subnetwork.sh

>analysis_with3Meta/network/03_create_pharmacogenomic_network.sh

#### Others

PCA
>src/statistics/PCA_whole_data.ipynb

Identification of confounding effects
>src/statistics/linear_model_variable_significance.ipynb

Pie chart for PANTHER results
>src/statistics/panther_pie_chart.ipynb

trimming the fastq files and alignment
>/Users/m221138/Aortitis_Public/preprocess/01_trim_rawdata.sh
>/Users/m221138/Aortitis_Public/preprocess/02_run_alignmnet.sh

#### Data

Read counts of 50 samples and 26,475 genes with STAR alignment

>data/aortitis.tsv

log2 transformed TPM values of 50 samples and 26,475 genes with RSEM

>data/tpm_profile.log2.tsv

Raw data (.fastq) files will be available once the manuscript has been accepted.
