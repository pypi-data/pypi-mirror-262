import setuptools

setuptools.setup(
    name='touchv2',
    version='1.1',
    install_requires=open('requirements.txt').read().splitlines(),
    packages=setuptools.find_packages()
)
