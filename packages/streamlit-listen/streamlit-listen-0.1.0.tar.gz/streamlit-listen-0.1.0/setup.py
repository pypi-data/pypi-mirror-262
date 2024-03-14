import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="streamlit-listen",
    version="0.1.0",
    author="Rafal Cegiela",
    author_email="rcegiela@gmail.com",
    description="Audio listener component for streamlit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/theevann/streamlit-audiorecorder",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.63"
    ],
)
