from setuptools import setup, find_packages

setup(
    name="openai_tools_gpt",
    version="0.1.1",
    packages=find_packages(),
    install_requires=["openai>=1.12.0", "retry>=0.9.2", "python-dotenv>=1.0.1"],
)
