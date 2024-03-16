from setuptools import setup,find_packages 
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="passlord",
    version="1.0.1",
    author="navnee1h",
    description="Passlord is a smart tool that creates lists of possible passwords using clever methods.",
    url='https://github.com/navnee1h/passlord',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'passlord.patterns':[ 'rules.txt' ],
    },
    classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: MIT License",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python :: 3",
    "Topic :: Security",
    "Topic :: Utilities",
    ],

    install_requires=[],
    entry_points={
        'console_scripts': [
            'passlord = passlord.passlord:run_main_function'
        ]
    }
)
