import setuptools

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="PPshare",
    version='0.0.9',
    author="zemengchuan",
    author_email="zemengchuan@gmail.com",
    license="MIT",
    description=
    "PPshare is an application platform that focuses on scientific research data for a long time. The platform provides direct crawling from the Internet, community collection, and team collation of data and storage into a database. It provides users with high-quality scientific research data through strict control over data quality.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zemengchuan/PPshare",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests", "pandas", "openpyxl", "python-Levenshtein", "fuzzywuzzy"
    ],
    keywords=["macro", "webcrawler", "data"],
    package_data={"": ["*.py", "*.xlsx"]},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)