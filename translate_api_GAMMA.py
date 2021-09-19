#!/usr/bin/env python
# coding: utf-8

# # IMPORTS

# In[1]:

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
from google.cloud import translate
import os





import subprocess


# # CREADENTIALS

# In[3]:


# cred_file points to the API key that you would need to download from Google
# The key should be enabled to use the credential file
cred_file = r'_________.json' # Enter path to credentials.
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_file


# In[ ]:





# # PROJECT ID

# In[4]:


project_id = '_____' # Enter GCP project ID



source_lang = input('''Please enter the source language of the text; i.e. ar or en; then press Enter.
''')
source_lang = str(source_lang).lower()
while source_lang not in ('ar', 'en'):
    source_lang = input('''Please enter a valid source language code;
    for English type en;
    for Arabic type ar;
    then Press Enter.
    ''')

if source_lang == 'en':
    target_lang = 'ar'
else:
    source_lang = 'ar'
    target_lang = 'en'





# # FUNCTIONS

# ## FUNCTION 1: TXT TRANSLATION




def txt_translate(txt_file="txt file", project_id="YOUR_PROJECT_ID"):
    """Translating .txt files using Google API translate.
    Target Language always opposite of the Source Language.
    """
    if target_lang == 'en':
        print(f'''Translating: {txt_file}
        from Arabic [ar] to English [en].''')
    else:
        print(f'''Translating: {txt_file} 
        from English [en] to Arabic [ar].''')

    with open(txt_file, encoding='utf-8') as input_file:
        text = input_file.readlines()
    text = [i.strip() for i in text]
    text = [i for i in text if i] # Getting rid of empty lines.

    client = translate.TranslationServiceClient()

    parent = client.common_location_path(project_id, "global")

    # Detail on supported types can be found here:
    # https://cloud.google.com/translate/docs/supported-formats
    result = []
    for source_text in text:
        response = client.translate_text(
            parent=parent,
            contents=[source_text],
            mime_type="text/plain",  # mime types: text/plain, text/html
            source_language_code= source_lang,
            target_language_code=target_lang,
            )
            # Display the translation for each input text provided
        for translation in response.translations:
            result.append((translation.translated_text, 
                         source_text))
    
    
    return result




# ## FUNCTION 2: BATCH TXT TRANSLATIONS


def batch_txt_translation(dir_name="Directory of txt", project_id="YOUR_PROJECT_ID"):
    '''Given a directory; translate all .txt files.'''

    result_batch = []
    files_list = [i for i in os.listdir(dir_name) if i.endswith('.txt')]
    for file in files_list:
        file_abs_path = os.path.join(os.path.abspath(dir_name), file)
        file_output_name = re.sub(r'\.txt$', '', file)
        file_output_name = file_output_name + '_TRASNLATED'
        print(f'''
        Input File:\t{file}
        Output File:\t{file_output_name} 
        ''')
        result_batch.append(
            ((txt_translate(file_abs_path, project_id=project_id)), file))
    return (result_batch, dir_name)








# ## FUNCTION 3: Write Bilingual Files to Desk




def create_bilingual_files(batch_translation_list="Output of batch_txt_translation function"):
    '''Given a list that was created by the:
        batch_txt_translation function;
        write bilingual files (target/source) in a folder created by the user.
    '''
    
    try:
        dir_name = batch_translation_list[1]
        print(f'Name of the directory to be translated: {dir_name}')
        dir_name_trans = f'{dir_name}_TRANSLATED'

        os.mkdir(dir_name_trans)

        proj_abs_path = os.path.abspath(dir_name_trans)
        print(f'''
        The bilingual files are in the following folder:
        {proj_abs_path}
        ''')
        
    except Exception as e:
        print('Running Exception .......')
        print(e)
        increment = 1

        while os.path.basename(dir_name_trans) in os.listdir(os.path.dirname(dir_name)):
            print(f'{dir_name_trans}')
            print('Going through while loop')
            print(f'Increment is now {increment}')
            dir_name_trans = re.sub('_copy_.*', '', dir_name_trans)
            dir_name_trans = dir_name_trans + f'_copy_{str(increment).zfill(2)}'
            increment += 1
        
        os.mkdir(dir_name_trans)
        proj_abs_path = os.path.abspath(dir_name_trans)
        print(f'''
        This folder already EXISTS!
        A copy of that name was created in the following path:
        {proj_abs_path}
        ''')    
    
    for entry in batch_translation_list[0]:
        file_name = entry[1]
        file_name = re.sub(r'\.txt$', '_TRANSLATED', file_name)
        translation = entry[0]
        with open(f'{proj_abs_path}/{file_name}.txt', encoding='utf-8', mode='w') as translated_file:
            for item in translation:
                target = item[0]
                source = item[1]
                target_source = target + "\n" + source + '\n\n'
                translated_file.write(target_source)
    subprocess.Popen(f'explorer /open,{proj_abs_path}')





input_dir = input('''
Please specify directory of input .TXT files:
''')
input_dir = os.path.abspath(input_dir)
print(input_dir)





batch_txt_translation_list = batch_txt_translation(input_dir, project_id=project_id)


create_bilingual_files(batch_txt_translation_list)

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