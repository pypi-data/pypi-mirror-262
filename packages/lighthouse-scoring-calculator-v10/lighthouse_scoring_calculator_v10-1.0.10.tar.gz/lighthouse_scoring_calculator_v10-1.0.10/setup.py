from setuptools import setup,find_packages

setup(
    name='lighthouse_scoring_calculator_v10',
    version='1.0.10',
    author="Fabio Manz",
    author_email="fabio.manz@t-online.de",
    description='A package for calculating Lighthouse scores.',
    long_description='A Python package for calculating Lighthouse scores based on performance metrics.',
    long_description_content_type='text/markdown',
    url='https://github.com/fabiomanz/lighthouse-scoring-calculator',
    packages=find_packages(),
    install_requires=['requests'],
    license='MIT',  # 라이선스 정보 추가
    classifiers=[
        'License :: OSI Approved :: MIT License',  # 라이선스 분류 추가
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
# setup(
#     name='lighthouse_scoring_calculator_v10',
#     version='1.0.10',
#     author="Fabio Manz",
#     author_email="fabio.manz@t-online.de",
#     description='A package for calculating Lighthouse scores.',
#     long_description='A Python package for calculating Lighthouse scores based on performance metrics.',
#     long_description_content_type='text/markdown',
#     url='https://github.com/fabiomanz/lighthouse-scoring-calculator',
#     packages=['lighthouse_scoring_calculator_v10'],
#     install_requires=['requests'],
#     classifiers=[
#         'License :: OSI Approved :: MIT License',
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: 3.8',
#         'Programming Language :: Python :: 3.9',
#         'Development Status :: 5 - Production/Stable',
#         'Intended Audience :: Developers',
#         'Topic :: Software Development :: Libraries :: Python Modules',
#     ],
# )
#
# from setuptools import setup, find_packages

