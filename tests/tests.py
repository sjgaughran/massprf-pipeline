from PreMassPrf.annotation import Annotation
from PreMassPrf.main import MassPrf
import unittest
import os



class AnnotationTests(unittest.TestCase):
    def setUp(self):
        loc = os.path.dirname(os.path.realpath(__file__))
        gff_loc = f'{loc}/test-files/NW_018734359.1.gff'
        ref_loc = f'{loc}/test-files/NW_018734359.1.fasta'
        self.annot = Annotation(gff_loc, ref_loc)
    
    def test_num_type(self):
        # test the num_type function
        self.assertEqual(self.annot.num_type("gene"), 110, "Number of genes in this gff file should be 110")
        
    def test_get_gene(self):
        # test get_gene
        gene = self.annot.get_gene('gene17317')
        self.assertEqual(gene.chrom, "NW_018734359.1")
    
    def test_transcript_dict(self):
        # test transcript_dict
        gene = self.annot.get_gene('gene17317')
        pos_dict, mRNA_transcripts = self.annot.transcript_dict(gene)
        self.assertEqual({'rna21038': 'ATGTCCAAGCCGGTGGACCACGTCAAGCGGCCCATGAACGCCTTCATGGTGTGGTCACGGGCTCAGCGGCGCAAGATGGCCCAGGAAAACCCCAAGATGCACAACTCAGAGATCAGCAAGCGCCTGGGCGCCGAGTGGAAGCTGCTCACCGAGTCGGAGAAGCGGCCGTTCATCGACGAGGCGAAGCGTCTGCGCGCCATGCACATGAAGGAGCACCCCGACTACAAGTACCGGCCGCGGCGCAAGCCCAAGACGCTGCTCAAGAAGGACAAGTTCGCCTTCCCGGTGCCCTACGGCCTGGGTGGCGTGGCCGACGCCGAGCACCCGGCGCTCAAGGCGGGCGCCGGGCTGCACGCGGGCGCCGGCGGCGGCCTGGTGCCTGAATCGCTGCTCGCCAATCCCGAGAAGGCGGCCGCCGCCGCAGCCGCCGCCGCCGCACGCGTCTTCTTCCCGCAGTCGGCCGCCGCCGCCGCCGCCGCCGCCGCCGCCGCCGCCGCCGGCAGTCCCTACTCGCTACTCGACTTGGGCTCCAAGATGGCAGAGATCTCGTCGTCGTCGTCCGGCCTCCCGTACGCGTCGTCGCTGGGCTACCCGACCGCGGGCGCCGGCGCCTTCCACGGCGCGGCGGCGGCGGCTGCAGCGGCGGCCGCGGCCGCCGGGGGGCACACGCACTCGCACCCCAGCCCGGGCAACCCGGGCTACATGATCCCGTGCAACTGCAGCGCGTGGCCCAGCCCCGGGCTGCAGCCGCCGCTCGCCTACATCCTGCTGCCGGGCATGGGCAAGCCTCAGCTGGACCCCTACCCCGCGGCCTACGCCGCCGCGCTATGA'}, mRNA_transcripts)

    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 3)), 6, "Should be 6")
        

class MassPrfTests(unittest.TestCase):
    def setUp(self):
        loc = os.path.dirname(os.path.realpath(__file__))
        gff_loc = f'{loc}/test-files/NW_018734359.1.gff'
        ref_loc = f'{loc}/test-files/NW_018734359.1.fasta'
        vcf_loc = f'{loc}/test-files/HMS_weddell_AFS_34359.vcf.gz'
        self.pmrf = MassPrf(vcf_loc, gff_loc, ref_loc, 'WED1', 'AFS1', True)

    
    def test_gen_ancestor(self):
        # test the gen_ancestor function
        data = {'HMS_Benny': {'rna20964': 'ATGAGGGAATGAT'}, 
        'HMS_PJ22': {'rna20964': 'ATGAGGGGGTAAT'},  
        'HMS_YE37': {'rna20964': 'ATGAGGGGGTGAT'},  
        'WED1': {'rna20964': 'ATGCGGGGGTGAT'}, 
        'AFS1': {'rna20964': 'ATGCGGGGGTGAT'}}
        ancestral = self.pmrf.gen_ancestor(None, tr_dict = data)

        self.assertEqual({'rna20964': {'consensus': '***S*********', 'ancestor': 'ATGCGGGGGTGAT'}}, ancestral)

    def test_consensus(self):
        # test the consensus function
        data = {'HMS_Benny': {'rna20964': 'ATGAGGGAATGAT'}, 
        'HMS_PJ22': {'rna20964': 'ATGAGGGGGTAAT'},  
        'HMS_YE37': {'rna20964': 'ATGAGGGGGTGAT'},  
        'WED1': {'rna20964': 'ATGCGGGGGTGAT'},
        'AFS1': {'rna20964': 'ATGCGGGGGTGAT'}}
        ancestral = self.pmrf.consensus(None, tr_dict = data)
        self.assertEqual({'rna20964': {'target': '*******RS*S****', 'divergent': '***S***********'}}, ancestral)


if __name__ == '__main__':
    unittest.main()