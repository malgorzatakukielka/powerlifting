# %% imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%% data loading
powerlifting = pd.read_csv('openpowerlifting.csv', low_memory=False)
# %%
powerlifting = powerlifting[(powerlifting['Equipment'] == 'Raw') & 
                            (powerlifting['TotalKg'] > 0) & 
                            (powerlifting['Event'] == 'SBD') &
                            (powerlifting['Country'] == 'Poland')]
print(powerlifting)
# %% weightclasses female
#IPF
def assign_ipf_class(weight, sex):
    if sex == 'F':
        if weight <= 43:
            return '43kg'
        elif weight <= 47:
            return '47kg'
        elif weight <= 52:
            return '52kg'
        elif weight <= 57:
            return '57kg'
        elif weight <= 63:
            return '63kg'
        elif weight <= 69:
            return '69kg'
        elif weight <= 76:
            return '76kg'
        elif weight <= 84:
            return '84kg'
        else:
            return '84+kg'

    elif sex == 'M':
        if weight <= 53:
            return '53kg'
        elif weight <= 59:
            return '59kg'
        elif weight <= 66:
            return '66kg'
        elif weight <= 74:
            return '74kg'
        elif weight <= 83:
            return '83kg'
        elif weight <= 93:
            return '93kg'
        elif weight <= 105:
            return '105kg'
        elif weight <= 120:
            return '120kg'
        else:
            return '120+kg'

    else:
        return None

#Traditional
def assign_traditional_class(weight, sex):
    if sex == 'F':
        if weight <= 44:
            return '44kg'
        elif weight <= 48:
            return '48kg'
        elif weight <= 52:
            return '52kg'
        elif weight <= 56:
            return '56kg'
        elif weight <= 60:
            return '60kg'
        elif weight <= 67.5:
            return '67.5kg'
        elif weight <= 75:
            return '75kg'
        elif weight <= 82.5:
            return '82.5kg'
        elif weight <= 90:
            return '90kg'
        else:
            return '90+kg'
    if sex == 'M':
        if weight <= 52:
            return '52kg'
        elif weight <= 56:
            return '56kg'
        elif weight <= 60:
            return '60kg'
        elif weight <= 67.5:
            return '67.5kg'
        elif weight <= 75:
            return '75kg'
        elif weight <= 82.5:
            return '82.5kg'
        elif weight <= 90:
            return '90kg'
        elif weight <= 100:
            return '100kg'
        elif weight <= 110:
            return '110kg'
        elif weight <= 125:
            return '125kg'
        elif weight <= 140:
            return '140kg'
        else:
            return '140+kg'
    else:
        return None
# %%
powerlifting['IPF_WeightClass'] = powerlifting.apply(
    lambda row: assign_ipf_class(row['BodyweightKg'], row['Sex']), axis=1)

powerlifting['Traditional_WeightClass'] = powerlifting.apply(
    lambda row: assign_traditional_class(row['BodyweightKg'], row['Sex']), axis=1)

print(powerlifting[['Sex', 'BodyweightKg', 'IPF_WeightClass', 'Traditional_WeightClass']])

#%% drop unused columns
powerlifting = powerlifting.drop(columns = ['MeetState','State', 'Squat4Kg', 'Bench4Kg', 'Deadlift4Kg'])
#%% check for missing values
print(powerlifting.isna().sum().sort_values(ascending=False))
print(powerlifting.columns)


# %%
# Pivot the weight classes columns to long format
long_data = powerlifting.melt(
    id_vars=['Name', 'Sex', 'Event', 'Equipment', 'Age', 'AgeClass',
       'BirthYearClass', 'Division', 'BodyweightKg', 'WeightClassKg',
       'Squat1Kg', 'Squat2Kg', 'Squat3Kg', 'Best3SquatKg', 'Bench1Kg',
       'Bench2Kg', 'Bench3Kg', 'Best3BenchKg', 'Deadlift1Kg', 'Deadlift2Kg',
       'Deadlift3Kg', 'Best3DeadliftKg', 'TotalKg', 'Place', 'Dots', 'Wilks',
       'Glossbrenner', 'Goodlift', 'Tested', 'Country', 'Federation',
       'ParentFederation', 'Date', 'MeetCountry', 'MeetTown', 'MeetName',
       'Sanctioned'],
    value_vars=['IPF_WeightClass', 'Traditional_WeightClass'],
    var_name='WeightClassType',
    value_name='WeightClass'
)

# %%
powerlifting.to_csv('powerlifting_cleaned.csv', index=False)