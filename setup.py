import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="redogm",
    version="0.0.1",
    author="Pedro Guzman",
    author_email="pedro@subvertic.com",
    description="A simple object graph mapper for RedisGraph",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/OneTesseractInMultiverse/redogm',
    packages=setuptools.find_packages(),
    install_requires=['redisgraph', 'python_cypher'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)