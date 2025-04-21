import os
from setuptools import setup, find_packages

# Read the contents of README file
with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mcp-panda-analyzer",
    version="0.1.0",
    author="Paul Nilsson",
    author_email="Paul.Nilsson@cern.ch",
    description="MCP-based PanDA job log analyzer using LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/palnilsson/mcp-panda-analyzer",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn>=0.22.0",
        "requests>=2.28.0",
        "pydantic>=2.0.0",
        "typing-extensions>=4.5.0",
    ],
    extras_require={
        "claude": ["anthropic>=0.5.0"],
        "llama": ["llama-cpp-python>=0.1.77"],
        "openai": ["openai>=1.0.0"],
        "all": [
            "anthropic>=0.5.0",
            "llama-cpp-python>=0.1.77",
            "openai>=1.0.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mcp-server=mcp_panda_analyzer.server.api:main",
            "mcp-agent=mcp_panda_analyzer.client.agent:main",
        ],
    },
    include_package_data=True,
    keywords="mcp, panda, llm, log analysis, grid computing",
    project_urls={
        "Bug Reports": "https://github.com/palnilsson/mcp-panda-analyzer/issues",
        "Source": "https://github.com/palnilsson/mcp-panda-analyzer",
    },
)