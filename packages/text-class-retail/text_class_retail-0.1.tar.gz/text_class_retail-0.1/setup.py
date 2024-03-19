from setuptools import setup, find_packages

setup(
    name='text_class_retail',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
        'joblib',
        'os'
    ],
    package_data={'text_class_retail': ['*.joblib']},
    include_package_data=True,
)
