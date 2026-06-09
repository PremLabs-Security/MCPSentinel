from setuptools import setup, find_packages

setup(
    name="mcpsentinel",
    version="0.1.0",
    author="Pramod Jogdand",
    author_email="pramod.jogdand@premlabs.security",
    description="A tool to detect exposed/unauthenticated MCP endpoints and Ollama servers.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PremLabs-Security/MCPSentinel",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
        "click>=8.0.0",
        "rich>=12.0.0",
        "pydantic>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "mcpsentinel=mcpsentinel.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
    ],
    python_requires=">=3.10",
)
