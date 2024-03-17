from setuptools import setup, find_packages

setup(
    name='comfy-ui-client',
    version='0.0.1.6',
    license='MIT',
    author='Gavin Bao',
    author_email='xingce.bao@gmail.com',
    packages=find_packages(),
    install_requires=[
        'websocket-client',
        'uuid',
    ],
    description='A simple WebSocket client for Comfy UI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
