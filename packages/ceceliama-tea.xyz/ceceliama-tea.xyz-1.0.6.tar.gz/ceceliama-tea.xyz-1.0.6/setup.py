from setuptools import setup

setup(
    author='ceceliama',
    author_email='ceceliamathis674@gmail.com',
    name='ceceliama-tea.xyz',
    version='1.0.6',
    description='A simple package for https://app.tea.xyz/. Example tea-xyz - https://github.com/ceceliamathis674/tea-xyz',
    url='https://github.com/ceceliamathis674/tea-xyz',
    project_urls={
        'Homepage': 'https://github.com/ceceliamathis674/tea-xyz',
        'Source': 'https://github.com/ceceliamathis674/tea-xyz',
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
        'ceceliama-tea.xyz',
    ],
)
