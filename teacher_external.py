class TeacherExternal:
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.rank = kwargs['rank'].value
        self.type = kwargs['type']
        self.region = kwargs['region'].value
        self.position = kwargs['position'].value
        self.school = kwargs['school'].value
        self.name = kwargs['name'].value
        self.birth = kwargs['birth'].value
        self.sex = kwargs['sex'].value
        self.career = kwargs['career'].value

        if isinstance(kwargs['major'].value, str):
            self.major = kwargs['major'].value
        else:
            self.major = None

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

        self.ab_type = kwargs['ab_type'].value
        self.ab_start = kwargs['ab_start'].value
        self.ab_end = kwargs['ab_end'].value
        self.related_school = kwargs['related_school'] .value
        self.relation = kwargs['relation'].value
        self.relation_person = kwargs['relation_person'].value
        self.address = kwargs['address'].value
        self.phone = kwargs['phone'].value
        self.email = kwargs['email'].value
        self.vehicle = kwargs['vehicle'].value
        self.remarks = kwargs['remarks'].value
        self.disposed = None
        # self.disposed = kwargs['disposed'].value

    def __str__(self) -> str:
        return '이름 = %-5s //  지역 = %s  //  성별 = %-3s//\n' \
               '생년월일 = %s  //  교육총경력 = %s\n' \
               '1지망 = %-5s  //  2지망 = %-5s //  3지망 = %-5s\n' \
               '휴직 종류 = %s  // 시작일 = %s  //  종료일 = %s\n' \
               '친인척 학교명 = %s  //  관계 = %s  //  성명  = %s\n' \
               '주소 = %s\n' \
               '비고 = %s' % (self.name, self.region, self.sex,
                            self.birth, self.career,
                            self.first, self.second, self.third,
                            self.ab_type, self.ab_start, self.ab_end,
                            self.related_school, self.relation, self.relation_person,
                            self.address,
                            self.remarks)
