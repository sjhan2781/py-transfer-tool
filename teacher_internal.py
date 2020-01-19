from none_checker import NoneChecker


class TeacherInternal:
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.rank = kwargs['rank'].value
        self.position = kwargs['position'].value
        self.type = kwargs['type'].value
        self.school = kwargs['school'].value
        self.name = kwargs['name'].value
        self.regist_num = kwargs['regist_num'].value
        self.sex = kwargs['sex'].value
        self.region_grade = kwargs['region_grade'].value
        # self.date = kwargs['date'].value
        self.transfer_score = NoneChecker.check_valid(self, kwargs['transfer_score'].value)
        self.transfer_year = NoneChecker.check_valid(self, kwargs['transfer_year'].value)

        self.first = kwargs['first'].value

        self.second = kwargs['second'].value

        self.third = kwargs['third'].value

        self.remarks = kwargs['remarks'].value
        self.disposed = kwargs['disposed'].value

        self.regist_num_str = str(self.regist_num)

        self.birth = '{}.{}.{}'.format(self.regist_num_str[0:2],
                                       self.regist_num_str[2:4],
                                       self.regist_num_str[4:6])

    def __lt__(self, other):
        if self.transfer_year != other.transfer_year:
            return self.transfer_year > other.transfer_year
        else:
            if self.transfer_score != other.transfer_score:
                return self.transfer_score > other.transfer_score
            else:
                return self.birth < other.birth

    def __str__(self) -> str:
        return '이름 = %-5s //  전보유형 = %-s  // 성별 = %s\n' \
               '전보년수 = %.2f  //  근평 = %.2f  //  생년월일 = %s\n' \
               '1지망 = %-5s //  2지망 = %-5s //  3지망 = %-5s\n' \
               '비고 = %s' % (self.name, self.type, self.sex,
                            self.transfer_year, self.transfer_score, self.birth,
                            self.first, self.second, self.third,
                            self.remarks)
