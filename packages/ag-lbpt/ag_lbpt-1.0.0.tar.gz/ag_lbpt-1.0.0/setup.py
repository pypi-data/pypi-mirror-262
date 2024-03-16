import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

LONG_DESCRIPTION = """

# Algoritmo Genético

#### Instalación

```
!pip install ag-lbpt
```
La guia de usuario puede encontrar en: [https://luispalma12345.github.io/ag_lbpt/index.html](https://luispalma12345.github.io/ag_lbpt/index.html)

[luis.palma@unsaac.edu.pe](mailto:luis.palma@unsaac.edu.pe), Luis Beltran Palma Ttito (autor)

"""

setup(
    name='ag_lbpt',
    version='1.0.0',
    description='Algoritmo Genético',
    long_description=LONG_DESCRIPTION,
    install_requires=['folium', 'networkx'],
    long_description_content_type="text/markdown",
    author='Luis Beltran Palma Ttito',
    author_email='luis.palma@unsaac.edu.pe',
    license='GPL',
    packages=find_packages(),
    include_package_data=True
)