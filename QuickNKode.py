# Importing main module to start the program.
# Encoders will be called at their respective time.
import pandas as pd
from sklearn.preprocessing import LabelEncoder


# The set of functions to perform type casting and dropping unwanted columns.
def user_drop_entry(data_cols, user_input_values, operation_signal):
    if operation_signal == 1:
        user_input_lower = [value.lower() for value in user_input_values]
        if 'exit' in user_input_lower:
            if set(user_input_values).issubset(data_cols):
                long_str = ', '.join(user_input_values)
                if len(user_input_values) == 1:
                    print("\nThis program will proceed now without the \"", user_input_values[0], "\" column",
                          sep='')
                else:
                    print("\nThis program will proceed further without these following columns:-\n",
                          long_str)
                return 1
            else:
                print("\nProgram terminated\nYou chose to exit")
                exit()
        elif set(user_input_values).issubset(data_cols):
            long_str = ', '.join(user_input_values)
            if len(user_input_values) == 1:
                print("\nThis program will proceed now without the \"", user_input_values[0], "\" column",
                      sep='')
            else:
                print("\nThis program will proceed further without these following columns:-\n",
                      long_str)
            return 1
        elif user_input_lower == ['']:
            print("\nSince you pressed enter without entering any column name\n"
                  "This program will proceed with the complete data-set")
            return 1
        else:
            print("\nWrong Input. There is a minor mistake in the entry. "
                  "\nCheck spellings or extra spaces.\nRe-enter your input:- ")
            return 0
    if operation_signal == 2:
        if set(user_input_values).issubset(data_cols):
            long_str = ', '.join(user_input_values)
            print("\nProceeding to encode with column " + long_str + " as categorical column[s].")
            return 1
        elif user_input_values == ['']:
            print("\nProceeding to encode.")
            return 1
        elif user_input_values[0].lower() == 'all':
            print("\nConverting all the columns to categorical columns.")
            return 1
        else:
            print("\nYou entered a column name that is not in the dataset.")
            print("Please, re-enter the names of the columns.")
            print("Is there any specific numerical column in this "
                  "dataset that you want to convert as categorical or object? "
                  "\nIf yes then type the name of the column[s] or simply press enter:-\n")
            return 0


# The Function to take user input for columns to operate on.
def column_choice(cols, signal):
    while 1:
        user_input = list(map(str, input().split(', ')))
        if user_drop_entry(cols, user_input, signal):
            break
    return user_input


# The function to drop unwanted columns.
def dropped_data(data):
    main_columns = list(tuple(data.columns))
    print("\nThe columns in this dataset are:-\n:::::::::::::::::::::::::::::::\n", main_columns, "\n")
    print("Type the name of columns you want to drop(separated by commas','and a space)"
          "\nPress enter to skip this operation or type 'exit' to terminate the program:-\n")
    user_entry = None
    if __name__ == '__main__':
        colom = column_choice(main_columns, 1)
        user_entry = colom
    if user_entry == ['']:
        compact_data = data
    else:
        compact_data = data.drop(labels=user_entry, axis=1)
    return compact_data


# The function to perform conversion of numerical columns to categorical columns.
def type_casting(data):
    columns = data.columns.tolist()
    print("\nThe columns in this dataset are:-")
    print("::::::::::::::::::::::::::::::::\n", columns, "\n")
    print("The data types for the specific columns are as follows:-")
    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print(data.dtypes.to_frame().transpose())
    num_columns = data.select_dtypes(exclude=['object', 'category']).columns.tolist()
    print("\nThe name of the columns that contain numerical values are:-")
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n", num_columns)
    print("\nIs there any specific numerical column in this dataset that you "
          "want to convert as categorical or object?"
          "\nIf yes, type the name of the column[s] or if no, simply press enter.\n"
          "(if you want to convert all the columns as categorical columns than type 'All' :-)")
    column_choices = column_choice(columns, 2)
    if column_choices == ['']:
        model_dataset = data
    elif column_choices[0].lower() == 'all':
        model_dataset = data.astype(dtype='object', copy=False)
    else:
        for column in column_choices:
            data[column] = data[column].astype(dtype='object', copy=False)
        model_dataset = data
    return model_dataset


