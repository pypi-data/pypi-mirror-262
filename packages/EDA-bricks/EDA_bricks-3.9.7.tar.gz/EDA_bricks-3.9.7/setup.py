from setuptools import setup, find_packages

setup(
    name='EDA_bricks',
    author='Geethanjali',
    version='3.9.7',
    packages=find_packages(),
    package_data={'': ['eda.py', 'requirements.txt',]},
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'bokeh',
        'dtaidistance',
        'factor_analyzer',
        'arch',
        'seaborn',
        'scipy',
        'statsmodels',
        'spectrum',
        'scikit-learn',
        'plotly',
        'psycopg2',
        'pymssql',
        'requests',
        'ipython',
        'jinja2',
        'pytz',
        'plotly',
        'sqlalchemy',
        'pyodbc',
        'cx_Oracle',
        'pandasql',
        'IPython',
    ]
    
)
