from setuptools import setup, find_packages
setup(
    name='yannylib',
    version='0.1.3',
    author='Quinn Colello',
    author_email='qcolello@berkeley.edu',
    description='Some matplotlib functions wrapped',
    packages=find_packages(where="src"),
    py_modules=["src/yannylib"],
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ],
    install_requires=["matplotlib"],
    python_requires='>=3.6',
)
