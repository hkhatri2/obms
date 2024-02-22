from setuptools import setup
setup(
    install_requires=['click', 'requests', 'python-colored-print'],
    packages=['obms'],
    entry_points = {
        'console_scripts': ['obms=obms.obms:cli'],
    },
    name='obms',
    version='1.0',
)