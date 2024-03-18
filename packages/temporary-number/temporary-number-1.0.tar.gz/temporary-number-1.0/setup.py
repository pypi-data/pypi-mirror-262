from setuptools import setup, find_packages

vers = "1.0"

setup(
    name="temporary-number",
    version=vers,
    description="Simple and Brilliant, TempSMS Scraper",
    long_description_content_type="text/markdown",
    long_description=open("README.md", encoding="utf-8").read(),
    packages=[
        "temporary-number"
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
    ],
)
