import setuptools

setuptools.setup(name='fileFuse',
                 version='0.0.6',
                 packages=setuptools.find_packages(),
                 include_package_data=True,
                 author="Jayant Khanna",
                 description="This project can easily read any file and return the contents of the file. For more information, visit the github page: https://github.com/jayantkhanna1/fileFuse",
                 classifiers=[
                     'Programming Language :: Python :: 3',
                     'Operating System :: OS Independent',
                     'Topic :: Scientific/Engineering :: Bio-Informatics'
                 ],
                 install_requires=['beautifulsoup4', 'numpy', 'openpyxl', 'pandas','PyPDF2', 'python-docx', 'python-pptx' ,'XlsxWriter','pypdf'],
                 python_requires='>=3'
                 )
