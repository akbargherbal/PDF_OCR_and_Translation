#!/usr/bin/env python
# coding: utf-8

# # IMPORT

# In[1]:


#!pip install regex


# In[2]:

# HLPER FUNCTION: Get Time Now:
from datetime import datetime
def time_now():
    '''Get Current Time'''
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    return now


############
print('Starting...')
start = time_now()
############


import regex as re


# In[3]:


import io
import os
from google.cloud import vision
import PyPDF2
import pikepdf
import subprocess


# # CREDENTIALS

# In[4]:


# cred_file points to the API key that you would need to download from Google
# The key should be enabled to use the credential file
cred_file = r'translate_cloud_serv_account_key.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_file


# # FUNCTION 1

# In[5]:


# 한 번에 최대 5페이지까지 text 추출 가능

# 첫 페이지는 .txt 파일을 생성해주어야 하므로 1~5 페이지는 따로 처리
def pdf2txt_w(path_num):
    pages = [1,2,3,4,5]
    requests = [{"input_config": input_config, "features": features, "pages": pages}]
    response = client.batch_annotate_files(requests=requests)

    for num, image_response in enumerate(response.responses[0].responses):
#         print(u"Full text: {}".format(image_response.full_text_annotation.text))
        if (num==0):
            with open(destination_path[path_num] + file_name[0:-4] + '.txt', "w",encoding='UTF-8') as f:
                f.write(response.responses[0].responses[num].full_text_annotation.text)
        else:
            with open(destination_path[path_num] + file_name[0:-4] + '.txt', "a",encoding='UTF-8') as f:
                f.write(response.responses[0].responses[num].full_text_annotation.text)


# # FUNCTION 2

# In[6]:


def pdf2txt(page, path_num):
    pages = [i for i in range(page, page+5)]
    requests = [{"input_config": input_config, "features": features, "pages": pages}]
    response = client.batch_annotate_files(requests=requests)

    for num, image_response in enumerate(response.responses[0].responses):
#         print(u"Full text: {}".format(image_response.full_text_annotation.text))

        with open(destination_path[path_num] + file_name[0:-4] + '.txt', "a",encoding='UTF-8') as f:
                f.write(response.responses[0].responses[num].full_text_annotation.text)


# # CREATE A UNIQUE PROJECT NAME

# In[7]:


try:
    project_name = input(str('''
    Choose a name for the Project Directory:
    Then press any key!

    '''))
    os.mkdir(project_name)
    proj_abs_path = os.path.abspath(project_name)
    print(f'''
    A project was created in:
    {proj_abs_path}
    ''')
except:
    increment = 1
    while project_name in os.listdir():
        project_name = re.sub('_copy_.*', '', project_name)
        project_name = project_name + f'_copy_{str(increment).zfill(2)}'
        increment += 1
    os.mkdir(project_name)
    proj_abs_path = os.path.abspath(project_name)
    print(f'''
    The project name already EXISTS!
    A copy of that name was created in the following path:
    {proj_abs_path}
    ''')    


# In[8]:


os.mkdir(f'./{project_name}/input_files')
os.mkdir(f'./{project_name}/output_files')


# In[ ]:





# In[9]:


#######################################################################
## source_path와 destination_path에 폴더가 들어가 있으면 에러남
## source_path엔 .pdf 파일만! destination_path는 가급적 빈 폴더!
source_path = [f"./{project_name}/input_files/"]
destination_path = [f"./{project_name}/output_files/"]
#######################################################################


# In[10]:


open_n_expl_input_files = os.path.abspath(source_path[0])


# In[11]:


subprocess.Popen(f'explorer /open,{open_n_expl_input_files}')


# In[12]:


print(f'''
Copy input files to the input_files directory;
ONLY PDF FILES ARE ALLOWED!
This is the directory:
{open_n_expl_input_files}
''')


# In[13]:


while(
    len(
        os.listdir(open_n_expl_input_files))
    )<1:
    input(f'''Please copy pdf files to the input directory:
{open_n_expl_input_files}\n\n

Then press any key!''')


# In[14]:


print('OCR is starting ....')


# In[15]:


file_count = [0]

