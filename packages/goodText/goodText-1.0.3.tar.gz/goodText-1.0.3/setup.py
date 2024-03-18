from setuptools import setup

setup(
    name = 'goodText',
    version = '1.0.3',
    author = 'Jonatas Miguel',
    author_email = 'jonatas.miguelss@gmail.com',
    packages = ['goodText'],
    description = 'Programa simples de mudança de cor de texto',
    keywords = 'Mudar cor texto',
    package_data={'goodText': ['libs/*']},
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Scientific/Engineering :: Physics'
    ]

)
