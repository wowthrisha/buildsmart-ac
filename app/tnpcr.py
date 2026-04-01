MINIMUMS = {
    'area':          600.0,   # sq ft minimum
    'frontage':      20.0,    # ft
    'depth':         30.0,    # ft
    'front_setback': 3.0,     # ft
    'rear_setback':  1.5,     # ft
    'side_setback':  1.5,     # ft
    'height':        8.5,     # metres (default 2 floors)
}

WARN_MARGIN = 0.10   # within 10% of minimum → warn

def flag(value, minimum):
    """Returns 'pass', 'warn', or 'fail'. None if value is None."""
    if value is None: return None
    if value >= minimum * (1 + WARN_MARGIN): return 'pass'
    if value >= minimum:                     return 'warn'
    return 'fail'

def compute_compliance(plot):
    return {
        'area':          flag(plot.area,          MINIMUMS['area']),
        'frontage':      flag(plot.frontage,       MINIMUMS['frontage']),
        'depth':         flag(plot.depth,          MINIMUMS['depth']),
        'front_setback': flag(plot.front_setback,  MINIMUMS['front_setback']),
        'rear_setback':  flag(plot.rear_setback,   MINIMUMS['rear_setback']),
        'side_setback':  flag(plot.side_setback,   MINIMUMS['side_setback']),
        'height':        flag(plot.height,          MINIMUMS['height']),
    }

def detect_track(plot):
    """
    Track A: plot >= 600 sq ft, residential, standard.
    Track B: commercial or large plots.
    Returns 'A' or 'B'.
    """
    if plot.area and plot.area < 1500:
        return 'A'
    return 'B'

def fuzzy_confidence(flags):
    """0–100 overall approvability score from per-field flags."""
    values = [v for v in flags.values() if v is not None]
    if not values: return 0
    score_map = {'pass': 100, 'warn': 60, 'fail': 0}
    total = sum(score_map[v] for v in values)
    return round(total / len(values))

PLAIN_LANGUAGE = {
    'pass': '✅ Meets TNPCR requirement',
    'warn': '⚠️ Slightly below requirement — may still be approvable',
    'fail': '❌ Does not meet TNPCR minimum — redesign needed',
}

TNPCR_EXPLANATIONS = {
    'area':          'Minimum plot area is 600 sq ft for residential.',
    'frontage':      'Minimum frontage (road-facing width) is 20 ft.',
    'depth':         'Minimum plot depth is 30 ft.',
    'front_setback': 'Front setback (distance from road) must be at least 3 ft.',
    'rear_setback':  'Rear setback must be at least 1.5 ft.',
    'side_setback':  'Side setback must be at least 1.5 ft.',
    'height':        'Maximum building height is 8.5 m for 2-floor residential.',
}
