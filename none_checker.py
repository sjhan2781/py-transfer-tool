from checker import Checker


class NoneChecker(Checker):

    @staticmethod
    def check_valid(self, value):
        if value is None:
            return 0
        else:
            return value
