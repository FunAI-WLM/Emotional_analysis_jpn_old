import oseti

if __name__ == '__main__':
    analyzer = oseti.Analyzer()
    a1 = analyzer.analyze('天国で待ってる。')
    
    # print("22222222222222222222222222222222222  {}  ".format(str(a1)))
    # => [1.0]


    # analyzer.analyze('遅刻したけど楽しかったし嬉しかった。すごく充実した！')
    # # => [0.3333333333333333, 1.0]

    # analyzer.count_polarity('遅刻したけど楽しかったし嬉しかった。すごく充実した！')
    # # => [{'positive': 2, 'negative': 1}, {'positive': 1, 'negative': 0}])
    # analyzer.count_polarity('そこにはいつもと変わらない日常があった。')
    # # => [{'positive': 0, 'negative': 0}]

    # analyzer.analyze_detail('お金も希望もない！')
    # # => [{'positive': [], 'negative': ['お金-NEGATION', '希望-NEGATION'], 'score': -1.0}])
    # analyzer.analyze_detail('お金がないわけではない')
    # # => [{'positive': ['お金'], 'negative': [], 'score': 1.0}]

    # # Applying user's dictionary
    # analyzer = oseti.Analyzer(word_dict={'カワイイ': 'p', 'ブサイク': 'n'},
    #                         wago_dict={'イカ する': 'ポジ', 'まがまがしい': 'ネガ'})
    # analyzer.analyze_detail("カワイイ")
    # # => [{'positive': ['カワイイ'], 'negative': [], 'score': 1.0}]
    # analyzer.analyze_detail("ブサイクだ")
    # # => [{'positive': [], 'negative': ['ブサイク'], 'score': -1.0}]
    # analyzer.analyze_detail("まがまがしい")
    # # => [{'positive': [], 'negative': ['まがまがしい'], 'score': -1.0}]
    # analyzer.analyze_detail("イカすよ")
    # # => [{'positive': ['イカ する'], 'negative': [], 'score': 1.0}]
