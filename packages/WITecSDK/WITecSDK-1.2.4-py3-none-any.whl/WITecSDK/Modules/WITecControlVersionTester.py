from WITecSDK.Parameters import COMParameters

class WITecControlVersionTester:

    def __init__(self, aCOMParameters: COMParameters):
        self._programVersionCOM = aCOMParameters.GetStringParameter("Status|Software|Application|ProgramVersion")
        self.Version: float = float(self.StringVersion.split(",")[1].strip())
        # Create IsVersionGreater... attributes
        versions: list[float,...] = [5.1, 5.2, 5.3, 6.0, 6.1, 6.2, 6.3]
        isversions: list[bool,...] = [(str(int(ver * 10)), self.Version >= ver) for ver in versions]
        for verstr, isver in isversions:
            setattr(self, 'IsVersionGreater' + verstr, isver)
    
    @property
    def StringVersion(self) -> str:
        return self._programVersionCOM.GetValue()