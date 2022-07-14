from sys import argv
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QComboBox, QFileDialog, QApplication, QLineEdit
from pandas import read_csv
import curve_extract_002 as curex
import damage_ratio_cal_v1 as drc

class External_Module_:
    def func_connect(self):
        self.CE = curex.CurveExtract()

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.a = 44.742
        self.b = 0.152
        self.uts = 46.5
        self.file_name = []
        # self.time = 4               #냉장고 시험시간 (12시간)
        self.time = 3               #오븐 시험시간
        self.make_curve_key = 0
        self.curve_open_key = 0
        self.CE = curex.CurveExtract()
        self.batch_file_name = 'stress_curve_extract.bat'
        self.cfile_name = 'stress_curve_extract.cfile'
        self.curve_prefix = 'stress_curve_'
        # self.fre = [6249,655.5,397,270.5,266,299.5,300,226.5,181.5,113,78,46,23.5,11,4.5,2]             #오븐용

    def setupUI(self):
        self.setGeometry(400, 200, 520, 230)
        self.setWindowTitle("Damage Ratio Calculator for Refrigerator")
        lspost_dir_data = open('post_directory.1').readlines()                        #setting파일 한줄씩 읽어서 변수지정
        lspost_dir_data_list = [line.rstrip('\n') for line in lspost_dir_data]   
        self.lspost_dir = lspost_dir_data_list[0]
        binnum_data = open('binnum.1').readlines()    
        binnum_data_list = [line.rstrip('\n') for line in binnum_data]   
        self.binnum = binnum_data_list[0]
        fre_data = open('frequent_rate.1').readlines()    
        self.fre = [line.rstrip('\n') for line in fre_data]   
        self.EID = '0'

        self.label = QLabel('Path: ',self)
        self.label.move(30,100)
        self.label.resize(400,80)
        self.label1 = QLabel('Material: ',self)
        self.label1.move(30,130)
        self.label1.resize(400, 80)
        self.label2 = QLabel('Damage ratio: ', self)
        self.label2.move(30, 160)
        self.label2.resize(400, 80)
        self.label3 = QLabel('Status: Ready', self)
        self.label3.move(30, 70)
        self.label3.resize(400, 80)

        btn1 = QPushButton("Curve open", self)
        btn1.move(220, 30)
        btn2 = QPushButton("Run", self)
        btn2.move(300, 30)
        btn3 = QPushButton("Make curves", self)
        btn3.move(132, 30)
        btn1.clicked.connect(self.pushButtonClicked)
        btn2.clicked.connect(self.pushButtonClicked2)
        btn3.clicked.connect(self.pushButtonClicked3)
        self.lineEdit1 = QLineEdit('EID', self)
        self.lineEdit1.move(60, 30)
        self.lineEdit1.resize(60,25)
        self.lineEdit2 = QLineEdit(self.binnum, self)
        self.lineEdit2.move(30, 30)
        self.lineEdit2.resize(20,25)
        self.lineEdit3 = QLineEdit(self.lspost_dir, self)
        self.lineEdit3.move(30, 60)
        self.lineEdit3.resize(470,25)
        self.lineEdit1.returnPressed.connect(self.linedEditEntered1)
        self.lineEdit2.returnPressed.connect(self.linedEditEntered2)
        self.lineEdit3.returnPressed.connect(self.linedEditEntered3)

        self.combo1 = QComboBox(self)
        self.combo1.addItem("ABS_RS670")
        self.combo1.addItem("Steel")
        self.combo1.addItem("SECC")
        self.combo1.addItem("PC_HF1100R")
        self.combo1.addItem("S45C")
        self.combo1.addItem("GP35")
        self.combo1.addItem("PP_HG41TSA")
        self.combo1.addItem("STS430")
        self.combo1.move(390,30)
        self.combo1.activated[str].connect(self.ComboBoxEvent)

    def linedEditEntered1(self):
        self.EID = self.lineEdit1.text()        #ex. 40809
        self.label3.setText('Status: EID entered')
        return self.EID

    def linedEditEntered2(self):
        self.binnum = self.lineEdit2.text()
        self.label3.setText('Status: bin number entered')
        f = open('binnum.1', 'w', encoding='utf-8')
        f.write(self.binnum)
        f.close()
        return self.binnum

    def linedEditEntered3(self):
        self.lspost_dir = self.lineEdit3.text()
        self.label3.setText('Status: lspost directory entered')
        f = open('post_directory.1', 'w', encoding='utf-8')
        f.write(self.lspost_dir)
        f.close()
        return self.lspost_dir

    def ComboBoxEvent(self, text):
        rawData = read_csv('set_mat_db.1',names=['ABS_RS670', 'Steel', 'SECC', 'PC_HF1100R', 'S45C', 'GP35', 'PP_HG41TSA', 'STS430'])
        a = rawData[text]
        self.a = a[1]
        self.b = a[2]
        self.uts = a[3]
        self.label1.setText('Material: ' + text)
        return self.a, self.b, self.uts

    def append_file_name(self,fname):
        self.file_name = fname

    def append_dir_name(self,dirnames):
        self.dir_names = dirnames

    def pushButtonClicked(self):
        try:
            fname = QFileDialog.getOpenFileNames(self, 'Select curve files')
            fname = fname[0]
            self.label.setText('Path: ' + fname[0])
            self.label3.setText('Status: Curves selected')
            self.append_file_name(fname)
            self.curve_open_key = 1
            self.make_curve_key = 0
            return self.make_curve_key, self.curve_open_key
        except:
            window.show()

    def pushButtonClicked2(self):
        if self.make_curve_key == 1:
            self.label3.setText('Status : running.....')
            if self.EID == '0':
                self.label3.setText('Status : EID should be entered')
                return
            if len(self.fre) >= int(self.binnum):
                del self.fre[int(self.binnum):]
            else:
                self.label3.setText('Status : need more frequent rate lists')
                return
            if self.dir_names == '':
                self.label3.setText('Status : directory should be selected')
                return
            else:
                dir_name_window = self.CE.dir_name_change(self.dir_names)
            lspost_dir, lspost_exe = self.CE.lspostdir_divide(self.lspost_dir)
            upper_file_name_list = []
            lower_file_name_list = []
            for bin1 in range(int(self.binnum)):
                if int(bin1+1) < 10:
                    upper_file_name_list.append(self.dir_names + '/upper_' + self.curve_prefix + self.EID + '_0' + str(bin1+1))
                    lower_file_name_list.append(self.dir_names + '/lower_' + self.curve_prefix + self.EID + '_0' + str(bin1+1))
                else:
                    upper_file_name_list.append(self.dir_names + '/upper_' + self.curve_prefix + self.EID + '_' + str(bin1+1))
                    lower_file_name_list.append(self.dir_names + '/lower_' + self.curve_prefix + self.EID + '_' + str(bin1+1))
                warning_key = self.CE.cfile_making(self.dir_names, dir_name_window, str(bin1+1), self.curve_prefix, self.EID, self.cfile_name)
                if warning_key == 1:
                    self.label3.setText('Status : cfile is created')
                else:
                    self.label3.setText('Status : directory or EID is wrong')
                    return
            warning_key = self.CE.bat_making(self.dir_names, self.binnum, lspost_dir, lspost_exe, self.batch_file_name, self.cfile_name)
            if warning_key == 1:
                self.label3.setText('Status : batch file is created')
            else:
                self.label3.setText('Status : directory or EID is wrong')
                return
            curex.CurveExtract().excute_batch(self.dir_names, self.batch_file_name)
            if len(upper_file_name_list) == int(self.binnum):
                self.damage_ratio_func1(upper_file_name_list, lower_file_name_list)
            else:
                self.label3.setText('Status : the number of curve files is not enough')
                return
        elif self.curve_open_key == 1:
            self.file_name.sort()
            self.binnum = len(self.file_name)
            f = open('binnum.1', 'w', encoding='utf-8')
            f.write(str(self.binnum))
            f.close()
            self.damage_ratio_func2(self.file_name)
        else:
            self.label3.setText('Status: Curves should be selected')
            return

