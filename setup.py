from setuptools import find_packages, setup

REQUIREMENTS_PATH = "requirements.txt"


with open(REQUIREMENTS_PATH) as our_file:
    required_libraries = our_file.read().splitlines()

setup(
    name="Data mining ochoba, specialized",
    version="0.1.1",
    description="Скачивание нужных файлов, более простая версия.",
    long_description="README.md",
    packages=find_packages(),
    install_requires=required_libraries,
    license="MIT",
    license_files="LICENSE",
)
