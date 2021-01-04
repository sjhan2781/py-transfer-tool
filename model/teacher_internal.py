from checker.none_checker import NoneChecker
from checker.regist_num_checker import RegistNumChecker


class TeacherInternal:

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        # 괄호를 기준으로 토큰분리
        self.tmp = kwargs['type'].split('(')[0]
        # 8조 1항일 경우 일반, 13조 1항일 경우 우대, 이외는 입력한대로(초빙, 비정기)
        self.type = {'제 8조 1항' in self.tmp: '일반', '제 13조 1항' in self.tmp: '우대'}.get(True, self.tmp)
        self.school = kwargs['school']
        self.name = kwargs['name']
        self.regist_num = kwargs['regist_num']
        self.sex = kwargs['sex']
        self.region_grade = kwargs['region_grade']
        # self.date = kwargs['date']
        self.transfer_score = NoneChecker.check_valid(self, kwargs['transfer_score'])
        self.transfer_year = NoneChecker.check_valid(self, kwargs['transfer_year'])
        self.current_school_year = NoneChecker.check_valid(self, kwargs['current_school_year'])
        self.first = kwargs['first']
        self.second = kwargs['second']
        self.third = kwargs['third']

        self.remarks = kwargs['remarks']
        self.disposed = kwargs['disposed']

        if self.second is not None:
            self.type += '만기'

        self.birth = RegistNumChecker.check_valid(self, kwargs['regist_num'])

        # 타입에 초빙, 우대가 들어가있을 때 해당 순위로 없을땐 3으로
        self.priority = {'초빙' in self.type: 1, '우대' in self.type: 2, '비정기' in self.type: 99}.get(True, 3)

    def __lt__(self, other):
        if self.priority != other.priority:
            return self.priority < other.priority
        else:
            if self.transfer_year != other.transfer_year:
                return self.transfer_year > other.transfer_year
            else:
                if self.transfer_score != other.transfer_score:
                    return self.transfer_score > other.transfer_score
                else:
                    if self.birth != other.birth:
                        return self.birth < other.birth
                    else:
                        return self.current_school_year > other.current_school_year

    def __str__(self) -> str:
        return '이름 = %-5s     전보유형 = %-s     성별 = %s\n' \
               '전보년수 = %.2f      근평 = %.2f      생년월일 = %s\n' \
               '1지망 = %-5s     2지망 = %-5s     3지망 = %-5s\n' \
               '비고 = %s' % (self.name, self.type, self.sex,
                            self.transfer_year, self.transfer_score, self.birth,
                            self.first, self.second, self.third,
                            self.remarks)

