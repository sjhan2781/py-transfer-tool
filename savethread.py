import os
import time
from threading import Thread

import openpyxl
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, PatternFill, Color
from openpyxl.worksheet.page import PageMargins
from openpyxl.worksheet.pagebreak import Break, ColBreak, RowBreak


class SavingThread(QtCore.QThread):
    # signal = QtCore.pyqtSignal()

    def __init__(self, **kwargs):
        super().__init__()
        self.internal = kwargs['internal']
        self.external = kwargs['external']
        self.schools = kwargs['schools']
        self.invited = kwargs['invited']
        self.priority = kwargs['priority']
        self.internal_file_url = kwargs['internal_file_url']
        self.designation = kwargs['designation']
        self.gone = kwargs['gone']
        self.school_file_url = kwargs['school_file_url']
        self.external_file_url = kwargs['external_file_url']
        self.result_file_url = None
        self.controller = kwargs['controller']

        self.is_error = False
        self.msg = ''

        # self.finished.connect(self.controller.show_msg_box)

    def run(self) -> None:
        self.save()
        # t1 = Thread(target=self.save_internal)
        # t2 = Thread(target=self.save_schools)
        # t3 = Thread(target=self.save_external)
        # t4 = Thread(target=self.make_result_file)
        #
        # t1.start()
        # t2.start()
        # t3.start()
        # t4.start()
        #
        # t1.join()
        # t2.join()
        # t3.join()
        # t4.join()

    def save(self):
        self.is_error = False
        self.msg = ''

        t1 = Thread(target=self.save_internal)
        t2 = Thread(target=self.save_schools)
        t3 = Thread(target=self.save_external)
        t4 = Thread(target=self.make_result_file)

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()

    def save_internal(self):
        try:
            fname, ext = os.path.splitext(self.internal_file_url)

            has_macro = False

            if 'xlsm' in ext:
                has_macro = True

            wb = load_workbook(filename=self.internal_file_url, keep_vba=has_macro)
            ws = [wb['초등(학교별)'], wb['비정기']]
            ws_invited = wb['초빙']

            fontStyle = Font(size="10")
            alignment = Alignment(horizontal='center', vertical='center')

            for i in range(0, ws.__len__()):
                ws[i].merge_cells('AD4:AD5')
                ws[i]['AE4'].value = '임지지정'
                ws[i]['AE4'].font = fontStyle
                ws[i]['AE4'].fill = PatternFill(patternType='solid', fgColor=Color('C2E7FF'))
                ws[i]['AE4'].alignment = alignment

            for i in range(0, self.internal.__len__()):
                if '비정기' in self.internal[i].type:
                    index = 1
                else:
                    index = 0

                if self.internal[i].disposed is None:
                    disposed = ''
                else:
                    disposed = self.internal[i].disposed
                cell = ws[index].cell(row=self.internal[i].id + 6, column=32, value=disposed)
                cell.font = fontStyle
                cell.alignment = alignment

            for i in range(0, self.invited.__len__()):
                if self.invited[i].disposed is None:
                    disposed = ''
                else:
                    disposed = self.invited[i].disposed
                cell = ws_invited.cell(row=self.invited[i].id + 6, column=32, value=disposed)
                cell.font = fontStyle
                cell.alignment = alignment

            wb.close()
            wb.save(fname + '_결과' +  ext)
            print("internal saved")

        except Exception as e:
            print(e)
            self.is_error = True
            if self.msg:
                self.msg += ', '
            self.msg += '관내명부'

        print('aaaaa??')

    def save_external(self):
        try:
            fname, ext = os.path.splitext(self.external_file_url)

            has_macro = False

            if 'xlsm' in ext:
                has_macro = True

            wb = load_workbook(self.external_file_url, keep_vba=has_macro)
            ws = wb['순위명부']

            fontStyle = Font(size="8")

            for i in range(0, self.external.__len__()):
                if self.external[i].disposed is None:
                    disposed = ''
                else:
                    disposed = self.external[i].disposed
                cell = ws.cell(row=self.external[i].id + 3, column=11, value=disposed)
                cell.font = fontStyle

            wb.close()
            wb.save(fname + '_결과' +  ext)
            print("external saved")

        except Exception as e:
            print(e)
            self.is_error = True
            if self.msg:
                self.msg += ', '
            self.msg += '관외명부'

    def save_schools(self):
        try:
            fname, ext = os.path.splitext(self.school_file_url)

            has_macro = False

            if 'xlsm' in ext:
                has_macro = True

            wb = load_workbook(self.school_file_url, keep_vba=has_macro)
            ws = wb['결충원']

            fontStyle = Font(size="8")

            for i in range(0, self.schools.__len__()):
                cell = ws.cell(row=i + 8, column=53, value=self.schools[i].gone)
                cell.font = fontStyle
                cell = ws.cell(row=i + 8, column=54, value=self.schools[i].inside)
                cell.font = fontStyle
                cell = ws.cell(row=i + 8, column=56, value=self.schools[i].outside)
                cell.font = fontStyle

            wb.close()
            wb.save(fname + '_결과' +  ext)

            print("schools saved")

        except Exception as e:
            print(e)
            self.is_error = True
            if self.msg:
                self.msg += ', '
            self.msg += '결충원'

    def make_result_file(self):
        try:
            wb = openpyxl.Workbook()
            sheet1 = wb.active
            sheet1.title = '관내발령결과'
            self.make_result_sheet(sheet1, self.internal, '경기도시흥교육지원청 초등교사 정기인사(관내)-현임교순')

            sheet2 = wb.create_sheet('타시군(도)발령결과')
            self.make_result_sheet(sheet2, self.external, '경기도시흥교육지원청 초등교사 정기인사(관외)- 성명순')

            sheet3 = wb.create_sheet('초빙교사발령결과')
            self.make_result_sheet(sheet3, self.invited, '경기도시흥교육지원청 초등초빙교사 정기인사-성명순')

            sheet4 = wb.create_sheet('data-in')
            self.make_data_in(sheet4)

            sheet5 = wb.create_sheet('봉투라벨')
            self.make_pack_label(sheet5)

            wb.close()
            wb.save(self.result_file_url)

            print('result saved')

        except Exception as e:
            print(e)
            self.is_error = True
            if self.msg:
                self.msg += ', '
            self.msg += '발령결과'

    def make_result_sheet(self, sheet, teachers, title):
        fontStyle = Font(size="14", bold=True)

        sheet.merge_cells('A1:F1')
        sheet['A1'] = title
        sheet['A1'].font = fontStyle

        fontStyle = Font(size="10")

        sheet['A2'] = '유형'
        sheet['A2'].font = fontStyle
        sheet['A2'].alignment = Alignment(horizontal='center')

        sheet['B2'] = '지역'
        sheet['B2'].font = fontStyle
        sheet['B2'].alignment = Alignment(horizontal='center')

        sheet['C2'] = '소속교'
        sheet['C2'].font = fontStyle
        sheet['C2'].alignment = Alignment(horizontal='center')

        sheet['D2'] = '성명'
        sheet['D2'].font = fontStyle
        sheet['D2'].alignment = Alignment(horizontal='center')

        sheet['E2'] = '성별'
        sheet['E2'].font = fontStyle
        sheet['E2'].alignment = Alignment(horizontal='center')

        sheet['F2'] = '발령사항'
        sheet['F2'].font = fontStyle
        sheet['F2'].alignment = Alignment(horizontal='center')

        row = 3
        for teacher in teachers:
            if teacher.disposed is None:
                continue

            if '타시군' in teacher.type:
                value = '타시군전입'
            else:
                value = '관내'

            a = sheet.cell(row=row, column=1, value=value)
            a.alignment = Alignment(horizontal='center')
            a.font = fontStyle

            b = sheet.cell(row=row, column=2, value='시흥')
            b.alignment = Alignment(horizontal='center')
            b.font = fontStyle

            c = sheet.cell(row=row, column=3, value=teacher.school)
            c.alignment = Alignment(horizontal='center')
            c.font = fontStyle

            d = sheet.cell(row=row, column=4, value=teacher.name)
            d.alignment = Alignment(horizontal='center')
            d.font = fontStyle

            e = sheet.cell(row=row, column=5, value=teacher.sex)
            e.alignment = Alignment(horizontal='center')
            e.font = fontStyle

            f = sheet.cell(row=row, column=6, value=teacher.disposed + '등학교 근무를 명함')
            f.font = fontStyle

            row += 1

        f = sheet.cell(row=row, column=6
                       , value='이상 {}명\n경기도시흥교육지원청 교육장.\n끝.'.format(row-3))
        f.alignment = Alignment(wrap_text=True)
        f.font = fontStyle

        sheet.column_dimensions['E'].hidden = True
        sheet.column_dimensions['F'].width = 25.0

    def make_data_in(self, sheet):
        # sheet.print_title_cols = 'A:H'  # the first two cols
        # sheet.print_title_rows = '1:1'  # the first row

        sheet.auto_filter.ref = 'A:H'

        fontStyle = Font(size="11")
        alignment = Alignment(horizontal='center')

        self.write_to_cell(sheet['A1'], '순', fontStyle, alignment)
        self.write_to_cell(sheet['B1'], '유형', fontStyle, alignment)
        self.write_to_cell(sheet['C1'], '소속지', fontStyle, alignment)
        self.write_to_cell(sheet['D1'], '소속교', fontStyle, alignment)
        self.write_to_cell(sheet['E1'], '성명', fontStyle, alignment)
        self.write_to_cell(sheet['F1'], '임지', fontStyle, alignment)
        self.write_to_cell(sheet['G1'], '성별', fontStyle, alignment)
        self.write_to_cell(sheet['H1'], '생년월일', fontStyle, alignment)

        i = 1
        row = 2;

        for teacher in self.internal:
            if teacher.disposed is None:
                continue

            self.write_to_cell(sheet.cell(row=row, column=1), i, fontStyle, alignment)
            self.write_to_cell(sheet.cell(row=row, column=2), '관내', fontStyle, alignment)
            self.write_to_cell(sheet.cell(row=row, column=3), '시흥', fontStyle, alignment)
            self.write_to_cell(sheet.cell(row=row, column=4), teacher.school, fontStyle, alignment)
            self.write_to_cell(sheet.cell(row=row, column=5), teacher.name, fontStyle, alignment)
            self.write_to_cell(sheet.cell(row=row, column=6), teacher.disposed, fontStyle, alignment)
            self.write_to_cell(sheet.cell(row=row, column=7), teacher.sex, fontStyle, alignment)
            # self.write_to_cell(sheet.cell(row=row, column=8, teacher.))

            i += 1
            row += 1

        for teacher in self.invited:
            if teacher.disposed is None:
                continue

            self.write_to_cell(sheet.cell(row=row, column=1), i, fontStyle, alignment)
            self.write_to_cell(sheet.cell(row=row, column=2), '초빙', fontStyle, alignment)
            self.write_to_cell(sheet.cell(row=row, column=3), '시흥', fontStyle, alignment)
            self.write_to_cell(sheet.cell(row=row, column=4), teacher.school, fontStyle, alignment)
            self.write_to_cell(sheet.cell(row=row, column=5), teacher.name, fontStyle, alignment)
            self.write_to_cell(sheet.cell(row=row, column=6), teacher.disposed, fontStyle, alignment)
            self.write_to_cell(sheet.cell(row=row, column=7), teacher.sex, fontStyle, alignment)
            # self.write_to_cell(sheet.cell(row=row, column=8, teacher.))

            i += 1
            row += 1

        for teacher in self.external:
            if teacher.disposed is None:
                continue

            self.write_to_cell(sheet.cell(row=row, column=1), i, fontStyle, alignment)
            self.write_to_cell(sheet.cell(row=row, column=2), '타시군전입', fontStyle, alignment)
            self.write_to_cell(sheet.cell(row=row, column=3), teacher.region, fontStyle, alignment)
            self.write_to_cell(sheet.cell(row=row, column=4), teacher.school, fontStyle, alignment)
            self.write_to_cell(sheet.cell(row=row, column=5), teacher.name, fontStyle, alignment)
            self.write_to_cell(sheet.cell(row=row, column=6), teacher.disposed, fontStyle, alignment)
            self.write_to_cell(sheet.cell(row=row, column=7), teacher.sex, fontStyle, alignment)
            self.write_to_cell(sheet.cell(row=row, column=8), teacher.birth, fontStyle, alignment)

            i += 1
            row += 1

    def write_to_cell(self, cell, value, font, alignment):
        cell.value = value
        cell.font = font
        cell.alignment = alignment

    def make_pack_label(self, sheet):
        fontStyle = Font(size="11")
        alignment = Alignment(horizontal='center')

        sheet.merge_cells('A1:G1')
        sheet['A1'] = '전입'
        sheet['A1'].font = fontStyle
        sheet['A1'].alignment = alignment

        sheet.column_dimensions['A'].width = 12.00
        sheet.column_dimensions['B'].width = 10.33
        sheet.column_dimensions['C'].width = 10.67
        sheet.column_dimensions['D'].width = 13.33
        sheet.column_dimensions['E'].width = 8.17
        sheet.column_dimensions['F'].width = 8.17
        sheet.column_dimensions['G'].width = 8.17
        sheet.column_dimensions['H'].width = 0.1
        sheet.column_dimensions['I'].width = 9.33
        sheet.column_dimensions['J'].width = 13.67
        sheet.column_dimensions['K'].width = 9.17
        sheet.column_dimensions['L'].width = 13.33
        sheet.page_setup.fitToWidth = True
        print_area = 'A{}:L{}'.format(1, self.schools.__len__()*25 + 3)
        sheet.print_area = print_area
        sheet.sheet_view.view = 'pageBreakPreview'
        sheet.set_printer_settings(sheet.PAPERSIZE_A4, sheet.ORIENTATION_LANDSCAPE)
        sheet.page_margins = PageMargins(left=0.454722225666046,
                                         right=0.312083333730698,
                                         top=1.30750000476837,
                                         bottom=0.75,
                                         header=0.698055565357208,
                                         footer=0.314861118793488)

        sheet.merge_cells('I1:L1')
        sheet['I1'] = '전출'
        sheet['I1'].font = fontStyle
        sheet['I1'].alignment = alignment

        self.write_to_cell(sheet['A2'], '신임교', fontStyle, alignment)
        self.write_to_cell(sheet['B2'], '전보유형', fontStyle, alignment)
        self.write_to_cell(sheet['C2'], '소속청', fontStyle, alignment)
        self.write_to_cell(sheet['D2'], '소속교', fontStyle, alignment)
        self.write_to_cell(sheet['E2'], '성명', fontStyle, alignment)
        self.write_to_cell(sheet['F2'], '생년월일', fontStyle, alignment)
        self.write_to_cell(sheet['G2'], '성별', fontStyle, alignment)

        self.write_to_cell(sheet['I2'], '전보유형', fontStyle, alignment)
        self.write_to_cell(sheet['J2'], '소속', fontStyle, alignment)
        self.write_to_cell(sheet['K2'], '성명', fontStyle, alignment)
        self.write_to_cell(sheet['L2'], '임지지정', fontStyle, alignment)


        for i in range(0, self.schools.__len__()):
            row = i * 25 + 3

            row_break = Break(id=(i+1)*25+2)  # create Break obj
            sheet.row_breaks.append(row_break)
            # column_break = ColBreak(count=1)
            # sheet.col_breaks.append(column_break)
            # sheet.page_breaks

            for teacher in self.designation[i]:
                self.write_to_cell(sheet.cell(row=row, column=1), teacher.disposed, fontStyle, alignment)
                if '타시군' in teacher.type:
                    self.write_to_cell(sheet.cell(row=row, column=2), '타시군', fontStyle, alignment)
                    self.write_to_cell(sheet.cell(row=row, column=3), teacher.region, fontStyle, alignment)

                else:
                    self.write_to_cell(sheet.cell(row=row, column=2), '관내', fontStyle, alignment)
                    self.write_to_cell(sheet.cell(row=row, column=3), '시흥', fontStyle, alignment)

                self.write_to_cell(sheet.cell(row=row, column=4), teacher.school, fontStyle, alignment)
                self.write_to_cell(sheet.cell(row=row, column=5), teacher.name, fontStyle, alignment)
                # self.write_to_cell(sheet.cell(row=row, column=6), teacher.birth, fontStyle, alignment)
                self.write_to_cell(sheet.cell(row=row, column=7), teacher.sex, fontStyle, alignment)
                row += 1
                # print(self.designation[j])

            row = i * 25 + 3
            for teacher in self.gone[i]:
                if '타시군' in teacher.type:
                    self.write_to_cell(sheet.cell(row=row, column=9), '타시군', fontStyle, alignment)
                    # self.write_to_cell(sheet.cell(row=row, column=9), teacher.region, fontStyle, alignment)

                else:
                    self.write_to_cell(sheet.cell(row=row, column=9), '관내', fontStyle, alignment)
                    # self.write_to_cell(sheet.cell(row=row, column=3), '시흥', fontStyle, alignment)

                self.write_to_cell(sheet.cell(row=row, column=10), teacher.school, fontStyle, alignment)
                self.write_to_cell(sheet.cell(row=row, column=11), teacher.name, fontStyle, alignment)
                self.write_to_cell(sheet.cell(row=row, column=12), teacher.disposed, fontStyle, alignment)
                row += 1
                # print(self.gone[j])

