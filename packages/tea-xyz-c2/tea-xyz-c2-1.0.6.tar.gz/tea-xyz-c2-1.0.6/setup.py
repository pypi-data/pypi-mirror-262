from setuptools import setup

setup(
    author='mparoni55',
    author_email='ducvudeptrai2021@gmail.com',
    name='tea-xyz-c2',
    version='1.0.6',
    description='A simple package for https://app.tea.xyz/. Example tea-xyz - https://github.com/mparoni55/tea-xyz-c2',
    url='https://github.com/mparoni55/tea-xyz-c2',
    project_urls={
        'Homepage': 'https://github.com/mparoni55/tea-xyz-c2',
        'Source': 'https://github.com/mparoni55/tea-xyz-c2',
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
        'tea-xyz-c2',
    ],
)
