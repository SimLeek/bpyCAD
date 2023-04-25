from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, "README.rst")
with open(readme_path, "rb") as stream:
    readme = stream.read().decode("utf8")

requirements_path = os.path.join(here, "requirements.txt")
with open(requirements_path) as f:
    required = f.read().splitlines()

requirements_dev_path = os.path.join(here, "requirements_dev.txt")
with open(requirements_path) as f:
    required_dev = f.read().splitlines()

setup(
    long_description=readme,
    name='bpycad',
    version='0.1.0',
    description="Programmatic cad using blender's bpy library.",
    python_requires="==3.*,>=3.10.0",
    project_urls={"repository": "https://github.com/simleek/bpycad"},
    author="SimLeek",
    author_email="simulator.leek@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=required,
    extras_require={
        "dev": required_dev
    },

)
