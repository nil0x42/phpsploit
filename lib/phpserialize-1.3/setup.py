import os
from setuptools import setup

def get_docs():
    result = []
    in_docs = False
    f = open(os.path.join(os.path.dirname(__file__), 'phpserialize.py'))
    try:
        for line in f:
            if in_docs:
                if line.lstrip().startswith(':copyright:'):
                    break
                result.append(line[4:].rstrip())
            elif line.strip() == 'r"""':
                in_docs = True
    finally:
        f.close()
    return '\n'.join(result)

setup(
    name='phpserialize',
    author='Armin Ronacher',
    author_email='armin.ronacher@active-4.com',
    version='1.3',
    url='http://dev.pocoo.org/hg/phpserialize-main',
    py_modules=['phpserialize'],
    description='a port of the serialize and unserialize '
                'functions of php to python.',
    long_description=get_docs(),
    zip_safe=False,
    test_suite='tests',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: PHP',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ]
)
