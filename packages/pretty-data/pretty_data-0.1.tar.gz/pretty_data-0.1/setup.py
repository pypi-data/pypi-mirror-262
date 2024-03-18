from distutils.core import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = ((((this_directory / "README.md").read_text().replace("ö", "o").replace("ü", "u").
                    replace("ğ","g")).replace("İ", "I").replace("Ü", "U")
                    .replace("Ö", "O")).replace("Ğ","G").replace("ş","s").
                    replace("ç", "c")).replace("Ç", "C").replace("Ş", "S")

setup(
    name='pretty_data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Hayati YURTOĞLU",
    author_email="hayatiyurtoglu71@gmail.com",
    version="0.1",
    license='MIT',
    install_requires=[
        'pandas',
        'scikit-learn',
        "seaborn",
        "matplotlib",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
      ],
)
