from os import path
from subprocess import call
# import time

# dir_name = 'D:/LGE/1.1 work_others/damage_ratio/new_ver4'
# bin = '16'
# EID = '32342'
# lspost_dir = 'C:\Program Files\LSTC\LS-PrePost 4.6\lsprepost4.6_x64.exe'

# batch_file_name = 'stress_curve_extract.bat'
# cfile_name = 'stress_curve_extract.cfile'
# curve_prefix = 'stress_curve_'

class CurveExtract:
#     def sleep__(self, now):
#         time.sleep(now)
#         return

    def dir_name_change(self, dir_name):
        dir_name_list = dir_name.split('/')
        dir_name_window = '\\'.join(dir_name_list)
        return dir_name_window

    def lspostdir_divide(self, lspost_dir):
        lspost_dir_list = lspost_dir.split('\\')
        lspost_exe = lspost_dir_list[-1]
        lspost_dir_list.pop()
        lspost_dir = '\\'.join(lspost_dir_list)
        return lspost_dir, lspost_exe

    def cfile_making(self, dir_name, dir_name_window, bin, curve_prefix, EID, cfile_name):
        try:
            if int(bin) < 10:
                msg = 'open d3plot "' + dir_name_window + '\\' + str(bin) + '\\d3plot"\nac\nfringe 9\npfringe\nident  select 1\ngenselect target element\ngenselect element add shell ' + EID + '/0\nshellsurf upper\netime 9 -2 ' + EID + '\nxyplot 1 savefile curve_file "' + dir_name_window + '\\' + 'upper_' + curve_prefix + EID + '_0' + bin + '" 1 all\ndeletewin 1\nclearpick\ngenselect target element\nmodel remove 1\nexit'
            else:
                msg = 'open d3plot "' + dir_name_window + '\\' + str(bin) + '\\d3plot"\nac\nfringe 9\npfringe\nident  select 1\ngenselect target element\ngenselect element add shell ' + EID + '/0\nshellsurf upper\netime 9 -2 ' + EID + '\nxyplot 1 savefile curve_file "' + dir_name_window + '\\' + 'upper_' + curve_prefix + EID + '_' + bin + '" 1 all\ndeletewin 1\nclearpick\ngenselect target element\nmodel remove 1\nexit'
            f = open(dir_name + '/' + bin + '/upper_' +cfile_name, 'w', encoding='utf-8')     # txt파일 생성
            f.write(msg)
            f.close()
            if int(bin) < 10:
                msg = 'open d3plot "' + dir_name_window + '\\' + str(bin) + '\\d3plot"\nac\nfringe 9\npfringe\nident  select 1\ngenselect target element\ngenselect element add shell ' + EID + '/0\nshellsurf lower\netime 9 -2 ' + EID + '\nxyplot 1 savefile curve_file "' + dir_name_window + '\\' + 'lower_' + curve_prefix + EID + '_0' + bin + '" 1 all\ndeletewin 1\nclearpick\ngenselect target element\nmodel remove 1\nexit'
            else:
                msg = 'open d3plot "' + dir_name_window + '\\' + str(bin) + '\\d3plot"\nac\nfringe 9\npfringe\nident  select 1\ngenselect target element\ngenselect element add shell ' + EID + '/0\nshellsurf lower\netime 9 -2 ' + EID + '\nxyplot 1 savefile curve_file "' + dir_name_window + '\\' + 'lower_' + curve_prefix + EID + '_' + bin + '" 1 all\ndeletewin 1\nclearpick\ngenselect target element\nmodel remove 1\nexit'
            g = open(dir_name + '/' + bin + '/lower_' +cfile_name, 'w', encoding='utf-8')     # txt파일 생성
            g.write(msg)
            g.close()
            warning_key = 1
            return warning_key
        except:
            warning_key = 0
            return warning_key

    def bat_making(self, dir_name, bin, lspost_dir, lspost_exe, batch_file_name, cfile_name):
        try:
            f = open(dir_name + '/upper_' + batch_file_name, 'w', encoding='utf-8')
            f.write('cd /d ' + lspost_dir + '\n')
            f.close()
            g = open(dir_name + '/lower_' + batch_file_name, 'w', encoding='utf-8')
            g.write('cd /d ' + lspost_dir + '\n')
            g.close()
            for bin in range(int(bin)):
                msgg = lspost_exe + ' c="' + dir_name + '/' + str(bin+1) + '/upper_' + cfile_name + '" -nographics\n'
                mmsgg = lspost_exe + ' c="' + dir_name + '/' + str(bin+1) + '/lower_' + cfile_name + '" -nographics\n'
                f = open(dir_name + '/upper_' + batch_file_name, 'a', encoding='utf-8')     # txt파일 생성
                f.write(msgg)
                g = open(dir_name + '/lower_' + batch_file_name, 'a', encoding='utf-8')     # txt파일 생성
                g.write(mmsgg)
            f.close()
            warning_key = 1
            return warning_key
        except:
            warning_key = 0
            return warning_key

    def excute_batch(self, dir_name, batch_file_name):
        try:
            call(dir_name + '/upper_' + batch_file_name)
            call(dir_name + '/lower_' + batch_file_name)
            warning_key = 1
            return warning_key
        except:
            warning_key = 0
            return warning_key

    def isfile_check(self, dir_name, bin, curve_prefix, EID):
        if int(bin) < 10:
            if path.isfile(dir_name + '/' + curve_prefix + EID + '_0' + bin):
                isfile_key = 1
            else:
                isfile_key = 0
        else:
            if path.isfile(dir_name + '/' + curve_prefix + EID + '_' + bin):
                isfile_key = 1
            else:
                isfile_key = 0
        return isfile_key

    def curve_extract(self, fname):
        data = open(fname).readlines()      #fname = 'D:/LGE/1.1 work_others/damage_ratio/new_ver4/17'
        start = 0
        end = 0
        offset1 = 0
        offset2 = 20
        col1 = []
        col2 = []
        for i, line in enumerate(data):
            line = line.lower()
            if '* maxval' in line:
                start = i+1
            if 'endcurve' in line:
                end = i
                id = str(data[start - 3]).split(' ')    
            for ii in range(start, end):
                col1.append(float(data[ii][offset1:offset2].replace(" ", "")))
                col2.append(float(data[ii][offset1+20:offset2+20].replace(" ", "")))
        return col1, col2
