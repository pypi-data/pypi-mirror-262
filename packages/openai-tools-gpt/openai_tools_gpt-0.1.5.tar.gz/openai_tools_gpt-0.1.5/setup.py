from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as file:
    description = file.read()

setup(
    name="openai_tools_gpt",
    version="0.1.5",
    packages=find_packages(),
    install_requires=["openai>=1.12.0", "retry>=0.9.2", "python-dotenv>=1.0.1"],
    # entry_points={
    #     "console_scripts": [
    #         "command = package_name:functoin_name",
    #     ],
    # },
    long_description=description,
    long_description_content_type="text/markdown",
)
