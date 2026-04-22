import serial
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import cheby1, sosfilt
import time

# ── CONFIG ─────────────────────────────
PORT = "COM14"
BAUD = 921600
DURATION = 5

FREQ = 1184
HALF_BW = 60
C = 343.0
Z = 0.2
d = 0.08

# ── CENTERED MIC POSITIONS ─────────────
mic_pos = np.array([
    [-d/2, -d*np.sqrt(3)/6, 0],
    [ d/2, -d*np.sqrt(3)/6, 0],
    [ 0,    d*np.sqrt(3)/3,  0]
])

# ── GRID ───────────────────────────────
grid_size = 0.3
res = 60

xs = np.linspace(-grid_size, grid_size, res)
ys = np.linspace(-grid_size, grid_size, res)

omega = 2*np.pi*FREQ

# ── SERIAL ─────────────────────────────
ser = serial.Serial(PORT, BAUD, timeout=0.01)

# ── PLOT SETUP ─────────────────────────
plt.ion()
fig, ax = plt.subplots()

img = ax.imshow(np.zeros((res, res)),
                extent=[xs[0], xs[-1], ys[0], ys[-1]],
                origin='lower',
                cmap='inferno',
                vmin=-40,
                vmax=0)

plt.colorbar(img, ax=ax, label="Power (dB)")

# markers
ax.scatter(0, 0, color='cyan', label='Center')

for m in mic_pos:
    ax.scatter(m[0], m[1], color='white', s=20)

peak_marker, = ax.plot(0, 0, 'go',markersize=14, label='Source')

ax.set_title("Live Sound Map (dB Scaled)")
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.legend()

plt.show(block=False)

print("Running 5-second loop...")

# ── FRAME READER ───────────────────────
def read_frames(duration):
    buf1, buf2, buf3 = [], [], []
    buffer = bytearray()

    start = time.time()

    while time.time() - start < duration:
        data = ser.read(1024)
        if data:
            buffer.extend(data)

            i = 0
            while i + 4 < len(buffer):
                if buffer[i] == 0xFF and buffer[i+1] == 0xAA:
                    buf1.append((buffer[i+2]-128)/128)
                    buf2.append((buffer[i+3]-128)/128)
                    buf3.append((buffer[i+4]-128)/128)
                    i += 5
                else:
                    i += 1

            buffer = buffer[i:]

    return buf1, buf2, buf3

# ── MAIN LOOP ──────────────────────────
while True:

    print("\n🎙 Recording 5 seconds...")

    buf1, buf2, buf3 = read_frames(DURATION)

    print(f"Samples: {len(buf1)}")

    if len(buf1) < 200:
        print("❌ Not enough data")
        continue

    fs = max(len(buf1) / DURATION,2400)
    print(f"Fs: {fs:.2f} Hz")

    x1 = np.array(buf1)
    x2 = np.array(buf2)
    x3 = np.array(buf3)

    # ── FREQUENCY DETECTION ─────────────
    def get_peak_freq(x):
        x = x - np.mean(x)
        x *= np.hanning(len(x))
        fft = np.abs(np.fft.rfft(x))
        freqs = np.fft.rfftfreq(len(x), 1/fs)
        return freqs[np.argmax(fft)]

    f1 = get_peak_freq(x1)
    f2 = get_peak_freq(x2)
    f3 = get_peak_freq(x3)

    print(f"🎧 Mic1: {f1:.1f} Hz | Mic2: {f2:.1f} Hz | Mic3: {f3:.1f} Hz")

    # ── FILTER ─────────────────────────
    def make_bandpass(f0, bw, fs):
        nyq = fs/2
        low = max((f0-bw)/nyq, 0.001)
        high = min((f0+bw)/nyq, 0.999)
        return cheby1(4, 1, [low, high], btype='band', output='sos')

    SOS = make_bandpass(FREQ, HALF_BW, fs)

    def bp(x):
        return sosfilt(SOS, x - np.mean(x))

    x1, x2, x3 = bp(x1), bp(x2), bp(x3)

    # ── COMPLEX AMPLITUDE ──────────────
    def complex_amp(x):
        t = np.arange(len(x)) / fs
        ref = np.exp(-1j * 2*np.pi*FREQ*t)
        return np.dot(x, ref)

    measured = np.array([
        complex_amp(x1),
        complex_amp(x2),
        complex_amp(x3)
    ])

    # ── BEAMFORMING ────────────────────
    power = np.zeros((res, res))

    for i, x in enumerate(xs):
        for j, y in enumerate(ys):

            p = np.array([x, y, Z])

            steering = []
 
            for m in mic_pos:
                dist = np.linalg.norm(p - m)
                tau = dist / C
                steering.append(np.exp(-1j * omega * tau))

            steering = np.array(steering)

            power[j, i] = np.abs(np.dot(measured, np.conj(steering)))

    # ── dB SCALING (FIXED) ─────────────
    power /= np.max(power) + 1e-9
    power_db = 20 * np.log10(power + 1e-9)
    power_db = np.clip(power_db, -40, 0)

    # ── PEAK ───────────────────────────
    peak_idx = np.unravel_index(np.argmax(power), power.shape)
    peak_x = xs[peak_idx[1]]
    peak_y = ys[peak_idx[0]]

    print(f"📍 Source: x={peak_x:.2f} m, y={peak_y:.2f} m")

    # ── UPDATE PLOT ────────────────────
    img.set_data(power_db)
    peak_marker.set_data([peak_x], [peak_y])

    fig.canvas.draw_idle()
    fig.canvas.flush_events()