"""here you import the necessary libarys to install them write in cmd 'pip istall pandas' and 'pip insatll numpy"""
import numpy as np
import pandas as pd

from pathlib import Path



class csv_Handler(object):

    """please adjust the path to the tables and the table names """
    """this method is used to initialize the paths to the tables"""
    def __init__(self):
        pd.set_option('mode.chained_assignment', None)
        self.main_path = "C:\\Users\\User\\Desktop\\\Sara_Master\\LD.csv"
        self.second_path = "C:\\Users\\User\\Desktop\\Sara_Master\\UD.csv"
        self.adj_path = "C:\\Users\\User\\Desktop\\Sara_Master\\Adjectives_masterfile.csv"

        self.main_path_lower = "C:\\Users\\User\\Desktop\\Sara_Master\\LD_lower.csv"
        self.second_path_lower = "C:\\Users\\User\\Desktop\\Sara_Master\\UD_lower.csv"
        self.pre_past_other = "C:\\Users\\User\\Desktop\\Sara_Master\\pre_past_other_valenz.csv"


        self.VPCodeIndex = self.get_column_index(self.second_path, 'VPCode')
        self.PartCodeIndex = self.get_column_index(self.main_path, 'ParticipantCode')

    """this method is only to help you check if data objects are nan"""
    def is_nan(self, x):
        return x is np.nan or x != x

    """this method returns the index of the column of the passed name and table """
    def get_column_index(self, path, column):
        index = 0
        dataset = pd.read_csv(path, sep=';')
        columns = dataset.columns.tolist()
        for i in columns:
            if i == column:
                return index
            else:
                index += 1

    ########################################################################################################
    #######################################Clean Tabel######################################################

    """this method goes through each row for each column until it finds a non-empty entry,
       if all fields are empty the column is deleted from the table """
    def delete_empty_column(self):
        dataset = pd.read_csv(self.main_path, sep=';')
        # get collums
        columns = dataset.columns.tolist()

        # for each column of the table
        keep_coll = []
        for i in columns:
            column_values = dataset[i]

            # for each row of one column
            for j in column_values:
                # if it is not Nan add it to the list of columns which should be preserved to
                if not self.is_nan(j) and j is not None and j != '\n' and j != '\t' and j != ' ':
                    keep_coll.append(i)
                    break

        # make new csv with same name and other columns
        new_dataset = dataset[keep_coll]
        new_dataset.to_csv(self.main_path, index=False, sep=';')
        print("deleted all unused columns")

    """this method returns the row to the respective VPCode of the UniparkData table"""
    def get_row_second_Table(self, name):
        try:
            df = pd.read_csv(self.second_path_lower, sep=';')
            df2 = df.set_index("VPCode", drop=False)
            return df2.loc[name, :]
        except:
            return False

    """This tasbelle inserts the UniparkData table into the Labvanced table"""
    def merge(self):
        # make all codes to lowercase
        self.make_lowercase()
        global other_Table_row
        # read the tables
        table2 = pd.read_csv(self.second_path_lower, sep=';')
        columns_table2 = table2.columns.tolist()
        table1 = pd.read_csv(self.main_path_lower, sep=';')
        # append the new columns
        for i in columns_table2:
            if i != 'VPCode':
                table1[i] = ""
        # write new columns to csv
        table1.to_csv(self.main_path_lower, index=False, sep=';')

        # go through all lines
        count_rows = table1.shape[0]
        for i in range(0, count_rows):
            # get the row from original Table
            row = table1.loc[i, :]
            # if the value is not None or NaN, get the correct row from the other Table

            if row[self.PartCodeIndex] is not None and not self.is_nan(row[self.PartCodeIndex]) and row[self.PartCodeIndex] != ' ' and row[self.PartCodeIndex] != '':
                other_Table_row = self.get_row_second_Table(row[self.PartCodeIndex])

                if other_Table_row is False:
                    pass

                help = 0
                # insert the new columns
                for c in columns_table2:
                    try:
                        table1._set_value(i, c, other_Table_row[help])
                        help += 1
                    except:
                        break

        # overwrite the new csv file
        table1.to_csv(self.main_path_lower, index=False, sep=';')
        print("Merged Tables")

    """this method helps to make the VPCode tidier, because sometimes upper and lower
     case letters and special characters have been swapped"""
    def make_lowercase(self):
        # secound Table
        # get the Table
        table2 = pd.read_csv(self.second_path, sep=';')
        count_rows = table2.shape[0]

        # go through the lines
        for i in range(0, count_rows):
            row = table2.loc[i, :]
            code_list = list(row[self.VPCodeIndex].lower())
            code = ""
            for c in code_list:
                if c == "a" or c == "b" or c == "c" or c == "d" or c == "e" or c == "f" or c == "g" \
                        or c == "h" or c == "i" or c == "j" or c == "k" or c == "l" or c == "m" or c == "n" \
                        or c == "o" or c == "p" or c == "q" or c == "r" or c == "s" or c == "t" or c == "u" \
                        or c == "v" or c == "w" or c == "x" or c == "y" or c == "z" or c == "1" or c == "2" \
                        or c == "3" or c == "4" or c == "5" or c == "6" or c == "7" or c == "8" or c == "9" \
                        or c == "0" or c == "ß" or c == "" or c == "b" or c == "b" or c == "b":
                    code += c

            table2._set_value(i, "VPCode", code)
        table2.to_csv(self.second_path_lower, index=False, sep=';')

        # main Table+
        # get the Table
        table1 = pd.read_csv(self.main_path, sep=';')
        count_rows = table1.shape[0]

        # go through the lines
        for i in range(0, count_rows):
            row = table1.loc[i, :]
            if not self.is_nan(row[self.PartCodeIndex]):
                code_list = list(row[self.PartCodeIndex].lower())
                code = ""
                for c in code_list:
                    if c == "a" or c == "b" or c == "c" or c == "d" or c == "e" or c == "f" or c == "g" \
                            or c == "h" or c == "i" or c == "j" or c == "k" or c == "l" or c == "m" or c == "n" \
                            or c == "o" or c == "p" or c == "q" or c == "r" or c == "s" or c == "t" or c == "u" \
                            or c == "v" or c == "w" or c == "x" or c == "y" or c == "z" or c == "1" or c == "2" \
                            or c == "3" or c == "4" or c == "5" or c == "6" or c == "7" or c == "8" or c == "9" \
                            or c == "0" or c == "ß" or c == "" or c == "b" or c == "b" or c == "b":
                        code += c
                table1._set_value(i, "ParticipantCode", code)

        table1.to_csv(self.main_path_lower, index=False, sep=';')
        print("all codes to Lowercase")




    ##########################################################################################################
    ##################################################Data Evaluation ########################################

    """this method is only a help to evaluate Which case occurred,
     whether the word was mentioned in encode or not, and which answer was given, 
     is put into practice and given an index from 0 to 5"""
    def evaluate_output(self, guess, trial_Ids, trial_Id):
        # evaluate output
        in_encode = False
        for i in trial_Ids:
            if int(i) == int(float(trial_Id)):
                in_encode = True

        if in_encode:
            #Wort wurde genannt

            if int(float(guess)) == 0:
                return 0
            elif int(float(guess)) == 1:
                return 1
            elif int(float(guess)) == 2:
                return 2

        else:
            #Wort wurde nicht genannt
            if int(float(guess)) == 0:
                return 3
            elif int(float(guess)) == 1:
                return 4
            elif int(float(guess)) == 2:
                return 5

        # 1, 2, 3

    """this method inserts a column in the table in which, depending on 
    the evaluation whether the adjective already existed or it is new and depending on 
    what was said by the respondent, the numbers 0, 1, 2, 3 are inserted at the level of recognition """

    def insert_recognition_evaluation(self, name= "recognition_evaluation"):
        print("start insert recognition evaluation test")
        # get tabel and append new column
        dataset = pd.read_csv(self.main_path_lower, sep=';',dtype='unicode')
        dataset[name] = ""
        # get the number of columns
        count_rows = dataset.shape[0]
        # make list and dir to save values
        trial_Ids = []
        dict_ID_TrtialIDs = {}
        # save the last and the old id "subje_ctcounter"
        old_id = 0
        last_id=dataset['subj_counter_global'][count_rows-1]
        # just in time to get the end of the last section
        count_last = 0
        # go through all rows

        for i in range(0, count_rows):
            # get the id of the row
            id = dataset['subj_counter_global'][i]

            # if the BlockName end with encode
            if not self.is_nan(dataset['Block_Name'][i]) and dataset['Block_Name'][i].endswith("encode"):

                """for each line check if it is not the last id, if not, append the values to the list until the id changes.
                    if the id changes add this list and the corresponding id to the dict. If the id is the last id, 
                    add the previous list to dict. and continue adding values to the list until counter 44 is reached"""

                if id != last_id:
                    if id != old_id:
                        if old_id != 0:
                            dict_ID_TrtialIDs.update({int(float(old_id)) : trial_Ids})

                        trial_Ids = []

                        trial_Ids.append(int(float(dataset['Trial_Id'][i])))
                        old_id = id
                    else:
                        trial_Ids.append(int(float(dataset['Trial_Id'][i])))
                        old_id = id
                else:
                    count_last += 1
                    if id != old_id:

                        dict_ID_TrtialIDs.update({int(float(old_id)): trial_Ids})
                        trial_Ids = []
                        trial_Ids.append(int(float(dataset['Trial_Id'][i])))
                        old_id = id

                    elif count_last != 44:
                        trial_Ids.append(int(float(dataset['Trial_Id'][i])))
                        old_id = id

                    elif count_last == 44:
                        dict_ID_TrtialIDs.update({int(float(id)): trial_Ids})


        #go through the table one more time
        for i in range(0, count_rows):

            # if the BlockName end with recognition
            if not self.is_nan(dataset['Block_Name'][i]) and dataset['Block_Name'][i].endswith("recognition") and\
                    dataset['Task_Nr'][i] != 1 and dataset['Task_Nr'][i] != "1":

                if not self.is_nan(dataset['subj_counter_global'][i]) and dataset['subj_counter_global'][i] != "" and\
                        dataset['subj_counter_global'][i] != " " and dataset['subj_counter_global'][i] != None:

                    """get the appropriate list from the dict. to see if the Triaal id has been used before.
                     Try catch, as it is possible that there may be entries for recognition of a person but not for encode"""

                    try:
                        trial_Id_List = dict_ID_TrtialIDs[int(float(dataset['subj_counter_global'][i]))]
                    except:
                        continue


                    #get values to evaluate the output
                    guess = dataset['RemKnoGue_55'][i]
                    trial_Id = dataset['Trial_Id'][i]

                    # evaluate the result of recognition and write it in the new column
                    evaluate = self.evaluate_output(guess, trial_Id_List, trial_Id)
                    dataset._set_value(i, name, evaluate)


        dataset.to_csv(self.main_path_lower, index=False, sep=';')

    """this method returns the valence of the adjective in the list adj,
     which is identified by the sub number and the list in which it appears 1 or 2"""
    def get_Valenz(self, liste, subNummer, adj):

        ka = 88
        for i in adj:
            t = adj.__getitem__(i)

            if t[0] == int(liste) and t[1] == int(float(subNummer)):
                ka = t[2]
        return ka

    """this method is only to help fill the dictonary which caches the values
     for each adjective with the new values  """
    def update_dict_trial(self, dic_trial_value, i, dataset, liste, adj):

        subNummer = dataset['Trial_Nr'][i]
        valenz = self.get_Valenz(liste, subNummer, adj)
        values = []
        #print(str(subNummer) + "   " + str(liste)+ " " + str(valenz))
        values.append(valenz)


        if not self.is_nan(dataset['02_factor_Pas-Oth-Pre'][i]) and dataset['02_factor_Pas-Oth-Pre'][i] != None and \
                dataset['02_factor_Pas-Oth-Pre'][i] != "" and dataset['02_factor_Pas-Oth-Pre'][i] != " ":
            values.append(dataset['02_factor_Pas-Oth-Pre'][i])

            dic_trial_value.update({int(float(dataset['Trial_Id'][i])): values})
            return dic_trial_value

        if not self.is_nan(dataset['factor02_Pr_Pa_Oth'][i]) and dataset['factor02_Pr_Pa_Oth'][i] != None and \
                dataset['factor02_Pr_Pa_Oth'][i] != "" and dataset['factor02_Pr_Pa_Oth'][i] != " ":
            values.append(dataset['factor02_Pr_Pa_Oth'][i])

            dic_trial_value.update({int(float(dataset['Trial_Id'][i])): values})
            return dic_trial_value

        if not self.is_nan(dataset['factor02_Oth-Pre-Pas'][i]) and dataset['factor02_Oth-Pre-Pas'][i] != None and \
                dataset['factor02_Oth-Pre-Pas'][i] != "" and dataset['factor02_Oth-Pre-Pas'][i] != " ":
            values.append(dataset['factor02_Oth-Pre-Pas'][i])

            dic_trial_value.update({int(float(dataset['Trial_Id'][i])): values})
            return dic_trial_value


        if not self.is_nan(dataset['factor1_Pr_Pa_Oth_55'][i]) and dataset['factor1_Pr_Pa_Oth_55'][i] != None and \
                dataset['factor1_Pr_Pa_Oth_55'][i] != "" and dataset['factor1_Pr_Pa_Oth_55'][i] != " ":
            values.append(dataset['factor1_Pr_Pa_Oth_55'][i])
            dic_trial_value.update({int(float(dataset['Trial_Id'][i])): values})
            return dic_trial_value


        if not self.is_nan(dataset['factor2_Oth_Pre_Pas_55'][i]) and dataset['factor2_Oth_Pre_Pas_55'][i] != None and \
                dataset['factor2_Oth_Pre_Pas_55'][i] != "" and dataset['factor2_Oth_Pre_Pas_55'][i] != " ":
            values.append(dataset['factor2_Oth_Pre_Pas_55'][i])

            dic_trial_value.update({int(float(dataset['Trial_Id'][i])): values})
            return dic_trial_value


        if not self.is_nan(dataset['factor3_Pas-Oth-Pre'][i]) and dataset['factor3_Pas-Oth-Pre'][i] != None and \
                dataset['factor3_Pas-Oth-Pre'][i] != "" and dataset['factor3_Pas-Oth-Pre'][i] != " ":
            values.append(dataset['factor3_Pas-Oth-Pre'][i])

            dic_trial_value.update({int(float(dataset['Trial_Id'][i])): values})
            return dic_trial_value

    """this method returns the list in which the adjective is located"""
    def get_Liste_for_adj(self, i , dataset):

        column = ['02_Readout_Oth-Pre-Pas_0', '02_Readout_Pas-Oth-Pre_0', '02_Readout_Pre-Pas-Oth', 'Readout_Oth_Pre_Pas_55', 'Readout_Pas-Oth-Pre_0', 'Readout_Pr_Pa_Oth_55']
        for c in column:
            if dataset[c][i] == 'depressiv':
                return 1
            elif dataset[c][i] == 'pessimistisch' or dataset[c][i] == 'behindert':
                return 2

    """this method creates a csv file if none exists and inserts how many adjectives of 
    Present Past or other with which valence have been correctly recognized by the test person"""
    def evaluate_past_present_other_test_with_valenz(self):
        global value_list
        print("start  evaluate_past_present_other_test_with valenz")
        dataset = pd.read_csv(self.main_path_lower, sep=';', dtype='unicode')
        count_rows = dataset.shape[0]

        count = 0  # um zu zelehn wie oft rcognition aufgerufen wurde
        help = False  # um zu gucken ob schon eine csv erstellt wurde
        file = Path(self.pre_past_other)
        if file.is_file():
            print("csv schon erstellt")
            help = True
        dic_id_dict = {}
        dic_trial_value ={}

        adj = self.get_adj_as_dict()
        #count variablen

        pres_pos = 0
        pres_neu = 0
        pres_neg = 0
        past_pos = 0
        past_neu = 0
        past_neg = 0
        oth_pos = 0
        oth_neu = 0
        oth_neg = 0
        notShown = 0

        #zeile der erstellten csv
        x = 0
        # for encode
        old_id = 0
        last_id = dataset['subj_counter_global'][count_rows - 1]
        count_last = 0

        #new values
        liste = 1
        # go through the lines

        for i in range(0, count_rows):
            id = dataset['subj_counter_global'][i]

            if not self.is_nan(dataset['Block_Name'][i]) and dataset['Block_Name'][i].endswith("encode"):

                if id != last_id:

                    if id != old_id:

                        if old_id != 0:
                            dic_id_dict.update({int(float(old_id)): dic_trial_value})

                        # quasi der naechste Anfang von encode...

                        liste = self.get_Liste_for_adj(i, dataset)
                        dic_trial_value = {}


                        help_dic = dic_trial_value.copy()
                        dic_trial_value = self.update_dict_trial(help_dic, i, dataset, liste, adj)
                        old_id = id

                    else:
                        help_dic = dic_trial_value.copy()
                        dic_trial_value = self.update_dict_trial(help_dic, i, dataset, liste, adj)
                        old_id = id

                else:
                    count_last += 1
                    if id != old_id:

                        dic_id_dict.update({int(float(old_id)): dic_trial_value})
                        help_dic = dic_trial_value.copy()
                        dic_trial_value = self.update_dict_trial(dic_trial_value, i, dataset, liste, adj)
                        old_id = id

                    elif count_last != 44:
                        help_dic = dic_trial_value.copy()
                        dic_trial_value = self.update_dict_trial(dic_trial_value, i, dataset, liste, adj)
                        old_id = id

                    elif count_last == 44:
                        dic_id_dict.update({int(float(id)): dic_trial_value})

        print(str(dic_id_dict))

        for i in range(0, count_rows):

            if not self.is_nan(dataset['Block_Name'][i]) and dataset['Block_Name'][i].endswith("recognition") and dataset['Task_Nr'][i] != 1 and dataset['Task_Nr'][i] != "1":
                id = dataset['subj_counter_global'][i]

                try:
                    if self.is_nan(id):
                        id = dataset['subj_counter_global'][i+3]

                    id_factor_dic = dic_id_dict[int(float(id))]

                    # wenn quasi die richtige antwort gegeben wurde
                    if dataset['recognition_evaluation'][i] == '1' or dataset['recognition_evaluation'][i] == '2' or \
                            dataset['recognition_evaluation'][i] == '3' or dataset['recognition_evaluation'][i] == 1 or \
                            dataset['recognition_evaluation'][i] == 3 or dataset['recognition_evaluation'][i] == 3:

                        try:
                            value_list = id_factor_dic[int(float(dataset['Trial_Id'][i]))]

                            if value_list[0] == 1:
                                # positiv
                                if value_list[1] == 'Past' or value_list[1] == 'past':
                                    past_pos += 1
                                elif value_list[1] == 'Present' or value_list[1] == 'present':
                                    pres_pos += 1
                                elif value_list[1] == 'other' or value_list[1] == 'Other':
                                    oth_pos += 1

                            elif value_list[0] == 0:
                                # neutal
                                if value_list[1] == 'Past' or value_list[1] == 'past':
                                    past_neu += 1
                                elif value_list[1] == 'Present' or value_list[1] == 'present':
                                    pres_neu += 1
                                elif value_list[1] == 'other' or value_list[1] == 'Other':
                                    oth_neu += 1

                            elif value_list[0] == -1:
                                if value_list[1] == 'Past' or value_list[1] == 'past':
                                    past_neg += 1
                                elif value_list[1] == 'Present' or value_list[1] == 'present':
                                    pres_neg += 1
                                elif value_list[1] == 'other' or value_list[1] == 'Other':
                                    oth_neg += 1

                        except:
                            notShown += 1

                    count += 1
                    if count == 90:
                        if not help:
                            id = dataset['subj_counter_global'][i]
                            data = {'id': [id],
                                    'present_positiv': [pres_pos],
                                    'present_negativ': [pres_neg],
                                    'present_neutral': [pres_neu],
                                    'past_positiv': [past_pos],
                                    'past_negativ': [past_neg],
                                    'past_neutral': [past_neu],
                                    'other_positiv': [oth_pos],
                                    'other_negativ': [oth_neg],
                                    'other_neutral': [oth_neu],
                                    'notShown': [notShown]
                                    }
                            df = pd.DataFrame(data, columns=['id', 'present_positiv', 'present_negativ', 'present_neutral', 'past_positiv', 'past_negativ', 'past_neutral', 'other_positiv', 'other_negativ', 'other_neutral', 'notShown'])
                            df.to_csv(self.pre_past_other, index=False, sep=';')
                            help = True
                            x += 1
                        else:

                            id = dataset['subj_counter_global'][i]
                            df = pd.read_csv(self.pre_past_other, sep=';', dtype='unicode')
                            df._set_value(x, "id", id)
                            df._set_value(x, "present_positiv", pres_pos)
                            df._set_value(x, "present_negativ", pres_neg)
                            df._set_value(x, "present_neutral", pres_neu)
                            df._set_value(x, "past_positiv", past_pos)
                            df._set_value(x, "past_negativ", past_neg)
                            df._set_value(x, "past_neutral", past_neu)
                            df._set_value(x, "other_positiv", oth_pos)
                            df._set_value(x, "other_negativ", oth_neg)
                            df._set_value(x, "other_neutral", oth_neu)
                            df._set_value(x, "notShown", notShown)

                            df.to_csv(self.pre_past_other, index=False, sep=';')
                            x += 1

                        count = 0
                        pres_pos = 0
                        pres_neu = 0
                        pres_neg = 0
                        past_pos = 0
                        past_neu = 0
                        past_neg = 0
                        oth_pos = 0
                        oth_neu = 0
                        oth_neg = 0
                        notShown = 0

                except KeyError:
                    ka = 0 #für ids die nicht gefunden wurden

    """this method returns the table of adjectives as dictionary"""
    def get_adj_as_dict(self, manipul=0):
        dataset = pd.read_csv(self.adj_path, sep=';', dtype='unicode')
        count_rows = dataset.shape[0]
        table_adj = {}
        for i in range(0, count_rows):
            id = dataset['Nr'][i]
            if manipul== 0:
                table_adj.update({int(id): [int(dataset['Liste'][i]), int(dataset['Subnumber'][i]), int(dataset['Valenz'][i])]})
            else:
                table_adj.update({dataset['Adjektiv'][i]: [0, 0]})
        print(table_adj)
        return table_adj

    """this method inserts the values in the table of results,
     ...which, according to index 0, 1, 2... FP, CF, CR,... were named correct / incorrect"""
    def special_data_requests(self, index=1):
        name = ""
        if index == 0:
            name = "FP"
        elif index == 1:
            name = "CF"
        elif index == 2:
            name = "CR"
        elif index == 3:
            name = "CN"
        elif index == 4:
            name = "FF"
        elif index == 5:
            name = "FR"


        print("start  special_data_requests " + str(index))
        dataset = pd.read_csv(self.main_path_lower, sep=';', dtype='unicode')
        count_rows = dataset.shape[0]

        x = 0
        count = 0  # um zu zelehn wie oft rcognition aufgerufen wurde
        help = False  # um zu gucken ob schon eine csv erstellt wurde
        file = Path(self.pre_past_other)
        if file.is_file():
            print("csv schon erstellt")
            help = True

        result = 0

        for i in range(0, count_rows):

            if not self.is_nan(dataset['Block_Name'][i]) and dataset['Block_Name'][i].endswith("recognition") and dataset['Task_Nr'][i] != 1 and dataset['Task_Nr'][i] != "1":
                id = dataset['subj_counter_global'][i]

                if self.is_nan(id):
                    id = dataset['subj_counter_global'][i+3]


                # wenn quasi die richtige antwort gegeben wurde
                if dataset['recognition_evaluation'][i] == str(index) or dataset['recognition_evaluation'][i] == index:
                    result += 1

                count += 1
                if count == 90:
                    if not help:
                        id = dataset['subj_counter_global'][i]
                        data = {'id': [id],
                                name : [int(result)]
                                }
                        df = pd.DataFrame(data, columns=['id', name])
                        df.to_csv(self.pre_past_other, index=False, sep=';')
                        help = True
                        x += 1
                    else:

                        id = dataset['subj_counter_global'][i]
                        df = pd.read_csv(self.pre_past_other, sep=';', dtype='unicode')
                        df._set_value(x, "id", id)
                        df._set_value(x, name, int(result))


                        df.to_csv(self.pre_past_other, index=False, sep=';')
                        x += 1

                    count = 0
                    result = 0

    """this method inserts several values from the Labvanced and Unipark table into the results table"""
    def merge_result(self):
        #get data
        # initilize
        dataset = pd.read_csv(self.main_path_lower, sep=';', dtype='unicode')
        count_rows = dataset.shape[0]
        # gucke ob tabellen schon zusammengefuegt wurden, ansonsten füge sie zusammen
        dic = {}
        values = []
        """try:
            k = dataset['VPCode'][33]
        except KeyError:
            self.merge()"""

        #get data from LD
        old_id = 0
        last_id=dataset['subj_counter_global'][count_rows-1]
        for i in range(count_rows):
            id = dataset['subj_counter_global'][i]

            if id != old_id:

                values.append(dataset['ParticipantCode'][i])
                group = dataset['group_name'][i]
                if not self.is_nan(group) and not self.is_nan(dataset['Gender1'][i]) :
                    gr_nr = int(list(group)[list(group).__len__() - 1])
                    gender = dataset['Gender1'][i]
                    gen = 0
                    if gender.startswith('W') or gender.startswith('w') or gender.startswith('F') or gender.startswith('f'):
                        gen = 1
                    elif gender.startswith('M') or gender.startswith('m'):
                        gen = 2
                    elif gender.startswith('D') or gender.startswith('d'):
                        gen = 88

                    values.append(gr_nr)
                    values.append(int(gen))
                    values.append(dataset['Age1'][i])
                    #print(str(values[0])+ " " + str(values[3]))
                    dic.update({int(float(dataset['subj_counter_global'][i])): values})
                    values = []
                    old_id = id

                values = []
            else:
                values = []

        # get data from Unipark
        self.insert_subjcounter_in_second_path()
        unipark = pd.read_csv(self.second_path_lower, sep=';', dtype='unicode')
        count_rows_unipark = unipark.shape[0]
        dic_ud = {}
        infos = []
        names = ['K_Mittelwert', 'PW_Mittelwert', 'SL_Mittelwert', 'A_Mittelwert', 'SA_Mittelwert', 'PB_Mittelwert', 'PWB_Mittelwert', 'self_esteem', 'social_psycologic_wellbeing', 'wissenaufgabentyp', 'BAMA', 'Semester', 'Studiengang', 'Student', 'Deutschkenntnisse', 'Bearbeitung']
        for i in range(count_rows_unipark):
            if not self.is_nan(unipark['subject_counter'][i]):
                for s in names:
                    infos.append(unipark[s][i])

                dic_ud.update({int(float(unipark['subject_counter'][i])): infos})

            infos = []

        # insert data
        print(dic_ud)
        df = pd.read_csv(self.pre_past_other, sep=';', dtype='unicode')
        count_rows_result = dataset.shape[0]
        for i in range(count_rows_result):
            try:
                if not self.is_nan(df['id'][i]):
                    id = int(float(df['id'][i]))
                    LD = dic[id]
                    UD = dic_ud[id]
                    df._set_value(i, "VPCode", LD[0])
                    df._set_value(i, "Gender", LD[2])
                    df._set_value(i, "Group", LD[1])
                    df._set_value(i, 'Age', LD[3])

                    x=0
                    for s in names:
                        df._set_value(i, s, UD[x])
                        x += 1


            except KeyError:
                l =0

        df.to_csv(self.pre_past_other, index=False, sep=';')

    """this method inserts the subjectcounter into the Unipark table to generate a foreign key"""
    def insert_subjcounter_in_second_path(self):

        dataset = pd.read_csv(self.main_path_lower, sep=';', dtype='unicode')
        count_rows = dataset.shape[0]
        dic = {}

        for i in range(count_rows):

            if not self.is_nan(dataset['ParticipantCode'][i]):

                if list(dataset['ParticipantCode'][i])[0] != 'se' and list(dataset['ParticipantCode'][i])[0] != 'Se':

                    dic.update({dataset['ParticipantCode'][i]: dataset['subj_counter_global'][i]})

        print(dic)
        df = pd.read_csv(self.second_path_lower, sep=';', dtype='unicode')
        count_rows_sec = df.shape[0]

        sbjc = ""
        for i in range(count_rows_sec):
            code = df['VPCode'][i]
            try:
                sbjc = dic.__getitem__(code)
                df._set_value(i, 'subject_counter', sbjc)
            except KeyError:
                for c in dic:
                    ld = list(c)
                    ud = list(code)
                    if ld[0]== ud[0] and ld[1] == ud[1] and ld[ld.__len__()-1] == ud[ud.__len__()-1]:
                        sbjc = dic.__getitem__(c)
                        df._set_value(i, 'subject_counter', sbjc)


        df.to_csv(self.second_path_lower, index=False, sep=';')
        print("subject_counter in Uniparkdata nachgetragen")


    """this method adds the column reco_ppo to the labvanced table,
     in which an index is written from 0 to 11, depending on whether the adjective present Past,
      other was or was not named and depending on whether 0 1 or 2 was trusted or not ticked 0 to 11"""
    def reco_eval_full(self, name= "reco_ppo"):
        print("start ihs")
        # get tabel and append new column
        dataset = pd.read_csv(self.main_path_lower, sep=';',dtype='unicode')
        dataset[name] = ""
        # get the number of columns
        count_rows = dataset.shape[0]
        # make list and dir to save values
        trial_ID_ppo_ = {}
        dict_ID_TrtialIDs = {}
        # save the last and the old id "subje_ctcounter"
        old_id = 0
        last_id=dataset['subj_counter_global'][count_rows-1]
        # just in time to get the end of the last section
        count_last = 0
        # go through all rows




        for i in range(0, count_rows):
            # get the id of the row
            id = dataset['subj_counter_global'][i]

            # if the BlockName end with encode
            if not self.is_nan(dataset['Block_Name'][i]) and dataset['Block_Name'][i].endswith("encode"):

                """for each line check if it is not the last id, if not, append the values to the list until the id changes.
                    if the id changes add this list and the corresponding id to the dict. If the id is the last id, 
                    add the previous list to dict. and continue adding values to the list until counter 44 is reached"""

                if id != last_id:
                    if id != old_id:
                        if old_id != 0:
                            dict_ID_TrtialIDs.update({int(float(old_id)) : trial_ID_ppo_})

                        """trial_Ids = []
                        trial_Ids.append(int(float(dataset['Trial_Id'][i])))
                        old_id = id"""
                        trial_ID_ppo_ = {}
                        trial_ID_ppo_ = self.get_Pre_past_other(dataset, i, trial_ID_ppo_)
                        old_id = id

                    else:
                        trial_ID_ppo_ = self.get_Pre_past_other(dataset, i, trial_ID_ppo_)
                        old_id = id
                else:
                    count_last += 1
                    if id != old_id:

                        dict_ID_TrtialIDs.update({int(float(old_id)): trial_ID_ppo_})
                        trial_Ids = []
                        trial_ID_ppo_ = self.get_Pre_past_other(dataset, i, trial_ID_ppo_)
                        old_id = id

                    elif count_last != 44:
                        trial_ID_ppo_ = self.get_Pre_past_other(dataset, i, trial_ID_ppo_)
                        old_id = id

                    elif count_last == 44:
                        dict_ID_TrtialIDs.update({int(float(id)): trial_ID_ppo_})


        print(str(dict_ID_TrtialIDs))

        #go through the table one more time
        for i in range(0, count_rows):

            # if the BlockName end with recognition
            if not self.is_nan(dataset['Block_Name'][i]) and dataset['Block_Name'][i].endswith("recognition") and\
                    dataset['Task_Nr'][i] != 1 and dataset['Task_Nr'][i] != "1":

                if not self.is_nan(dataset['subj_counter_global'][i]) and dataset['subj_counter_global'][i] != "" and\
                        dataset['subj_counter_global'][i] != " " and dataset['subj_counter_global'][i] != None:

                     #get the appropriate list from the dict. to see if the Triaal id has been used before.
                     #Try catch, as it is possible that there may be entries for recognition of a person but not for encode

                    try:
                        trial_Id_dic = dict_ID_TrtialIDs[int(float(dataset['subj_counter_global'][i]))]
                    except:
                        continue


                    #get values to evaluate the output
                    guess = dataset['RemKnoGue_55'][i]
                    trial_Id = int(float(dataset['Trial_Id'][i]))

                    # evaluate the result of recognition and write it in the new column
                    evaluate = self.evaluate_reco_pre_past_other(guess, trial_Id_dic, trial_Id)
                    dataset._set_value(i, name, evaluate)


        dataset.to_csv(self.main_path_lower, index=False, sep=';')


    """this method updates the passed diconary with the respective 
    value from one of the 6 lines for Pre past or Other"""
    def get_Pre_past_other(self, dataset, i, dic_trial_ppo):

        if not self.is_nan(dataset['02_factor_Pas-Oth-Pre'][i]) and dataset['02_factor_Pas-Oth-Pre'][i] != None and \
                dataset['02_factor_Pas-Oth-Pre'][i] != "" and dataset['02_factor_Pas-Oth-Pre'][i] != " ":
            dic_trial_ppo.update({int(float(dataset['Trial_Id'][i])): dataset['02_factor_Pas-Oth-Pre'][i]})

            return dic_trial_ppo

        if not self.is_nan(dataset['factor02_Pr_Pa_Oth'][i]) and dataset['factor02_Pr_Pa_Oth'][i] != None and \
                dataset['factor02_Pr_Pa_Oth'][i] != "" and dataset['factor02_Pr_Pa_Oth'][i] != " ":
            dic_trial_ppo.update({int(float(dataset['Trial_Id'][i])): dataset['factor02_Pr_Pa_Oth'][i]})

            return dic_trial_ppo

        if not self.is_nan(dataset['factor02_Oth-Pre-Pas'][i]) and dataset['factor02_Oth-Pre-Pas'][i] != None and \
                dataset['factor02_Oth-Pre-Pas'][i] != "" and dataset['factor02_Oth-Pre-Pas'][i] != " ":
            dic_trial_ppo.update({int(float(dataset['Trial_Id'][i])): dataset['factor02_Oth-Pre-Pas'][i]})

            return dic_trial_ppo

        if not self.is_nan(dataset['factor1_Pr_Pa_Oth_55'][i]) and dataset['factor1_Pr_Pa_Oth_55'][i] != None and \
                dataset['factor1_Pr_Pa_Oth_55'][i] != "" and dataset['factor1_Pr_Pa_Oth_55'][i] != " ":
            dic_trial_ppo.update({int(float(dataset['Trial_Id'][i])): dataset['factor1_Pr_Pa_Oth_55'][i]})

            return dic_trial_ppo

        if not self.is_nan(dataset['factor2_Oth_Pre_Pas_55'][i]) and dataset['factor2_Oth_Pre_Pas_55'][i] != None and \
                dataset['factor2_Oth_Pre_Pas_55'][i] != "" and dataset['factor2_Oth_Pre_Pas_55'][i] != " ":
            dic_trial_ppo.update({int(float(dataset['Trial_Id'][i])): dataset['factor2_Oth_Pre_Pas_55'][i]})

            return dic_trial_ppo

        if not self.is_nan(dataset['factor3_Pas-Oth-Pre'][i]) and dataset['factor3_Pas-Oth-Pre'][i] != None and \
                dataset['factor3_Pas-Oth-Pre'][i] != "" and dataset['factor3_Pas-Oth-Pre'][i] != " ":
            dic_trial_ppo.update({int(float(dataset['Trial_Id'][i])): dataset['factor3_Pas-Oth-Pre'][i]})

            return dic_trial_ppo

    """this method is only for overview and evaluates the index according to the data provided"""
    def evaluate_reco_pre_past_other(self, guess, trial_Id_dic, trial_Id):
        # ist es in encode ?
        ppo = ''
        in_encode = False
        try:
            ppo = trial_Id_dic[trial_Id]
            in_encode = True
        except:
            in_encode = False

        if in_encode:
            #Wort wurde genannt

            if ppo == 'Present' or ppo == 'present':

                if int(float(guess)) == 0:
                    return 0
                elif int(float(guess)) == 1:
                    return 1
                elif int(float(guess)) == 2:
                    return 2

            elif ppo == 'Past' or ppo == 'past':
                if int(float(guess)) == 0:
                    return 3
                elif int(float(guess)) == 1:
                    return 4
                elif int(float(guess)) == 2:
                    return 5

            elif ppo == 'Other' or ppo == 'other':
                if int(float(guess)) == 0:
                    return 6
                elif int(float(guess)) == 1:
                    return 7
                elif int(float(guess)) == 2:
                    return 8

        else:
            #Wort wurde nicht genannt
            if int(float(guess)) == 0:
                return 9
            elif int(float(guess)) == 1:
                return 10
            elif int(float(guess)) == 2:
                return 11





    """this method makes the query on the created index reco_ppo
     and inserts the respective column of the count into the result table"""
    def special_data(self, index=1):
        name = ""
        if index == 0:
            name = "FP_present"
        elif index == 1:
            name = "CF_present"
        elif index == 2:
            name = "CR_present"
        elif index == 3:
            name = "FP_past"
        elif index == 4:
            name = "CF_past"
        elif index == 5:
            name = "CR_past"
        elif index == 6:
            name = "FP_other"
        elif index == 7:
            name = "CF_other"
        elif index == 8:
            name = "CR_other"
        elif index == 9:
            name = "CN"
        elif index == 10:
            name = "FF"
        elif index == 11:
            name = "FR"


        print("start  special_data_requests " + str(index))
        dataset = pd.read_csv(self.main_path_lower, sep=';', dtype='unicode')
        count_rows = dataset.shape[0]

        x = 0
        count = 0  # um zu zelehn wie oft rcognition aufgerufen wurde
        help = False  # um zu gucken ob schon eine csv erstellt wurde
        file = Path(self.pre_past_other)
        if file.is_file():
            print("csv schon erstellt")
            help = True

        result = 0

        for i in range(0, count_rows):

            if not self.is_nan(dataset['Block_Name'][i]) and dataset['Block_Name'][i].endswith("recognition") and dataset['Task_Nr'][i] != 1 and dataset['Task_Nr'][i] != "1":
                id = dataset['subj_counter_global'][i]

                if self.is_nan(id):
                    id = dataset['subj_counter_global'][i+3]


                # wenn quasi die richtige antwort gegeben wurde
                if dataset['reco_ppo'][i] == str(index) or dataset['reco_ppo'][i] == index:
                    result += 1

                count += 1
                if count == 90:
                    if not help:
                        id = dataset['subj_counter_global'][i]
                        data = {'id': [id],
                                name : [int(result)]
                                }
                        df = pd.DataFrame(data, columns=['id', name])
                        df.to_csv(self.pre_past_other, index=False, sep=';')
                        help = True
                        x += 1
                    else:

                        id = dataset['subj_counter_global'][i]
                        df = pd.read_csv(self.pre_past_other, sep=';', dtype='unicode')
                        df._set_value(x, "id", id)
                        df._set_value(x, name, int(result))


                        df.to_csv(self.pre_past_other, index=False, sep=';')
                        x += 1

                    count = 0
                    result = 0


    """Manipulatipon check, """
    """this method inserts the two columns controllpast and controll present into the adjective table, 
    in which the average of all liquid values stands for present or past, per adjective.
    This method is similar to the manipulation Chek for encode"""
    def manipulation_encode(self):
        print("start special")
        #self.clean_adj()
        #adjective = self.adj_as_dic()

        dataset = pd.read_csv(self.main_path_lower, sep=';',dtype='unicode')
        count_rows = dataset.shape[0]
        # make list and dir to save values
        adjective ={}
        prepastoth = {}
        values = []



        for i in range(0, count_rows):
            # get the id of the row
            id = dataset['subj_counter_global'][i]

            # if the BlockName end with encode
            if not self.is_nan(dataset['Block_Name'][i]) and dataset['Block_Name'][i].endswith("encode"):
                adj = self.get_adj_encode(i, dataset)
                ppo = self.get_prepastother_encode(i, dataset)
                liq = float(self.get_liq_encode(i, dataset))
                try:
                    ppoHelp = adjective[adj]
                    try:
                        ppoHelp.update({ppo.lower() : [ppoHelp[ppo.lower()][0] + liq, ppoHelp[ppo.lower()][1] + 1]})
                        adjective.update({adj : ppoHelp})
                    except KeyError:
                        ppoHelp.update({ppo.lower() : [liq, 1]})
                        adjective.update({adj : ppoHelp})

                except KeyError:
                    prepastoth.update({ppo.lower(): [liq, 1]})
                    adjective.update({adj: prepastoth})
                    prepastoth = {}

        print(str(adjective))

        df = pd.read_csv(self.adj_path, sep=';', dtype='unicode')
        df = df.set_index("Adjektiv", drop=False)
        column_names = ['encode_past', "encode_present", "encode_other"]
        for p in column_names:
            df[p] = 0.00

        for i in adjective:
            past = float(int(adjective[i]['past'][0]) / int(adjective[i]['past'][1]))
            df["encode_past"][i] = past.__round__(3)
            present = float(int(adjective[i]['present'][0]) / int(adjective[i]['present'][1]))
            df["encode_present"][i] = present.__round__(3)
            other = float(int(adjective[i]['other'][0]) / int(adjective[i]['other'][1]))
            df["encode_other"][i] = other.__round__(3)


        df.to_csv(self.adj_path, index=False, sep=';', float_format='%.3f', decimal='.', header=True)


    """this method is to help you get the prepast or other value 
    from the 6 different columns each for encode"""
    def get_prepastother_encode(self, i, dataset):
        if not self.is_nan(dataset['02_factor_Pas-Oth-Pre'][i]) and dataset['02_factor_Pas-Oth-Pre'][i] != None and \
                dataset['02_factor_Pas-Oth-Pre'][i] != "" and dataset['02_factor_Pas-Oth-Pre'][i] != " ":

            return dataset['02_factor_Pas-Oth-Pre'][i]

        if not self.is_nan(dataset['factor02_Pr_Pa_Oth'][i]) and dataset['factor02_Pr_Pa_Oth'][i] != None and \
                dataset['factor02_Pr_Pa_Oth'][i] != "" and dataset['factor02_Pr_Pa_Oth'][i] != " ":

            return dataset['factor02_Pr_Pa_Oth'][i]

        if not self.is_nan(dataset['factor02_Oth-Pre-Pas'][i]) and dataset['factor02_Oth-Pre-Pas'][i] != None and \
                dataset['factor02_Oth-Pre-Pas'][i] != "" and dataset['factor02_Oth-Pre-Pas'][i] != " ":

            return dataset['factor02_Oth-Pre-Pas'][i]

        if not self.is_nan(dataset['factor1_Pr_Pa_Oth_55'][i]) and dataset['factor1_Pr_Pa_Oth_55'][i] != None and \
                dataset['factor1_Pr_Pa_Oth_55'][i] != "" and dataset['factor1_Pr_Pa_Oth_55'][i] != " ":

            return dataset['factor1_Pr_Pa_Oth_55'][i]
        if not self.is_nan(dataset['factor2_Oth_Pre_Pas_55'][i]) and dataset['factor2_Oth_Pre_Pas_55'][i] != None and \
                dataset['factor2_Oth_Pre_Pas_55'][i] != "" and dataset['factor2_Oth_Pre_Pas_55'][i] != " ":

            return dataset['factor2_Oth_Pre_Pas_55'][i]

        if not self.is_nan(dataset['factor3_Pas-Oth-Pre'][i]) and dataset['factor3_Pas-Oth-Pre'][i] != None and \
                dataset['factor3_Pas-Oth-Pre'][i] != "" and dataset['factor3_Pas-Oth-Pre'][i] != " ":

            return dataset['factor3_Pas-Oth-Pre'][i]

    """this method is to help you get the liq value 
    from the 6 different columns each for encode"""
    def get_liq_encode(self, i, dataset):
        if not self.is_nan(dataset['02_Save_likert_Oth-Pre-Pas'][i]) and dataset['02_Save_likert_Oth-Pre-Pas'][i] != None and \
                dataset['02_Save_likert_Oth-Pre-Pas'][i] != "" and dataset['02_Save_likert_Oth-Pre-Pas'][i] != " ":
            return dataset['02_Save_likert_Oth-Pre-Pas'][i]

        if not self.is_nan(dataset['02_Save_likert_Pas-Oth-Pre'][i]) and dataset['02_Save_likert_Pas-Oth-Pre'][i] != None and \
                dataset['02_Save_likert_Pas-Oth-Pre'][i] != "" and dataset['02_Save_likert_Pas-Oth-Pre'][i] != " ":
            return dataset['02_Save_likert_Pas-Oth-Pre'][i]

        if not self.is_nan(dataset['02_Save_likert_Pr_Pa_Oth'][i]) and dataset['02_Save_likert_Pr_Pa_Oth'][i] != None and \
                dataset['02_Save_likert_Pr_Pa_Oth'][i] != "" and dataset['02_Save_likert_Pr_Pa_Oth'][i] != " ":
            return dataset['02_Save_likert_Pr_Pa_Oth'][i]

        if not self.is_nan(dataset['Save_likert_Pr_Pa_Oth_55'][i]) and dataset['Save_likert_Pr_Pa_Oth_55'][i] != None and \
                dataset['Save_likert_Pr_Pa_Oth_55'][i] != "" and dataset['Save_likert_Pr_Pa_Oth_55'][i] != " ":
            return dataset['Save_likert_Pr_Pa_Oth_55'][i]
        if not self.is_nan(dataset['Save_likert_Oth_Pre_Pas_55'][i]) and dataset['Save_likert_Oth_Pre_Pas_55'][i] != None and \
                dataset['Save_likert_Oth_Pre_Pas_55'][i] != "" and dataset['Save_likert_Oth_Pre_Pas_55'][i] != " ":
            return dataset['Save_likert_Oth_Pre_Pas_55'][i]

        if not self.is_nan(dataset['Save_likert_Pas-Oth-Pre'][i]) and dataset['Save_likert_Pas-Oth-Pre'][i] != None and \
                dataset['Save_likert_Pas-Oth-Pre'][i] != "" and dataset['Save_likert_Pas-Oth-Pre'][i] != " ":
            return dataset['Save_likert_Pas-Oth-Pre'][i]

    """this method is to help you get the adjective 
    from the 6 different columns each for encode"""
    def get_adj_encode(self, i, dataset):
        if not self.is_nan(dataset['02_Readout_Pas-Oth-Pre_0'][i]) and dataset['02_Readout_Pas-Oth-Pre_0'][i] != None and \
                dataset['02_Readout_Pas-Oth-Pre_0'][i] != "" and dataset['02_Readout_Pas-Oth-Pre_0'][i] != " ":

            return dataset['02_Readout_Pas-Oth-Pre_0'][i]

        if not self.is_nan(dataset['02_Readout_Pre-Pas-Oth'][i]) and dataset['02_Readout_Pre-Pas-Oth'][i] != None and \
                dataset['02_Readout_Pre-Pas-Oth'][i] != "" and dataset['02_Readout_Pre-Pas-Oth'][i] != " ":
            return dataset['02_Readout_Pre-Pas-Oth'][i]


        if not self.is_nan(dataset['02_Readout_Oth-Pre-Pas_0'][i]) and dataset['02_Readout_Oth-Pre-Pas_0'][i] != None and \
                dataset['02_Readout_Oth-Pre-Pas_0'][i] != "" and dataset['02_Readout_Oth-Pre-Pas_0'][i] != " ":

            return dataset['02_Readout_Oth-Pre-Pas_0'][i]


        if not self.is_nan(dataset['Readout_Oth_Pre_Pas_55'][i]) and dataset['Readout_Oth_Pre_Pas_55'][i] != None and \
                dataset['Readout_Oth_Pre_Pas_55'][i] != "" and dataset['Readout_Oth_Pre_Pas_55'][i] != " ":

            return dataset['Readout_Oth_Pre_Pas_55'][i]

        if not self.is_nan(dataset['Readout_Pas-Oth-Pre_0'][i]) and dataset['Readout_Pas-Oth-Pre_0'][i] != None and \
                dataset['Readout_Pas-Oth-Pre_0'][i] != "" and dataset['Readout_Pas-Oth-Pre_0'][i] != " ":
            return dataset['Readout_Pas-Oth-Pre_0'][i]

        if not self.is_nan(dataset['Readout_Pr_Pa_Oth_55'][i]) and dataset['Readout_Pr_Pa_Oth_55'][
            i] != None and \
                dataset['Readout_Pr_Pa_Oth_55'][i] != "" and dataset['Readout_Pr_Pa_Oth_55'][i] != " ":
            return dataset['Readout_Pr_Pa_Oth_55'][i]



    """Manipulatipon check, """
    """this method inserts the two columns controllpast and controll present into the adjective table, 
    in which the average of all liquid values stands for present or past, per adjective.
    This method is similar to the manipulation Chek for controll"""
    def manipulation_controll(self):
        print("start special")
        #self.clean_adj()

        dataset = pd.read_csv(self.main_path_lower, sep=';',dtype='unicode')
        count_rows = dataset.shape[0]
        # make list and dir to save values
        adjective ={}
        prepastoth = {}


        for i in range(0, count_rows):


            if not self.is_nan(dataset['Block_Name'][i]) and dataset['Block_Name'][i].endswith("contr"):
                adj = self.get_adj_controll(i, dataset)
                ppo = self.get_prepastother_controll(i, dataset)
                liq = float(self.get_liq_controll(i, dataset))
                try:
                    ppoHelp = adjective[adj]
                    try:
                        ppoHelp.update({ppo.lower() : [ppoHelp[ppo.lower()][0] + liq, ppoHelp[ppo.lower()][1] + 1]})
                        adjective.update({adj : ppoHelp})
                    except KeyError:
                        ppoHelp.update({ppo.lower() : [liq, 1]})
                        adjective.update({adj : ppoHelp})

                except KeyError:
                    prepastoth.update({ppo.lower(): [liq, 1]})
                    adjective.update({adj: prepastoth})
                    prepastoth = {}

        print(str(adjective))

        df = pd.read_csv(self.adj_path, sep=';', dtype='unicode')
        df = df.set_index("Adjektiv", drop=False)
        column_names = ['controll_past', "controll_present"]
        for p in column_names:
            df[p] = 0.00

        for i in adjective:
            df = df.set_index("Adjektiv", drop=False)
            past = float(int(adjective[i]['past'][0]) / int(adjective[i]['past'][1]))
            df["controll_past"][i] = past.__round__(3)
            present = float(int(adjective[i]['present'][0]) / int(adjective[i]['present'][1]))
            df["controll_present"][i] = present.__round__(3)




        df.to_csv(self.adj_path, index=False, sep=';', float_format='%.3f', decimal='.', header=True)


    """this method is to help you get the prepast or other value 
    from the 6 different columns each for controll"""
    def get_prepastother_controll(self, i, dataset):
        if not self.is_nan(dataset['Manipul_02_factor_Pas-Oth-Pre'][i]) and dataset['Manipul_02_factor_Pas-Oth-Pre'][i] != None and \
                dataset['Manipul_02_factor_Pas-Oth-Pre'][i] != "" and dataset['Manipul_02_factor_Pas-Oth-Pre'][i] != " ":

            return dataset['Manipul_02_factor_Pas-Oth-Pre'][i]

        if not self.is_nan(dataset['Manipul_factor02_Oth-Pre-Pas'][i]) and dataset['Manipul_factor02_Oth-Pre-Pas'][i] != None and \
                dataset['Manipul_factor02_Oth-Pre-Pas'][i] != "" and dataset['Manipul_factor02_Oth-Pre-Pas'][i] != " ":

            return dataset['Manipul_factor02_Oth-Pre-Pas'][i]

        if not self.is_nan(dataset['Manipul_factor02_Pr_Pa_Oth'][i]) and dataset['Manipul_factor02_Pr_Pa_Oth'][i] != None and \
                dataset['Manipul_factor02_Pr_Pa_Oth'][i] != "" and dataset['Manipul_factor02_Pr_Pa_Oth'][i] != " ":

            return dataset['Manipul_factor02_Pr_Pa_Oth'][i]

        if not self.is_nan(dataset['Manipul_factor1_Pr_Pa_Oth'][i]) and dataset['Manipul_factor1_Pr_Pa_Oth'][i] != None and \
                dataset['Manipul_factor1_Pr_Pa_Oth'][i] != "" and dataset['Manipul_factor1_Pr_Pa_Oth'][i] != " ":

            return dataset['Manipul_factor1_Pr_Pa_Oth'][i]
        if not self.is_nan(dataset['Manipul_factor2_Oth_Pre_Pas'][i]) and dataset['Manipul_factor2_Oth_Pre_Pas'][i] != None and \
                dataset['Manipul_factor2_Oth_Pre_Pas'][i] != "" and dataset['Manipul_factor2_Oth_Pre_Pas'][i] != " ":

            return dataset['Manipul_factor2_Oth_Pre_Pas'][i]

        if not self.is_nan(dataset['Manipul_factor3_Pas-Oth-Pre'][i]) and dataset['Manipul_factor3_Pas-Oth-Pre'][i] != None and \
                dataset['Manipul_factor3_Pas-Oth-Pre'][i] != "" and dataset['Manipul_factor3_Pas-Oth-Pre'][i] != " ":

            return dataset['Manipul_factor3_Pas-Oth-Pre'][i]

    """this method is to help you get the liq value 
    from the 6 different columns each for controll"""
    def get_liq_controll(self, i, dataset):
        if not self.is_nan(dataset['Manipul_02_Save_likert_Oth-Pre-Pas'][i]) and dataset['Manipul_02_Save_likert_Oth-Pre-Pas'][i] != None and \
                dataset['Manipul_02_Save_likert_Oth-Pre-Pas'][i] != "" and dataset['Manipul_02_Save_likert_Oth-Pre-Pas'][i] != " ":
            return dataset['Manipul_02_Save_likert_Oth-Pre-Pas'][i]

        if not self.is_nan(dataset['Manipul_02_Save_likert_Pas-Oth-Pre'][i]) and dataset['Manipul_02_Save_likert_Pas-Oth-Pre'][i] != None and \
                dataset['Manipul_02_Save_likert_Pas-Oth-Pre'][i] != "" and dataset['Manipul_02_Save_likert_Pas-Oth-Pre'][i] != " ":
            return dataset['Manipul_02_Save_likert_Pas-Oth-Pre'][i]

        if not self.is_nan(dataset['Manipul_02_Save_likert_Pr_Pa_Oth'][i]) and dataset['Manipul_02_Save_likert_Pr_Pa_Oth'][i] != None and \
                dataset['Manipul_02_Save_likert_Pr_Pa_Oth'][i] != "" and dataset['Manipul_02_Save_likert_Pr_Pa_Oth'][i] != " ":
            return dataset['Manipul_02_Save_likert_Pr_Pa_Oth'][i]

        if not self.is_nan(dataset['Manipul_Save_likert_Pas-Oth-Pre'][i]) and dataset['Manipul_Save_likert_Pas-Oth-Pre'][i] != None and \
                dataset['Manipul_Save_likert_Pas-Oth-Pre'][i] != "" and dataset['Manipul_Save_likert_Pas-Oth-Pre'][i] != " ":
            return dataset['Manipul_Save_likert_Pas-Oth-Pre'][i]
        if not self.is_nan(dataset['Manipul_Save_likert_Pr_Pa_Oth'][i]) and dataset['Manipul_Save_likert_Pr_Pa_Oth'][i] != None and \
                dataset['Manipul_Save_likert_Pr_Pa_Oth'][i] != "" and dataset['Manipul_Save_likert_Pr_Pa_Oth'][i] != " ":
            return dataset['Manipul_Save_likert_Pr_Pa_Oth'][i]

        if not self.is_nan(dataset['Manipul_Save_likert_Oth_Pre_Pas'][i]) and dataset['Manipul_Save_likert_Oth_Pre_Pas'][i] != None and \
                dataset['Manipul_Save_likert_Oth_Pre_Pas'][i] != "" and dataset['Manipul_Save_likert_Oth_Pre_Pas'][i] != " ":
            return dataset['Manipul_Save_likert_Oth_Pre_Pas'][i]

    """this method is to help you get the adjective 
    from the 6 different columns each for controll"""
    def get_adj_controll(self, i, dataset):
        if not self.is_nan(dataset['Manipul_02_Readout_Oth-Pre-Pas_66'][i]) and dataset['Manipul_02_Readout_Oth-Pre-Pas_66'][i] != None and \
                dataset['Manipul_02_Readout_Oth-Pre-Pas_66'][i] != "" and dataset['Manipul_02_Readout_Oth-Pre-Pas_66'][i] != " ":

            return dataset['Manipul_02_Readout_Oth-Pre-Pas_66'][i]

        if not self.is_nan(dataset['Manipul_02_Readout_Pas-Oth-Pre_66'][i]) and dataset['Manipul_02_Readout_Pas-Oth-Pre_66'][i] != None and \
                dataset['Manipul_02_Readout_Pas-Oth-Pre_66'][i] != "" and dataset['Manipul_02_Readout_Pas-Oth-Pre_66'][i] != " ":
            return dataset['Manipul_02_Readout_Pas-Oth-Pre_66'][i]


        if not self.is_nan(dataset['Manipul_02_Readout_Pre-Pas-Oth_66'][i]) and dataset['Manipul_02_Readout_Pre-Pas-Oth_66'][i] != None and \
                dataset['Manipul_02_Readout_Pre-Pas-Oth_66'][i] != "" and dataset['Manipul_02_Readout_Pre-Pas-Oth_66'][i] != " ":

            return dataset['Manipul_02_Readout_Pre-Pas-Oth_66'][i]


        if not self.is_nan(dataset['Manipul_Readout_Oth_Pre_Pas_66'][i]) and dataset['Manipul_Readout_Oth_Pre_Pas_66'][i] != None and \
                dataset['Manipul_Readout_Oth_Pre_Pas_66'][i] != "" and dataset['Manipul_Readout_Oth_Pre_Pas_66'][i] != " ":

            return dataset['Manipul_Readout_Oth_Pre_Pas_66'][i]

        if not self.is_nan(dataset['Manipul_Readout_Pas-Oth-Pre_66'][i]) and dataset['Manipul_Readout_Pas-Oth-Pre_66'][i] != None and \
                dataset['Manipul_Readout_Pas-Oth-Pre_66'][i] != "" and dataset['Manipul_Readout_Pas-Oth-Pre_66'][i] != " ":
            return dataset['Manipul_Readout_Pas-Oth-Pre_66'][i]

        if not self.is_nan(dataset['Manipul_Readout_Pr_Pa_Oth_final'][i]) and dataset['Manipul_Readout_Pr_Pa_Oth_final'][i] != None and \
                dataset['Manipul_Readout_Pr_Pa_Oth_final'][i] != "" and dataset['Manipul_Readout_Pr_Pa_Oth_final'][i] != " ":
            return dataset['Manipul_Readout_Pr_Pa_Oth_final'][i]



    """Manipulation recognition"""
    """this method inserts the two spades just_12 and correct_12 into the table of results,
     this is the manipulation check for recognition. This means that it counts how often 1 or 2 was checked or 
     how often the word was correctly named and 1 or 2 was checked"""
    def manipulation_reco(self):

        print("start insert recognition evaluation test")
        # get tabel and append new column
        dataset = pd.read_csv(self.main_path_lower, sep=';', dtype='unicode')

        # get the number of columns
        count_rows = dataset.shape[0]
        # make list and dir to save values
        adje = []
        dict_ID_TrtialIDs = {}
        # save the last and the old id "subje_ctcounter"
        old_id = 0
        last_id = dataset['subj_counter_global'][count_rows - 1]
        # just in time to get the end of the last section
        count_last = 0
        # go through all rows

        for i in range(0, count_rows):
            # get the id of the row
            id = dataset['subj_counter_global'][i]

            # if the BlockName end with encode
            if not self.is_nan(dataset['Block_Name'][i]) and dataset['Block_Name'][i].endswith("encode"):

                if id != last_id:
                    if id != old_id:
                        if old_id != 0:
                            dict_ID_TrtialIDs.update({int(float(old_id)): adje})

                        adje = []
                        adje.append(self.get_adj_encode(i, dataset))
                        old_id = id
                    else:
                        adje.append(self.get_adj_encode(i, dataset))
                        old_id = id
                else:
                    count_last += 1
                    if id != old_id:

                        dict_ID_TrtialIDs.update({int(float(old_id)): adje})
                        adje = []
                        adje.append(self.get_adj_encode(i, dataset))
                        old_id = id

                    elif count_last != 44:
                        adje.append(self.get_adj_encode(i, dataset))
                        old_id = id

                    elif count_last == 44:
                        dict_ID_TrtialIDs.update({int(float(id)): adje})

        print(dict_ID_TrtialIDs)
        adjective = self.get_adj_as_dict(manipul=1)
        print(adjective)
        # go through the table one more time
        for i in range(0, count_rows):

            # if the BlockName end with recognition
            if not self.is_nan(dataset['Block_Name'][i]) and dataset['Block_Name'][i].endswith("recognition") and \
                    dataset['Task_Nr'][i] != 1 and dataset['Task_Nr'][i] != "1":

                if not self.is_nan(dataset['subj_counter_global'][i]) and dataset['subj_counter_global'][i] != "" and \
                        dataset['subj_counter_global'][i] != " " and dataset['subj_counter_global'][i] != None:

                    #get the appropriate list from the dict. to see if the Triaal id has been used before.
                     #Try catch, as it is possible that there may be entries for recognition of a person but not for encode

                    try:
                        adjec = dict_ID_TrtialIDs[int(float(dataset['subj_counter_global'][i]))]
                    except:
                        continue

                    # get values to evaluate the output
                    guess = int(float(dataset['RemKnoGue_55'][i]))
                    current_adj = dataset['Readout_Recognition_55'][i]
                    in_encode = self.in_list(adjec, current_adj)
                    kk = adjective[current_adj][0]

                    if guess == 1 or guess == 2:

                        if in_encode:
                            adjective.update({current_adj : [kk + 1, adjective[current_adj][1]]})
                        else:
                            adjective.update({current_adj : [adjective[current_adj][0], adjective[current_adj][1]+1]})



        df = pd.read_csv(self.adj_path, sep=';', dtype='unicode')
        df = df.set_index("Adjektiv", drop=False)
        column_names = ['correct_12', "just_12"]
        for p in column_names:
            df[p] = 0

        for i in adjective:
            df = df.set_index("Adjektiv", drop=False)

            df["correct_12"][i] = int(adjective[i][0])
            df["just_12"][i] = int(adjective[i][1])




        df.to_csv(self.adj_path, index=False, sep=';', float_format='%.3f', decimal='.', header=True)

        print(adjective)


    """returns true if the passed string is in the passed list"""
    def in_list(self, list, string):
        for i in list:
            if i == string:
                return True

        return False

    """this method deletes from all adjectives ä,ö,ü and any special characters"""
    def clean_adj(self):
        print("start clean adjective")
        dataset = pd.read_csv(self.main_path_lower, sep=';',dtype='unicode')
        count_rows = dataset.shape[0]

        #all columns to be treated
        columns = ['02_Readout_Oth-Pre-Pas_0', '02_Readout_Pas-Oth-Pre_0', '02_Readout_Pre-Pas-Oth',
                   'Manipul_02_Readout_Oth-Pre-Pas_66', 'Manipul_02_Readout_Pas-Oth-Pre_66',
                   'Manipul_02_Readout_Pre-Pas-Oth_66', 'Manipul_Readout_Oth_Pre_Pas_66',
                   'Manipul_Readout_Pas-Oth-Pre_66', 'Manipul_Readout_Pr_Pa_Oth_final',
                   'Readout_Oth_Pre_Pas_55', 'Readout_Pas-Oth-Pre_0', 'Readout_Pr_Pa_Oth_55', "Readout_Recognition_55"]

        #for all columns go through each line and clean the adjectives
        for i in range(0, count_rows):
            for c in columns:
                if not self.is_nan(dataset[c][i]) and dataset[c][i] != None:
                    dataset._set_value(i, c, self.clean_string(dataset[c][i]))

        dataset.to_csv(self.main_path_lower, index=False, sep=';')

        df = pd.read_csv(self.adj_path, sep=';', dtype='unicode')
        co_rows = df.shape[0]
        for i in range(0, co_rows):
            df._set_value(i, 'Adjektiv', self.clean_string(df['Adjektiv'][i]))

        df.to_csv(self.adj_path, index=False, sep=';')

    """this method gets a string passed to it lists it and returns it in lower case,
     without 'ä' 'ö' and 'ü', this is necessary because adjectives with ä,ö,ü
      were not entered correctly in the table"""
    def clean_string(self, str):
        str_list = list(str.lower())
        str = ""
        for c in str_list:
            if c == "a" or c == "b" or c == "c" or c == "d" or c == "e" or c == "f" or c == "g" \
                    or c == "h" or c == "i" or c == "j" or c == "k" or c == "l" or c == "m" or c == "n" \
                    or c == "o" or c == "p" or c == "q" or c == "r" or c == "s" or c == "t" or c == "u" \
                    or c == "v" or c == "w" or c == "x" or c == "y" or c == "z" or c == "1" or c == "2" \
                    or c == "3" or c == "4" or c == "5" or c == "6" or c == "7" or c == "8" or c == "9" \
                    or c == "0" or c == "ß" or c == "" or c == "b" or c == "b" or c == "b":
                str += c
        return str

    """this method returns a dictonary consisting of the adjectieves and their valence"""
    def adj_as_dic(self):
        dataset = pd.read_csv(self.adj_path, sep=';', dtype='unicode')
        count_rows = dataset.shape[0]
        dic = {}

        for i in range(0, count_rows):
            dic.update({dataset['Adjektiv'][i] : dataset['Valenz'][i]})

        print(str(dic))
        return dic

    ############################################### Unipark data evaluation###################################
    ##########################################################################################################
    ##########################################################################################################

    """this method inserts values such as KW, PW mean value, ... into the Unipark data table a"""
    def insert_psychological_wellbeing(self):
        print("start  insert_psychological_wellbeing")
        dataset = pd.read_csv(self.second_path_lower, sep=';', dtype='unicode')
        count_rows = dataset.shape[0]

        column_names = ['K_Mittelwert', 'PW_Mittelwert', 'SL_Mittelwert', 'A_Mittelwert', 'SA_Mittelwert', 'PB_Mittelwert', 'PWB_Mittelwert']
        for i in column_names:
            dataset[i] = 0.00

        K = {  'v_27': 0,
                'v_32': 1,
                'v_37': 1,
                'v_42': 0,
                'v_45': 1,
                'v_54': 0,
                'v_61': 0,
                'v_74': 1,
                'v_78': 0
                }

        Pw = {  'v_28': 1,
                'v_43': 1,
                'v_46': 0,
                'v_51': 1,
                'v_62': 0,
                'v_66': 1,
                'v_75': 1,
                'v_79': 1
                }

        SL = {  'v_33': 1,
                'v_38': 1,
                'v_47': 1,
                'v_52': 1,
                'v_55': 1,
                'v_58': 0,
                'v_63': 0,
                'v_67': 0,
                'v_71': 1
                }

        A = {  'v_31': 0,
                'v_36': 0,
                'v_41': 1,
                'v_44': 0,
                'v_50': 1,
                'v_60': 0,
                'v_65': 1,
                'v_69': 1,
                'v_77': 0
                }

        SA = {  'v_29': 0,
                'v_34': 0,
                'v_39': 1,
                'v_48': 0,
                'v_53': 0,
                'v_56': 1,
                'v_68': 1,
                'v_70': 0,
                'v_73': 0,
                'v_76': 0
                }

        Pb = {  'v_26': 0,
                'v_30': 1,
                'v_35': 1,
                'v_40': 0,
                'v_49': 1,
                'v_57': 1,
                'v_59': 0,
                'v_64': 1,
                'v_72': 0
                }

        for i in range(0, count_rows):
            self.evaluate_psychological(i, K, 'K_Mittelwert', dataset, True)
            self.evaluate_psychological(i, Pw, 'PW_Mittelwert', dataset, True)
            self.evaluate_psychological(i, SL, 'SL_Mittelwert', dataset, True)
            self.evaluate_psychological(i, A, 'A_Mittelwert', dataset, True)
            self.evaluate_psychological(i, SA, 'SA_Mittelwert', dataset, True)
            self.evaluate_psychological(i, Pb, 'PB_Mittelwert', dataset, True)

            dataset['PWB_Mittelwert'][i] = (self.evaluate_psychological(i, K, 'K_Mittelwert', dataset, False) + self.evaluate_psychological(i, K, 'PW_Mittelwert', dataset, False)\
                                           + self.evaluate_psychological(i, K, 'SL_Mittelwert', dataset, False) + self.evaluate_psychological(i, K, 'A_Mittelwert', dataset, False) \
                                           + self.evaluate_psychological(i, K, 'SA_Mittelwert', dataset, False) + self.evaluate_psychological(i, K, 'PB_Mittelwert', dataset, False)) / 54
            dataset.to_csv(self.second_path_lower, index=False, sep=';', float_format='%.3f', decimal='.', header=True)

    """this method is only for help and evaluates the output depending on whether the data
     needs to be turned over or not"""
    def evaluate_psychological(self, i, colums, name, dataset, teilen):
       if teilen :
           sum = 0
           for j in colums:
               if int(colums.__getitem__(j)) == 0:
                   # has not to be inverted
                   sum += int(dataset[j][i])

               elif int(colums.__getitem__(j)) == 1:
                   # has to be inverted
                   value = int(dataset[j][i])
                   if value == 1:
                       sum += 6
                   elif value == 2:
                       sum += 5
                   elif value == 3:
                       sum += 4
                   elif value == 4:
                       sum += 3
                   elif value == 5:
                       sum += 2
                   elif value == 6:
                       sum += 1

           sum = sum / colums.__len__()
           dataset[name][i] = sum.__round__(2)

           # dataset.insert(i, name, sum)
       else:
           sum = 0
           for j in colums:
               if int(colums.__getitem__(j)) == 0:
                   # has not to be inverted
                   sum += int(dataset[j][i])

               elif int(colums.__getitem__(j)) == 1:
                   # has to be inverted
                   value = int(dataset[j][i])
                   if value == 1:
                       sum += 6
                   elif value == 2:
                       sum += 5
                   elif value == 3:
                       sum += 4
                   elif value == 4:
                       sum += 3
                   elif value == 5:
                       sum += 2
                   elif value == 6:
                       sum += 1

           return sum

    """that method evaluates self_esteem"""
    def self_esteem(self):
        print("start  self_esteem")
        dataset = pd.read_csv(self.second_path_lower, sep=';', dtype='unicode')
        count_rows = dataset.shape[0]
        dataset['self_esteem'] = 0
        se = {  'v_80': 0,
                'v_81': 1,
                'v_82': 0,
                'v_83': 0,
                'v_84': 1,
                'v_85': 1,
                'v_86': 0,
                'v_87': 1,
                'v_88': 1,
                'v_89': 0
                }
        for i in range(count_rows):
            sum = 0
            for j in se:
                if int(se.__getitem__(j)) == 0:
                    # has not to be inverted
                    sum += int(dataset[j][i])

                elif int(se.__getitem__(j)) == 1:
                    # has to be inverted
                    value = int(dataset[j][i])
                    if value == 1:
                        sum += 4
                    elif value == 2:
                        sum += 3
                    elif value == 3:
                        sum += 2
                    elif value == 4:
                        sum += 1

            dataset['self_esteem'][i] = sum.__round__(2)

        dataset.to_csv(self.second_path_lower, index=False, sep=';', float_format='%.3f', decimal='.', header=True)

    """that method evaluates psycologic_wellbeing"""
    def social_psycologic_wellbeing(self):
        pd.set_option('mode.chained_assignment', None)
        pd.set_option('mode.chained_assignment', None)

        print("start  social_psycologic_wellbeing")
        sum = 0
        dataset = pd.read_csv(self.second_path_lower, sep=';', dtype='unicode')
        count_rows = dataset.shape[0]
        dataset['social_psycologic_wellbeing'] = 0
        se = ['v_90', 'v_91', 'v_92', 'v_93', 'v_94', 'v_95', 'v_96', 'v_97']
        for i in range(count_rows):
            sum = 0
            for j in se:
                sum += int(dataset[j][i])

            dataset['social_psycologic_wellbeing'][i] = sum
        dataset.to_csv(self.second_path_lower, index=False, sep=';', float_format='%.3f', decimal='.', header=True)

    """ here all methods are called in sequence"""
    ###################################### main function - Programm start ######################################
def main():

    csv = csv_Handler()

    csv.delete_empty_column()
    csv.make_lowercase()
    csv.merge()
    csv.insert_recognition_evaluation()



    csv.evaluate_past_present_other_test_with_valenz()

    csv.insert_psychological_wellbeing()
    csv.self_esteem()

    csv.social_psycologic_wellbeing()
    csv.insert_subjcounter_in_second_path()


    csv.special_data_requests(0)
    csv.special_data_requests(1)
    csv.special_data_requests(2)
    csv.special_data_requests(3)
    csv.special_data_requests(4)
    csv.special_data_requests(5)


    csv.merge_result()
    csv.reco_eval_full()
    for i in range(0, 12):
         csv.special_data(i)
    csv.clean_adj()
    csv.manipulation_encode()
    csv.manipulation_controll()
    csv.manipulation_reco()




# start of the programs
if __name__ == '__main__':
    main()




