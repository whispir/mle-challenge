import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

print(setuptools.find_packages())

setuptools.setup(
    name="windml",  # Replace with your own username
    version="0.0.1",
    author="Whispir AI",
    author_email="aiml@whispir.com",
    description="Whispir AI Wind Active Power Estimator",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/ruodingt/mle-challenge",
    packages=['windml'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: pair_id_scope/A",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['uvicorn==0.15.0',
                      'fastapi==0.70.0',
                      'uvloop==0.16.0',
                      'httptools==0.3.0',
                      'pytorch-lightning==1.5.0',
                      'jsonargparse',
                      'pandas==1.3.4']
)
