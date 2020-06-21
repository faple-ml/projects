#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import zipfile
import datetime
import argparse
import os
from itertools import product
from threading import Thread
import string
"""
功能：
    1. 解压缩包（无密码)
        python3 extrazip.py -e 1.zip
    2. 解压缩包（有密码）
        python3 extrazip.py -e 1.zip -p 123456
    3. 爆破压缩包密码
        python3 extrazip.py -e 1.zip --brute-force
    4. 字典爆破
        python3 extrazip.py -e 1.zip --dic dic.txt
"""

def print_info(archive):
    print("Archive: ", archive)
    print("Name \t Last Modified Date \t Compressed Size \t Uncompressed Size")
    print("---- \t ------------------ \t --------------- \t -----------------")
    with zipfile.ZipFile(archive) as zf:
        for info in zf.infolist():
            modified_date = datetime.datetime(*info.date_time)
            print(info.filename,"\t",modified_date,"\t",info.compress_size,"\t\t\t",info.file_size)

def extract_archive(archive):
    print_info(archive)
    print("\nStart extracting...")
    if os.path.isdir(archive.replace('.zip','')):
        filename=archive.replace('.zip','')+'_extract'
        os.mkdir(filename)
    else:
        filename=archive.replace('.zip', '')
        os.mkdir(filename)
    with zipfile.ZipFile(archive) as zf:
        for file in zf.namelist():
            zf.extract(file, filename+'/')
    print("Extract finish.")

def extract_with_password(archive, password):
    print_info(archive)
    print("\nStart extracting...")
    if os.path.isdir(archive.replace('.zip', '')):
        filename = archive.replace('.zip', '') + '_extract'
        os.mkdir(filename)
    else:
        filename = archive.replace('.zip', '')
        os.mkdir(filename)
    with zipfile.ZipFile(archive, 'r') as zf:
        try:
            zf.extractall(path=filename+'/', pwd=str.encode(password))
            print("Extract finish.")
        except Exception as ex:
            print(ex)


class ExtractFile:
    def __init__(self):
        self.result = False

    def run(self, zf, pwd, path):
        try:
            
            zf.extractall(path=path, pwd=str.encode(pwd))
        except Exception as ex:
            self.result=False
            # print(".",end=".")
            return
        # print("True")
        print("Extract finish. \nPassword:", pwd)
        self.result=True
        return

    def get_result(self):
        return self.result

def brute_force_pwd(archive, bit, supplement):
    print_info(archive)
    print("\nStart extracting...")
    if os.path.isdir(archive.replace('.zip', '')):
        filename = archive.replace('.zip', '') + '_extract'
        os.mkdir(filename)
    else:
        filename = archive.replace('.zip', '')
        os.mkdir(filename)

    strs=[]
    if supplement=='*':
        strs=[chr(i) for i in range(33,127)]
    else:
        s=supplement.split('+')
        for i in s:
            if i=='l':
                strs+=list(string.ascii_lowercase)
            elif i=='u':
                strs+=list(string.ascii_uppercase)
            elif i=='d':
                strs+=list(string.digits)
            elif i=='p':
                al = [chr(i) for i in range(33, 127)]
                temp = list(string.ascii_letters + string.digits)
                strs += list(set(al).difference(set(temp)))
            else:
                print("Wrong supplement!")
                return
    ef=ExtractFile()
    zf=zipfile.ZipFile(archive)
    for item in product(strs, repeat=bit):
        passwd="".join(item)
        t=Thread(target=ef.run, args=(zf, passwd, filename+'/'))
        t.start()
        if ef.get_result():
            return

def brute_force_dic(archive, dic):
    print_info(archive)
    print("\nStart extracting...")
    if os.path.isdir(archive.replace('.zip', '')):
        filename = archive.replace('.zip', '') + '_extract'
        os.mkdir(filename)
    else:
        filename = archive.replace('.zip', '')
        os.mkdir(filename)

    ef=ExtractFile()
    zf = zipfile.ZipFile(archive)
    with open(dic,'r') as f:
        for line in f:
            passwd=line.replace('\n','')
            t = Thread(target=ef.run, args=(zf, passwd, filename + '/'))
            t.start()
            if ef.get_result():
                return

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description="This is a description.")
    parser.add_argument('-i', '--info', dest='zf_i', help='show infomation of the zip file')
    parser.add_argument('-e', '--extract', dest='zf_e', help='extract an archive')
    parser.add_argument('-p', '--password', dest='password', help='extract an archive with password')
    parser.add_argument('--brute-force', type=int, dest='bit', help='brute force the password')
    parser.add_argument('-s', '--supplement', dest='supplement', help='set type of strings in the password, e.g. l+d = lower letters and digitals')
    parser.add_argument('--dic', dest='dic', help='brute force the password using a dictionary')
    args=parser.parse_args()
    if args.zf_i:
        print_info(args.zf_i)
    if args.zf_e:
        if args.password:
            extract_with_password(args.zf_e, args.password)
        elif args.bit:
            if args.supplement:
                brute_force_pwd(args.zf_e, args.bit, args.supplement)
            else:
                brute_force_pwd(args.zf_e, args.bit, '*')
        elif args.dic:
            brute_force_dic(args.zf_e, args.dic)
        else:
            extract_archive(args.zf_e)