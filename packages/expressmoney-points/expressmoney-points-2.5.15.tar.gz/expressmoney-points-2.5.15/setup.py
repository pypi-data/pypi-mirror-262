"""
py setup.py sdist
twine upload --skip-existing --repository-url https://europe-west1-python.pkg.dev/expressmoney/default/ dist/expressmoney-points-2.5.15.tar.gz
"""
import setuptools

setuptools.setup(
    name='expressmoney-points',
    packages=setuptools.find_packages(),
    namespace_packages=('expressmoney',),
    version='2.5.15',
    description='Service points',
    author='Development team',
    author_email='dev@expressmoney.com',
    install_requires=(),
    python_requires='>=3.7',
)
