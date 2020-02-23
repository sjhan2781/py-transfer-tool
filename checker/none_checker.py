from checker.base_checker import BaseChecker


class NoneChecker(BaseChecker):

    @staticmethod
    def check_valid(self, value):
        if value is None:
            return 0
        else:
            return value
