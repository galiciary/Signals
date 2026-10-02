import matplotlib # no GUI window, write files instead
import os
import pylab as pl
import numpy as np

matplotlib.use("Agg") 
OUT_DIR = "plots"
os.makedirs(OUT_DIR, exist_ok=True)

MESSAGE = "You're all I ever needed, yeah"
V = 1
SAMPLES_PER_BIT = 100

MESSAGE = "You're all I ever needed, yeah"
V = 1
SAMPLES_PER_BIT = 100

def string_to_bits(s):
    bits = []
    for ch in s:
        bits.extend(int(b) for b in format(ord(ch), '08b'))
    return bits

BITS = string_to_bits(MESSAGE)  # 30 chars x 8 = 240 bits

def plot_signal(levels, title, yticks):
    """Multi-row plot sized for docx portrait page width (6.5 in).
    Splits 240 bits into 4 rows of 60 so bit annotations stay legible."""
    rows, bpr = 4, len(BITS) // 4
    fig, axes = pl.subplots(rows, 1, figsize=(6.5, 7.8))

    for r, ax in enumerate(axes):
        a, b = r * bpr, (r + 1) * bpr
        s0, s1 = a * SAMPLES_PER_BIT, b * SAMPLES_PER_BIT
        t = np.arange(s0, s1) / SAMPLES_PER_BIT
        ax.plot(t, levels[s0:s1], color='magenta', linewidth=1.0)
        for i in range(a, b):
            ax.text(i + 0.5, max(yticks) + 0.25, str(BITS[i]),
                    ha='center', va='bottom', fontsize=5)
            ax.axvline(i, color='gray', linewidth=0.2, alpha=0.4)
        ax.axvline(b, color='gray', linewidth=0.2, alpha=0.4)
        ax.set_xlim(a, b)
        ax.set_ylim(min(yticks) - 0.5, max(yticks) + 0.7)
        ax.set_yticks(yticks)
        ax.set_ylabel('V')
        ax.grid(True, axis='y', linestyle='--', alpha=0.3)
    axes[0].set_title(title)
    axes[-1].set_xlabel('Bit index')

    pl.tight_layout()
    fname = title.lower().replace(" ", "_").replace("(", "").replace(")", "")
    pl.savefig(os.path.join(OUT_DIR, f"{fname}.png"), dpi=200)
    pl.close(fig)

# Section 1: Unipolar NRZ
def unipolar_nrz(bits, V=1):
    out = []

    for b in bits:
        level = V if b == 1 else 0
        out.extend([level] * SAMPLES_PER_BIT)
    return out

levels = unipolar_nrz(BITS, V)
plot_signal(levels, "Unipolar NRZ", yticks=[0, V])

# Section 2: Polar NRZ-L
def polar_nrz_l(bits, V=1):
    out = []

    for b in bits:
        level = -V if b == 1 else V
        out.extend([level] * SAMPLES_PER_BIT)
    return out

levels = polar_nrz_l(BITS, V)
plot_signal(levels, "Polar NRZ-L", yticks=[-V, 0, V])

# Section 3: Polar NRZ-I
def polar_nrz_i(bits, V=1):
    out = []
    current = V  # arbitrary starting level

    for b in bits:
        if b == 1:
            current = -current
        out.extend([current] * SAMPLES_PER_BIT)
    return out

levels = polar_nrz_i(BITS, V)
plot_signal(levels, "Polar NRZ-I", yticks=[-V, 0, V])

# Section 4: Polar RZ
def polar_rz(bits, V=1):
    out = []
    half = SAMPLES_PER_BIT // 2

    for b in bits:
        start = V if b == 1 else -V
        out.extend([start] * half)
        out.extend([0] * (SAMPLES_PER_BIT - half))
    return out

levels = polar_rz(BITS, V)
plot_signal(levels, "Polar RZ", yticks=[-V, 0, V])

# Section 5: Polar Biphase (Manchester)
def manchester(bits, V=1):
    out = []
    half = SAMPLES_PER_BIT // 2

    for b in bits:
        if b == 1:
            out.extend([-V] * half)
            out.extend([V] * (SAMPLES_PER_BIT - half))
        else:
            out.extend([V] * half)
            out.extend([-V] * (SAMPLES_PER_BIT - half))
    return out

levels = manchester(BITS, V)
plot_signal(levels, "Polar Biphase (Manchester)", yticks=[-V, 0, V])

# Section 6: Polar Biphase (Differential Manchester)
def differential_manchester(bits, V=1):
    out = []
    half = SAMPLES_PER_BIT // 2
    current = V  # arbitrary starting level

    for b in bits:
        if b == 0:
            current = -current  # transition at start of bit interval
        out.extend([current] * half)
        current = -current       # always transition at mid-bit
        out.extend([current] * (SAMPLES_PER_BIT - half))
    return out

levels = differential_manchester(BITS, V)
plot_signal(levels, "Polar Biphase (Differential Manchester)", yticks=[-V, 0, V])

# Section 7: Bipolar AMI
def bipolar_ami(bits, V=1):
    out = []
    last = -V  # so first 1 encodes as +V

    for b in bits:
        if b == 0:
            out.extend([0] * SAMPLES_PER_BIT)
        else:
            last = -last
            out.extend([last] * SAMPLES_PER_BIT)
    return out

levels = bipolar_ami(BITS, V)
plot_signal(levels, "Bipolar AMI", yticks=[-V, 0, V])

# Section 8: Bipolar Pseudoternary
def bipolar_pseudoternary(bits, V=1):
    out = []
    last = -V  # so first 0 encodes as +V
    
    for b in bits:
        if b == 1:
            out.extend([0] * SAMPLES_PER_BIT)
        else:
            last = -last
            out.extend([last] * SAMPLES_PER_BIT)
    return out

levels = bipolar_pseudoternary(BITS, V)
plot_signal(levels, "Bipolar Pseudoternary", yticks=[-V, 0, V])