for path_num in range(len(source_path)):
    print(path_num)
    print(range(len(source_path)))
    file_list = os.listdir(source_path[path_num])

    file_count.append(file_count[path_num-1]+len(file_list))

    for i in range(len(file_list)):
        file_name = file_list[i]
        client = vision.ImageAnnotatorClient()
        file_path = source_path[path_num] + file_name

        # Supported mime_type: application/pdf, image/tiff, image/gif
        mime_type = "application/pdf"

        try:
            with io.open(file_path, "rb") as f:
                content = f.read()
                pdf_reader = PyPDF2.PdfFileReader(open(file_path, "rb"), strict = False)
        #         pdf_reader = PyPDF2.PdfFileReader(f)
                num_of_pages = pdf_reader.numPages

        except:
            output_path = source_path[path_num] + "decrypted_" + file_list[i]
            file_path = source_path[path_num] + file_name
            pdf = pikepdf.Pdf.new()

            for _, page in enumerate(input_pdf.pages):
                pdf.pages.append(page)

            pdf.save(output_path)
            input_pdf.close()
            print("saved at : {}".format(output_path))

            file_path = source_path[path_num] + "decrypted_" + file_list[i]

            with io.open(file_path, "rb") as f:
                content = f.read()
                pdf_reader = PyPDF2.PdfFileReader(open(file_path, "rb"), strict = False)
        #         pdf_reader = PyPDF2.PdfFileReader(f)
                num_of_pages = pdf_reader.numPages


        input_config = {"mime_type": mime_type, "content": content}
        features = [{"type_": vision.Feature.Type.DOCUMENT_TEXT_DETECTION}]

        for p in range(1, num_of_pages+1, 5):
            if(p==1):
                pdf2txt_w(path_num)
            else:
                pdf2txt(p, path_num)


# In[16]:


print('Finished OCR!')


# In[17]:


file_output = os.path.abspath(destination_path[path_num])


# In[18]:


subprocess.Popen(f'explorer /open,{file_output}')


# In[19]:


print(f'''
Check OCR output in the following directory:
{file_output}
''')


# In[20]:


print(F'''

1) Number of Output Files: {len(os.listdir(source_path[0]))}

2) Number of Output Files: {len(os.listdir(destination_path[0]))}

3) Input Files:
\t{os.listdir(source_path[0])}

4) Output Files:
\t{os.listdir(destination_path[0])}
''')


# In[84]:


print(os.path.abspath(destination_path[0]))


# # Preprocessing Output of the OCR.

# In[124]:


def process_text(file_path, output_file_name):
    '''Given the output of Google OCR API;
    in the form of a text file (file_path);
    clean text files for downstream use.'''
    with open(fr'{file_path}', encoding='utf-8') as text_file:
        text_list = text_file.readlines()
    
    text_list = [re.sub(r'\s*BREAKHERE\s*\n', '.\n', i) for i in text_list]
    text_list = [re.sub(r' *[\.\؛\؟\:\!]+ *\n', '_NEW_LINE_HERE_', line) for line in text_list]
    text_list = [re.sub('\n', ' ', i) for i in text_list]
    text_01 = ' '.join(text_list)
    text_01 = re.sub('_NEW_LINE_HERE_', '.\n', text_01)
    text_01 = re.sub(' {2,}', ' ', text_01)

    with open(fr'{output_file_name}.txt', encoding='utf-8', mode='w') as text_output_file:
        text_output_file.write(text_01) 
        # Since it's written in 'w' mode; it will automatically delete the file if it already exists.


# In[125]:


def batch_process_text(dir_name):
    '''Given a directory (dir_name) which contains .txt files;
    Batch process them using the process_text function.
    It's worth mentioning that these .txt files come from Google OCR API.
    '''
    files_list = [i for i in os.listdir(dir_name) if i.endswith('.txt')]
    try:
        dir_name_pp = f"{dir_name}_PP"
        os.mkdir(dir_name_pp)
        dir_name_pp_abs_path = os.path.abspath(dir_name_pp)
        print(f'''
        A project was created in:
        {dir_name_pp_abs_path}
        ''')
    except:
        increment = 1
        while dir_name_pp in os.listdir():
            dir_name_pp = re.sub('_copy_.*', '', dir_name_pp)
            dir_name_pp = dir_name_pp + f'_copy_{str(increment).zfill(2)}'
            increment += 1
        os.mkdir(dir_name_pp)
        dir_name_pp_abs_path = os.path.abspath(dir_name_pp)
        print(f'''
        The project name already EXISTS!
        A copy of that name was created in the following path:
        {dir_name_pp_abs_path}
        ''')  
    for file in files_list:
        file_abs_path = os.path.join(os.path.abspath(dir_name), file)
        file_output_name = re.sub(r'\.txt$', '', file)
        file_output_name = file_output_name + '_PP'
        print(f'''
        Input File:\t{file}
        Output File:\t{file_output_name} 
        ''')
        process_text(file_abs_path, fr'{dir_name_pp}/{file_output_name}')


# In[126]:


pp_folder = os.path.abspath(destination_path[0])


# In[127]:


batch_process_text(pp_folder)


############
print('Finished...')
end = time_now()
############
duration = end - start
duration_min = round(duration.seconds/60, 3)
if duration_min < 2:
    time_unit = 'minute'
else:
    time_unit = 'minutes'
print(f'Total duration of translation is {duration_min} {time_unit}.')




