import os,sys,argparse
# import fileinput,time
import glob
import re,bisect
import pandas as pd
import numpy as np
import matplotlib
from scipy import stats





indir = 'f2_bedfiles_merged'
outdir = 'f3_coBinding_merge'
os.makedirs(outdir,exist_ok=True)

# name_match = pd.read_excel('../../data/TCGA/TCGA-ATAC_SE_cancerType_match.xlsx',index_col=0)   
# name_match = name_match.dropna()

selected_factors = {}
tfbs_cp_dir = '../f2_cor_CP_SE_AICAP/f9_per_CT_TFBS_CP_cor_zscore_CP/TFBS_CP/'
for ct in ['MCF-7','HCT-116'][:]:
    df = pd.read_csv('{}/_CP_TFBS_all_vs_TFMS_{}.csv'.format(tfbs_cp_dir,ct),index_col=0)
    selected_factors['{} top_TFBSCP'.format(ct)] = df['TFBS CP rank'].sort_values().iloc[:3].index
    selected_factors['{} top_zscored_TFBSCP'.format(ct)] = df['avg rank'].sort_values().iloc[:3].index

# selected_factors = {#'MCF-7 top_TFBSCP':['ERG','ELK1','FOS'],
#                     'MCF-7 top_zscored_TFBSCP':['ERG','JUND','ZNF143'],
#                     #'HCT-116 top_TFBSCP':['ELF1','JUND','SRF',],
#                     'HCT-116 top_zscored_TFBSCP':['JUND','CEBPB','YY1']}

for treat_flag in ['percentile_T','percentile_T_ExtendMerge'][:]:
    for ct in ['MCF-7','HCT-116'][:]:
        for factorType in ['top_TFBSCP','top_zscored_TFBSCP'][:]:
            factors = selected_factors['{} {}'.format(ct,factorType)]
            # print(factors)
            bedfiles = ['{}/{}/{}_{}_{}.merge.bed'.format(indir,ct,ct,i,treat_flag) for i in factors]
            subdir = '{}_{}'.format(ct,factorType)
            os.makedirs(outdir+os.sep+subdir,exist_ok=True)
            
            catFile = '{}/{}/{}.cat.bed'.format(outdir,subdir,treat_flag)
            sortFile = '{}/{}/{}.sort.bed'.format(outdir,subdir,treat_flag)
            mergeFile = '{}/{}/{}.merge.bed'.format(outdir,subdir,treat_flag)
            commandLine = '\ncat {} > {}\n'.format(' \\\n'.join(bedfiles),catFile)
            print(commandLine)
            commandLine = 'bedtools sort -i {} > {}'.format(catFile,sortFile)
            print(commandLine)
            commandLine = 'bedtools merge -i {} > {}\n'.format(sortFile,mergeFile)
            print(commandLine)
            
            
            for factor in factors:
                afile = mergeFile
                bfile = '{}/{}/{}_{}_{}.merge.bed'.format(indir,ct,ct,factor,treat_flag)
                outfile = '{}/{}/{}.merge.{}.overlapped.bed'.format(outdir,subdir,treat_flag,factor)
                commandLine = 'bedtools intersect -a {} -b {} -wa -c > {}'.format(afile,bfile,outfile)
                print(commandLine)
                
            for prename in ['hg38_exons', 'hg38_introns', 'hg38_4k_promoter_geneID' ]:
                afile = mergeFile
                bfile = '/nv/vol190/zanglab/zw5j/data/geneID_annotation/hg38/{}.bed'.format(prename)
                outfile = '{}/{}/{}.merge.{}.overlapped.bed'.format(outdir,subdir,treat_flag,prename)
                commandLine = 'bedtools intersect -a {} -b {} -wa -c > {}'.format(afile,bfile,outfile)
                print(commandLine)
            
        
        




