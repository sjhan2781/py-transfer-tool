class TeacherExternal:
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.rank = kwargs['rank']
        self.type = kwargs['type']
        self.region = kwargs['region']
        self.position = kwargs['position']
        self.school = kwargs['school']
        self.name = kwargs['name']
        self.birth = kwargs['birth']
        self.sex = kwargs['sex']
        self.career: str = str(kwargs['career'])

        if isinstance(kwargs['major'], str):
            self.major = kwargs['major']
        else:
            self.major = None

        if kwargs['first'] == 0:
            self.first = None
        else:
            self.first = kwargs['first']

        if kwargs['second'] == 0:
            self.second = None
        else:
            self.second = kwargs['second']

        if kwargs['third'] == 0:
            self.third = None
        else:
            self.third = kwargs['third']

        self.ab_type = kwargs['ab_type']
        self.ab_start = kwargs['ab_start']
        self.ab_end = kwargs['ab_end']
        self.related_school = kwargs['related_school'] 
        self.relation = kwargs['relation']
        self.relation_person = kwargs['relation_person']
        self.address = kwargs['address']
        self.phone = kwargs['phone']
        self.email = kwargs['email']
        self.vehicle = kwargs['vehicle']
        self.remarks = kwargs['remarks']
        self.disposed = None
        # self.disposed = kwargs['disposed']

    def __str__(self) -> str:
        return '이름 = %-5s     지역 = %s      성별 = %-3s\n' \
               '생년월일 = %s      교육총경력 = %s\n' \
               '1지망 = %-5s      2지망 = %-5s     3지망 = %-5s\n' \
               '휴직 종류 = %s     시작일 = %s      종료일 = %s\n' \
               '친인척 학교명 = %s      관계 = %s      성명  = %s\n' \
               '주소 = %s\n' \
               '비고 = %s' % (self.name, self.region, self.sex,
                            self.birth, self.career,
                            self.first, self.second, self.third,
                            self.ab_type, self.ab_start, self.ab_end,
                            self.related_school, self.relation, self.relation_person,
                            self.address,
                            self.remarks)
