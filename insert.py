import csv
from datetime import datetime

# Check if cell is a specific date format.
def is_date_matching(date_str, format):
    try:
        return bool(datetime.strptime(date_str, format))
    except ValueError:
        return False

# Read a csv file and generate insert statements and write into sql file. 
def generate_sql(file_name,table_name, format, output_file, mode):
    with open(f'{file_name}.csv', 'r') as csv_in:
        csv_reader = csv.DictReader(csv_in, delimiter = ',')
        with open(f'{output_file}.sql', mode) as f:

            for row in csv_reader:  
                for cell in row.items(): 
                    if is_date_matching(cell[1],format):
                        row[cell[0]] = "DATE \'"+cell[1]+"\'"
                    elif not cell[1].isdigit(): 
                        row[cell[0]] = "\'"+cell[1].replace("'","''")+"\'"
            
                f.write(f'INSERT INTO {table_name} VALUES ({",".join(row.values())});\n')
            f.write('\n\n\n')

def main():
    try:
        file_name=input("Enter a csv file name (without the extension): ")
        table_name=(input("Enter the table name: ")).upper()
        output_file=input("Enter the output file name (without the extension): ")
        mode=input("Enter the mode (r/w): w - write or a - append :")
        format = "%Y-%m-%d"
        generate_sql(file_name, table_name, format, output_file, mode)
    except FileNotFoundError:
        print("Error: Enter a valid file name!!!")
    except Exception as e:
        print(e)
    finally:
        if input("Press any key to start again, x to exit: ") != 'x':
            main()

main()
            
                

