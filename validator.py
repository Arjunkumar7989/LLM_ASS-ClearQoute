def validate_vehicle(vehicle_type, manufacturer):
    """
    Validates vehicle metadata.
    Ensures required string fields are non-empty and meaningful.
    """
    if not isinstance(vehicle_type, str) or not isinstance(manufacturer, str):
        return False, "Vehicle type and manufacturer must be strings"

    if not vehicle_type.strip() or not manufacturer.strip():
        return False, "Vehicle type or manufacturer is missing"

    return True, None


def validate_damage(severity, confidence):
    """
    Validates damage attributes.
    Severity must be between 1 (minor) and 5 (severe).
    Confidence must be between 0.0 and 1.0.
    """
    try:
        severity = int(severity)
        confidence = float(confidence)
    except (ValueError, TypeError):
        return False, "Severity or confidence has invalid type"

    if not (1 <= severity <= 5):
        return False, "Severity must be between 1 and 5"

    if not (0.0 <= confidence <= 1.0):
        return False, "Confidence must be between 0.0 and 1.0"

    return True, None
