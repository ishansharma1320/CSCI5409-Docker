from flask import Blueprint,request
import os
import pandas as pd
summation_api_bp = Blueprint('summation',__name__)

@summation_api_bp.route('/csv',methods=['POST'])
def sumCSV():
    content_type = request.headers.get("Content-Type")
    result = {}
    if content_type == 'application/json':
        json_data = request.json
        file = json_data.get('file',None)
        result['file'] = file
        product = json_data.get('product',None)
        if os.path.exists(os.path.join('/usr/files/',file)):
            file_path = os.path.join('/usr/files/',file)
            csv_is_validated = validateCSV(file_path)
            if csv_is_validated:
                df = pd.read_csv(file_path)
                filtered_df = df[df['product'] == product]
                total_amount = sum(filtered_df['amount'])
                result['sum'] = total_amount
            else:
                result['error'] = "Input file not in CSV format."
        else:
            result['error'] = "File not found."

    else:
        result['error'] = f'Unsupported Content-Type: {content_type}'

    return result



def validateCSV(file_path):
    df = pd.read_csv(file_path)
    required_columns = ['product','amount']
    columns_in_df = [x.lower() for x in df.columns]
    column_headers_validated = set(required_columns) == set(columns_in_df)
    wrong_format_flag = False
    if column_headers_validated:
        df = df.replace('^\s*$',None,regex=True)
        column_values_empty = False
        column_values_check_list = []
        for column in df.columns:
            column_values_check_list.append(any(df[column].isnull().tolist()))
        
        column_values_empty = any(column_values_check_list)
        column_values_validated = not column_values_empty
        if column_values_validated:
            amount_column_datatype = df['amount'].apply(lambda x: str(type(x))).unique().tolist()
            amount_available_datatypes = ["<class 'float'>","<class 'int'>"]

            amount_column_validated = len([x for x in amount_column_datatype if x in amount_available_datatypes]) > 0

            product_column_datatype = df['product'].apply(lambda x: str(type(x))).unique().tolist()
            product_available_datatypes = ["<class 'str'>"]

            product_column_validated = len([x for x in product_column_datatype if x in product_available_datatypes]) > 0

            if not (amount_column_validated and product_column_validated):
                wrong_format_flag = True
        else:
            wrong_format_flag = True
    else:
            wrong_format_flag = True
    
    return not wrong_format_flag