# This function will return the main dataset we need for encoding after type casting.
def main_data():
    print("\n*****************************")
    file = str(input("Enter the address of the file:- "))
    data = pd.read_csv(file)
    data = dropped_data(data)
    operational_data = type_casting(data)
    return operational_data


# Function to check if a users choice is valid or not.
def user_entry_check(expected, entered):
    if entered in expected:
        return 1
    elif entered.lower() == "exit":
        print("\nProgram terminated\nYou chose to exit")
        exit()
    else:
        print("Please enter a valid input:-")
        return 0


# This function will perform an infinite loop till the user enters a valid input.
def check_input(condition_list):
    while 1:
        input_value = str(input())
        if user_entry_check(condition_list, input_value):
            break
    return input_value


# All the encoding on the required dataset will be performed here.
def encoded(dataset):
    print("\n:::::::::::::::::\nStarting Encoding\n:::::::::::::::::")
    print("What kind of encoding method you want to apply?")
    print("1: Encoded for all categorical columns at once.")
    print("2: Select encoder for each categorical column.")
    print("\nEnter your choice: ")
    choices = ['1', '2']
    signal = check_input(choices)
    column_list = dataset.select_dtypes(include=['object', 'category']).columns.tolist()
    if signal == '1':
        print("\nCaution: You want to perform encoding on all the categorical columns at once.")
        print("What kind of encoder you would want to apply on all the columns?")
        print("1: Label Encoder\n2: One Hot Encoder")
        print("Enter your choice: ")
        signal = check_input(choices)
        if signal == '1':
            lb = LabelEncoder()
            for column in column_list:
                dataset[column] = lb.fit_transform(dataset[column])
            print("\nLabel Encoder applied successfully.")
            print("==================================")
            modified_data = dataset
            return modified_data
        if signal == '2':
            modified_data = dataset.select_dtypes(exclude=['object', 'category'])
            for column in column_list:
                encoded_series = pd.get_dummies(dataset[column])
                modified_data = pd.concat([modified_data, encoded_series], axis=1)
            print("\nOne Hot Encoder applied successfully")
            print("====================================")
            return modified_data
    if signal == '2':
        modified_data = dataset
        print("\nYou chose to select encoder column wise:- \n")
        print(":::::::::::::::::::::::::::::::::::::::")
        for column in column_list:
            print("The name of the column you are encoding is:- ", column)
            print("Number of Unique values in the column = ", dataset[column].nunique())
            print("The values in this column are as follows:- \n")
            unique_values = dataset[column].value_counts()
            indexes = unique_values.index
            values = unique_values.values
            print(pd.DataFrame(dict(Values=indexes, Total_counts=values)))
            print("\nChoose the type of encoder to apply for column->", column, ":")
            print("1. Label Encoder\n2. One Hot Encoder")
            print("Enter your choice: ")
            signal = check_input(choices)
            if signal == '1':
                lb = LabelEncoder()
                modified_data[column] = lb.fit_transform(modified_data[column])
            if signal == '2':
                encoded_series = pd.get_dummies(dataset[column])
                modified_data = modified_data.drop(column, axis=1)
                modified_data = pd.concat([modified_data, encoded_series], axis=1)
        return modified_data


# Main Program
print("\nWelcome to QuickNKode. Your one stop platform to encode your dataset.")
print("====================================================================")
print("\nCaution: This program is associated to the family QuickSeries.")
print("Please, only enter a dataset which does not have a missing value or has \nbeen "
      "ran successfully with imputation from it's sibling QuickWash application.")
main_dataset = main_data()
print("\nThe data types for the columns will be as follows:-\n")
print(main_dataset.dtypes.to_frame().transpose())
encoded_data = encoded(main_dataset)
print("\nThe final dataset is as follows:-\n::::::::::::::::::::::::::::::::\n")
print(encoded_data.head(5))
print("\nEnter a name for the dataset: ")
name = str(input())
file_name = name + ".csv"
encoded_data.to_csv(file_name, index=False)
print("Your file has been successfully saved.")
print("Thank you for using QuickNKode.")
print(":::::::::::::::::::::::::::::::")
input("\nPress any key to exit.")
