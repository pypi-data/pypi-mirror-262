from setuptools import setup, find_packages

setup(
    name="swagMerge",
    version="1.0.1",
    description="Combine multiple Swagger files into a single YAML file.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url='https://gitlab.allence.cloud/commons-acp/python/swagmerge',
    author='yacine.jlassi',
    author_email='mohamedyacine.jlassi@allence-tunisie.com',
    packages=find_packages(),
    install_requires=[
        "argparse",
        "PyYAML"
    ],
    entry_points={
        'console_scripts': [
            'swagMerge=src.swag:main'
        ]
    }

)
