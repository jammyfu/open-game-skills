"""Original small reference model. Units: logical pixels, seconds; y points down."""
import math


def viewport(window, base=(320, 180)):
    if min(*window, *base) <= 0:
        raise ValueError('dimensions must be positive')
    scale = min(window[0] // base[0], window[1] // base[1])
    if scale < 1:
        raise ValueError('window below logical resolution; choose explicit fallback')
    return scale, ((window[0] - base[0] * scale) // 2,
                   (window[1] - base[1] * scale) // 2)


def leaf_offset(time, world_x, strength=1, edge=1):
    # Absolute sampling avoids render-frame accumulation; custom 2 s / 80 px wave.
    tick = math.floor(time * 10 + 1e-9)
    phase = 2 * math.pi * ((tick % 20) / 20 - (world_x % 80) / 80)
    return (round(strength * edge * (1 - math.cos(phase)) / 2),
            round(-strength * edge * max(0, math.sin(phase))))


def recovery(time):
    # Closed-form underdamped response to an initial displacement, zero velocity.
    decay, omega = 2.0, 4.0
    return math.exp(-decay * time) * (math.cos(omega * time) +
                                      decay / omega * math.sin(omega * time))


def haze(rgba, sky_rgb, amount, foreground=False):
    if not 0 <= amount <= 1:
        raise ValueError('amount outside [0, 1]')
    if foreground or amount == 0:
        return rgba
    return tuple(round(c * (1 - amount) + s * amount)
                 for c, s in zip(rgba[:3], sky_rgb)) + (rgba[3],)
