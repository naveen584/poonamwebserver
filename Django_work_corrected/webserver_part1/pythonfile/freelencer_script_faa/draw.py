import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.patches as mpatches
from os import listdir
from os.path import isfile, join
import numpy as np

#draw from summary
max = 0
maxtotal = 0
incount = 0

def draw_with_summary(filename, l_plt, pos_y):
    global max
    in_count = 0
    with open("./data/{}".format(filename), 'rb') as f:
        l_plt.text(-5, pos_y, filename, fontsize=6, horizontalalignment='right',
                   verticalalignment='center')
        while True:
            line = f.readline()
            if line == '':
                continue
            if not line:
                break
            params = line.split()
            print(params)
            pos_start = int(params[0])
            pos_end = int(params[1])
            mark = str(params[2])
            print(pos_end - pos_start)
            if mark.find("in") != -1:
                if(pos_end - pos_start > 250):
                    mk = 'i'
                else :
                    mk = 'o'
            elif mark.find("trans") != -1:
                mk = 't'
            else:
                mk = 'o'
            print(mark)
            draw_image(l_plt, start=pos_start, end=pos_end, mark=mk, pos_y=pos_y)
            if max <= pos_end :
                max = pos_end
#        process(line)

def draw_image(l_plt, start, end, mark, pos_y):
    print(mark)
    global incount
    if mark == 'i':
        l_plt.text(start, pos_y+12, str(start), fontsize=6)
        circle = Ellipse(((start+end)/2, pos_y), width=(end-start), height=40, fc='b')
        l_plt.text((start+end)/2, pos_y, "I N {}".format(incount+1), fontsize=6, horizontalalignment='center', verticalalignment='center', color='white')
        l_plt.text(end-15, pos_y+12, str(end), fontsize=6)
        l_plt.gca().add_patch(circle)
    elif mark == 't':
        rectangle = plt.Rectangle((start, pos_y-20), end-start, 40, fc='r')
        l_plt.gca().add_patch(rectangle)
    else :
        line = plt.Line2D((start, end), (pos_y, pos_y), lw=1)
        l_plt.gca().add_line(line)

def draw_test():
    plt.axes()

    circle = plt.Circle((0, 0), radius=100, fc='y')
    plt.gca().add_patch(circle)
    rectangle = plt.Rectangle((0, 0), 30, 30, fc='r')
    plt.gca().add_patch(rectangle)
    dotted_line = plt.Line2D((2, 8), (4, 4), lw=5.,
                             ls='-.', marker='.',
                             markersize=50,
                             markerfacecolor='r',
                             markeredgecolor='r',
                             alpha=0.5)
    plt.gca().add_line(dotted_line)

    plt.axis('scaled')
    plt.show()

if __name__ == '__main__':
    datapath = './data'
    onlyfiles = [f for f in listdir(datapath) if isfile(join(datapath, f))]
    i = 0
    for fn in onlyfiles:
        if fn.find(".summary") != -1:
            max = 0
            incount = 0
            pos_y = 50 + i * 50
            plt.gca().get_yaxis().set_visible(False)
            draw_with_summary(fn, l_plt=plt, pos_y=pos_y)
            i += 1
            plt.text(max, pos_y, "{}aa".format(max), fontsize=6, horizontalalignment='left', verticalalignment='center')
            if maxtotal < max :
                maxtotal = max

    red_patch = mpatches.Patch(color='red', label='Transmembrane helix')
    blue_patch = mpatches.Patch(color='blue', label='Inside')
    plt.legend(handles=[red_patch, blue_patch], loc='upper center', bbox_to_anchor=(1.05, 1), borderaxespad=0.)

    line = plt.Line2D((0, maxtotal), (0, 0), lw=1)
    plt.gca().add_line(line)
    plt.box(on=None)
    plt.xlabel("Scale", horizontalalignment='left', x=0.0, fontweight='bold')
    plt.xticks(np.arange(0, max , 100))
    plt.axis('scaled')
    plt.show()

