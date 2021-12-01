# This class currently only contains a single function that helps with filesystem schenanigans.
class PermissionHelper:
    @staticmethod
    def NumberToChmod(number) -> str:
        """Extracts the classic chmod format (like 777) from the rather strange number format you get from stat() like functions."""
        return str(oct(number))[-3:]