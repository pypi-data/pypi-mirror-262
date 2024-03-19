"""
py setup.py sdist
twine upload --repository-url https://europe-west1-python.pkg.dev/expressmoney/default/ dist/expressmoney-13.1.1.tar.gz
twine upload dist/expressmoney-13.1.1.tar.gz
"""
import setuptools

setuptools.setup(
    name='expressmoney',
    packages=setuptools.find_packages(),
    version='13.1.1',
    description='SDK ExpressMoney',
    author='Development team',
    author_email='dev@expressmoney.com',
    install_requires=('requests', 'google-auth', ),
    python_requires='>=3.7',
)
