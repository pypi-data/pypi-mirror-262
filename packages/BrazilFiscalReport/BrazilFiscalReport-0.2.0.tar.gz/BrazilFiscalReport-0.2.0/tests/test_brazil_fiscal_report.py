import os
import unittest

from brazilfiscalreport import pdf_docs, xfpdf


class TestBrazilFiscalReport(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.xfpdf = xfpdf.xFPDF()

    def test_code128_format(self):
        data = "123456789"
        expected_result = [
            xfpdf.CODE128C["StartC"],
            12,
            34,
            56,
            78,
            100,
            25,
            79,
            xfpdf.CODE128C["Stop"],
        ]
        result = self.xfpdf.code128_format(data)
        self.assertEqual(result, expected_result)

    def test_format_cpf_cnpj(self):
        nfedanfe_instance = pdf_docs
        cpf = nfedanfe_instance.format_cpf_cnpj("76586507812")
        self.assertEqual("765.865.078-12", cpf)

    def test_format_number(self):
        nfedanfe_instance = pdf_docs
        number = nfedanfe_instance.format_number("19500")
        self.assertEqual("19.500", number)

    def test_create_danfe_pdf(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))

        xml_file_path = os.path.join(current_dir, "data", "NFe_teste_1.xml")
        with open(xml_file_path, encoding="utf8") as f:
            xmls = [f.read()]
        pdf = pdf_docs.Danfe(
            xmls=xmls, image=None, cfg_layout="ICMS_ST", receipt_pos="top"
        )
        pdf.output("danfe.pdf")

        self.assertTrue(os.path.isfile("danfe.pdf"))

    def test_create_danfe_page_2_pdf(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))

        xml_file_path = os.path.join(current_dir, "data", "NFe_teste_3.xml")
        with open(xml_file_path, encoding="utf8") as f:
            xmls = [f.read()]
        pdf = pdf_docs.Danfe(
            xmls=xmls, image=None, cfg_layout="ICMS_ST", receipt_pos="top"
        )
        pdf.output("danfe_page_2.pdf")

        self.assertEqual(pdf.nr_pages, 2)
        self.assertEqual(pdf.title, "DANFE")
        self.assertTrue(os.path.isfile("danfe_page_2.pdf"))

    def test_create_danfe_pdf_logo(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))

        xml_file_path = os.path.join(current_dir, "data", "NFe_teste_1.xml")
        logo_file_path = os.path.join(current_dir, "data", "Logo-Engenere.jpg")
        with open(xml_file_path, encoding="utf8") as f:
            xmls = [f.read()]
        pdf = pdf_docs.Danfe(
            xmls=xmls, image=logo_file_path, cfg_layout="ICMS_ST", receipt_pos="top"
        )
        pdf.output("danfe_logo.pdf")

        self.assertTrue(os.path.isfile("danfe_logo.pdf"))

    def test_create_danfe_pdf_paisagem(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        xml_file_path = os.path.join(current_dir, "data", "NFe_teste_1.xml")

        with open(xml_file_path, encoding="utf8") as f:
            xmls = [f.read()]
        xmls_paisagem = [
            xml.replace("<tpImp>1</tpImp>", "<tpImp>2</tpImp>") for xml in xmls
        ]
        pdf = pdf_docs.Danfe(
            xmls=xmls_paisagem, image=None, cfg_layout="ICMS_ST", receipt_pos="top"
        )

        pdf.recibo_l()
        pdf.output("danfe_paisagem.pdf")
        self.assertTrue(os.path.isfile("danfe_paisagem.pdf"))

    def test_create_cce_pdf(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))

        xml_file_path = os.path.join(current_dir, "data", "xml_cce_1.xml")
        logo_file_path = os.path.join(current_dir, "data", "Logo-Engenere.jpg")

        # DaCCe
        emitente = {
            "nome": "COMPANY ME-EPP",
            "end": "AV TEST, 00",
            "bairro": "TEST",
            "cep": "00000-000",
            "cidade": "SÃO PAULO",
            "uf": "SP",
            "fone": "(11) 1234-5678",
        }
        with open(xml_file_path, encoding="utf8") as f:
            xmls = [f.read()]

        pdf_cce = pdf_docs.DaCCe(xmls=xmls, emitente=emitente, image=logo_file_path)
        pdf_cce.output("cce.pdf")

        self.assertTrue(os.path.isfile("cce.pdf"))


if __name__ == "__main__":
    unittest.main()
