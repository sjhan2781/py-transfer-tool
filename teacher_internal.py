class TeacherInternal:
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.rank = kwargs['rank'].value
        self.position = kwargs['position'].value
        self.type = kwargs['type'].value
        self.school = kwargs['school'].value
        self.name = kwargs['name'].value
        self.regist_num = kwargs['regist_num'].internal_value
        self.sex = kwargs['sex'].value
        self.region_grade = kwargs['region_grade'].value
        # self.date = kwargs['date'].value
        self.transfer_score = kwargs['transfer_score'] .internal_value
        self.transfer_year = kwargs['transfer_year'] .internal_value

        if kwargs['first'].value == 0:
            self.first = None
        else:
            self.first = kwargs['first'].value

        if kwargs['second'].value == 0:
            self.second = None
        else:
            self.second = kwargs['second'].value

        if kwargs['third'].value == 0:
            self.third = None
        else:
            self.third = kwargs['third'].value

        self.remarks = kwargs['remarks'].value
        self.disposed = kwargs['disposed'].value
        self.birth = ''
        # self.birth = '{}.{}.{}'.format(self.regist_num / 100000000000,
        #                                self.regist_num / 1000000000,
        #                                self.regist_num / 10000000)

    def __lt__(self, other):
        if self.transfer_year != other.transfer_year:
            return self.transfer_year > other.transfer_year
        else:
            if self.transfer_score != other.transfer_score:
                return self.transfer_score > other.transfer_score
            # else:
            #     return self.birth > other.birth

    def __str__(self) -> str:
        return '이름 = %-5s //  전보유형 = %-s  // 성별 = %s\n' \
               '전보년수 = %.2f  //  근평 = %.2f  //  생년월일 = %s\n' \
               '1지망 = %-5s //  2지망 = %-5s //  3지망 = %-5s\n' \
               '비고 = %s' % (self.name, self.type, self.sex,
                            self.transfer_year, self.transfer_score, self.birth,
                            self.first, self.second, self.third,
                            self.remarks)
