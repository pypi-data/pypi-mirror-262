from setuptools import setup

setup(
    name="BrazilFiscalReport",
    version="0.2.0",
    long_description="""
    Python library for generating Brazilian auxiliary
    fiscal documents in PDF from XML documents.
    """,
    url="https://github.com/Engenere/BrazilFiscalReport",
    author="Engenere",
    keywords="brazil fiscal report",
    packages=["brazilfiscalreport"],
    license="AGPL-3.0",
    install_requires=["fpdf2"],
)
