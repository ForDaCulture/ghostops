from setuptools import setup, find_packages

setup(
    name="ghostrecon",
    version="1.0.0",
    description="GhostOps Recon – Automated OSINT and Attack Surface Mapping Tool",
    author="YourName",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "python-whois",
        "dnspython",
        "aiohttp",
        "requests",
        "python-dotenv",
        "streamlit"
    ],
    entry_points={
        'console_scripts': [
            'ghostrecon=ghostrecon.cli:main'
        ]
    },
    include_package_data=True,
)
