DOMAIN = "choremate"

def setup(hass, config):
    """Basic setup."""
    hass.states.set("choremate.status", "ready")
    return True
