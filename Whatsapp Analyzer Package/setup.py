from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'This is whatsapp group chat analysis library or package which will basically help you to create beautiful interactive charts of various interesting insights in just 2 to 3 lines of code. You do not have to worry about anything, just load the chat file and enjoy it.'
LONG_DESCRIPTION = \
    'This is whatsapp group chat analysis library or package which will basically help you to create beautiful interactive charts of various interesting insights in just 2 to 3 lines of code. ' \
    'You do not have to worry about anything, just load the chat file and enjoy it. Actually their are more than 15 methods are available, using them you can ' \
    'create beautiful user interactive charts. Even you can download the preprocessed data, charts and use it. This is my small open source contribution to python\'s community.'

# Setting up
setup(
    name="WhatsApp-Analyzer",
    version=VERSION,
    author="ronil08",
    author_email="ronyy0080@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['plotly', 'nltk', 'numpy', 'emoji', 'wordcloud', 'matplotlib', 'pandas'],
    keywords=['whatsapp analyzer', 'whatsapp lib', 'whatsapp analysis', 'whatsapp python', 'chat', 'whatsapp group chat analysis', 'whatsapp library', 'ronil patil', 'ronil08'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)