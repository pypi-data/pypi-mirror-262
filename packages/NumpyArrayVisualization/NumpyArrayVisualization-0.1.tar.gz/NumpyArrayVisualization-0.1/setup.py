import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="NumpyArrayVisualization",
    version="0.1",
    author="JohnsonSii",
    author_email="",
    description="https://www.bilibili.com/video/BV1WX4y1h775/",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JohnsonSii/NumpyArrayVisualization",
    packages=setuptools.find_packages(),
    install_requires=['Pillow>=5.1.0', 'numpy==1.14.4', 'PyQt5==5.15.4'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)