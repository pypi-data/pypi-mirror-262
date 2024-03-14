from setuptools import setup, find_packages

setup(
    name="secret_lib",
    version="0.1.1",
    author="vladimir gorea",
    author_email="vladimir@smileservices.dev",
    description="A wrapper for different configuration/secret sources.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/smileservices/secret_lib",
    packages=find_packages(),
    install_requires=[
        "hvac",
        "python-dotenv"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
