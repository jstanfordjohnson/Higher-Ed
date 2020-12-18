## DATA WRANGLING | Create dataset to determine the cohort program components most predictive of 4- and 5-year graduation from Spelman.
# Code written by J. Johnson
# 12/12/2020

# Import data
import pandas
import seaborn as sn
#import matplotlib.pyplot as plt
import xlsxwriter

# Import FTFT Cohort data
df_2013 = pandas.read_excel('Fall_2013_FTFT_Cohort.xlsx', sheet_name='Fall_2013_Cohort_IPEDS_Reported')
df_2014 = pandas.read_excel('Fall_2014_FTFT_Cohort.xlsx', sheet_name='Fall_2014_FTFT_Cohort')
df_2015 = pandas.read_excel('Fall 2015 Cohort List.xlsx', sheet_name='Fall_2015_FTFT_Cohort_IPEDS')
df_2016 = pandas.read_excel('Fall_2016_First-Time_Full-Time_Cohort.xlsx', sheet_name='Sheet1')

# Import graduation data
#grad_df = pandas.read_excel('1983-2018_Graduates_data_for_NSC_FINAL with Major.xlsx', sheet_name='1983-2018_Graduates_FINAL')
grad_df = pandas.read_excel('2015 to 2020 Graduates_final CUM_GPA.xlsx', sheet_name='2015 to 2020 Graduates')

# Import PELL data
df_pell2013 = pandas.read_excel('Fall_2013_FirstGen_Enrollment_Pell_Recipients_ATI.xlsx', sheet_name='Fall_2013_FirstGen_Enrollment_P')
df_pell2014 = pandas.read_excel('Fall_2014_FirstGen_Enrollment_Pell_Recipients_ATI.xlsx', sheet_name='Fall_2014_FirstGen_Enrollment_P')
df_pell2015 = pandas.read_excel('Fall_2015_FirstGen_Enrollment_Pell_Recipients_ATI.xlsx', sheet_name='Fall_2015_FirstGen_Enrollment_P')
df_pell2016 = pandas.read_excel('Fall_2016_FirstGen_Enrollment_Pell_Recipients_ATI.xlsx', sheet_name='Fall_2016_FirstGen_Enrollment_P')


# Import first generation data
firstgen_df2013 = pandas.read_excel('First_Generation_201309.xlsx', sheet_name='First_Generation_201309')
firstgen_df2014 = pandas.read_excel('First_Generation_201409.xlsx', sheet_name='First_Generation_201409')
firstgen_df2015 = pandas.read_excel('First_Generation_201509.xlsx', sheet_name='First_Generation_201509')
firstgen_df2016 = pandas.read_excel('First_Generation_201609.xlsx', sheet_name='First_Generation_201609')

# Import special population data
wistem_df = pandas.read_excel('2013 WiSTEM Cohort.xlsx', sheet_name='ssc-search-2020-12-12')
honors_df = pandas.read_excel('Honors Program 2007 to 2017.xlsx', sheet_name='ssc-search-2019-07-03 (1)')
research_df = pandas.read_excel('2008-17 Research Day Dataset.xlsx', sheet_name='2008 to 2017 Research Day Datas')
bonner_df = pandas.read_excel('2013-16 Bonner Cohorts.xlsx', sheet_name='Sheet1')
rise_df = pandas.read_excel('RISE Scholars 2008-2019.xlsx', sheet_name='Sheet1')

# For inspection, print whole sheet data
"""print(df_2013)
print(df_2014)
print(df_2015)
print(df_2016)
print(grad_df)"""
#print(df_pell2016)
#print(firstgen_df2013)

# Print column names
# iterating the columns 
#for col in research_df.columns: 
#    print(col)

# Desired column names: TERM_CODE_KEY, ID, LAST_NAME, FIRST_NAME, MIDDLE_INITIAL
# df_2013 is properly named

# df_2014 is properly named

# df_2015 needs column renaming
df_2015.rename(columns={'STUDENT_ID': 'ID'}, inplace=True)
df_2015['TERM_CODE_KEY'] = 201509
#print(df_2015)

# df_2016 needs column renaming
df_2016.rename(columns={'SP_ID': 'ID', 'TERM_CODE': 'TERM_CODE_KEY', 'LNAME': 'LAST_NAME', 'FNAME' : 'FIRST_NAME', 'MI' : 'MIDDLE_INITIAL'}, inplace=True)
#print(df_2016)

