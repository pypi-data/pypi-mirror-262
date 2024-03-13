__version__ = "0.0.16.dev8"


def dash_board():
    """Launches the dash board."""
    from .dashBoard import main
    dashBoard.main()


def getShipments():
    """getShipments."""
    from .GetShipments import main
    main()


def glueWeight():
    """glue weight."""
    from .GlueWeight import main
    main()


def groundVITests():
    """GND/VI tests."""
    from .GroundVITests import main
    main()


def sendShipments():
    """Send items."""
    from .SendShipments import main
    main()

def uploadTest():
    """Upload a single tests."""
    from .UploadTest import main
    main()


def uploadMultipleTests():
    """Upload multiple tests."""
    from .UploadMultipleTests import main
    main()

def uploadModuleIV():
    """Upload IV files of single and double modules"""
    from .UploadModuleIV import main
    main()

def wirebondTest():
    """Inputs data and eventually upload wirebod test."""
    from .WireBondGui import main
    main()
