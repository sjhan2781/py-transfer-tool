import os

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMessageBox
from openpyxl import load_workbook

from loadingwidget import LoadingWidget
from postthread import PostingThread
from savethread import SavingThread
from schoolstatus import SchoolStatus
from start_view import StartView
from tableWidget import WorkingField
from teacher_external import TeacherExternal
from teacher_internal import TeacherInternal


class StartController(QObject):

    def __init__(self) -> None:
        super().__init__()

        self.internal_list = list()
        self.school_list = list()
        self.external_list = list()
        self.invited_list = list()
        self.priority_list = list()
        self.hash_schools = dict()

        self.designation = list()
        self.gone = list()

        self.internal_file_url = None
        self.external_file_url = None
        self.school_file_url = None

        self.post_thread = PostingThread(internal=self.internal_list,
                                         external=self.external_list,
                                         schools=self.school_list,
                                         hash_schools=self.hash_schools,
                                         invited=self.invited_list,
                                         priority=self.priority_list)

        self.save_thread = SavingThread(internal=self.internal_list,
                                        external=self.external_list,
                                        schools=self.school_list,
                                        hash_schools=self.hash_schools,
                                        invited=self.invited_list,
                                        priority=self.priority_list,
                                        designation=self.designation,
                                        gone=self.gone,
                                        internal_file_url=self.internal_file_url,
                                        external_file_url=self.external_file_url,
                                        school_file_url=self.school_file_url,
                                        controller=self)

        self.loading_post = LoadingWidget(**{'controller': self,
                                        'title': '기다려주세요..',
                                        'internal': self.internal_list,
                                        'school': self.school_list,
                                        'external': self.external_list,
                                        'invited': self.invited_list})
        
        self.loading_save = LoadingWidget(**{'controller': self,
                                        'title': '저장중입니다..',
                                        'internal': self.internal_list,
                                        'school': self.school_list,
                                        'external': self.external_list,
                                        'invited': self.invited_list})

        self.init_thread()

        self.flag_internal = False
        self.flag_schools = False
        self.flag_external = False

    def init_thread(self):
        self.post_thread.started.connect(self.loading_post.exec_)
        self.post_thread.finished.connect(self.loading_post.close)
        self.post_thread.finished.connect(self.show_next_view)

        self.save_thread.started.connect(self.loading_save.exec_)
        self.save_thread.finished.connect(self.loading_save.close)
        # self.save_thread.finished.connect(self.show_next_view)

    def get_internal_list(self, file_url):
        self.internal_list.clear()
        self.invited_list.clear()
        self.internal_file_url = file_url

        fname, ext = os.path.splitext(file_url)

        has_macro = False

        if 'xlsm' in ext:
            has_macro = True

        try:
            wb = load_workbook(file_url, data_only=True, keep_vba=has_macro, read_only=True)
            ws = wb['초등(학교별)']

            i = 0

            for row in ws.iter_rows(min_row=6):
                if row[0].value is None:
                    break

                t = TeacherInternal(id=i, rank=row[0], school=row[1], region_grade=row[2], position=row[3],
                                    name=row[4], sex=row[5], regist_num=row[6], type=row[9], transfer_year=row[23],
                                    transfer_score=row[22], first=row[24], second=row[25], third=row[26],
                                    date=row[8], remarks=row[27])

                if '우대' in t.type:
                    self.priority_list.append(t)
                else:
                    self.internal_list.append(t)
                i += 1

            i = 0
            ws = wb['초빙']

            for row in ws.iter_rows(min_row=6):
                if row[0].value is None:
                    break

                t = TeacherInternal(id=i, rank=row[0], school=row[1], region_grade=row[2], position=row[3], name=row[4],
                                    sex=row[5], regist_num=row[6], type=row[9], transfer_year=row[23],
                                    transfer_score=row[22],
                                    first=row[24], second=row[25], third=row[26], date=row[8], remarks=row[27])

                self.invited_list.append(t)
                i += 1

            ws = wb['비정기']

            i = 0
            for row in ws.iter_rows(min_row=6):
                if row[0].value is None:
                    break

                t = TeacherInternal(id=i, rank=row[0], school=row[1], region_grade=row[2], position=row[3], name=row[4],
                                    sex=row[5], regist_num=row[6], type=row[9], transfer_year=row[23],
                                    transfer_score=row[22],
                                    first=row[24], second=row[25], third=row[26], date=row[8], remarks=row[27])

                self.internal_list.append(t)
                i += 1

            self.internal_list.sort()
            print('intenal size = {}'.format(self.internal_list.__len__()))
            wb.close()

        # except KeyError as e:
        #     show_msg_box("올바른 파일을 선택해주세요.", True)
        #     self.flag_internal = False

        except Exception as e:
            print(type(e))
            StartView.show_msg_box("올바른 파일을 선택해주세요.", True)
            self.flag_internal = False

        else:
            self.flag_internal = True
            StartView.show_msg_box("성공적으로 불러왔습니다.", False)

    def get_school_list(self, file_url):
        self.school_list.clear()
        self.school_file_url = file_url
        fname, ext = os.path.splitext(file_url)

        has_macro = False

        if 'xlsm' in ext:
            has_macro = True

        try:
            wb = load_workbook(file_url, data_only=True, keep_vba=has_macro, read_only=True)
            ws = wb['결충원']

            for row in ws.iter_rows(min_row=8):
                if row[0].value is None:
                    break

                # print('{}'.format(row[51].internal_value))
                self.school_list.append(SchoolStatus(row[0], row[2], row[51]))
                self.hash_schools[row[2].value] = row[0].internal_value
                self.designation.append([])
                self.gone.append([])

            print('get school {}'.format(self.school_list.__len__()))
            wb.close()

            # except KeyError as e:
            #     show_msg_box("올바른 파일을 선택해주세요.", True)
            #     self.flag_schools = False

        except Exception as e:
            print(type(e))
            StartView.show_msg_box("올바른 파일을 선택해주세요.", True)
            self.flag_schools = False

        else:
            # self.designation = [[] for row in range(self.school_list.__len__())]
            # self.gone = [[] for row in range(self.school_list.__len__())]
            self.flag_schools = True
            StartView.show_msg_box("성공적으로 불러왔습니다.", False)

    def get_external_list(self, file_url):
        self.external_list.clear()
        self.external_file_url = file_url

        fname, ext = os.path.splitext(file_url)

        has_macro = False

        if 'xlsm' in ext:
            has_macro = True

        try:
            wb = load_workbook(filename=file_url, data_only=True, keep_vba=has_macro, read_only=True)
            ws = wb['배정전정리']

            i = 0

            for row in ws.iter_rows(min_row=4):
                if row[0].value is None:
                    break

                t = TeacherExternal(i, row[0], '타시군전입', row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],
                                    row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17],
                                    row[18], row[19], row[21], row[22], row[23])

                self.external_list.append(t)
                i += 1

            wb.close()

        # except KeyError as e:
        #     StartView.show_msg_box("올바른 파일을 선택해주세요.", True)
        #     self.flag_external = False

        except Exception as e:
            print(e)
            StartView.show_msg_box("올바른 파일을 선택해주세요.", True)
            self.flag_external = False

        else:
            self.flag_external = True
            StartView.show_msg_box("성공적으로 불러왔습니다.", False)

    def is_valid(self):
        if self.flag_internal and self.flag_external and self.flag_schools:
            return True

        else:
            msg = '불러오지 않은 파일이 있습니다.\n'

            if not self.flag_schools:
                msg += '결충원 현황'

            if not self.flag_internal:
                if msg:
                    msg += ', '
                msg += '순위명부'

            if not self.flag_external:
                if msg:
                    msg += ', '
                msg += '타시군 전입명부'

            StartView.show_msg_box(msg=msg, is_error=True)

            return False

    def start_program(self):
        self.post_thread.start()

    def show_next_view(self):
        print('internal {} school {} external {}'
              .format(self.internal_list.__len__(), self.school_list.__len__(), self.external_list.__len__()))
        field = WorkingField(internal=self.internal_list,
                             external=self.external_list,
                             schools=self.school_list,
                             invited=self.invited_list,
                             hash_school=self.hash_schools,
                             designation=self.designation,
                             gone=self.gone,
                             priority=self.priority_list,
                             controller=self)

    def save(self, file_url):
        self.save_thread.internal_file_url = self.internal_file_url
        self.save_thread.external_file_url = self.external_file_url
        self.save_thread.school_file_url = self.school_file_url
        self.save_thread.result_file_url = file_url
        self.save_thread.start()

    def print_state(self):
        for t in self.internal_list:
            print(t)

        for t in self.external_list:
            print(t)

    def show_msg_box(self):
        msg_box = QMessageBox()

        if self.save_thread.is_error:
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText('저장 중에 문제가 발생했습니다.\n' + self.save_thread.msg)
        else:
            msg_box.setIcon(QMessageBox.NoIcon)
            msg_box.setText('저장되었습니다.')

        msg_box.setWindowTitle("")
        # msg_box.setText(self.save_thread.msg)
        msg_box.setStandardButtons(QMessageBox.Ok)
        result = msg_box.exec_()