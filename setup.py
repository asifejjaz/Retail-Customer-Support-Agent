"""
Setup configuration for Retail Customer Support Agent package
"""

from setuptools import setup, find_packages

with open("docs/README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="retail-customer-support-agent",
    version="1.0.0",
    author="Asif Ejaz",
    author_email="asifejaz.me@gmail.com",
    description="AI-powered customer support chatbot for jewelry retail",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asifejjaz/Retail-Customer-Support-Agent",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
    install_requires=[
        "streamlit>=1.28.0",
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
        "beautifulsoup4>=4.12.0",
        "requests>=2.31.0",
        "python-docx>=0.8.11",
        "matplotlib>=3.7.0",
        "pandas>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "retail-agent=src.chatbot.app:main",
        ],
    },
)
