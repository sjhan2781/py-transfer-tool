from checker.none_checker import NoneChecker
from checker.regist_num_checker import RegistNumChecker


class TeacherInternal:
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.rank = kwargs['rank']
        self.position = kwargs['position']
        self.type = kwargs['type']
        self.school = kwargs['school']
        self.name = kwargs['name']
        self.regist_num = kwargs['regist_num']
        self.sex = kwargs['sex']
        self.region_grade = kwargs['region_grade']
        # self.date = kwargs['date']
        self.transfer_score = NoneChecker.check_valid(self, kwargs['transfer_score'])
        self.transfer_year = NoneChecker.check_valid(self, kwargs['transfer_year'])

        self.first = kwargs['first']

        self.second = kwargs['second']

        self.third = kwargs['third']

        self.remarks = kwargs['remarks']
        self.disposed = kwargs['disposed']

        # self.regist_num_str = str(self.regist_num)
        # self.birth_compare = (int(self.regist_num_str[0:6]) + 500000) % 1000000

        self.birth = RegistNumChecker.check_valid(self, kwargs['regist_num'])

    def __lt__(self, other):
        if self.transfer_year != other.transfer_year:
            return self.transfer_year > other.transfer_year
        else:
            if self.transfer_score != other.transfer_score:
                return self.transfer_score > other.transfer_score
            else:
                return self.birth < other.birth

    def __str__(self) -> str:
        return '이름 = %-5s     전보유형 = %-s     성별 = %s\n' \
               '전보년수 = %.2f      근평 = %.2f      생년월일 = %s\n' \
               '1지망 = %-5s     2지망 = %-5s     3지망 = %-5s\n' \
               '비고 = %s' % (self.name, self.type, self.sex,
                            self.transfer_year, self.transfer_score, self.birth,
                            self.first, self.second, self.third,
                            self.remarks)
