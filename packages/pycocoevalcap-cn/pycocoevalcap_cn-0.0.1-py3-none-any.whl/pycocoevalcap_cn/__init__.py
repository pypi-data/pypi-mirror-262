"""
refer to https://github.com/wangleihitcs/CaptionMetrics/
"""

from .bleu.bleu import Bleu
from .cider.cider import Cider
import json


def load_gts_res(gts_file, res_file):
    """
    gts_file example:
    {"ff7f0e868583e800": ["一个 老式 蒸汽 火车 行驶 在 铁路 上", "一个 火车 行驶 在 铁路 上"], 
    "0f06c2420280ffff": ["街边 有 几个 临时 搭建 的 公共 卫生间 。"]}
    res_file example:
    {"ff7f0e868583e800": ["一列 喷着 蒸汽 的 火车 在 火车 轨道 上 行驶"], 
    "0f06c2420280ffff": ["临时 搭建 的 公共 卫生间 。"], 
    """
    with open(gts_file, 'r') as file:
        gts = json.load(file)
    with open(res_file, 'r') as file:
        res = json.load(file)
    return gts, res

def bleu(gts, res):
    scorer = Bleu(n=4)
    # scorer += (hypo[0], ref1)   # hypo[0] = 'word1 word2 word3 ...'
    #                                 # ref = ['word1 word2 word3 ...', 'word1 word2 word3 ...']
    score, scores = scorer.compute_score(gts, res)

    # print('belu = %s' % score)
    return score, scores

def cider(gts, res):
    scorer = Cider()
    # scorer += (hypo[0], ref1)
    (score, scores) = scorer.compute_score(gts, res)
    # print('cider = %s' % score)
    return score, scores

def evaluate(gts, res):
    belu_score, belu_scores = bleu(gts, res)
    cider_score, cider_scores = cider(gts, res)
    return belu_score, belu_scores, cider_score, cider_scores

def evaluate_from_file(gts_file, res_file):
    gts, res = load_gts_res(gts_file, res_file)
    return evaluate(gts, res)


if __name__ == '__main__':
    gts = {"ff7f0e868583e800": ["一个 老式 蒸汽 火车 行驶 在 铁路 上", "一个 火车 行驶 在 铁路 上"], 
    "0f06c2420280ffff": ["街边 有 几个 临时 搭建 的 公共 卫生间 。"]}
    res = {"ff7f0e868583e800": ["一列 喷着 蒸汽 的 火车 在 火车 轨道 上 行驶"], 
    "0f06c2420280ffff": ["临时 搭建 的 公共 卫生间 。"]}
    print(evaluate(gts, res))
