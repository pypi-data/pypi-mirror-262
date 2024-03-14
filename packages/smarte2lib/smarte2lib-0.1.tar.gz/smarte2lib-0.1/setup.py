from setuptools import setup, find_packages

setup(
    name="smarte2lib",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pymysql>=1.1.0',
        'sshtunnel>=0.4.0',
        'pandas>=2.1.4'  
    ],
    # Otra metadata opcional
    author="Robert Novak, Marcos Delgado Álvaro",
    author_email="senialaburjc@gmail.com",
    description="Common tools for the SmartE2 organization.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)