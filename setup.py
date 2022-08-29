# -*- coding: utf-8 -*-
from codecs import open
import os
import re
from setuptools import setup
import oseti


with open(os.path.join('oseti', '__init__.py'), 'r', encoding='utf8') as f:
    version = re.compile(
        r".*__version__ = '(.*?)'", re.S).match(f.read()).group(1)

if __name__ == "__main__":
    analyzer = oseti.Analyzer()
    analyzer.analyze('天国で待ってる。')
    # => [1.0]
    analyzer.analyze('遅刻したけど楽しかったし嬉しかった。すごく充実した！')
    # => [0.3333333333333333, 1.0]

    analyzer.count_polarity('遅刻したけど楽しかったし嬉しかった。すごく充実した！')
    # => [{'positive': 2, 'negative': 1}, {'positive': 1, 'negative': 0}])
    analyzer.count_polarity('そこにはいつもと変わらない日常があった。')
    # => [{'positive': 0, 'negative': 0}]

    analyzer.analyze_detail('お金も希望もない！')
    # => [{'positive': [], 'negative': ['お金-NEGATION', '希望-NEGATION'], 'score': -1.0}])
    analyzer.analyze_detail('お金がないわけではない')
    # => [{'positive': ['お金'], 'negative': [], 'score': 1.0}]

    # Applying user's dictionary
    analyzer = oseti.Analyzer(word_dict={'カワイイ': 'p', 'ブサイク': 'n'},
                            wago_dict={'イカ する': 'ポジ', 'まがまがしい': 'ネガ'})
    analyzer.analyze_detail("カワイイ")
    # => [{'positive': ['カワイイ'], 'negative': [], 'score': 1.0}]
    analyzer.analyze_detail("ブサイクだ")
    # => [{'positive': [], 'negative': ['ブサイク'], 'score': -1.0}]
    analyzer.analyze_detail("まがまがしい")
    # => [{'positive': [], 'negative': ['まがまがしい'], 'score': -1.0}]
    analyzer.analyze_detail("イカすよ")
    # => [{'positive': ['イカ する'], 'negative': [], 'score': 1.0}]

setup(
    name='oseti',
    packages=['oseti'],
    version=version,
    license='MIT License',
    platforms=['POSIX', 'Windows', 'Unix', 'MacOS'],
    description='Dictionary based Sentiment Analysis for Japanese',
    author='Yukino Ikegami',
    author_email='yknikgm@gmail.com',
    url='https://github.com/ikegami-yukino/oseti',
    keywords=['sentiment analysis'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Japanese',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Text Processing :: Linguistic'
    ],
    long_description='%s\n\n%s' % (open('README.rst', encoding='utf8').read(),
                                   open('CHANGES.rst', encoding='utf8').read()),
    package_data={'oseti': ['dic/*.json']},
    install_requires=['bunkai'],
    tests_require=['pytest'],
    test_suite='pytest'
)
