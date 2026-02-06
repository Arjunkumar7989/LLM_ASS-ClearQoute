def validate_vehicle(vehicle_type, manufacturer):
    if not vehicle_type or not manufacturer:
        return False
    return True


def validate_damage(severity, confidence):
    try:
        severity = int(severity)
        confidence = float(confidence)
    except:
        return False

    if severity < 1 or severity > 5:
        return False

    if confidence < 0.0 or confidence > 1.0:
        return False

    return True
