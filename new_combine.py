import os
import xlsxwriter
import csv
import sys

folder_list = []
folder_path = []


def scan_folders():
    """
        Asks user for path that contains the Labradar SR folders, if no SR folders are present
        Error is presented to either exit or try another location, folder names and paths are saved
        in lists outside the function
    """

    try:
        path = input("Where is the root Labradar folder that contains all the SR folders?\n")
        exclude = {'TRK'}
        error = OSError
        if os.path.exists(path):
            for root, dirs, files in os.walk(path, topdown=True):
                dirs[:] = [d for d in dirs if d not in exclude]
                for dir in sorted(dirs):
                    if dir.__contains__('SR'):
                        folder_path.append(root)
                        folder_list.append(dir)
        else:
            raise FileNotFoundError
    except OSError or FileNotFoundError:
        try_again = input("Folder does not contain SR folders, Try again?\n")
        if "no" in try_again.lower():
            sys.exit()


def rename_folders():
    """
        Uses list from scan_folders to rename the folders to
        user defined names.
    """

    rn_lp = 0
    while rn_lp < len(folder_list):
        try:
            new_name = input("What would you like to rename {} to?\n".format(folder_list[rn_lp]))
            os.rename(os.path.join(folder_path[rn_lp], folder_list[rn_lp]),
                      (os.path.join(folder_path[rn_lp], new_name)))
            folder_list[rn_lp] = new_name
            rn_lp += 1
        except OSError:
            print("File name error, please try again")
        if rn_lp == len(folder_list):
            break
    return True


def combine_csv(path):
    """
    Function that uses created lists of folders and .csv files to create
    a multi sheet .xlsx file in the desired location.
    :param path: File path to save location
    :return: None
    """

    sheets = []
    shot_path = []

    for x in range(0, len(folder_path)):
        scan_path = os.path.join(folder_path[x], folder_list[x])
        for root, dirs, files in os.walk(scan_path):
            for file in sorted(files):
                if file.endswith(".csv"):
                    sep = " "
                    sheets.append(file.split(sep, 1)[0])
                    shot_path.append(os.path.join(root, file))
        workbook_name = (os.path.join(path, folder_list[x]) + ".xlsx")
        wb = xlsxwriter.Workbook(workbook_name, {'strings_to_numbers': True})
        for i in sheets:
            wb.add_worksheet(i)

        for s in range(0, len(sheets)):
            ws = wb.get_worksheet_by_name(sheets[s])
            with open(shot_path[s], 'r') as f:
                reader = csv.reader((line.replace('\0', '') for line in f), delimiter=';')
                next(f)
                for r, row in enumerate(reader):
                    for c, val in enumerate(row):
                        ws.write(r, c, val)

        shot_path = []
        sheets = []
        wb.close()


def main():

    while not len(folder_list):
        scan_folders()
    rename_question = input("Do you want to rename the folders?\n").lower()
    if 'yes' in rename_question:
        rename = False
        while not rename:
            rename = rename_folders()

    save_location = input("Where do you want to save the combined .xlxs spreadhseets? Complete path\n"
                          "ex: /Users/user/Desktop\n")
    combine_csv(save_location)


if __name__ == "__main__":
    main()
