# -*- coding: utf-8 -*- 
import os
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
  







 

