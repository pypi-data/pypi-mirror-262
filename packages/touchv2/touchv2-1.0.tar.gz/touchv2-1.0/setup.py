import setuptools

setuptools.setup(
    name='touchv2',
    version='1.0',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
