import os
import pandas as pd
def automatediff():
    # print("diiffff")
        # DIFF code here
    dpt =jarinfo_files
    dpt2=jarinfo_files2
    fi1 = os.listdir(dpt)
    fi2 = os.listdir(dpt2)

    uncommon_f = set(fi1).symmetric_difference(fi2)        # |
    for file in uncommon_f:                                # |
      file_path1 = os.path.join(dpt, file)                 # |   DELETING UNCOMMON FILES
      file_path2 = os.path.join(dpt2, file)                # |
      if os.path.isfile(file_path1):                       # |
          os.remove(file_path1)                            # |
      if os.path.isfile(file_path2):
          os.remove(file_path2)                            # |

    fi1.sort()
    fi2.sort()
    i=0 
    for x, y in zip(fi1, fi2): 
        # print('x ',x)
        # print('y ',y)
      
        i+=1
        path1 = os.path.join(dpt, x)
        path2 = os.path.join(dpt2, y)
        path1=path1.replace('\\', '/')
        path2=path2.replace('\\', '/')
        df1 = pd.read_excel(path1)
        df2 = pd.read_excel(path2)
        merged_df = pd.merge(df1, df2, on='Jar Name', suffixes=('_sheet1', '_sheet2'), how='outer')
        # print(merged_df)
        
        def get_version_diff(row):
          if not hasattr(get_version_diff, "has_run"):
            setattr(get_version_diff, "has_run", True)
            return ''
          if pd.isna(row['Version_sheet2']):
            return 'New Jar'
          elif pd.isna(row['Version_sheet1']):
            return 'Jar deleted in latest version'
          elif row['Version_sheet2'] != row['Version_sheet1']:
            return str(row['Version_sheet2']) + " -> " + str(row['Version_sheet1'])
          else:
            return ''

        def get_license_diff(row):
          if row['License_sheet2'] != row['License_sheet1'] and (pd.isna(row['License_sheet2'])==False or pd.isna(row['License_sheet1'])==False):
            if(pd.isna(row['License_sheet2'])==True and pd.isna(row['License_sheet1'])==False):
                return str(row['License_sheet1'])
            elif(pd.isna(row['License_sheet1'])==True and pd.isna(row['License_sheet2'])==False):
                return str(row['License_sheet2'])
            return str(row['License_sheet2']) + " -> " + str(row['License_sheet1'])
          else:
            return ''
        def get_location(row):
          if not hasattr(get_location, "has_run"):
              setattr(get_location, "has_run", True)
              return ''
          r=root_path
          r=r+'/'+x[:-5]
          r=r.replace('-','/')
          return r
        merged_df['version_diff'] = merged_df.apply(get_version_diff, axis=1)
        merged_df['license_diff'] = merged_df.apply(get_license_diff, axis=1)
        merged_df['LOCATION'] = merged_df.apply(get_location,axis=1)
        merged_df = merged_df[['Jar Name', 'Version_sheet1', 'Version_sheet2', 'License_sheet1', 'License_sheet2', 'version_diff', 'license_diff','LOCATION']]
        
        merged_df.to_excel(compare_files+x+'.xlsx', index=False)
    

    # Compare append

    pathz = compare_files

    df_list = []
    for filez in os.listdir(pathz):
        if filez.endswith(".xlsx"):
            data = pd.read_excel(os.path.join(pathz, filez))
            new_row0 = pd.DataFrame({'Jar Name': [''], 'Version_sheet1': [''],'Version_sheet2': [''],'License_sheet1': [''],'License_sheet2': [''],'version_diff':[''],'license_diff':[''],'LOCATION':['']})
            # new_row = pd.DataFrame({'Jar Name': [filez], 'Version_sheet1': [''],'Version_sheet2': [''],'License_sheet1': [''],'License_sheet2': [''],'version_diff':[''],'license_diff':['']})
            df_list.append(new_row0)
            # df_list.append(new_row)
            df_list.append(new_row0)
            
            df_list.append(data)
    merged_data = pd.concat(df_list, ignore_index=True)
    merged_data.to_excel(final_Sheet, index=False)



root_path = "C:/Progress_122" 

jarinfo_files='C:/Users/sazar/Documents/check117_8'
jarinfo_files2='C:/Users/sazar/Documents/check117_7'
compare_files="C:/Users/sazar/Documents/chckCOMPARE117/"

final_Sheet ="C:/Users/sazar/Documents/chckFinaL117.xlsx"
automatediff()