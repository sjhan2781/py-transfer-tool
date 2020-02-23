from checker.basechecker import BaseChecker


class RegistNumChecker(BaseChecker):

    @staticmethod
    def check_valid(self, value):

        if value is None:
            year = '00'
            month = '00'
            day = '00'
        else:
            regist_num_str = str(value)

            year = regist_num_str[0:2]
            month = regist_num_str[2:4]
            day = regist_num_str[4:6]

        return '{}.{}.{}'.format(year, month, day)