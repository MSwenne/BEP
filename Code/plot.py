from matplotlib.ticker import PercentFormatter
from collections import Counter, OrderedDict
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import functools

def plot_hist(data, title):
    fig, ax = plt.subplots(figsize=(7,5))
    data = [data]
    labels = list(sorted(
        functools.reduce(lambda x, y: x.union(y.keys()), data, set())))

    labels_dict = OrderedDict()
    for label in labels:
        labels_dict[label] = 0
    color = ['#648fff', '#dc267f', '#785ef0', '#ffb000', '#fe6100']
    for item, execution in enumerate(data):
        values = []
        for key in labels_dict:
            if key not in execution:
                values.append(0)
            else:
                labels_dict[key] += 1
                values.append(execution[key])
        values = np.array(values, dtype=float)
        pvalues = values / sum(values)
        numelem = len(values)
        ind = np.arange(numelem)  # the x locations for the groups
        width = 1/(len(data)+1)  # the width of the bars
        rects = []
        for idx, val in enumerate(pvalues):
            label = None
            rects.append(ax.bar(idx+item*width, val, width, label=label,
                                color=color[item % len(color)],
                                zorder=2))
        # add some text for labels, title, and axes ticks
        ax.set_ylabel('Probabilities', fontsize=14)
        ax.set_xticks(ind)
        ax.set_xticklabels(labels, fontsize=14, rotation=70)
        ax.set_ylim([0., min([1.2, max([1.2 * val for val in pvalues])])])
        # attach some text labels
        for rect in rects:
            for rec in rect:
                height = rec.get_height()
                if height >= 1e-3:
                    ax.text(rec.get_x() + rec.get_width() / 2., 1.05 * height,
                            '%.3f' % float(height),
                            ha='center', va='bottom', zorder=3)
                else:
                    ax.text(rec.get_x() + rec.get_width() / 2., 1.05 * height,
                            '0',
                            ha='center', va='bottom', zorder=3)

    ax.yaxis.set_major_locator(MaxNLocator(5))
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(14)
    ax.set_facecolor('#eeeeee')
    plt.grid(which='major', axis='y', zorder=0, linestyle='--')
    plt.title(title)