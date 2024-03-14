from setuptools import setup, find_packages

setup(
    name='shscan',
    version='0.1',
    packages=find_packages(),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'shscan = shscan.shscan:main'
        ]
    },
    author='boyinf',
    author_email='gustavoboy1702@gmail.com',
    description='A package for checking the security headers of a URL.',
    long_description="The shscan tool was developed with the purpose of assisting in checking the security headers enabled on specific or internal websites. Created to simplify this process, the tool is notable for its simplicity and efficiency, representing the result in an intuitive way.",
    url='https://github.com/boyinf/shscan',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

)
