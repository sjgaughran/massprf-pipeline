# massprf-pipeline

## Requirements
- Python 3.6
- C compiler (for pysam)

## Installation
```
$ git clone https://github.com/sjgaughran/massprf-pipeline.git
$ cd massprf-pipeline
$ pip3 install --editable .
$ PMRF --help
```

## Usage
There are three commands, `seq`, `ancestor`, and `consensus`. 

```
$ PMRF [command] -v 'VARIANTS.vcf.gz' -f 'REFERENCE.fasta' -n 'ANNOTATION.gff' -d 'SISTER SAMPLE NAME' -o 'OUTPUT DIRECTORY NAME' -a 'OUTGROUP SAMPLE NAME'
```
### Example
```
$ cd massprf-pipeline/testfiles
$ PMRF seq -v 'HMS_weddell_AFS_34359.vcf.gz' -f 'NW_018734359.1.fasta' -n 'NW_018734359.1.gff' -d 'WED1' -o 'output' -a 'AFS1'
```