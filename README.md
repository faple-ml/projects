# projects
Some primary projects, for practice

### extrazip.py
* 解压zip文件
* 功能：
  * -i 显示压缩文件信息
  * -e 解压zip文件
    `python3 extrazip.py -e 1.zip`
  * -p 输入密码
    `python3 extrazip.py -e 1.zip -p 123456`
  * --brute-force 暴力破解 e.g. 爆破6位密码
    `python3 extrazip.py -e 1.zip --brute-force 6`
  * -s 组成密码的字符类型（l-小写字母，u-大写字母，d-数字，p-标点） e.g. 爆破6位密码，由小写字母和数字组成
    `python3 extrazip.py -e 1.zip --brute-force 6 -s l+d`
  * --dic 字典爆破
    `python3 extrazip.py -e 1.zip --dic dictionary.txt`
    
