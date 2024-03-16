from setuptools import setup, find_packages

setup(
    name='django_auditable_model',
    version='0.1.4',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A Django app providing reusable abstract models.',
    long_description=open('django_auditable_model/README.md').read(),
    long_description_content_type='text/markdown',
    author='Shubham Sharma',
    author_email='sharma.shubham6522@gmail.com',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)