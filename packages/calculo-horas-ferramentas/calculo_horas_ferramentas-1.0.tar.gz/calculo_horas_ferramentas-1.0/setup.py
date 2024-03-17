from setuptools import setup,find_packages
from pathlib import Path

setup(
    name='calculo_horas_ferramentas',
    version=1.0,
    description='Este pacote ira fornecer ferramentas para calculo de horas extras e calculo de horas noturnas',
    long_description=Path('README.md').read_text(),
    author='Paulo Andre Vale Castanha',
    author_email='p33castanha@outlook.com',
    keywords=['Horas', 'Extras', 'Noturnas', 'Calculo', 'Adicional'],
    packages=find_packages())
