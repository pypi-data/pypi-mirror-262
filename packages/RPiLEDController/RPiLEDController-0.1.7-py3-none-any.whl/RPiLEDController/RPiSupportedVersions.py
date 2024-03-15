class RPiSupportedVersions:
    RPi4 = 4
    RPi5 = 5

    RPis = [RPi4, RPi5]

    @staticmethod
    def is_supported_version(version):
        return version in [RPiSupportedVersions.RPi4, RPiSupportedVersions.RPi5]

    @staticmethod
    def get_supported_versions():
        return RPiSupportedVersions.RPis