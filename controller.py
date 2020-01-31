import os

from PyQt5.QtCore import QObject, pyqtSlot, qDebug
from PyQt5.QtWidgets import QMessageBox, QApplication
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

from loadingwidget import LoadingWidget
from postthread import PostingThread
from savethread import SavingThread
from savingwidget import SavingWidget
from schoolstatus import SchoolStatus
from start_view import StartView
from tableWidget import WorkingField
from teacher_external import TeacherExternal
from teacher_internal import TeacherInternal
from updatethread import UpdatingThread
from updatingwidget import UpdatingWidget


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
                                        controller=self)

        self.update_thread = UpdatingThread(internal=self.internal_list,
                                            external=self.external_list,
                                            schools=self.school_list,
                                            hash_schools=self.hash_schools,
                                            invited=self.invited_list,
                                            priority=self.priority_list,
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

        self.waiting_save = SavingWidget(**{'controller': self,
                                            'title': '저장중입니다..',
                                            'internal': self.internal_list,
                                            'school': self.school_list,
                                            'external': self.external_list,
                                            'invited': self.invited_list,
                                            'designation': self.designation,
                                            'gone': self.gone})

        self.waiting_update = UpdatingWidget(**{'controller': self,
                                                'title': '저장중입니다..',
                                                'internal': self.internal_list,
                                                'schools': self.school_list,
                                                'external': self.external_list,
                                                'invited': self.invited_list,
                                                'priority': self.priority_list})

        self.init_thread()

        self.flag_internal = False
        self.flag_schools = False
        self.flag_external = False

    def init_thread(self):
        self.post_thread.started.connect(self.loading_post.show)
        self.post_thread.finished.connect(self.loading_post.close)
        self.post_thread.finished.connect(self.show_next_view)

        self.update_thread.show_msg_box.connect(self.show_msg_box)
        self.update_thread.started.connect(self.waiting_update.show)
        self.update_thread.started.connect(self.waiting_update.set_maximum)
        self.update_thread.set_state_internal.connect(self.waiting_update.ui.progressBar_internal.setValue)
        self.update_thread.set_state_external.connect(self.waiting_update.ui.progressBar_external.setValue)
        self.update_thread.set_state_school.connect(self.waiting_update.ui.progressBar_school.setValue)
        self.update_thread.finished.connect(self.waiting_update.close)

        self.save_thread.show_msg_box.connect(self.show_msg_box)
        self.save_thread.started.connect(self.waiting_save.show)
        self.save_thread.started.connect(self.waiting_save.set_maximum)
        self.save_thread.set_state_result.connect(self.waiting_save.ui.progressBar_result.setValue)
        self.save_thread.finished.connect(self.waiting_save.close)

    def get_internal_list(self, file_url):
        self.internal_list.clear()
        self.invited_list.clear()
        self.priority_list.clear()
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
                t = TeacherInternal(id=i, rank=row[0].value, school=row[1].value, region_grade=row[2].value,
                                    position=row[3].value, name=row[4].value, sex=row[5].value, regist_num=row[6].value,
                                    type=row[9].value, transfer_year=row[23].value, transfer_score=row[30].value,
                                    first=row[24].value, second=row[25].value, third=row[26].value,
                                    date=row[8].value, remarks=row[27].value, disposed=None) 
                # 임지지정 후 불러오기...
                # t = TeacherInternal(id=i, rank=row[0], school=row[1], region_grade=row[2], position=row[3],
                #                     name=row[4], sex=row[5], regist_num=row[6], type=row[9], transfer_year=row[23],
                #                     transfer_score=row[30], first=row[24], second=row[25], third=row[26],
                #                     date=row[8], remarks=row[27], disposed=row[31])

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

                t = TeacherInternal(id=i, rank=row[0].value, school=row[1].value, region_grade=row[2].value,
                                    position=row[3].value, name=row[4].value, sex=row[5].value, regist_num=row[6].value,
                                    type=row[9].value, transfer_year=row[23].value, transfer_score=row[30].value,
                                    first=row[24].value, second=row[25].value, third=row[26].value,
                                    date=row[8].value, remarks=row[27].value, disposed=None)
                # 임지지정 후 불러오기...
                # t = TeacherInternal(id=i, rank=row[0], school=row[1], region_grade=row[2], position=row[3],
                #                     name=row[4], sex=row[5], regist_num=row[6], type=row[9], transfer_year=row[23],
                #                     transfer_score=row[30], first=row[24], second=row[25], third=row[26],
                #                     date=row[8], remarks=row[27], disposed=row[31])

                self.invited_list.append(t)
                i += 1

            ws = wb['비정기']
            i = 0
            for row in ws.iter_rows(min_row=6):
                if row[0].value is None:
                    break

                t = TeacherInternal(id=i, rank=row[0].value, school=row[1].value, region_grade=row[2].value,
                                    position=row[3].value, name=row[4].value, sex=row[5].value, regist_num=row[6].value,
                                    type=row[9].value, transfer_year=row[23].value, transfer_score=row[30].value,
                                    first=row[24].value, second=row[25].value, third=row[26].value,
                                    date=row[8].value, remarks=row[27].value, disposed=None)
                # 임지지정 후 불러오기...
                # t = TeacherInternal(id=i, rank=row[0], school=row[1], region_grade=row[2], position=row[3],
                #                     name=row[4], sex=row[5], regist_num=row[6], type=row[9], transfer_year=row[23],
                #                     transfer_score=row[30], first=row[24], second=row[25], third=row[26],
                #                     date=row[8], remarks=row[27], disposed=row[31])

                self.internal_list.append(t)
                i += 1

            self.internal_list.sort()

        except TypeError as e:
            print(e)
            print(t.id)
            self.show_msg_box("{}시트 {}번 행 서식을 확인해주세요.".format(ws.title, i + 6), True)
            self.flag_internal = False
            wb.close()

        except KeyError as e:
            print(e)
            self.show_msg_box("시트 이름을 확인해주세요.", True)
            self.flag_internal = False
            wb.close()

        except Exception as e:
            print(e)
            self.show_msg_box("올바른 파일을 선택해주세요.", True)
            self.flag_internal = False
            # wb.close()

        else:
            self.flag_internal = True
            self.show_msg_box("성공적으로 불러왔습니다.", False)
            wb.close()

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

            i = 0
            for row in ws.iter_rows(min_row=8):
                if row[0].value is None:
                    break

                # print('{}'.format(row[51].internal_value))
                self.school_list.append(SchoolStatus(num=row[0].value, name=row[2].value, status=row[51].value,
                                                     outside=0, inside=0, gone=0, term=0, area=row[1].value))

                # 불러오기 할 때
                # self.school_list.append(SchoolStatus(num=row[0].value, name=row[2].value, status=row[51].value,
                #                                      outside=row[55].value, inside=row[53].value, gone=row[52].value,
                #                                      term=row[63].value, area=row[1].value))
                self.hash_schools[row[2].value] = row[0].internal_value
                self.designation.append([])
                self.gone.append([])
                print(self.school_list[i])
                i += 1
        except TypeError as e:
            print(e)
            self.show_msg_box("{}번째 행 서식을 확인해주세요.".format(i + 8), True)
            self.flag_internal = False
            wb.close()

        except KeyError as e:
            print(e)
            self.show_msg_box("시트 이름을 확인해주세요.", True)
            self.flag_internal = False
            wb.close()

        except Exception as e:
            print(e)

            # if isinstance(e, InvalidFileException):
            StartView.show_msg_box("올바른 파일을 선택해주세요.", True)
            self.flag_schools = False
            # wb.close()

        else:
            # self.designation = [[] for row in range(self.school_list.__len__())]
            # self.gone = [[] for row in range(self.school_list.__len__())]
            self.flag_schools = True
            StartView.show_msg_box("성공적으로 불러왔습니다.", False)
            wb.close()

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

                if '미충원' in row[4].value:
                    type = '미충원'
                else:
                    type = '타시군전입'

                t = TeacherExternal(id=i, rank=row[0].value, type=type, region=row[1].value, position=row[3].value,
                                    school=row[2].value, name=row[4].value, birth=row[5].value, sex=row[6].value,
                                    major=row[8].value, career=row[7].value, first=row[9].value, second=row[10].value,
                                    third=row[11].value, ab_type=row[12].value, ab_start=row[13].value,
                                    ab_end=row[14].value, related_school=row[15].value, relation=row[16].value,
                                    relation_person=row[17].value, address=row[18].value, phone=row[19].value,
                                    email=row[21].value, vehicle=row[22].value, remarks=row[23].value)

                self.external_list.append(t)
                i += 1

        except TypeError as e:
            print(e)
            self.show_msg_box("{}번째 행 서식을 확인해주세요.".format(i + 2), True)
            self.flag_internal = False
            wb.close()

        except KeyError as e:
            print(e)
            self.show_msg_box("시트 이름을 확인해주세요.", True)
            self.flag_internal = False
            wb.close()

        except Exception as e:
            print(e)
            StartView.show_msg_box("올바른 파일을 선택해주세요.", True)
            self.flag_external = False
            wb.close()

        else:
            self.flag_external = True
            StartView.show_msg_box("성공적으로 불러왔습니다.", False)
            wb.close()

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

        self.field = WorkingField(internal=self.internal_list,
                                  external=self.external_list,
                                  schools=self.school_list,
                                  invited=self.invited_list,
                                  hash_school=self.hash_schools,
                                  designation=self.designation,
                                  gone=self.gone,
                                  priority=self.priority_list,
                                  controller=self, )

    def save(self, file_url):
        self.save_thread.result_file_url = file_url
        self.save_thread.start()

    def update(self):
        self.update_thread.invited = self.invited_list
        self.update_thread.priority = self.priority_list
        self.update_thread.internal_file_url = self.internal_file_url
        self.update_thread.external_file_url = self.external_file_url
        self.update_thread.school_file_url = self.school_file_url
        self.update_thread.start()

    def show_msg_box(self, msg, is_error):
        msg_box = QMessageBox()

        if is_error:
            msg_box.setIcon(QMessageBox.Warning)
        else:
            msg_box.setIcon(QMessageBox.NoIcon)

        msg_box.setText(msg)
        msg_box.setWindowTitle("")
        msg_box.setStandardButtons(QMessageBox.Ok)
        result = msg_box.exec()

    def show_dialog_exit(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("")
        msg_box.setText('종료하시겠습니까?')
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.No)
        result = msg_box.exec_()

        if result == QMessageBox.Ok:
            QApplication.quit()
