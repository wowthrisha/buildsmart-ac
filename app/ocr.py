import os

def extract_dimensions(filepath):
    """
    Returns dict of extracted fields with confidence scores.
    confidence = -1 means 'manually entered / not extracted'.
    confidence = 0.0–1.0 means OCR confidence.
    """
    # Stub: return empty values — architect fills manually
    return {
        'area':         {'value': None, 'confidence': 0.0},
        'frontage':     {'value': None, 'confidence': 0.0},
        'depth':        {'value': None, 'confidence': 0.0},
        'road_width':   {'value': None, 'confidence': 0.0},
        'front_setback':{'value': None, 'confidence': 0.0},
        'rear_setback': {'value': None, 'confidence': 0.0},
        'side_setback': {'value': None, 'confidence': 0.0},
        'height':       {'value': None, 'confidence': 0.0},
    }
