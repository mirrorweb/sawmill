from setuptools import setup


dependencies = [
    'python_decouple~=3.1'
]

dev_dependencies = [
    'coverage==4.5',
    'sphinx==1.8',
    'flake8==3.6',
    'isort==4.3.21',
]

setup(
    name='sawmill',
    version='0.0.3',
    description='A custom Python logger with colour formatter for working with MirrorWeb projects',
    packages=['sawmill'],
    url='https://github.com/mirrorweb/sawmill',
    author='Lee Booth, MirrorWeb Ltd.',
    author_email='lee.booth@mirrorweb.com',
    install_requires=dependencies,
    extra_require={'dev': dev_dependencies},
    dependency_links=[],
)
