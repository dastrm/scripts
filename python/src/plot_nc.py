import sys

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr


def get_masked_2d(arr1, arr2, mins, maxs):
    mask1 = (arr1 >= mins[0]) & (arr1 <= maxs[0])
    mask2 = (arr2 >= mins[1]) & (arr2 <= maxs[1])
    return arr1[mask1 & mask2], arr2[mask1 & mask2]


def plot_latlon(fname):
    grid = xr.open_dataset(fname)

    plt.figure()
    plt.clf()
    plt.rc("axes", axisbelow=True)
    plt.scatter(grid.clon, grid.clat)
    plt.scatter(grid.elon, grid.elat, c="r")
    plt.scatter(grid.vlon, grid.vlat, c="g")
    plt.grid("both")

    # plt.show()
    plt.savefig("lonlat_" + fname[:-3] + ".pdf")
    plt.close()


def plot_cartesian(fname):
    grid = xr.open_dataset(fname)

    plt.figure()
    plt.clf()
    plt.rc("axes", axisbelow=True)

    mins, maxs = [0, 0], [1e3, 1e3]

    x, y = get_masked_2d(
        grid.cell_circumcenter_cartesian_x,
        grid.cell_circumcenter_cartesian_y,
        mins,
        maxs,
    )
    plt.scatter(x, y, label="center")

    x, y = get_masked_2d(
        grid.edge_middle_cartesian_x, grid.edge_middle_cartesian_y, mins, maxs
    )
    plt.scatter(x, y, c="r", label="edge")

    x, y = get_masked_2d(
        grid.cartesian_x_vertices, grid.cartesian_y_vertices, mins, maxs
    )
    plt.scatter(x, y, c="g", label="vertex")

    plt.grid("both")
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), fancybox=True, ncol=3)
    outname = "cartesian_" + fname[:-3] + ".pdf"
    plt.savefig(outname)
    print(f"Saved {outname}")
    plt.close()


def plot_cartesian_corners(fname):
    grid = xr.open_dataset(fname)

    plt.rc("axes", axisbelow=True)
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

    def populate_ax(ax, mins, maxs):
        x, y = get_masked_2d(
            grid.cell_circumcenter_cartesian_x,
            grid.cell_circumcenter_cartesian_y,
            mins,
            maxs,
        )
        ax.scatter(x, y, label="center")

        x, y = get_masked_2d(
            grid.edge_middle_cartesian_x, grid.edge_middle_cartesian_y, mins, maxs
        )
        ax.scatter(x, y, c="r", label="edge")

        x, y = get_masked_2d(
            grid.cartesian_x_vertices, grid.cartesian_y_vertices, mins, maxs
        )
        ax.scatter(x, y, c="g", label="vertex")
        ax.grid("both")

    pmin, pmax, prange = 0.0, max(grid.domain_length, grid.domain_height), 1e3
    populate_ax(ax1, [pmin, pmax - prange], [pmin + prange, pmax])
    populate_ax(ax2, [pmax - prange, pmax - prange], [pmax, pmax])
    populate_ax(ax3, [pmin, pmin], [pmin + prange, pmin + prange])
    populate_ax(ax4, [pmax - prange, pmin], [pmax, pmin + prange])

    # plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), fancybox=True, ncol=3)
    fig.tight_layout()
    for ax in fig.get_axes():
        ax.label_outer()
        ax.set_aspect(1)

    outname = "cartesian_" + fname[:-3] + ".pdf"
    plt.savefig(outname)
    print(f"Saved {outname}")
    plt.close()


def main():
    if len(sys.argv) < 2:
        print("nc filename needed")
        exit(1)
    fname = sys.argv[1]
    print(f"Plotting {fname}")

    # plot_latlon(fname)
    # plot_cartesian(fname)
    plot_cartesian_corners(fname)


if __name__ == "__main__":
    main()
