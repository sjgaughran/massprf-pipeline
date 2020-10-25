import gffutils
from pyfaidx import Fasta
import os

def assign_pos(pos_dict, mRNA_id, CDS_length, start, sequence):
    """
    Helper function for assigning position to nucleotide 
    for a given CDS sequence string (ex. ATCGTTA) and a start position (ex. 2399), return a dict
    {
    <position number>: <nucleotide letter>
    }
    :return: dict
    """
    for i in range(len(sequence)):
        if (start + i) not in pos_dict:
            pos_dict[start + i] = []
        pos_dict[start + i].append([mRNA_id, CDS_length + i, sequence[i]])

    return pos_dict


def assign_pos_rev(pos_dict, mRNA_id, CDS_length, end, sequence):
    """
    Helper function for assigning position to nucleotide 
    for a given CDS sequence string (ex. ATCGTTA) and a start position (ex. 2399), return a dict
    {
    <position number>: <nucleotide letter>
    }
    :return: dict
    """
    for i in range(len(sequence)):
        if (end - i) not in pos_dict:
            pos_dict[end - i] = []
        pos_dict[end - i].append([mRNA_id, CDS_length + i, sequence[len(sequence) - 1 - i]])

    return pos_dict


class Annotation:
    """ A class to manipulate the reference (fasta) file and gene-finding format (gff) file

    Attributes:
        gff_file:  gff file location
        ref_file: fasta file location
        ref: fasta file parser object
        db: local sqlite3 file-based database made from the gff file
    """
    def __init__(self, gff_file, ref_file):
        self.gff_file = gff_file
        self.ref_file = ref_file
        self.ref = Fasta(self.ref_file)
        self.db = self.__make_db()

    def __make_db(self):
        """
        Creates a local sqlite3 file-based database for a given gff file
        dependancy: gffutils
        :return:
        """

        gff_db = self.gff_file.split('/')[-1][0:-4] + '.db'

        if not os.path.exists(gff_db): 
            print(f"Creating database for {self.gff_file} called {gff_db}")
            gffutils.create_db(self.gff_file, dbfn=gff_db, force=True, keep_order=True, merge_strategy='merge',
                               sort_attribute_values=True)
            print(f"Finished initializing {gff_db}")
        else: 
            print(f'Using existing {gff_db}')
        return gffutils.FeatureDB(gff_db, keep_order=True)

    def get_all_genes(self):
        """
        Gets all the genes, based on the gff file
        :return: iterator of genes
        """

        # TODO: get only genes where gene_biotype=protein_coding. 
        # Right now pseudogenes are also being included which results in transcript_dict returned an empty object 
        return self.db.features_of_type("gene")

    def get_gene(self, name):
        """
        Gets the gene feature object for a given gene name (as defined in the gff file)
        :param name: string of gene name
        :return: gene feature object
        """
        return self.db[name]


    def num_type(self, kind):
        """
        Returns how many of some feature type like exon or gene or CDS
        :param kind: string such as "exon", "gene", "tRNA"
        :return int
        """
        return self.db.count_features_of_type(kind)

    def transcript_dict(self, gene):
        """
        Returns dictionaries which relates chromosome position to transcript position, as well as transcripts
        :param gene: ex. <Feature gene (2L:7529-9484[+]) at 0x...>
        :return: pos_dict - a dictionary which relates position in chromosome to position in transcript. 
                 pos_dict[position#] = [['mRNA ID', index in transcript string, nucleotide letter]]  
                 - ex. pos_dict[15563950] = [['rna21038', 795, 'G'], ['rna21039', 672, 'G']]   
                 mRNA_transcripts - a dicitonary of all the transcripts of the gene
                 mRNA_transcripts['mRNA ID'] = 'ATGNNNNNNNNNNNNSTOP'
        """
        mRNA_all = self.db.children(gene, featuretype='mRNA', order_by='start')  # returns a generator
        pos_dict = {}
        mRNA_transcripts = {}
        

        for mRNA in mRNA_all:
            # print(mRNA.id)
            CDS_all = self.db.children(mRNA, featuretype='CDS', order_by='start')
            CDS_length = 0
            CDS_str = ''
            if gene.strand == '-':
                CDS_all = reversed(list(CDS_all))
                # print("reversed")
            i = 0
            frame_offset = 0

            for CDS in CDS_all:
                if i == 0 and CDS.frame != '0': # adjust for frame of first CDS
                    frame_offset = int(CDS.frame)
                else:
                    frame_offset = 0
                i += 1

                if CDS.strand == "+":
                    sequence = self.ref[gene.chrom][CDS.start - 1 + frame_offset:CDS.end].seq.upper()
                    pos_dict = assign_pos(pos_dict, mRNA.id, CDS_length, CDS.start, sequence)
                    #print(CDS.start, CDS.end, sequence)
                    CDS_str += sequence
                    # print(CDS_str)
                else:
                    sequence = self.ref[gene.chrom][CDS.start - 1:CDS.end - frame_offset].complement
                    pos_dict = assign_pos_rev(pos_dict, mRNA.id, CDS_length, CDS.end, sequence.seq.upper())
                    CDS_str += sequence.reverse.seq.upper()
                    # print("minus", self.ref[gene.chrom][CDS.start - 1:CDS.end].complement.seq)
                    # print(CDS.start, CDS.end)
                CDS_length += abs(CDS.end - CDS.start + 1)
                # print(CDS_length, CDS_str)

            mRNA_transcripts[mRNA.id] = CDS_str

        if mRNA_transcripts is {}:
            print('No mRNA transcripts for this gene. Could be pseudogene.')

        return pos_dict, mRNA_transcripts