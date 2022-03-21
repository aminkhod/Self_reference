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