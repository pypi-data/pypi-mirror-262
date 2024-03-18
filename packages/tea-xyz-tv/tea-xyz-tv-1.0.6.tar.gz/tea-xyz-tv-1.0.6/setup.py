from setuptools import setup

setup(
    author='TV',
    author_email='tuanvofg@gmail.com',
    name='tea-xyz-tv',
    version='1.0.6',
    description='A simple package testnet for https://app.tea.xyz/. Example tea-xyz-tv - https://github.com/tuanvofg/tea-xyz',
    url='https://github.com/tuanvofg/tea-xyz',
    project_urls={
        'Homepage': 'https://github.com/tuanvofg/tea-xyz',
        'Source': 'https://github.com/tuanvofg/tea-xyz',
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
        'tea-xyz',
    ],
)
