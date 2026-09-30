# -*- coding: utf-8 -*-
"""
淘宝用户行为数据分析 · 结果可视化

数据来源：全量分析结果（1 亿条，2017-11-25 ~ 2017-12-03），见「用户行为数据分析.md」。
运行方式（在仓库根目录）：
    python 可视化/draw_analysis.py

输出：
    可视化/图1_用户行为转化漏斗.png
    可视化/图2_核心指标总览.png

说明：日均流量、24 小时活跃分布等趋势图依赖 Hive 查询结果（CSV），
    后续补充时在常量区加载对应 CSV 即可绘图。
"""
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============ 全量结果常量（来源：用户行为数据分析.md）============
PV = 89660671        # 总点击数
UV = 987991          # 总用户数
FAV = 2888258        # 收藏数
CART = 5530446       # 加购物车数
BUY = 2015807        # 购买数
FAVCART = FAV + CART     # 收藏 + 加购
REPURCHASE_RATE = 0.6601  # 复购率 66.01%

PV2FAVCART = FAVCART / PV      # 点击 -> 收藏/加购
FAVCART2BUY = BUY / FAVCART    # 收藏/加购 -> 购买
PV2BUY = BUY / PV              # 点击 -> 购买（整体转化率 2.25%）


def draw_funnel():
    """图1：用户行为转化漏斗"""
    stages = [
        ('点击浏览 PV', PV),
        ('收藏 + 加购', FAVCART),
        ('购买', BUY),
    ]
    colors = ['#4472C4', '#ED7D31', '#70AD47']
    fig, ax = plt.subplots(figsize=(8.6, 4.8), dpi=150)
    ys = list(range(len(stages)))[::-1]
    for yi, (name, val), color in zip(ys, stages, colors):
        ax.barh(yi, val, height=0.55, color=color, alpha=0.88)
        ax.text(val + PV * 0.015, yi, '{}\n{:,}'.format(name, val),
                ha='left', va='center', color='#262626', fontsize=11.5)
    ax.set_yticks([])
    ax.set_xlim(0, PV * 1.14)
    ax.set_xticks([0, 2e7, 4e7, 6e7, 8e7])
    ax.set_xticklabels(['0', '2000万', '4000万', '6000万', '8000万'])
    ax.set_xlabel('行为次数（全量：PV 共 8966 万次）')
    ax.set_title('图1  用户行为转化漏斗（2017-11-25 ~ 2017-12-03）', fontsize=13, fontweight='bold')
    ax.spines[['top', 'right']].set_visible(False)
    note = ('点击→收藏/加购 {:.2f}%   收藏/加购→购买 {:.2f}%   整体转化率（点击→购买）{:.2f}%'
            .format(PV2FAVCART * 100, FAVCART2BUY * 100, PV2BUY * 100))
    ax.text(0, -0.75, note, fontsize=11, color='#404040')
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, '图1_用户行为转化漏斗.png'), bbox_inches='tight')
    plt.close(fig)


def draw_overview():
    """图2：核心指标总览（关键行为量 + 关键结论）"""
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(11.5, 4.6), dpi=150,
        gridspec_kw={'width_ratios': [1.5, 1]})
    # 左：关键行为量（万）
    names = ['点击 PV', '加购', '购买', '收藏', '用户 UV']
    vals = [PV, CART, BUY, FAV, UV]
    colors = ['#4472C4', '#ED7D31', '#70AD47', '#FFC000', '#5B9BD5']
    bars = ax1.bar(names, [v / 10000 for v in vals], color=colors, alpha=0.88)
    for b, v in zip(bars, vals):
        ax1.text(b.get_x() + b.get_width() / 2, b.get_height() + 120,
                 '{:.1f}万'.format(v / 10000), ha='center', va='bottom', fontsize=10)
    ax1.set_ylim(0, max(vals) / 10000 * 1.15)
    ax1.set_ylabel('数量（万）')
    ax1.set_title('关键行为量（全量）', fontsize=12, fontweight='bold')
    ax1.spines[['top', 'right']].set_visible(False)
    # 右：关键结论卡片
    ax2.axis('off')
    ax2.set_title('关键结论', fontsize=12, fontweight='bold')
    cards = [
        ('整体转化率', '2.25%', '点击 → 购买'),
        ('复购率', '66.01%', '购买 ≥ 2 次的用户占比'),
        ('活跃高峰', '21–22 点', '凌晨 4 点最低'),
        ('周活跃', '周末更高', '12-02 / 12-03 恰逢周末'),
    ]
    for i, (k, v, d) in enumerate(cards):
        y = 0.86 - i * 0.24
        ax2.text(0.04, y, k, fontsize=12, color='#404040')
        ax2.text(0.42, y, v, fontsize=17, fontweight='bold', color='#1F4E79')
        ax2.text(0.04, y - 0.085, d, fontsize=9.5, color='#808080')
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, '图2_核心指标总览.png'), bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    draw_funnel()
    draw_overview()
    print('已生成：')
    for name in ('图1_用户行为转化漏斗.png', '图2_核心指标总览.png'):
        print('  ' + os.path.join(OUT_DIR, name))
