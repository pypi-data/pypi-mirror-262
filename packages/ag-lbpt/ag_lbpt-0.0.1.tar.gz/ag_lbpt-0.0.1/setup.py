import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

LONG_DESCRIPTION = """

# **Algoritmos Metaheurísticos para el problema TSP**

"""

setup(
    name='ag_lbpt',
    version='0.0.1',
    description='Algoritmo Genético',
    long_description=LONG_DESCRIPTION,
    install_requires=['folium', 'networkx','csv'],
    long_description_content_type="text/markdown",
    author='Luis Beltran Palma Ttito',
    author_email='luis.palma@unsaac.edu.pe',
    license='GPL',
    packages=find_packages(),
    include_package_data=True
)