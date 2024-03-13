from setuptools import setup, find_packages

setup(
    name='optimize_device_analysis',
    version='0.1.2',
    author='Akhilesh Keerthi',
    author_email='akhileshkeerthi@gmail.com',
    maintainer='Akhilesh Keerthi, Sai Kumar Aili',
    maintainer_email='akeerthi@gmu.edu, saili@gmu.edu',
    packages=find_packages(),
    install_requires=[
        'psutil',
        'matplotlib',
        'requests',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'optimize_device_analysis = optimize_device_analysis.__main__:main',
        ],
    },
)