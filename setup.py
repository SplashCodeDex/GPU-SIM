from setuptools import setup, find_packages

setup(
    name="gpu-sim",
    version="1.0.0",
    description="Virtual GPU Simulator for Windows",
    author="CodeDeX",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "PyQt5>=5.15.0",
        "pywin32>=305",
        "WMI>=1.5.1",
        "pyyaml>=6.0",
        "jsonschema>=4.0",
    ],
    entry_points={
        "console_scripts": [
            "gpu-sim=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Win32 (MS Windows)",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.8",
        "Topic :: System :: Hardware",
    ],
)