#ex. 40809
    def damage_ratio_func1(self, upper_file_name_list, lower_file_name_list):
        self.lv_dmg = drc.dyna_parsing1(upper_file_name_list,lower_file_name_list,self.a,self.b,self.uts,self.fre,self.time,self.binnum)
        if self.lv_dmg > 1:
            self.label2.setText('Damage ratio: ' + str(self.lv_dmg) + ' --->  파손 발생')
        else:
            self.label2.setText('Damage ratio: ' + str(self.lv_dmg) + ' --->  파손 안됨')
        return self.lv_dmg

    def damage_ratio_func2(self, file_name_list):
        self.lv_dmg = drc.dyna_parsing2(file_name_list,self.a,self.b,self.uts,self.fre,self.time,self.binnum)
        if self.lv_dmg > 1:
            self.label2.setText('Damage ratio: ' + str(self.lv_dmg) + ' --->  파손 발생')
        else:
            self.label2.setText('Damage ratio: ' + str(self.lv_dmg) + ' --->  파손 안됨')
        return self.lv_dmg

    def pushButtonClicked3(self):
        try:
            dirnames = QFileDialog.getExistingDirectory(self, 'Select directory including D3PLOT')
            self.label.setText('Path: ' + dirnames)
            if dirnames == '':
                self.label3.setText('Status: Directory should be selected')
            else:
                self.label3.setText('Status: Directory selected')
            self.append_dir_name(dirnames)
            self.make_curve_key = 1
            self.curve_open_key = 0
            return self.make_curve_key, self.curve_open_key
        except:
            window.show()

if __name__ == "__main__":
    app = QApplication(argv)
    window = MyWindow()
    window.show()
    app.exec_()
