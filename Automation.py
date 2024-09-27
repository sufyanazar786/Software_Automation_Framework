import re
import zipfile
import xml.etree.ElementTree as ET
import openpyxl
import os
import shutil
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import requests

def automate(oep):
  if(oep):
    wb = openpyxl.Workbook()      
    data=(("Jar Name","Version","License"),())
    ws = wb.active
    for i in data:
        ws.append(i)
    cc=0  
    for fn in os.scandir(oep):
      k=0
      cc+=1    
      
      if(fn.is_file() and (os.path.isfile(fn.path) and os.path.splitext(fn.path)[1]=='.jar') ):# and str(fn.path)[52:]=="commons-discovery.jar": 
        jar_path=str(fn.path)
        # jn=jar_path[30:]
        jn=os.path.basename(os.path.normpath(jar_path))                 #printing the name of jar
        print(jn)
        if('RELEASE' in jn or 'Final' in jn):
            jv = re.search(r'\d+(\.\d+)+(\.\w+)?', jn).group()
            jname = jn.replace("-" + jv, "").replace(".jar", "")
        else:
          name = jn.replace(".jar", "")
          match = re.search(r'\d+(\.\d+)+(\.\w+)?', name)
          if not match:
            jname=name
            jv=-1
          else:
            pattern = r'^(?P<name>[a-zA-Z]+)-(?P<version>[\d\.a-zA-Z-]+)\.jar$'
            match = re.match(pattern, jn)      
            if(re.search(r'^(.+?)-([\d.]+)\.jar$', jn)):
              match1=re.search(r'^(.+?)-([\d.]+)\.jar$', jn)
              jname = match1.group(1)
              jv=match1.group(2)
            elif match:
              jname = match.group('name')
              jv = match.group('version')
            else:
              jname=jn[:-4]
              jv=-1
        #version having alphabets-------------------------------
        pattern = r'^([\w-]+)-([\d\.]+[a-zA-Z]*[\d]*)\.jar$'
        match = re.match(pattern, jn)
        if match:
            jar_name = match.group(1)
            jar_version = match.group(2)
            if any(c.isalpha() for c in jar_version):
                pattern = r'^(.*)-([\w\.]+)\.jar$'
                match1 = re.match(pattern, jn)
                if match1:
                    jname = match1.group(1)
                    jv = match1.group(2)  
       
        num=-2
        cnt=0
        if(jv==-1):
          with zipfile.ZipFile(jar_path, 'r') as jar_file:
            file_list = jar_file.namelist()
            
            if('META-INF/' in file_list and 'META-INF/MANIFEST.MF' in file_list):
              manifest = jar_file.read('META-INF/MANIFEST.MF')
              for line in manifest.splitlines():
                  if line.startswith(b'Implementation-Version:'):
                      cnt+=1
                      jv= line.split(b':')[1].strip().decode('utf-8')
                      if(re.search(r'^\d+\.\d+\.\d+', jv)):
                        jv = re.search(r'^\d+\.\d+\.\d+', jv).group(0)
                      num=0
            
        if(cnt>1):
          jv=-1
        
        p=OEjars+jname+'.jar'   # p has C:/Users/sazar/Desktop/OEjars/oelogging-12.7.0.jar
        isOE = os.path.exists(p)  
        if(isOE):                                          # Check for OpenEdge jar
          # to=(jn,"OpenEdge jar")
          # ws.append(to)
          # print("OE")
          continue
        if(jn[0:8]=="javahelp" or jn[0:4]=="soap" or jn[0:13]=="xmlParserAPIs" or jn[0:3]=="xsd" or jn[0:7]=="common-" or jn[0:5]=="ecore"):
          tp=(jname,jv,"No info")
          ws.append(tp)
          continue
                    

        with zipfile.ZipFile(jar_path, 'r') as jar_file:
          lic = None
          pom=None
          for file_path in jar_file.namelist():
              if file_path.endswith('LICENSE.txt') or file_path.endswith('LICENSE') or file_path.endswith('license') or file_path.endswith('license.txt'):
                lic = file_path
                break
          for file_path in jar_file.namelist():
              if file_path.endswith('pom.xml') or file_path.endswith('pom'):
                pom = file_path
                break
          if lic:
            lic_data = jar_file.read(lic)
            s=str(lic_data)
            # print(s)  and (ord(s[d-3])>47 and ord(s[d-3])<58)
            if(s.find("COMMON DEVELOPMENT")>=0 and s.find("COMMON DEVELOPMENT")<30):
              v=s.find("Version")
              if(v<65):
                v2="COMMON DEVELOPMENT AND DISTRIBUTION LICENSE (CDDL) Version "+s[v+8:v+11]
                w=(jname,jv,v2)
                ws.append(w)
                k=1
            elif(s.find("Apache License")>=0 and s.find("Apache License")<200 or (s.find("Apache Software License")>=0 and s.find("Apache Software License")<200)):
              v=s.find("Version")
              d=v+11
              if(v<200 and (ord(s[d-3])>47 and ord(s[d-3])<58)):
                v2="Apache License, "+s[v:d]
                w=(jname,jv,v2)
                ws.append(w)
                k=1
            
          if pom:
            if(lic):
              continue
            #pom is present
            with zipfile.ZipFile(jar_path, 'r') as myzip:
              with myzip.open(pom) as myfile:
                  tree = ET.parse(myfile)
                  root = tree.getroot()
                  
                  
                  b=root.find('{http://maven.apache.org/POM/4.0.0}licenses')
                  if(b!=None):
                    # if(b.findall('{http://maven.apache.org/POM/4.0.0}license')):
                    a=b.findall('{http://maven.apache.org/POM/4.0.0}license')
                    linfo=""
                    ln=len(a)
                    for x in a:
                      if(x.find('{http://maven.apache.org/POM/4.0.0}name')!=None):
                        nm=x.find('{http://maven.apache.org/POM/4.0.0}name').text
                        linfo=linfo+nm
                        if(len(a)>1 and ln>1):
                          linfo+=" ; "
                          ln-=1
                    tpom=(jname,jv,linfo)
                    ws.append(tpom)
                    k=1
                                  
                  
        
        if(k!=1):
          match = re.search(r'^(.+?)-([\d.]+)\.jar$', jn)                                     # Regex to get the jar name and version also
          if('RELEASE' in jn or 'Final' in jn or 'release' in jn or 'final' in jn):
            ver = re.search(r'\d+(\.\d+)+(\.\w+)?', jn).group()
            name = jn.replace("-" + ver, "").replace(".jar", "")
            
          elif match:
            name = match.group(1)
            ver = match.group(2)
          else:
            name=jname
            ver=jv
          if(num==0):
            artifact_id=jname
            version=jv
          else:
            artifact_id = name
            version = ver
          # print('j ',name,' v ',ver)
          # if(version==-1):
          #   continue
          if(jv!=-1):
            maven_url = f"https://search.maven.org/solrsearch/select?q=a:{artifact_id}&wt=xml" # API to get groupid from mvn
            response = requests.get(maven_url)
            i=""
            j=0
            if response.status_code == 200:
              root = ET.fromstring(response.content)
              
              while(j>=0):
                try:
                  gid = root.findall(".//str[@name='g']")[j]
                except IndexError:
                  tpl=(jname,jv,"Not found")
                  ws.append(tpl)
                  break
                j+=1
                url=(f"https://mvnrepository.com/artifact/{gid.text}/{artifact_id}/{version}")
                rp=requests.get(url)
                if rp.status_code == 404:
                  continue
                # print(f"The group ID of {artifact_id} version {version} is {group_id.text}")
                # print(url)
                service = Service('C:/Users/sazar/AppData/Local/Programs/Python/Python311/PythonVS1/chromedriver.exe')
                driver = webdriver.Chrome(service=service)
                # driver = webdriver.Chrome('C:/Users/sazar/AppData/Local/Programs/Python/Python311/PythonVS1/chromedriver.exe')
                driver.get(url)           
                
                lics= driver.find_elements(By.TAG_NAME,'main')
                # a=lics.find_elements(By.TAG_NAME,'div')
                
                ls=[]
                for i in lics:
                  ls.append(i.text)
                # print(ls)
                if len(ls)==0:
                  print("No content in License")
                  continue       
                if(ls[0].find('Licenses')):
                  k=(ls[0].find('Licenses'))
                  j=-1
                else:
                  print("No license info")
                  continue
                k=k+21
                kk=k+200
                st=ls[0][k:kk]
                ans=""
                jl=[]
                ss=""
                for i in range(len(st)):
                  ss+=st[i]
                  if(st[i]=="\n"):
                    jl.append(ss)
                    ss=""
                for i in range(len(jl)):                      #
                  if(i==0):                                   #
                    ans+=jl[i]                                #storing license and excluding the url below
                    continue
                  if("http" in jl[i]):
                    ans+=jl[i]
                ans=ans.strip()
                ans2 = re.sub(r"http\S+", "",ans)
                # print(ans)

                # for i in range(len(st)):
                #   if(st[i]=='\n'):
                #     if(st[i+1:i+1+7]=="Indexed" or st[i+1:i+1+10]=="Developers" or st[i+1:i+1+7]=="Mailing"):
                #       break
                #   ans+=st[i] 
                
                t=(name,ver,ans2)
                ws.append(t)  
          else:
            t=(jname,jv,'Not found')
            ws.append(t)
        sub="oemgmt"
        sub2="OpenEdge"
      
        if("oemgmt" in oep):
          indx=oep.index(sub)
          xl=oep[indx:]                         # This part is for slicing root_path 
        elif("OpenEdge" in oep):                # (to remove C:/Progress_122 from path and remain with for ex; oemgmt/jars)
          indx2=oep.index(sub2)
          xl=oep[indx2:]
        xl=xl.replace('\\','-')
        # print(xl)
        wb.save(jarinfo_files+xl+'.xlsx')
        
        
  #--------------------------------------------------------


'''

`|`  |\  | | ```|``` |   /\   ```|``` |````       |   |  |```` |```) |````
 |   | \ | |    |    |  /--\     |    |---        |---|  |---  |__/  |---
_|_  |  \| |    |    | /    \    |    |____       |   |  |____ |  \  |____

'''

  #  THE ACTUAL INITIAL STEP FOR RUNNING CODE - 

root_path = "C:/Progress_122"               

OEjars ="C:/Users/sazar/Desktop/OEjars"

jarinfo_files="C:/Users/sazar/Documents/check122_a/"                                             # NOTE: Change this folder path when the code is executed for 2nd time 


jar_files = []
for root, direc, files in os.walk(root_path):
  for file in files:
    if file.endswith(".jar"):
      if(root not in jar_files):
          jar_files.append(root)

for jar_fpath in jar_files:
    if("oeide" not in str(jar_fpath) and "archive" not in str(jar_fpath) and "jdk" not in str(jar_fpath)):
      automate(jar_fpath)

# automate('diff')

