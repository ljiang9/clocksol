#!/usr/bin/env python3
"""clocksol - 终端时钟纸牌 (Clock Solitaire)。

规则: 13 堆牌摆成钟面 (A=1 点 ... Q=12 点, K=中央)。
翻开中央堆顶牌, 按点数放到对应牌堆底下并翻开该堆顶牌, 循环。
第 4 张 K 出现时若还有牌没翻完则失败; 52 张全翻完则胜利。
纯运气游戏, 无决策点。
"""
import argparse
import random
import secrets
import sys

RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUITS = ["\u2660", "\u2665", "\u2666", "\u2663"]
RANK_PILE = {r: i for i, r in enumerate(RANKS)}  # A->0 ... K->12


def new_deck(rng):
    deck = [(r, s) for r in RANKS for s in SUITS]
    rng.shuffle(deck)
    return deck


def deal(seed=None):
    """发牌: 13 堆, 每堆 4 张(牌背朝上)。返回 piles 列表。"""
    rng = random.Random(seed) if seed is not None else secrets.SystemRandom()
    deck = new_deck(rng)
    return [deck[i * 4:(i + 1) * 4] for i in range(13)]


def play(seed=None, verbose=False):
    """玩一局。返回 (won, flips, kings_seen)。"""
    piles = deal(seed)
    # 每堆用列表表示, 末尾为堆顶(未翻)。翻开的牌直接计数, 不再放回。
    kings = 0
    flips = 0
    # 从中央(K 堆, 索引 12)顶翻第一张
    pile_idx = 12
    while True:
        if not piles[pile_idx]:
            # 该堆已空(理论上只在胜局末尾发生)
            break
        card = piles[pile_idx].pop()
        flips += 1
        rank = card[0]
        if verbose:
            dest = "\u4e2d\u592e" if rank == "K" else rank + "\u70b9\u4f4d"
            print(f"\u7ffb {card[0]}{card[1]} -> {dest}")
        if rank == "K":
            kings += 1
            if kings == 4:
                break
        pile_idx = RANK_PILE[rank]
        if flips == 52:
            break
    won = flips == 52
    return won, flips, kings


def render_last(seed=None):
    won, flips, kings = play(seed)
    print(f"{'\u8d0f\u5229' if won else '\u5931\u8d25'}: \u7ffb\u724c {flips}/52, \u89c1\u5230 K \u00d7{kings}")


def auto(n, seed=None):
    rng = random.Random(seed)
    wins = 0
    for _ in range(n):
        won, _, _ = play(rng.randrange(2 ** 32))
        wins += won
    print(f"\u6a21\u62df {n} \u5c40: \u80dc {wins}, \u8d0f\u7387 {wins / n * 100:.2f}%")


def main(argv=None):
    ap = argparse.ArgumentParser(description="时钟纸牌 Clock Solitaire - 纯运气, 无决策点")
    ap.add_argument("--auto", type=int, metavar="N", help="自动模拟 N 局并统计胜率")
    ap.add_argument("--seed", type=int, default=None, help="随机种子")
    ap.add_argument("-v", "--verbose", action="store_true", help="打印每一步翻牌")
    args = ap.parse_args(argv)
    if args.auto is not None:
        if args.auto < 1:
            print("error: --auto 需要正整数", file=sys.stderr)
            return 2
        auto(args.auto, args.seed)
        return 0
    won, flips, kings = play(args.seed, args.verbose)
    print(f"{'\U0001f389 \u8d0f\u5229! 52 张牌全部翻完。' if won else f'\U0001f480 \u5931\u8d25: 第 4 张 K 出现, 只翻了 {flips}/52 张。'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
