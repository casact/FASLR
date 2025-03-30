import matplotlib.pyplot as plt
import numpy as np


def draw_stick_figure(ax, x=.5, y=.5, radius=.03, quote=None, color='k', lw=2, xytext=(0, 20)):
    """
    Taken from https://alimanfoo.github.io/2016/05/31/matplotlib-xkcd.html.
    """
    # draw the head
    head = plt.Circle((x, y), radius=radius, transform=ax.transAxes,
                      edgecolor=color, lw=lw, facecolor='none', zorder=10)
    ax.add_patch(head)

    # draw the body
    body = plt.Line2D([x, x], [y - radius, y - (radius * 4)],
                      color=color, lw=lw, transform=ax.transAxes)
    ax.add_line(body)

    # draw the arms
    arm1 = plt.Line2D([x, x + (radius)], [y - (radius * 1.5), y - (radius * 5)],
                      color=color, lw=lw, transform=ax.transAxes)
    ax.add_line(arm1)
    arm2 = plt.Line2D([x, x - (radius * .8)], [y - (radius * 1.5), y - (radius * 5)],
                      color=color, lw=lw, transform=ax.transAxes)
    ax.add_line(arm2)

    # draw the legs
    leg1 = plt.Line2D([x, x + (radius)], [y - (radius * 4), y - (radius * 8)],
                      color=color, lw=lw, transform=ax.transAxes)
    ax.add_line(leg1)
    leg2 = plt.Line2D([x, x - (radius * .5)], [y - (radius * 4), y - (radius * 8)],
                      color=color, lw=lw, transform=ax.transAxes)
    ax.add_line(leg2)

    # say something
    if quote:
        ax.annotate(quote, xy=(x + radius, y + radius), xytext=xytext,
                    xycoords='axes fraction', textcoords='offset points',
                    arrowprops=dict(arrowstyle='-', lw=1))


with plt.xkcd():
    # Based on "Stove Ownership" from XKCD by Randall Munroe
    # https://xkcd.com/418/

    fig = plt.figure()
    ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
    ax.spines[['top', 'right']].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ylim([-30, 10])

    data = np.ones(100)
    data[70:] -= np.arange(30)

    ax.annotate(
        'THE DAY I STARTED\nMY ACTUARIAL RESERVING\nROTATION',
        xy=(70, 1), arrowprops=dict(arrowstyle='->'), xytext=(15, -10))

    ax.plot(data)

    ax.set_xlabel('time')
    ax.set_ylabel('my  overall  health')

    # ax.text(
    #     40,
    #     12,
    #     'ROTATIONS',
    #     color='black',
    #     # bbox=dict(facecolor='none', edgecolor='black', pad=10.0)
    # )

    draw_stick_figure(
        ax,
        x=.1,
        y=.45,
        quote='           '
    )

    # plt.show()

    plt.savefig('docs/_static/xkcd_reserving_rotation.png')