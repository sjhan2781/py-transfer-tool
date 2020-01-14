import datetime


class TeacherExternal:
    def __init__(self, id, rank, type, region, school, position, name, birth, sex, career, major,
                 first, second, third, ab_type, ab_start, ab_end, related_school, relation, relation_name,
                 address, phone, email, vehicle, remarks):
        self.id = id
        self.rank = rank.value
        self.type = type
        self.region = region.value
        self.position = position.value
        self.school = school.value
        self.name = name.value
        self.birth = birth.value
        self.sex = sex.value
        self.career = career.value

        if isinstance(major.value, str):
            self.major = major.value
        else:
            self.major = None

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

        self.ab_type = ab_type.value
        self.ab_start = ab_start.value
        self.ab_end = ab_end.value
        self.related_school = related_school.value
        self.relation = relation.value
        self.relation_name = relation_name.value
        self.address = address.value
        self.phone = phone.value
        self.email = email.value
        self.vehicle = vehicle.value
        self.remarks = remarks.value
        self.disposed = None


    def __str__(self) -> str:
        return 'id = %3d 이름 = %4s 전보유형 = %2s 1지망 = %5s 2지망 = %5s 3지망 = %5s 배정교 = %s' % (self.id,
                                                                                                     self.name,
                                                                                                     self.type,
                                                                                                     self.first,
                                                                                                     self.second,
                                                                                                     self.third,
                                                                                                     self.disposed)
