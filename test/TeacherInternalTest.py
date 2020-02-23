import unittest

from model.teacher_internal import TeacherInternal


class MyTestCase(unittest.TestCase):
    def test_something(self):
        t1 = TeacherInternal(id=0, rank=0, school='OO초', region_grade=None,
                             position=None, name='test1', sex=None, regist_num='960920-1111111',
                             type=None, transfer_year=90, transfer_score=100,
                             first=None, second=None, third=None,
                             date=None, remarks=None, disposed=None)

        t2 = TeacherInternal(id=0, rank=0, school='OO초', region_grade=None,
                             position=None, name='test2', sex=None, regist_num='870920-2222222',
                             type=None, transfer_year=90, transfer_score=100,
                             first=None, second=None, third=None,
                             date=None, remarks=None, disposed=None)

        t3 = TeacherInternal(id=0, rank=0, school='OO초', region_grade=None,
                             position=None, name='test3', sex=None, regist_num=None,
                             type=None, transfer_year=90, transfer_score=100,
                             first=None, second=None, third=None,
                             date=None, remarks=None, disposed=None)



        t_list = list()
        t_list.append(t1)
        t_list.append(t2)

        t_list.sort()

        for t in t_list:
            print(t)

        print(t3)
        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
