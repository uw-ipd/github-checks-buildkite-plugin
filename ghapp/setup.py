from setuptools import setup, find_packages

setup(
    name="ghapp",
    author="Alex Ford",
    author_email='fordas@uw.edu',
    license="MIT license",
    description="Sandbox for github app integrationn",
    url='https://github.com/asford/gh_app_sandbox',

    version='0.0.2',

    packages=find_packages(),
    entry_points={
        'console_scripts' : [
        'git-credential-github-app-auth='
            'ghapp.cli:credential',
        'ghapp='
            'ghapp.cli:main',
        ]
    },
    python_requires='>=3.6',
    install_requires=[
        open("requirements.txt").read()
    ],

    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-aiohttp"],
)
