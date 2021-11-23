class PermissionHelper:
    @staticmethod
    def NumberToChmod(number):
        return str(oct(number))[-3:]