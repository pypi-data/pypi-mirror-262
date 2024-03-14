from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('LICENSE', 'r', encoding='utf-8') as f:
    license_text = f.read()

setup(
    name='transutil',
    version='1.0.1',
    description="Introducing Transutil, the ultimate productivity utility tool designed to streamline your workflow. Packed with an array of powerful features, Transutil offers a seamless experience like no other. Enjoy a secure and efficient workflow with our built-in chiper, providing a robust alternative to JWT.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Pawan kumar',
    author_email='embrakeproject@gmail.com',
    url='https://github.com/embrake/aquilify/',
    packages=find_packages(),
    keywords=['tool-box', 'Python utils', 'user-friendly', 'high-level', 'ASGI', 'backend'],
    license='BSD-3-Clause',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)