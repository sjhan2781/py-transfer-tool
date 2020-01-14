import datetime


class TeacherInternal:
    def __init__(self, id, rank, position, type, school, name, regist_num, sex, region_grade, transfer_year,
                 transfer_score,
                 first, second, third, remarks, date):
        self.id = id
        self.rank = rank.value
        self.position = position.value
        self.type = type.value
        self.school = school.value
        self.name = name.value
        self.regist_num = regist_num.internal_value
        self.sex = sex.value
        self.region_grade = region_grade.value
        # print(date.value)
        # self.date = datetime.datetime.strptime(date.value, '%m/%d/%Y')
        self.date = date.value
        self.transfer_score = transfer_score.internal_value
        self.transfer_year = transfer_year.internal_value

        if first.value == 0:
            self.first = None
        else:
            self.first = first.value

        if second.value == 0:
            self.second = None
        else:
            self.second = second.value

        if third.value == 0:
            self.third = None
        else:
            self.third = third.value
        # self.preferential = preferential.value
        self.remarks = remarks.value
        # self.designation = designation.value
        self.disposed = None

    def __lt__(self, other):
        if self.transfer_year != other.transfer_year:
            return self.transfer_year > other.transfer_year
        else:
            if self.transfer_score != other.transfer_score:
                return self.transfer_score > other.transfer_score

        # return if self.transfer_year > other.transfer_year : else if

    def __str__(self) -> str:
        return 'id = %3d 이름 = %4s 전보유형 = %2s 1지망 = %5s 2지망 = %5s 3지망 = %5s 배정교 = %s' % (self.id,
                                                                                                     self.name,
                                                                                                     self.type,
                                                                                                     self.first,
                                                                                                     self.second,
                                                                                                     self.third,
                                                                                                     self.disposed)
