from setuptools import setup

VERSION = '0.0.1'
DESCRIPTION = 'USPS Address API 3.0 Python wrapper'

setup(
    name='pyuspsaddress',
    version=VERSION,
    description=DESCRIPTION,
    url='https://github.com/achillis2/pyuspsaddress',
    author='Ding Li',
    author_email='dingli@gmail.com',
    license='MIT',
    packages=['pyuspsaddress'],
    install_requires=['requests',
                      'djangorestframework',
                      'pytest'
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
