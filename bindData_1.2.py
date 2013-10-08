#-*- encoding:utf-8 -*-
import os
import string
import xlrd
import sqlite3
import random

KEY='13484605075'
#电话号码加密函数，可以加密手机号和座机号
def bind_encrypt(msg,key):
  index=msg.find('-')
  #加密座机号，加密后的号码后缀为"-区号位数"
  if index>=0:
    re=int(''.join(msg.split('-')))^int(key)
    print re
    encrypted_msg=str(re)+'-'+str(index)
  else :
    encrypted_msg=str(int(msg)^int(key))

  return encrypted_msg

if __name__ == '__main__':
  print bind_encrypt('13484605075','15062108750'),
  print bind_encrypt('0516-88718983','15062108750')

#打开Excel文件
def open_excel(excel_file):
    try:
       data = xlrd.open_workbook(excel_file)
       return data
    except Exception,e:
         print u"Excel文件打开失败"
         print str(e)

def bind_data_dispose(input_path=u"./input/",output_path=u"./output/",province_configfile=u"./config/ProvinceListConfig",excel_table_name_configfile=u"./config/ExcelTableNameConfig",description_config_path=u"./config/DescriptionConfig/"):
  input_file=os.listdir(input_path)[0] #默认input路径下只有一个文件
  data=open_excel(input_path+input_file)
  #生成男女身高体重的词典、年龄列表
  height_dic={}
  weight_dic={}
  height_dic['women']=range(155,170)
  weight_dic['women']=range(40,60)
  height_dic['man']=range(170,185)
  weight_dic['man']=range(60,80)
  age_list=range(17,35)

  #记录描述个人信息用的词典
  description={}
  files=os.listdir(description_config_path)
  for filename in files:
    fconfig=open(description_config_path+filename)
    description[filename]=fconfig.readlines()
    #print description[filename]

  db_file=sqlite3.connect(output_path+input_file.split('.')[0]+u'.db') #创建与Excel同名的db文件
  try:
    fconfig=open(province_configfile,"r")
  except Exception,e:
    print u"ProvinceListConfig文件打开失败"
    print str(e)
    return
  #读取并且简单处理省份的列表,去除空行、空格以及换行符
  province_list=fconfig.readlines()
  i=0
  for index in range(0,len(province_list)):
    province_list[i]="".join(province_list[i].split())
    if (not province_list[i].split())  :
      del province_list[i]
    else :
      i=i+1
  fconfig.close()
  province_list_length=len(province_list)
  print str(province_list_length)+u"个省级单位"
  print province_list
  try:
    fconfig=open(excel_table_name_configfile,'r')
  except Exception,e:
    print u"ExcelTableNameConfig文件打开失败"
    print str(e)
    return 
  table_name_list=fconfig.readlines()
  i=0
  for index in range(0,len(table_name_list)):
    table_name_list[i]="".join(table_name_list[i].split())
    if not table_name_list[i].split():
      del table_name_list[i]
    else:
      i+=1
  fconfig.close()
  table_name_list_length=len(table_name_list)
  print str(table_name_list_length)+u"个excel统计表"
  print table_name_list
  #数据库建表,每个省级单位名对应一个
  cursor=db_file.cursor()
  for province_name in province_list:
    cursor.execute('CREATE TABLE IF NOT EXISTS '+province_name+ ' (id integer PRIMARY KEY, name varchar(20),sex varchar(20),age integer ,height integer,weight integer,city varchar(20),zone varchar(20),type varchar(20),phone varchar(50),desc text)')
  #fconfig=open(description_config_path+'')
  
  type_list=os.listdir(description_config_path)
  table_number=data.nsheets
  #print type_list
  #print table_number

  table=data.sheets()[0]
  #print table.nrows
  #print table.ncols
  #print table.name
  #print table.col_values(0)
  i=0
  for i in range(0,table_number):
    table=data.sheets()[i]
    col_number=table.ncols
    if 0==cmp(table.name,'M-F'):    # women
      sex_value=u'women'
      desired_type=u'women'
    elif 0==cmp(table.name,'M-M'):  # gay
      desired_type=u'gay'
      sex_value=u'man'
    elif 0==cmp(table.name,'F-F'):  # lesbian
      desired_type=u'lesbian'
      sex_value=u'women'
    elif 0==cmp(table.name,'F-M'):  # man
      desired_type=u'man'
      sex_value=u'man'
    for col_index in range(0,col_number):
      #print col_index
      #print col_number
      province_name=province_list[col_index]
      phone_list=table.col_values(col_index) #获得一整列的数据
      #逐条插入数据库中对应的表文件中,第一条是城市名，从第二行开始才是电话号码
      city=phone_list[0]
      phone_list_length=len(phone_list)
      for phone_number_index in range(1,phone_list_length):
        phone_number=phone_list[phone_number_index]
        phone_number="".join(str(phone_number).split())
        if (not phone_number.split())  :    #如果空行
          continue
        phone_number=phone_number.split('.')[0] #处理会出现小数点的情况,取小数点之前的部分
        phone_number=bind_encrypt(phone_number,KEY) #电话号码加密
        #用于产生描述信息的随机数
        index_height=random.randint(0,len(height_dic[sex_value])-1)
        index_weight=random.randint(0,len(weight_dic[sex_value])-1)
        index_age=random.randint(0,len(age_list)-1)
        #print desired_type
        index_desc=random.randint(0,len(description[desired_type])-1)
        height=height_dic[sex_value][index_height]
        weight=weight_dic[sex_value][index_weight]
        age=age_list[index_age]
        desc=description[desired_type][index_desc]
        '''
        cursor.execute(u'INSERT INTO '+province_name+u'(sex,age,height,weight,city,type,phone,desc) VALUES ('+sex+u','+ str(age)+u','+str(height)+u','+str(weight)+u','+city+u','+desired_type+u','+phone_number+u','+desc+u')')
        '''
        '''
        cursor.execute(u'INSERT INTO '+province_name+u'(sex,age,height,weight,city,type,phone,desc) VALUES (?,?,?,?,?,?,?,?)',(sex_value,age,height,weight,city,desired_type,phone_number,desc))
        '''
        cursor.execute(u'INSERT INTO '+province_name+u'(name,sex,age,height,weight,city,type,phone,desc) VALUES (?,?,?,?,?,?,?,?)',(sex_value,age,height,weight,city,desired_type,phone_number,desc.decode('utf-8')))
        desc=unicode(desc,'utf-8')
        #print s1
        print u"导入数据"
        print "%s,%d,%d,%d,%s,%s,%s,%s" % (sex_value,age,height,weight,city,desired_type,phone_number,desc)
        #print sex_value,age,height,weight,city,desired_type,phone_number,unicode(desc,'utf-8')
        #cursor.execute('INSERT INTO '+province_name+'(sex) VALUES (?)',(sex_value,))
      db_file.commit()
      
#开始处理       

if __name__=='__main__':
  print u"开始导入数据"
  bind_data_dispose()
  print u"数据导入完成数据，请到output目录下查看"
  print u"按下任意键退出程序"
  raw_input()

