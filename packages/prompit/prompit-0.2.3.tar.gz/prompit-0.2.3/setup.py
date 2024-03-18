from setuptools import setup, find_packages

setup(
    name="prompit",
    version="0.2.3",
    description="Prompit",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords="AI engineering, prompt engineering",
    license="MIT",
    author="oliveirabruno01",
    author_email="brunocabeludo321@gmail.com",
    url="https://github.com/oliveirabruno01/prompit",
    py_modules=["prompit"],
    package_dir={"": "src"},
    packages=find_packages("src"),
    entry_points={
        "console_scripts": [
            "prompit=prompit.cli:main",
        ]
    },
    python_requires=">=3.8.0",
    install_requires=[
        "pathspec~=0.12.1",
        "pytest~=8.1.1",
        "pytest-cov",
        "pathlib~=1.0.1",
    ],
)
