class StiLicense:

### Private

    __licenseKey: str = None
    __licenseFile: str = None

    def __clearKey(self) -> None:
        self.__licenseKey = None
        self.__licenseFile = None


### Public

    def setKey(self, key: str) -> None:
        """Set the license key in Base64 format."""
    
        self.__clearKey()
        self.__licenseKey = key

    def setFile(self, file: str) -> None:
        """Set the path or URL to the license key file."""
    
        self.__clearKey()
        self.__licenseFile = file

    def getHtml(self) -> str:
        """Get the HTML representation of the component."""
        
        if len(self.__licenseKey or '') > 0:
            return f"Stimulsoft.Base.StiLicense.Key = '{self.__licenseKey}';\n"
        
        if len(self.__licenseFile or '') > 0:
            return f"Stimulsoft.Base.StiLicense.loadFromFile('{self.__licenseFile}');\n"

        return ''
        