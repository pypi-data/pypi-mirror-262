import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='DigitalSoul',  # Replace with your package name
    version='1.0.0',
    author='Neural Dream Research',
    author_email='alihakimxyz@gmail.com',
    description='Unified Compute Platform - CPU, GPU, FPGA, Quantum Computing',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/NeuralDreamResearch/DigitalSoult',  # Optional
    py_modules=['DigitalSoul'],  # List your single file module
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',  # Specify minimum Python version
    install_requires=[
        
    ],
)

