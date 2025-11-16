import pandas as pd
import numpy as np
class Univariate():
    def qualQuan(dataset):
        qual=[]
        quan=[]
        for columnName in dataset.columns:
            if dataset[columnName].dtypes=='object':
                qual.append(columnName)
            else:
                quan.append(columnName)
        return qual,quan

    def dataFrameTable(dataset,quan):
        descriptive = pd.DataFrame(index=['Mean','Median','Mode','Min','Q1-25%','Q2-50%','Q3-75%','99th','Q4-100%','IQR','1.5rule','Lesser','min','max','Greater'],columns=quan) #it creates table with given index value in row and column value
        for columnName in quan:
            descriptive.loc['Mean',columnName]=dataset[columnName].mean() # Assign mean value to 'Mean' row for the current column
            descriptive.loc['Median',columnName]=dataset[columnName].median()
            descriptive.loc['Mode',columnName]=dataset[columnName].mode()[0]
            # NOTE: This percentile method: (np.percentile(dataset[columnName],0)) returns NaN for the 'salary' field because it contains missing (NaN) values.
            # We will skip percentile calculation unless missing values are handled.
            descriptive.loc['Min',columnName]=dataset.describe()[columnName]['min']
            descriptive.loc['Q1-25%',columnName]=dataset.describe()[columnName]['25%']
            descriptive.loc['Q2-50%',columnName]=dataset.describe()[columnName]['50%']
            descriptive.loc['Q3-75%',columnName]=dataset.describe()[columnName]['75%']
            descriptive.loc['99th',columnName]=(np.percentile(dataset[columnName],99))
            descriptive.loc['Q4-100%',columnName]=dataset.describe()[columnName]['max']
            descriptive.loc['IQR',columnName]=descriptive.loc['Q3-75%',columnName]-descriptive.loc['Q1-25%',columnName]
            descriptive.loc['1.5rule',columnName]=1.5*descriptive.loc['IQR',columnName]
            descriptive.loc['Lesser',columnName]=descriptive.loc['Q1-25%',columnName]-descriptive.loc['1.5rule',columnName]
            descriptive.loc['min',columnName]=dataset.describe()[columnName]['min']
            descriptive.loc['max',columnName]=dataset.describe()[columnName]['max']
            descriptive.loc['Greater',columnName]=descriptive.loc['Q3-75%',columnName]+descriptive.loc['1.5rule',columnName]
        return descriptive

    def findOutliers(descriptive,quan):
        # Identifying columns where outliers exist:
        # - 'lesser' stores columns with values below the lower bound
        # - 'greater' stores columns with values above the upper bound

        lesser = []
        greater = []

        for columnName in quan:
            if descriptive.loc['Lesser',columnName]>descriptive.loc['min',columnName]:
                lesser.append(columnName)
            if descriptive.loc['Greater',columnName]<descriptive.loc['max',columnName]:
                greater.append(columnName)
        return lesser,greater

    def replaceOutliers(dataset,descriptive,lesser,greater):
        #REPLACING THE OUTLIER VALUES
        for columnName in lesser:
            dataset.loc[dataset[columnName]<descriptive.loc['Lesser',columnName],columnName]=descriptive.loc['Lesser',columnName]
        for columnName in greater:
            dataset.loc[dataset[columnName]>descriptive.loc['Greater',columnName],columnName]=descriptive.loc['Greater',columnName]
        return dataset

    def freqTable(columnName,dataset):
        freqTable = pd.DataFrame(columns=["Unique_Values","Frequency","Relative_Frequency","Cumsum"])
        freqTable['Unique_Values']=dataset[columnName].value_counts().index #value_counts means count the frequency of each unique value. index gives unique value
        freqTable['Frequency']=dataset[columnName].value_counts().values #.values means frequency of each unique value
        freqTable['Relative_Frequency']=(freqTable['Frequency']/freqTable['Unique_Values'].size) # Calculate relative frequency as proportion of each frequency to the total count
        freqTable["Cumsum"]=freqTable['Relative_Frequency'].cumsum() #count the current+previous value using inbulit function called cumsum
        return freqTable
            