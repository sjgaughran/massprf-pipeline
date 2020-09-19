# massprf-pipeline

## Contents
- [Purpose](#purpose)
- [Features](#features)
- [mafs2vcf](#mafs2vcf)
  * [Requirements](#requirements)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Example](#example)
- [PMRF](#pmrf)
  * [Requirements](#requirements-1)
  * [Installation](#installation-1)
  * [Usage](#usage-1)
  * [Example](#example-1)

## Purpose

Population genomic variant data are almost never stored as genomic sequence files, yet some software require input data to be in sequence format. One such software package, [MASS-PRF](https://github.com/Townsend-Lab-Yale/MASSPRF), is a powerful statistical tool that estimates the local strength of selection in protein-coding genes using the Poisson Random Field (PRF) framework (Zhao et al. 2017).

`massprf-pipeline` provides tools that prepare input files for analysis in MASS-PRF, as well as scripts to efficiently process and plot the results from MASS-PRF. The pipeline was created with genome-wide analyses in mind, but it can also be used on smaller subsets of genes. 

## Features 

This pipeline has two notable features that make it a powerful preprocessing tool for MASS-PRF:
* **Variant likelihood integration** (in `mafs2vcf`): Unlike other McDonald-Kreitman/PRF methods, MASS-PRF does not make use of the allele frequency spectrum for polymorphism data, instead relying on a binary category of polymorphic or invariant. MASS-PRF can therefore be used when the polymorphic state of a site can be established at the population level, even if individual genotypes are highly uncertain, as is often the case with low-coverage sequencing data from non-model organisms. We take advantage of this aspect of MASS-PRF by creating an optional pipeline to transform minor allele frequency estimate (`.mafs`) files from ANGSD into consensus sequence input files for MASS-PRF. 
* **Ancestral Sequence Reconstruction** (in `PMRF`): The standard PRF framework relies on assessing the pattern of divergent sites between two species. Some derived sites, however, could have been fixed in the non-target lineage, diluting the desired signal of selection in the target lineage. To avoid this, ancestral sequence reconstruction can be used to show divergence from the ancestral sequence rather than divergence from a sister species. In PMRF ancestor, we apply simple parsimony to assign the ancestral nucleotide for every variant position with the use of an additional outgroup species (i.e. ((target, sister)outgroup)). Parsimony-based ancestral sequence reconstruction can work well for closely related species with clearly resolved phylogenetic relationship, but is not recommended for more deeply divergent species. 

## mafs2vcf

`mafs2vcf` is a tool that transforms polymorphism likelihood (`.mafs`) files from ANGSD into pseudo-VCF files, which can then be processed in PMRF and used in MASS-PRF. Because ANGSD assesses allele frequencies at a site without calling individual genotypes, this opens the possibility of running tests for selection in MASS-PRF on (extremely) low-coverage genome sequencing data. 

`.mafs` files are generated in [ANGSD](http://www.popgen.dk/angsd/index.php/SNP_calling). In generating these files, you can apply quality filters in ANGSD (e.g. keeping SNPs with a p-value below a certain threshold, or setting a minimum minor allele frequency). The resulting `.mafs` files generally have the following format:

```
chromo  position        major   minor   unknownEM       pu-EM   nInd
1       14000873        G       A       0.282476        0.000000e+00    10
1       14001018        T       C       0.259890        7.494005e-14    9
1       14001867        A       G       0.272099        6.361578e-14    10
1       14002422        A       T       0.377890        0.000000e+00    9
1       14003581        C       T       0.194393        5.551115e-16    9
1       14004623        T       C       0.259172        2.424727e-13    10
```

Separate `.mafs` files must be generated for each species (target, sister, etc.). In `mafs2vcf`, the user specifies the role of each `.mafs` file (see [Usage](#usage)), and `mafs2vcf` generates a pseudo-VCF capturing the polymorphic (`0/1`) or divergent (`0/0`, `1/1`) state of the target population (SAMP1, SAMP2), the sister species (DIV1), and the outgroup species (ANC1). This pseudo-VCF can then be used as input for `PMRF consensus` or `PMRF ancestor` (see [PMRF Usage](#usage-1)). 

### Requirements


### Installation


### Usage


## PMRF




### Requirements
- Python 3.6
- C compiler (for pysam)

### Installation
```
$ git clone https://github.com/sjgaughran/massprf-pipeline.git
$ cd massprf-pipeline
$ pip3 install --editable .
$ PMRF --help
```

### Usage
`PMRF` has three commands:
* `seq`: creates
* `consensus`:
* `ancestor`:

```
$ PMRF [command] -v 'VARIANTS.vcf.gz' -f 'REFERENCE.fasta' -n 'ANNOTATION.gff' -d 'SISTER SAMPLE NAME' -o 'OUTPUT DIRECTORY NAME' -a 'OUTGROUP SAMPLE NAME'
```
### Example
```
$ cd massprf-pipeline/testfiles
$ PMRF seq -v 'HMS_weddell_AFS_34359.vcf.gz' -f 'NW_018734359.1.fasta' -n 'NW_018734359.1.gff' -d 'WED1' -o 'output' -a 'AFS1'
```
