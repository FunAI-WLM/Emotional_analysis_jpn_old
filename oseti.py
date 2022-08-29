# -*- coding: utf-8 -*-
import json
import os

import MeCab
from bunkai import Bunkai

NEGATION = ('ない', 'ず', 'ぬ')
PARELLEL_PARTICLES = ('か', 'と', 'に', 'も', 'や', 'とか', 'だの', 'なり', 'やら')
DICT_DIR = os.path.join(os.path.dirname(__file__), 'dic')


class Analyzer(object):

    def __init__(self, mecab_args='', word_dict={}, wago_dict={}):
        self.word_dict = json.load(open(os.path.join(DICT_DIR, 'pn_noun.json')))
        if word_dict:
            self.word_dict.update(word_dict)
        self.wago_dict = json.load(open(os.path.join(DICT_DIR, 'pn_wago.json')))
        if wago_dict:
            self.wago_dict.update(wago_dict)
        self.tagger = MeCab.Tagger(mecab_args)
        self.tagger.parse('')  # for avoiding bug
        self.bunkai = Bunkai()

    def _lookup_wago(self, lemma, lemmas):
        # print("00000000000000000000000000000000000  self.wago_dict:  {}  ".format(str(self.wago_dict)))
        if lemma in self.wago_dict:
            print("111111111111111111111111111111111  lemma:  {}  ".format(str(lemma)))
            return lemma
        for i in range(10, 0, -1):
            wago = ' '.join(lemmas[-i:]) + ' ' + lemma
            print("00000000000000000000000000000000000  wago:  {}  ".format(str(wago)))
            # print("00000000000000000000000000000000000  self.wago_dict:  {}  ".format(str(self.wago_dict)))
            if wago in self.wago_dict:
                return wago
        return ''

    def _has_arujanai(self, substring):
        return 'あるじゃない' in substring

    def _calc_sentiment_polarity(self, sentence):
        polarities = []
        lemmas = []
        n_parallel = 0
        substr_count = 0
        node = self.tagger.parseToNode(sentence)
        while node:
            if 'BOS/EOS' not in node.feature:
                # print("00000000000000000000000000000000000  node.feature  {}  ".format(str(node.feature)))
                surface = node.surface
                # print("00000000000000000000000000000000000  node.surface  {}  ".format(str(node.surface)))
                substr_count += len(surface)
                feature = node.feature.split(',')
                lemma = feature[6] if feature[6] != '*' else node.surface
                # print("00000000000000000000000000000000000  lemma  {}  ".format(str(lemma)))
                # print("00000000000000000000000000000000000  self.word_dict  {}  ".format(str(self.word_dict)))
                # print("00000000000000000000000000000000000  PARELLEL_PARTICLES  {}  ".format(str(PARELLEL_PARTICLES)))
                wago = ''
                if lemma in self.word_dict:
                    polarity = 1 if self.word_dict[lemma] == 'p' else -1
                    n_parallel += node.next.surface in PARELLEL_PARTICLES
                    # print("00000000000000000000000000000000000  n_parallel  {}  ".format(str(n_parallel)))
                else:
                    print("00000000000000000000000000000000000  lemma:  {}  ".format(str(lemma)))
                    print("00000000000000000000000000000000000  lemmas:  {}  ".format(str(lemmas)))
                    wago = self._lookup_wago(lemma, lemmas)
                    # print("00000000000000000000000000000000000  wago:  {}  ".format(str(wago)))
                    if wago:
                        polarity = 1 if self.wago_dict[wago].startswith('ポジ') else -1
                    else:
                        polarity = None
                
                # print("00000000000000000000000000000000000  polarity  {}  ".format(str(polarity)))

                # print("00000000000000000000000000000000000  polarities  {}  ".format(str(polarities)))
                # print("00000000000000000000000000000000000  surface  {}  ".format(str(surface)))
                # print("00000000000000000000000000000000000  NEGATION  {}  ".format(str(NEGATION)))
                # print("00000000000000000000000000000000000  sentence[:substr_count]  {}  ".format(str(sentence[:substr_count])))

                if polarity:
                    # print("00000000000000000000000000000000000  polarity  {}  ".format(str(polarity)))
                    polarities.append([wago or lemma, polarity])
                elif polarities and surface in NEGATION and not self._has_arujanai(sentence[:substr_count]):
                    # print("00000000000000000000000000000000000  polarity  {}  ".format(str(polarity)))
                    polarities[-1][1] *= -1
                    if polarities[-1][0].endswith('-NEGATION'):
                        polarities[-1][0] = polarities[-1][0][:-9]
                    else:
                        polarities[-1][0] += '-NEGATION'
                    # parallel negation
                    if n_parallel and len(polarities) > 1:
                        n_parallel = len(polarities) if len(polarities) > n_parallel else n_parallel + 1
                        n_parallel = n_parallel + 1 if len(polarities) == n_parallel else n_parallel
                        for i in range(2, n_parallel):
                            polarities[-i][1] *= -1
                            if polarities[-i][0].endswith('-NEGATION'):
                                polarities[-i][0] = polarities[-i][0][:-9]
                            else:
                                polarities[-i][0] += '-NEGATION'
                        n_parallel = 0
                lemmas.append(lemma)
            node = node.next
        return polarities

    def count_polarity(self, text):
        """Calculate sentiment polarity counts per sentence
        Arg:
            text (str)
        Return:
            counts (list) : positive and negative counts per sentence
        """
        counts = []
        for sentence in self.bunkai(text):
            count = {'positive': 0, 'negative': 0}
            polarities = self._calc_sentiment_polarity(sentence)
            for polarity in polarities:
                if polarity[1] == 1:
                    count['positive'] += 1
                elif polarity[1] == -1:
                    count['negative'] += 1
            counts.append(count)
        return counts

    def analyze(self, text):
        """Calculate sentiment polarity scores per sentence
        Arg:
            text (str)
        Return:
            scores (list) : scores per sentence
        """
        scores = []

        # aaaa = self.bunkai(text)
        # print("00000000000000000000000000000000000   aaaa  {}  ".format(str(aaaa)))

        for sentence in self.bunkai(text):
            # print("00000000000000000000000000000000000  sentence  {}  ".format(str(sentence)))
            polarities = self._calc_sentiment_polarity(sentence)
            # print("11111111111111111111111111111111111  {}  ".format(str(polarities)))
            if polarities:
                scores.append(sum(p[1] for p in polarities) / len(polarities))
            else:
                scores.append(0)
        return scores

    def analyze_detail(self, text):
        """Calculate sentiment polarity scores per sentence
        Arg:
            text (str)
        Return:
            results (list) : analysis results
        """
        results = []
        for sentence in self.bunkai(text):
            polarities = self._calc_sentiment_polarity(sentence)
            if polarities:
                result = {
                    'positive': [p[0] for p in polarities if p[1] == 1],
                    'negative': [p[0] for p in polarities if p[1] == -1],
                    'score': sum(p[1] for p in polarities) / len(polarities),
                }
            else:
                result = {'positive': [], 'negative': [], 'score': 0.0}
            results.append(result)
        return results
