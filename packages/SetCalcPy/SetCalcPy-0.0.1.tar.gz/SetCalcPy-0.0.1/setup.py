import setuptools


with open('README.md', 'r') as fh:
    description = fh.read()

setuptools.setup(name='SetCalcPy',
                 version='0.0.1',
                 author='SockRocks',
                 packages=['SetCalcPy'],
                 long_description=description,
                 long_description_content_type="text/markdown",
                 url='https://github.com/SockRocks/Python-Elementary-Set-Theory-Calculator',
                 license='MIT',
                 python_requires='>=3.8',
                 install_requires=[]
                 )