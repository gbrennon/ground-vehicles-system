class InvalidLatitudeError(ValueError):
    """Exception raised for errors in the latitude value."""
    def __init__(self):
        self.message = "Latitude must be between -90 and 90 degrees."
        super().__init__(self.message)

class InvalidLongitudeError(ValueError):
    """Exception raised for errors in the longitude value."""
    def __init__(self):
        self.message = "Longitude must be between -180 and 180 degrees."
        super().__init__(self.message)
