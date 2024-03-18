from setuptools import setup, find_packages

vers = "1.0.1.1"

setup(
    name="temporary-number",
    version=vers,
    description="Simple TempSMS Scraper",
    long_description_content_type="text/markdown",
    long_description=open("README.md", encoding="utf-8").read(),
    packages=[
        "temporary_number"
    ],
    author="@ham_86",
    url=f"http://pypi.python.org/pypi/temporary-number",
    license="MIT",
    project_urls={
        "Homepage": "https://github.com/hamutan-86/Temporary-Number",
    },
    install_requires=[
        "tls-client",
        "beautifulsoup4",
        "lxml",
    ],
)
