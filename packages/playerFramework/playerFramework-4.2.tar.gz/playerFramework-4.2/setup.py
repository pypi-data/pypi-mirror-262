import setuptools

reqs = [
    'pydub'
]
version = '4.2'

setuptools.setup(
    name='playerFramework',
    version=version,
    description="A simple way to play audio in Python.",
    long_description="A simple way to play audio in Python.",
    packages=setuptools.find_packages(),
    install_requires=reqs
)
