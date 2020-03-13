
'''
StuID: 3119305630
Mail: zhusiyuan@stu.xjtu.edu.cn
Date: 2020/3/13

一副扑克有52张牌，每张牌由一个花色和一个数字构成。
花色为以下四者之一：
- 方片 D
- 黑桃 S
- 红桃 H
- 梅花 C

数字为以下13者之一，且大小顺序如下：
2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A

花色是大小无序的，但数字有序，2最小，A最大。
一手牌有5张。根据花色和数字的不同，其大小按照以下规则决定。

满足下面规则的手牌会大于满足上面规则的手牌。
同花顺＞铁支＞葫芦＞同花＞顺子＞三条＞两对＞对子＞散牌

散牌：
不符合其他任何规则的五张牌。 比较最大一张牌的大小，如果相同，比较第二大的牌的牌点数，如果五张牌的牌点数都相同，则为平局。
对子：
有两张同样大小的牌片。 比较两张大小一样的牌的牌点数，如果相同，依次比较剩余的三张牌大小。若大小都相同，则为平局。
两对：
有两个对子牌。 比较大对子的大小，若相同，比较小对子的大小，若还相同，比较单张牌的大小，若还相同，则为平局。
三条：
有三张同样大小的牌片。 比较三张大小一样的牌的牌点数大小。
顺子：
五张相连的牌。 比较最大的牌点数。若大小都相同，则为平局。
同花：
五张牌的花色相同。 按照散排规则比较大小。
葫芦：
三条+对子。 比较三张大小一样的牌的牌点数。
铁支：
有四张同样大小的牌片。 比较四张大小一样的牌的牌点数。
同花顺：
同一种花色的顺子。 比较最大的牌的牌的大小。若大小都相同，则为平局。

你的工作是为两手牌判断大小。
例如：
输入: Black: 2H 3D 5S 9C KD White: 2C 3H 4S 8C AH 输出: White wins - high card: Ace
输入: Black: 2H 4S 4C 2D 4H White: 2S 8S AS QS 3S 输出: Black wins - full house
输入: Black: 2H 3D 5S 9C KD White: 2C 3H 4S 8C KH 输出: Black wins - high card: 9
输入: Black: 2H 3D 5S 9C KD White: 2D 3H 5C 9S KH 输出: Tie
'''

def hand_rank(hand):
    "Return a value indicating the ranking of a hand."
    ranks = card_ranks(hand) 
    if straight(ranks) and flush(hand): 
        # 同花顺（顺子+同花）
        return (9, max(ranks))
    elif kind(4, ranks):
        # 铁支（有四张同样大小的牌片）
        return (8, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        # 葫芦（三条+对子）
        return (7, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        # 同花（五张牌的花色相同）
        return (6, ranks)
    elif straight(ranks):
        # 顺子（五张相连的牌）
        return (5, max(ranks))
    elif kind(3, ranks):
        # 三条（有三张同样大小的牌片）
        return (4, kind(3, ranks), ranks)
    elif two_pair(ranks):
        # 两对（有两个对子牌）
        return (3, two_pair(ranks), ranks)
    elif kind(2, ranks):
        # 对子（有两张同样大小的牌片）
        return (2, kind(2, ranks), ranks)
    else:
        # 散牌（不符合其他任何规则的五张牌）
        return (1, ranks)


def card_ranks(hand):
    # 排序
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand] # -- 起占位作用，使得2的index仍然是2
    ranks.sort(reverse = True)
    return ranks


def flush(hand):
    # 同花
    suits = [s for r,s in hand]
    return len(set(suits)) == 1


def straight(ranks):
    # 顺子
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5


def kind(n, ranks):
    # 有n张同样大小的牌片
    for r in ranks:
        if ranks.count(r) == n: return r
    return None


def two_pair(ranks):
    # 对子
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))
    if pair and lowpair != pair:
        return (pair, lowpair)
    else:
        return None


def compare(black, white):
    result_black = hand_rank(black)
    result_white = hand_rank(white)

    if result_black > result_white:
        return 'Black wins'
    if result_black < result_white:
        return 'White wins'
    if result_black == result_white:
        return 'Tie'

    return 'ERROR'


def test(): # 示例
    assert compare(black=['2H', '3D', '5S', '9C', 'KD'],
                   white=['2C', '3H', '4S', '8C', 'AH']) == 'White wins'
    assert compare(black=['2H', '4S', '4C', '2D', '4H'],
                   white=['2S', '8S', 'AS', 'QS', '3S']) == 'Black wins'
    assert compare(black=['2H', '3D', '5S', '9C', 'KD'],
                   white=['2C', '3H', '4S', '8C', 'KH']) == 'Black wins'
    assert compare(black=['2H', '3D', '5S', '9C', 'KD'],
                   white=['2D', '3H', '5C', '9S', 'KH']) == 'Tie'


def test(): # 同花 & 顺子
    assert compare(black=['2H', '3H', '4H', '5H', '6H'],
                   white=['3C', '4C', '5C', '6C', '7C']) == 'White wins'
    assert compare(black=['2H', '3H', '4H', '5H', '6H'],
                   white=['3C', '4H', '5S', '6C', '7H']) == 'Black wins'
    assert compare(black=['2H', '3D', '4S', '5C', '6D'],
                   white=['3C', '4H', '5S', '6C', '7H']) == 'White wins'
    assert compare(black=['2C', '3C', '5C', '8C', '6C'],
                   white=['3H', '5H', '8H', '6H', '2H']) == 'Tie'


def main():

    black=['2H', '3D', '5S', '9C', 'KD']
    white=['2C', '3H', '4S', '8C', 'AH'] # 'White wins'
    print(hand_rank(black), hand_rank(white))

    black=['2H', '4S', '4C', '2D', '4H']
    white=['2S', '8S', 'AS', 'QS', '3S'] # 'Black wins'
    print(hand_rank(black), hand_rank(white))

    black=['2H', '3D', '5S', '9C', 'KD']
    white=['2C', '3H', '4S', '8C', 'KH'] # 'Black wins'
    print(hand_rank(black), hand_rank(white))
    
    black=['2H', '3D', '5S', '9C', 'KD']
    white=['2D', '3H', '5C', '9S', 'KH'] # 'Tie'
    print(hand_rank(black), hand_rank(white))



if __name__ == '__main__':

    import pytest
    pytest.main(['-q', 'poker.py'])

    # main()







