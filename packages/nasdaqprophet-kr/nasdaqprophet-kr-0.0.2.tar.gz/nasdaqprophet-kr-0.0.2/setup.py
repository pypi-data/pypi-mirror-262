from setuptools import setup, find_packages

setup(
    name='nasdaqprophet-kr',
    version='0.0.2',
    description='nasdaq prophet for Korean Won',
    author='neddy0318',
    author_email='neddy0318@gmail.com',
    url='https://github.com/neddy0318/nasdaqprophet-kr',
    install_requires=['yfinance', 'pandas', 'numpy', 'prophet', 'sklearn', 'matplotlib.pyplot', 'pandas.tseries.offsets', 'currency_converter'],
    packages=find_packages(exclude=[]),
    keywords=['neddy0318', 'nasdaq', 'korean won', 'prophet', 'stock'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)