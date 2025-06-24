from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='terraform-versions-bumper',
    version='0.0.4',
    description='CLI tool to update terraform and provider versions in tf files',
    scripts=['src/terraform-versions-bumper'],
    install_requires=['httpx==0.28.1', 'pygohcl==1.2.5'],
    python_requires='>=3.9'
)
