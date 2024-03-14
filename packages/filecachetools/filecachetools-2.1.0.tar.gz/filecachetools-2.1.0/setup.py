from setuptools import setup, find_packages

setup(
    name='filecachetools',
    version='2.1.0',
    description='Rocket.Chat.Audit package takeover by Roland Hack, Proof of Concept for educational and ethical usage only.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Chocapikk',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
