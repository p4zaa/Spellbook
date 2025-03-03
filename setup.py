from setuptools import setup, find_packages

setup(
    name="spellbook",
    version="0.1.0",
    packages=find_packages(include=["spellbook", "spellbook.*"]),
    install_requires=[
        "numpy",
        "matplotlib",
        "polars",
        "fastexcel",
        "scikit-learn",
        # Add other dependencies here
    ],
    package_data={"spellbook.fonts": ["*.ttf", "*.otf", "*.woff", "*.woff2"],},
    include_package_data=True,
    description="A collection of useful code snippets and utilities.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/p4zaa/SpellBook",
    author="Pathompong Muangthong",
    author_email="pathompong.workspace@gmail.com",
    license="MIT",
)