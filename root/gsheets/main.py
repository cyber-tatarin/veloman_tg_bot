import os.path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import pygsheets
import asyncio

from root.logger.config import logger

logger = logger
key_json = os.path.abspath(os.path.join('root', 'gsheets', 'gsheets_key.json'))

print(key_json)


def find_row_number(user_id, worksheet):
    try:
        # Authenticate using service account credentials
        # gc = pygsheets.authorize(service_file=key_json)
        
        # Open the Google Sheet by name
        # sheet = gc.open('FERC telegram bot overview')
        # worksheet = sheet[0]
        
        cells_list_of_lists = worksheet.find(str(user_id), matchEntireCell=True)  # [[]]
        if cells_list_of_lists:  # empty list object considered as false
            return cells_list_of_lists[0].row
        else:
            return None
    except Exception as x:
        logger.exception(x)


worksheet_indexes_by_roles = {
    'loyalty_user': 0,
    'outsource_user': 1,
    'newbie': 4
}


def register_user(dict_with_kwargs: dict):
    try:
        user_id = dict_with_kwargs.get('user_id')
        user_full_name = dict_with_kwargs.get('user_full_name')
        username = f"@{dict_with_kwargs.get('username')}"
        
        # Authenticate using service account credentials
        gc = pygsheets.authorize(service_file=key_json)
        
        # Open the Google Sheet by name
        sheet = gc.open('Veloman telegram bot overview')
        # Select the first worksheet in the Google Sheet
        worksheet = sheet[0]
        
        now = datetime.now()
        epoch = datetime(1899, 12, 30)
        delta = now - epoch
        current_time = delta.days + (delta.seconds / 86400)
        
        row_number = find_row_number(user_id, worksheet)
        
        if row_number is None:
            id_user_time = [[user_id, user_full_name, username, current_time, 0]]
            
            last_row = worksheet.get_col(1, include_empty=False)
            # get the index of the first empty row
            insert_index = len(last_row)
            worksheet.insert_rows(row=insert_index, values=id_user_time, inherit=True)
        
        else:
            col_index = 4
            # Get the cell object for the specific column and edit its value
            worksheet.update_value((row_number, col_index), current_time)
    
    except Exception as x:
        logger.exception(x)


def set_user_country(dict_with_kwargs: dict):
    try:
        user_id = dict_with_kwargs.get('user_id')
        country = dict_with_kwargs.get('country')
        
        # Authenticate using service account credentials
        gc = pygsheets.authorize(service_file=key_json)
        
        # Open the Google Sheet by name
        sheet = gc.open('Veloman telegram bot overview')
        # Select the first worksheet in the Google Sheet
        worksheet = sheet[0]
        
        row_number = find_row_number(user_id, worksheet)
        
        if row_number is not None:
            col_index = 6
            worksheet.update_value((row_number, col_index), country)
    
    except Exception as x:
        logger.exception(x)


def set_user_bel_bank(dict_with_kwargs: dict):
    try:
        user_id = dict_with_kwargs.get('user_id')
        bel_bank = dict_with_kwargs.get('bel_bank')
        
        # Authenticate using service account credentials
        gc = pygsheets.authorize(service_file=key_json)
        
        # Open the Google Sheet by name
        sheet = gc.open('Veloman telegram bot overview')
        # Select the first worksheet in the Google Sheet
        worksheet = sheet[0]
        
        row_number = find_row_number(user_id, worksheet)
        
        if row_number is not None:
            col_index = 9
            worksheet.update_value((row_number, col_index), bel_bank)
    
    except Exception as x:
        logger.exception(x)


def set_user_bel_bank_category(dict_with_kwargs: dict):
    try:
        user_id = dict_with_kwargs.get('user_id')
        bel_bank_category = dict_with_kwargs.get('bel_bank_category')
        
        # Authenticate using service account credentials
        gc = pygsheets.authorize(service_file=key_json)
        
        # Open the Google Sheet by name
        sheet = gc.open('Veloman telegram bot overview')
        # Select the first worksheet in the Google Sheet
        worksheet = sheet[0]
        
        row_number = find_row_number(user_id, worksheet)
        
        if row_number is not None:
            col_index = 10
            worksheet.update_value((row_number, col_index), bel_bank_category)
    
    except Exception as x:
        logger.exception(x)


def set_user_bel_bank_creds(dict_with_kwargs: dict):
    try:
        user_id = dict_with_kwargs.get('user_id')
        bel_bank_creds = dict_with_kwargs.get('bel_bank_creds')
        
        # Authenticate using service account credentials
        gc = pygsheets.authorize(service_file=key_json)
        
        # Open the Google Sheet by name
        sheet = gc.open('Veloman telegram bot overview')
        # Select the first worksheet in the Google Sheet
        worksheet = sheet[0]
        
        row_number = find_row_number(user_id, worksheet)
        
        if row_number is not None:
            col_index = 11
            worksheet.update_value((row_number, col_index), bel_bank_creds)
    
    except Exception as x:
        logger.exception(x)


