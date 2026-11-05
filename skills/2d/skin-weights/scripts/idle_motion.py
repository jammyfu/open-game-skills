"""Build a seamless small-motion idle (breathing, sway, follow-through) as ogs.skin-motion/1.

Config (JSON):
  {"duration": 2.0, "sampleRate": 60, "breaths": 2, "inhale": 0.4,
   "channels": [{"bone": "chest", "property": "y", "amplitude": -0.6},
                {"bone": "spine", "property": "rotate", "amplitude": 1.2, "lag": 0.06},
                {"bone": "head", "property": "rotate", "amplitude": -1.5, "lag": 0.14}],
   "fixedContacts": [...optional, passed through to the audit...]}

Every channel follows ONE breath curve: it rises from rest to the peak over the first `inhale` share of
a breath and settles over the rest (asymmetric, eased at both ends), `breaths` whole breaths per loop.
`lag` delays a channel by that share of a breath (follow-through: shoulders after the chest, the head
last). Phase 0 is exactly the setup pose for every channel with lag 0, and a lagged channel wraps
continuously, so the loop seam is invisible. Values are offsets added to the setup (rotate in degrees,
x/y in world units). Out-of-range values are refused, never clamped: breaths 1..8, inhale 0.2..0.8,
lag 0..0.5, |rotate amplitude| <= 15 degrees. Exit 0 ok, 2 invalid.
Breath shape and lag idea after sprite-gen's breathe layer (aldegad/sprite-gen, Apache-2.0); independent implementation.
"""
import argparse
import json
import math

import numpy as np

from skinlib import MOTION_SCHEMA, SkinError, finite, load_rig, read_json, require, write_json


def breath(phase, inhale):
    """0 at phase 0 (and 1), 1 at phase `inhale`; eased rise, longer eased fall. Periodic with period 1."""
    p = np.mod(phase, 1.0)
    rise = p < inhale
    u = np.where(rise, p/inhale, (p - inhale)/(1 - inhale))
    ease = u*u*(3 - 2*u)
    return np.where(rise, ease, 1 - ease)


def validate(config, rig):
    duration, rate = config.get('duration', 2.0), config.get('sampleRate', 60)
    require(finite(duration) and duration > 0 and finite(rate) and rate > 0, 'duration and sampleRate must be positive')
    count = duration*rate
    require(abs(count - round(count)) < 1e-9, 'duration must be a whole number of samples')
    breaths = config.get('breaths', 1)
    require(type(breaths) is int and 1 <= breaths <= 8, 'breaths must be an integer 1..8 (whole breaths per loop; never stretched to fit)')
    inhale = config.get('inhale', 0.4)
    require(finite(inhale) and 0.2 <= inhale <= 0.8, 'inhale must be within 0.2..0.8 of a breath')
    channels = config.get('channels')
    require(isinstance(channels, list) and channels, 'channels must be a nonempty list')
    seen = set()
    for c in channels:
        require(c.get('bone') in rig['_bones'], f'channel bone {c.get("bone")} is not in the rig')
        require(c.get('property') in ('rotate', 'x', 'y'), 'channel property must be rotate, x or y (no scale or shear)')
        key = (c['bone'], c['property'])
        require(key not in seen, f'duplicate channel {key}')
        seen.add(key)
        require(finite(c.get('amplitude')) and c['amplitude'] != 0, f'{key}: amplitude must be a nonzero number')
        if c['property'] == 'rotate':
            require(abs(c['amplitude']) <= 15, f'{key}: |rotate amplitude| above 15 degrees is not a small-motion idle; author a pose instead')
        lag = c.get('lag', 0.0)
        require(finite(lag) and 0 <= lag <= 0.5, f'{key}: lag must be within 0..0.5 of a breath')
    return int(round(count)), rate, breaths, inhale


def build(config, rig):
    count, rate, breaths, inhale = validate(config, rig)
    t = np.arange(count + 1)/rate
    duration = count/rate
    tracks = []
    for c in config['channels']:
        phase = breaths*t/duration - c.get('lag', 0.0)
        values = c['amplitude']*breath(phase, inhale)
        values[-1] = values[0]                                   # exact seam
        tracks.append({'bone': c['bone'], 'property': c['property'], 'keys': [{'t': round(float(a), 9), 'v': round(float(v), 9)} for a, v in zip(t, values)]})
    return {'schema': MOTION_SCHEMA, 'sampleRate': rate, 'duration': duration, 'loop': True,
            'scope': config.get('scope', f'small-motion idle: {breaths} breath(s), inhale {inhale:g}'),
            'tracks': tracks, 'ik': config.get('ik', []), 'contacts': config.get('contacts', []),
            'fixedContacts': config.get('fixedContacts', []),
            'idle': {'breaths': breaths, 'inhale': inhale, 'channels': config['channels']}}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('rig')
    parser.add_argument('config')
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    rig = load_rig(args.rig)
    motion = build(read_json(args.config), rig)
    write_json(args.out, motion)
    print(json.dumps({'status': 'WRITTEN', 'tracks': len(motion['tracks']), 'samples': len(motion['tracks'][0]['keys'])}))


if __name__ == '__main__':
    try:
        main()
    except SkinError as error:
        raise SystemExit(f'BLOCKED: {error}')
