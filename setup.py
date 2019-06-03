from setuptools import setup


dependencies = [
    'python_decouple==3.1'
]

dev_dependencies = [
    'coverage==4.5',
    'sphinx==1.8',
    'flake8==3.6',
    'isort==4.3',
]

setup(
    name='sawmill',
    version='0.0.1',
    description='A custom Python logger with colour formatter for working with MirrorWeb projects',
    packages=[],
    url='https://github.com/mirrorweb/sawmill',
    author='Lee Booth, MirrorWeb Ltd.',
    author_email='lee.booth@mirrorweb.com',
    install_requires=dependencies,
    extra_require={'dev': dev_dependencies},
    dependency_links=[
        'git+ssh://git@github.com/mirrorweb/dora.git@refactor/improved-tooling#egg=dora-3.0.0',
    ],
)