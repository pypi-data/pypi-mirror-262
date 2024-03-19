"""
py setup.py sdist
twine upload --skip-existing --repository-url https://europe-west1-python.pkg.dev/expressmoney/default/ dist/expressmoney-service-1.4.17.tar.gz
"""
import setuptools

setuptools.setup(
    name='expressmoney-service',
    packages=setuptools.find_packages(),
    version='1.4.17',
    description='Remote services',
    author='Development team',
    author_email='dev@expressmoney.com',
    install_requires=('django-phonenumber-field[phonenumberslite]',),
    python_requires='>=3.7',
)
