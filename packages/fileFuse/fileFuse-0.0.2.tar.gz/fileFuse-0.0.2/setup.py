# [metadata]
# name = fileFuse
# version = 0.0.1
# author = Jayant Khanna
# author_email = jayantkhanna3105@gmail.com
# description = This project is used to read a file and return the contents of the file
# long_description = file: README.md
# long_description_content_type = text/markdown
# url = https://github.com/jayantkhanna1/fileFuse
# classifiers =
#     Programming Language :: Python :: 3
#     Operating System :: OS Independent
# [options]
# packages = find:
# python_requires = >=3.7
# include_package_data = True
import setuptools

setuptools.setup(name='fileFuse',
                 version='0.0.2',
                 packages=setuptools.find_packages(),
                 include_package_data=True,
                 author="Jayant Khanna",
                 description="This project can easily read any file and return the contents of the file. For more information, visit the github page: https://github.com/jayantkhanna1/fileFuse",
                 classifiers=[
                     'Programming Language :: Python :: 3',
                     'Operating System :: OS Independent',
                     'Topic :: Scientific/Engineering :: Bio-Informatics'
                 ],
                 install_requires=['beautifulsoup4', 'numpy', 'openpyxl', 'pandas','PyPDF2', 'python-docx', 'python-pptx' ,'XlsxWriter'],
                 python_requires='>=3'
                 )