def set_user_phone_number(dict_with_kwargs: dict):
    try:
        user_id = dict_with_kwargs.get('user_id')
        phone_number = dict_with_kwargs.get('phone_number')
        
        # Authenticate using service account credentials
        gc = pygsheets.authorize(service_file=key_json)
        
        # Open the Google Sheet by name
        sheet = gc.open('Veloman telegram bot overview')
        # Select the first worksheet in the Google Sheet
        worksheet = sheet[0]
        
        row_number = find_row_number(user_id, worksheet)
        
        if row_number is not None:
            col_index = 7
            worksheet.update_value((row_number, col_index), phone_number)
    
    except Exception as x:
        logger.exception(x)


def set_user_mobile_operator(dict_with_kwargs: dict):
    try:
        user_id = dict_with_kwargs.get('user_id')
        mobile_operator = dict_with_kwargs.get('mobile_operator')
        
        # Authenticate using service account credentials
        gc = pygsheets.authorize(service_file=key_json)
        
        # Open the Google Sheet by name
        sheet = gc.open('Veloman telegram bot overview')
        # Select the first worksheet in the Google Sheet
        worksheet = sheet[0]
        
        row_number = find_row_number(user_id, worksheet)
        
        if row_number is not None:
            col_index = 8
            worksheet.update_value((row_number, col_index), mobile_operator)
    
    except Exception as x:
        logger.exception(x)


def submitted_review(dict_with_kwargs: dict):
    try:
        user_id = dict_with_kwargs.get('user_id')
        
        # Authenticate using service account credentials
        gc = pygsheets.authorize(service_file=key_json)
        
        # Open the Google Sheet by name
        sheet = gc.open('Veloman telegram bot overview')
        # Select the first worksheet in the Google Sheet
        worksheet = sheet[0]
        
        row_number = find_row_number(user_id, worksheet)
        
        if row_number is not None:
            num_of_projects_col_index = 5
            
            num_of_projects = worksheet.get_value((row_number, num_of_projects_col_index))
            if num_of_projects is not None and num_of_projects != '':
                worksheet.update_value((row_number, num_of_projects_col_index), int(num_of_projects) + 1)
            else:
                worksheet.update_value((row_number, num_of_projects_col_index), 1)
    
    except Exception as x:
        logger.exception(x)
        
        
def get_value(dict_with_kwargs):
    user_id = dict_with_kwargs.get('user_id')
    col_index = dict_with_kwargs.get('col_index')
    
    # Authenticate using service account credentials
    gc = pygsheets.authorize(service_file=key_json)
    
    # Open the Google Sheet by name
    sheet = gc.open('Veloman telegram bot overview')
    # Select the first worksheet in the Google Sheet
    worksheet = sheet[0]
    
    row_number = find_row_number(user_id, worksheet)
    
    if row_number is not None:
        value = worksheet.get_value((row_number, col_index))
        if value is not None and value != '':
            return value
        return False
    

def check_if_user_has_saved_creds(dict_with_kwargs):
    user_id = dict_with_kwargs.get('user_id')
    creds_type = dict_with_kwargs.get('creds_type')
    
    # Authenticate using service account credentials
    gc = pygsheets.authorize(service_file=key_json)
    
    # Open the Google Sheet by name
    sheet = gc.open('Veloman telegram bot overview')
    # Select the first worksheet in the Google Sheet
    worksheet = sheet[0]
    
    row_number = find_row_number(user_id, worksheet)
    
    phone_number_index = 7
    mobile_operator_index = 8
    
    bank_index = 9
    bank_category_index = 10
    bank_creds_index = 11
    
    if row_number is not None:
        if creds_type == 'phone':
            phone_number = worksheet.get_value((row_number, phone_number_index))
            mobile_operator = worksheet.get_value((row_number, mobile_operator_index))
            if phone_number is not None and phone_number != '' and mobile_operator is not None and mobile_operator != '':
                return phone_number, mobile_operator
            return False
        
        elif creds_type == 'bel_bank':
            bank = worksheet.get_value((row_number, bank_index))
            bank_category = worksheet.get_value((row_number, bank_category_index))
            bank_creds = worksheet.get_value((row_number, bank_creds_index))
            if bank is not None and bank != '' and bank_category is not None and bank_category != '' and bank_creds is not None and bank_creds != '':
                return bank, bank_category, bank_creds
            return False
    

async def async_execute_of_sync_gsheets(func, **kwargs):
    executor = ThreadPoolExecutor(max_workers=10)
    loop = asyncio.get_running_loop()
    try:
        # run the blocking sync operation in a separate thread
        res = await loop.run_in_executor(executor, func, kwargs)
        return res
    except Exception as x:
        logger.exception(x)
    finally:
        executor.shutdown(wait=True)


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.create_task(async_execute_of_sync_gsheets(register_loyalty_user(user_id=8, username=7, user_full_name=7)))
    pass
    logger.info('gogogogogooo')