# Concatenate the four data frames
df_3 = df_2013[['ID','LAST_NAME', 'FIRST_NAME', 'MIDDLE_INITIAL', 'TERM_CODE_KEY']]
df_4 = df_2014[['ID','LAST_NAME', 'FIRST_NAME', 'MIDDLE_INITIAL', 'TERM_CODE_KEY']]
df_5 = df_2015[['ID','LAST_NAME', 'FIRST_NAME', 'MIDDLE_INITIAL', 'TERM_CODE_KEY']]
df_6 = df_2016[['ID','LAST_NAME', 'FIRST_NAME', 'MIDDLE_INITIAL', 'TERM_CODE_KEY']]

df = pandas.concat([df_3, df_4, df_5, df_6])
#print(df)

pell3 = df_pell2013[['SPRIDEN_ID', 'RPRAWRD_FUND_CODE']]
pell4 = df_pell2014[['SPRIDEN_ID', 'RPRAWRD_FUND_CODE']]
pell5 = df_pell2015[['SPRIDEN_ID', 'RPRAWRD_FUND_CODE']]
pell6 = df_pell2016[['SPRIDEN_ID', 'RPRAWRD_FUND_CODE']]

pell = pandas.concat([pell3, pell4, pell5, pell6])
#print(pell)

fgen3 = firstgen_df2013[['SPRIDEN_ID', 'FIRST GENERATION']]
fgen4 = firstgen_df2014[['SPRIDEN_ID', 'FIRST GENERATION']]
fgen5 = firstgen_df2015[['SPRIDEN_ID', 'FIRST GENERATION']]
fgen6 = firstgen_df2016[['SPRIDEN_ID', 'FIRST GENERATION']]

fgen = pandas.concat([fgen3, fgen4, fgen5, fgen6])
#print(pell)

# Check row count
total1 = df.shape[0]
total2 = df_3.shape[0] + df_4.shape[0] + df_5.shape[0] + df_6.shape[0]
#print(total1)
#print(total2)

# Merge columns: STUDENT_ID, GRADUATION_TERM, MAJOR
grad_df.rename(columns={'SP_ID': 'ID'}, inplace=True)
pell.rename(columns={'SPRIDEN_ID': 'ID'}, inplace=True)
fgen.rename(columns={'SPRIDEN_ID': 'ID'}, inplace=True)
wistem_df.rename(columns={'Student External ID': 'ID'}, inplace=True)
honors_df.rename(columns={'Student External ID': 'ID'}, inplace=True)
bonner_df.rename(columns={'Student External ID': 'ID', 'Bonner Program': 'Bonner'}, inplace=True)
research_df.rename(columns={'Spelman ID': 'ID', 'Research Day': 'ResearchDay'}, inplace=True)

wistem = wistem_df[['ID', 'WiSTEM']]
honors = honors_df[['ID', 'Honors']]
bonner = bonner_df[['ID', 'Bonner']]
research = research_df[['ID', 'ResearchDay']]
rise = rise_df[['ID', 'RISE']]

grads = grad_df[['ID', 'TERM_CODE_GRAD', 'CUM_GPA']]
gdf = pandas.merge(df, grads, how='left', on='ID')
gdf2 = pandas.merge(gdf, pell, how='left', on='ID')
gdf3 = pandas.merge(gdf2, fgen, how='left', on='ID')
gdf4 = pandas.merge(gdf3, wistem, how='left', on='ID')
gdf5 = pandas.merge(gdf4, honors, how='left', on='ID')
gdf6 = pandas.merge(gdf5, bonner, how='left', on='ID')
gdf7 = pandas.merge(gdf6, research, how='left', on='ID')
gdf8 = pandas.merge(gdf7, rise, how='left', on='ID')


#gdf3 = pandas.concat([df, grads, pell, fgen], axis=1, sort=False)
#gdf3 = df.merge(grads,on='ID').merge(pell,on='ID').merge(fgen,on='ID')
df_new = gdf8.drop_duplicates().reset_index(drop=True)
df_new['Count Special'] = df_new[['WiSTEM', 'Honors', 'Bonner', 'ResearchDay', 'RISE']].apply(lambda x: 5 - x.isnull().sum(), axis='columns')
df_new['Faculty Mentor'] = 0
df_new['Peer Mentor'] = 0
df_new['Scholarship/Stipend'] = 0
df_new['Research'] = 0
df_new['Student Development'] = 0

