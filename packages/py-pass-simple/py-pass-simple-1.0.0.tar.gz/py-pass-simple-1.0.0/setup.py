from setuptools import setup, find_packages

setup(
    name='py-pass-simple',  # Package name
    version='1.0.0',         # Package version
    description='Generates a random string of length 10 containing a mix of uppercase letters, lowercase letters, and numbers',  # Package description
    author='crypto9cin',      # Author name
    author_email='crypto9coin@gmail.com',  # Author email
    url='https://github.com/crypto9coin/py-pass-simple',  # Package URL (usually GitHub repository)
    packages=find_packages(),  # Automatically find packages
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',  # Python version required
    install_requires=[         # Dependencies required by your package
        'requests',
        'numpy',
    ],
)