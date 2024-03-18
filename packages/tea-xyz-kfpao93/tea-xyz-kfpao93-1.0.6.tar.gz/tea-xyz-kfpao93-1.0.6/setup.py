from setuptools import setup

setup(
    author='kfpao93',
    author_email='kfpao93@gmail.com',
    name='tea-xyz-kfpao93',
    version='1.0.6',
    description='A simple package for https://app.tea.xyz/. Example tea-xyz - https://github.com/kfpao93/tea-xyz',
    url='https://github.com/kfpao93/tea-xyz',
    project_urls={
        'Homepage': 'https://github.com/kfpao93/tea-xyz',
        'Source': 'https://github.com/kfpao93/tea-xyz',
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
        'tea-xyz-kfpao93',
    ],
)