df_new['In Cohort?'] = df_new['Count Special'].apply(lambda x: 'Y' if x > 0 else 'N')

# Place "hash marks" under each applicable program component
df_new.loc[df_new.WiSTEM.notnull(), ['Faculty Mentor', 'Peer Mentor', 'Scholarship/Stipend', 'Student Development']] += 1
df_new.loc[df_new.Honors.notnull(), ['Faculty Mentor', 'Scholarship/Stipend', 'Student Development']] += 1
df_new.loc[df_new.Bonner.notnull(), ['Scholarship/Stipend', 'Student Development']] += 1
df_new.loc[df_new.ResearchDay.notnull(), ['Faculty Mentor', 'Research']] += 1
df_new.loc[df_new.RISE.notnull(), ['Faculty Mentor', 'Research', 'Scholarship/Stipend', 'Student Development']] += 1

df_new['Mentorship'] = df_new['Faculty Mentor'] + df_new['Peer Mentor']
df_new['Spel Grad?'] = df_new['TERM_CODE_GRAD'].notnull()
df_new['TERM_CODE_GRAD_YR'] = df_new['TERM_CODE_GRAD'].astype(str).str[:4]
df_new['TERM_CODE_KEY_YR'] = df_new['TERM_CODE_KEY'].astype(str).str[:4]
df_new['TERM_CODE_GRAD_YR'] = df_new['TERM_CODE_GRAD_YR'].astype('float')
df_new['TERM_CODE_KEY_YR'] = df_new['TERM_CODE_KEY_YR'].astype('float')
#print(df_new['TERM_CODE_KEY_YR'])
df_new['Yrs Enrolled'] = df_new['TERM_CODE_GRAD_YR'] - df_new['TERM_CODE_KEY_YR']
df_new['Yrs Enrolled'] = df_new['Yrs Enrolled'].astype('float')
#print(df_new['Yrs Enrolled'])
df_new['Years to Grad'] = df_new['Yrs Enrolled'].fillna('Has not graduated')
#df_new['Years to Grad'] = df_new['Yrs Enrolled'].apply(lambda x: 'Four years' if x == 4.0 else ('More than four years' if x > 4.0 else ('Less than four years' if x < ))
del df_new['TERM_CODE_GRAD_YR']
del df_new['TERM_CODE_KEY_YR']

df_new['Yrs Enrolled'].fillna(0, inplace=True)
df_new['FIRST GENERATION'].fillna('N', inplace=True)
df_new['RPRAWRD_FUND_CODE'].fillna('NOT PELL', inplace=True)
#print(df_new.dtypes)

## Write to Excel file
writer = pandas.ExcelWriter('Cohort Dataset.xlsx', engine='xlsxwriter')
df_new.to_excel(writer, sheet_name='Sheet1')
writer.save()
df_new.to_csv('Cohort Dataset.csv', index=False)

'''
# X = feature values, all the columns except the last column
X = df_new[['RPRAWRD_FUND_CODE', 'FIRST GENERATION', 'Count Special', 'Faculty Mentor', 'Peer Mentor', 'Scholarship/Stipend', 'Research', 'Student Development', 'Years to Grad', 'Spel Grad?']].iloc[:,:-1]

# y = target values, last column of the data frame
y = df_new[['RPRAWRD_FUND_CODE', 'FIRST GENERATION', 'Count Special', 'Faculty Mentor', 'Peer Mentor', 'Scholarship/Stipend', 'Research', 'Student Development', 'Years to Grad', 'Spel Grad?']].iloc[:,-1]

# filter out the applicants that got admitted
graduated = df_new.loc[y == True]

# filter out the applicants that din't get admission
not_graduated = df_new.loc[y == False]

# plots
plt.scatter(graduated.iloc[:, 0], graduated.iloc[:, 1], s=10, label='Graduated')
plt.scatter(not_graduated.iloc[:, 0], not_graduated.iloc[:, 1], s=10, label='Not Graduated')
plt.legend()
plt.show()
'''

'''# Correlation Matrix
corrMatrix = X.corr()
sn.heatmap(corrMatrix, annot=True)
plt.show()'''