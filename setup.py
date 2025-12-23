from setuptools import setup, find_packages

setup(
    name="phantom-cli",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'phantom': ['data/*.json'],
    },
    install_requires=[
        "requests",
        "beautifulsoup4",
        "colorama",
    ],
    entry_points={
        "console_scripts": [
            "phantom=phantom.main:entry_point",
        ],
    },
    author="Ghost",
    description="Cyberpunk Security Toolkit",
)
