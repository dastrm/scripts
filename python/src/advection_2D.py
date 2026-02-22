import matplotlib.pyplot as plt
import numpy as np


def main():
    Lt = 10.0
    Nt = 5000
    t, dt = np.linspace(0.0, Lt, Nt, retstep=True)
    Lx = 1e5
    Ly = 1e5
    Nh = 50
    x = np.linspace(0.0, Lx, Nh)
    y = np.linspace(0.0, Ly, Nh)
    X, Y = np.meshgrid(x, y)
    vx = lambda x, y, t: (
        -Lx
        * np.sin(np.pi * x / Lx) ** 2
        * np.cos(np.pi * y / Ly)
        * np.sin(np.pi * y / Ly)
        * np.cos(2.0 * np.pi * t / Lt)
        * t
        / Lt
    )
    vy = lambda x, y, t: (
        Ly
        * np.cos(np.pi * x / Lx)
        * np.sin(np.pi * x / Lx)
        * np.sin(np.pi * y / Ly) ** 2
        * np.cos(2.0 * np.pi * t / Lt)
        * t
        / Lt
    )
    theta = np.linspace(0.0, 1.0, 14, endpoint=False)
    p = np.vstack(
        (
            (0.5 * np.sin(2.0 * np.pi * theta) * 0.2 + 0.50) * Lx,
            (0.5 * np.cos(2.0 * np.pi * theta) * 0.2 + 0.75) * Ly,
        )
    )
    for step, time in enumerate(t):
        # print(f"{step = :4d}, {time = :5.2e}")
        VX = vx(X, Y, time)
        VY = vy(X, Y, time)
        V = np.sqrt(VX**2 + VY**2) + np.finfo(np.float64).eps
        if step % (Nt / 10) == 0 or step == Nt - 1:
            fig, ax = plt.subplots()
            ax.set_title(f"Single Vortex, {time = :5.2f}")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_aspect("equal")
            c = plt.pcolormesh(X, Y, V)
            c.set_clim(0.0, 2.0 * max(Lx / Lt, Ly / Lt))
            cbar = plt.colorbar(c)
            q = plt.quiver(X, Y, VX / V, VY / V, pivot="mid", color="w")
            plt.plot(p[0], p[1], "ro")
            # plt.show()
            plt.savefig(f"plot_{step}.pdf")
            print(f"Saved step {step}.")
        p += dt * np.array([vx(p[0], p[1], time), vy(p[0], p[1], time)])


if __name__ == "__main__":
    main()
