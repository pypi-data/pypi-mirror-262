from setuptools import setup, find_packages

setup(
    name="nexus-python",
    version="0.2.1",
    packages=find_packages(),
    install_requires=["requests>=2.25.1", "tabulate>=0.9.0"],
    author="Will Humble",
    author_email="w@astraanalytics.co",
    description="A simple interface for interacting with NexusDB.",
    keywords="database nexusdb",
    url="https://www.nexusdb.io/",
)
