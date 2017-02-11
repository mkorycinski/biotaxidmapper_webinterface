import unittest
import genome_context as gc

class ModuleTests(unittest.TestCase):
    def test_protein_acc_to_locus_tag(self):
        in_data = "AAB89752.1"
        out_data = "AF_1502"
        self.assertEqual(gc.protein_acc_to_locus_tag(in_data), out_data)

    def test_get_genomic_vicinity(self):
        loci_list = list('abcdefghijklmnop')
        locus_tag = 'h'
        vicinity_range = 5

        func_out = gc.get_genomic_vicinity(loci_list=loci_list,
                                           locus_tag=locus_tag,
                                           vicinity_range=vicinity_range)
        correct_ans = list('cdefgijklm')

        self.assertEqual(func_out, correct_ans)


class GeneObjTests(unittest.TestCase):
    testing_gene = gc.Gene(locus_tag="AF_1502")

    def test_taxid(self):
        self.assertEqual(self.testing_gene.taxid, '224325')

    def test_genome_acc(self):
        self.assertEqual(self.testing_gene.genome_acc, 'NC_000917.1')

    def test_query_gene_id(self):
        self.assertEqual(self.testing_gene.query_gene_id, '1484729')

    def test_correct_locus(self):
        self.assertEqual(self.testing_gene.locus_tag, 'AF_RS07570')

if __name__ == "__main__":
    unittest.main()
