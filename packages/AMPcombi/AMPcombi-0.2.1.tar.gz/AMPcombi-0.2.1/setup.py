from setuptools import setup

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name='AMPcombi',
    version='0.2.1',
    author='Anan Ibrahim, Louisa Perelo',
    author_email='ananhamido@hotmail.com, louperelo@gmail.com',
    packages=['ampcombi'],
    scripts=['ampcombi/ampcombi.py',
             'ampcombi/amp_database.py',
             'ampcombi/amp_fasta.py',
             'ampcombi/check_input.py',
             'ampcombi/diamond_alignment.sh',
             'ampcombi/diamond_makedb.sh',
             'ampcombi/reformat_tables.py',
             'ampcombi/functionality.py',
             'ampcombi/optional_inputs.py',
             'ampcombi/complete_summary.py',
             'ampcombi/signalpep_pred.py',
             'ampcombi/parse_gbks.py',
             'ampcombi/hmm_to_csv_input_file.py',
             'ampcombi/clustering_hits.py',
             'ampcombi/print_header.py',
             'ampcombi/version.py'],
    url='http://pypi.python.org/pypi/AMPcombi/',
    license='LICENSE.txt',
    description='A parsing tool for AMP tools.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["Proteomics", "Antimicrobial peptides", "Diamond", "MMSeqs2"
              "Standardization", "Formatting","Functional annotation"],
    install_requires=['pandas==1.5.2',
                      'biopython==1.80',
                      'requests'],
    python_requires='==3.11.*',
    entry_points={  
        'console_scripts': [
            'ampcombi = ampcombi:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.11",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Information Analysis"
        ],
)