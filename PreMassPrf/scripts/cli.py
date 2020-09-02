import click
from PreMassPrf.main import MassPrf
import os

@click.group()
def PMRF():
    pass

@PMRF.command()
@click.option('-v', '--vcf', required=True, type=click.Path(exists=True), help='Variant file in sorted VCF format [file.vcf]. Needs to be bgzipped and tabix (.tbi) indexed')
@click.option('-f', '--reference-file', required=True, type=click.Path(exists=True), help='Reference genome file in fasta format [ref.fasta]')
@click.option('-n', '--annotation-file', required=True, type=click.Path(exists=True), help='Annotation file (GTF or GFF) [annot.gtf, annot.gff]')
@click.option('-d', '--sister-species-sample', required=True, help='Sister/divergence sample name as seen in VCF')
@click.option('-o', '--out-directory', required=True, help='Path to output directory for the many files that will be generated')
@click.option('-g', '--gene-list', required=False, type=click.Path(exists=True), help='Use only genes contained in list. .txt file of gene names, one on each line [genes.txt]')
@click.option('-a', '--outgroup-sample', required=False, help='Ancestral sample name as seen in VCF')
@click.option('--verbose', is_flag=True, help='Make program run verbose')
def consensus(vcf, reference_file, annotation_file, sister_species_sample, out_directory, gene_list, outgroup_sample, verbose):
    # print(vcf, reference_file, annotation_file, sister_species_sample, out_directory, gene_list)
    # vcf_file, gff_file, ref_file, divergent, outgroup
    if not os.path.exists(out_directory):
        os.mkdir(out_directory)
        print(f"Created output directory {out_directory}")

    M1 = MassPrf(vcf, annotation_file, reference_file, sister_species_sample, outgroup_sample, verbose)

    print("Started generating consensus sequences...")
    if gene_list:
    	M1.consensus_specific(gene_list, out_directory)
    else:
    	M1.consensus_all_genes(out_directory)
    print("Finished.")

@PMRF.command()
@click.option('-v', '--vcf', required=True, type=click.Path(exists=True), help='Variant file in sorted VCF format [file.vcf]. Needs to be bgzipped and tabix (.tbi) indexed')
@click.option('-f', '--reference-file', required=True, type=click.Path(exists=True), help='Reference genome file in fasta format [ref.fasta]')
@click.option('-n', '--annotation-file', required=True, type=click.Path(exists=True), help='Annotation file (GTF or GFF) [annot.gtf, annot.gff]')
@click.option('-d', '--sister-species-sample', required=True, help='Sister/divergence sample name as seen in VCF')
@click.option('-a', '--outgroup-sample', required=True, help='Ancestral sample name as seen in VCF')
@click.option('-o', '--out-directory', required=True, help='Path to output directory for the many files that will be generated')
@click.option('-g', '--gene-list', required=False, help='Use only genes contained in list. .txt file of gene names, one on each line [genes.txt]')
@click.option('--verbose', is_flag=True, help='Make program run verbose')
def ancestor(vcf, reference_file, annotation_file, sister_species_sample, outgroup_sample, out_directory, gene_list, verbose):
    if not os.path.exists(out_directory):
        os.mkdir(out_directory)
        print(f"Created output directory {out_directory}")

    M1 = MassPrf(vcf, annotation_file, reference_file, sister_species_sample, outgroup_sample, verbose)

    print("Started ancestral consensus generation...")
    if gene_list:
    	M1.ancestral_specific(gene_list, out_directory)
    else:
    	M1.ancestral_all_genes(out_directory)
    print("Finished.")

@PMRF.command()
@click.option('-v', '--vcf', required=True, type=click.Path(exists=True), help='Variant file in sorted VCF format [file.vcf]. Needs to be bgzipped and tabix (.tbi) indexed')
@click.option('-f', '--reference-file', required=True, type=click.Path(exists=True), help='Reference genome file in fasta format [ref.fasta]')
@click.option('-n', '--annotation-file', required=True, type=click.Path(exists=True), help='Annotation file (GTF or GFF) [annot.gtf, annot.gff]')
@click.option('-d', '--sister-species-sample', required=True, help='Sister/divergence sample name as seen in VCF')
@click.option('-o', '--out-directory', required=True, help='Path to output directory for the many files that will be generated')
@click.option('-g', '--gene-list', required=False, help='Use only genes contained in list. .txt file of gene names, one on each line [genes.txt]')
@click.option('-a', '--outgroup-sample', required=False, help='Ancestral sample name as seen in VCF')
@click.option('--verbose', is_flag=True,  help='Make program run verbose')
def seq(vcf, reference_file, annotation_file, sister_species_sample, out_directory, gene_list, outgroup_sample, verbose):
    if not os.path.exists(out_directory):
        os.mkdir(out_directory)
        print(f"Created output directory {out_directory}")

    M1 = MassPrf(vcf, annotation_file, reference_file, sister_species_sample, outgroup = outgroup_sample, verbose = verbose)
    print("Started seqeunce generation...")
    if gene_list:
    	M1.full_fasta_specific(gene_list, out_directory)
    else:
    	M1.full_fasta_all(out_directory)
    print("Finished.")

    	# loc = "/home/accts/ewa2/PMF/PreMassPrf"
    	# gff_loc = f'{loc}/NW_018734359.1.gff'
    	# ref_loc = f'{loc}/NW_018734359.1.fasta'
    	# vcf_loc = f'{loc}/HMS_weddell_AFS_34359.vcf.gz'

    	# PMRF consensus -v 'HMS_weddell_AFS_34359.vcf.gz' -f 'NW_018734359.1.fasta' -n 'NW_018734359.1.gff' -d 'WED1' -o 'output' -g 'testing.txt' -a 'AFS1'