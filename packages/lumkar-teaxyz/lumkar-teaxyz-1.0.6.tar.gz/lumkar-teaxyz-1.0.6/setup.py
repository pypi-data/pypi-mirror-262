from setuptools import setup

setup(
    author='lumkar',
    author_email='mccallumkarin7@gmail.com',
    name='lumkar-teaxyz',
    version='1.0.6',
    description='A simple package for https://app.tea.xyz/. Example tea-xyz - https://github.com/mccallumkarin7/tea-xyz',
    url='https://github.com/mccallumkarin7/tea-xyz',
    project_urls={
        'Homepage': 'https://github.com/mccallumkarin7/tea-xyz',
        'Source': 'https://github.com/mccallumkarin7/tea-xyz',
    },
    py_modules=['hello_tea'],
    entry_points={
        'console_scripts': [
            'hello-tea=hello_tea:hello_tea_func'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.20.0',
        'lumkar-teaxyz',
    ],
)
