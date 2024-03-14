from setuptools import setup, find_packages

setup(
    name='log-reg-dre',  
    version='0.1.6', 
    author='Sean Zhang',
    author_email='szhang120@gmail.com',
    description='Combines logistic regression for estimating density ratios with RU regression to mitigate distributional shift',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown', 
    packages=find_packages(),  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  
    install_requires=[
        'numpy',
        'torch',
        'matplotlib',
        'scikit-learn',
    ],
)

