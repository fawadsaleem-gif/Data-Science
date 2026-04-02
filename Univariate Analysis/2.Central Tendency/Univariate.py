class Univariate():
    
    def quanQual(dataset):
        quan=[]
        qual=[]
        for columnName in dataset.columns:
            #print(columnName)
            if(dataset[columnName].dtype=='O'):
            #print("qual")
            qual.append(columnName)
            else:
                #print("quan")
                quan.append(columnName)
        return quan,qual
    
    
    
    

def freqTable(columnName, dataset):
    
    freqTable = pd.DataFrame(columns=["Unique_Values","Frequency","Relative_Frequency","CumSum"])
    # → Create an empty table to store frequency results
    freqTable["Unique_Values"] = dataset[columnName].value_counts().index
    # → Get all unique values in the column
    freqTable["Frequency"] = dataset[columnName].value_counts().values
    # → Count how many times each value appears
    freqTable["Relative_Frequency"] = freqTable["Frequency"] / freqTable["Frequency"].sum()
    # → Convert frequency into percentage/proportion
    freqTable["CumSum"] = freqTable["Relative_Frequency"].cumsum()
    # → Running total of relative frequency

    return freqTable
    # → Return the final frequency table
    
    
    

def Univariate(dataset, Quan):

    descriptive = pd.DataFrame(
        index=["Mean","Median","Mode","Q1:25%","Q2:50%","Q3:75%","99%","Q4:100%",
               "IQR","1.5rule","Lesser","Greater","Min","Max"],
        columns=Quan
    )
    # → Create empty table to store statistical measures

    for columnName in Quan:
    # → Loop through each numeric column
        descriptive[columnName]["Mean"] = dataset[columnName].mean()
        # → Calculate average value
        descriptive[columnName]["Median"] = dataset[columnName].median()
        # → Find middle value
        descriptive[columnName]["Mode"] = dataset[columnName].mode()[0]
        # → Find most frequent value
        descriptive[columnName]["Q1:25%"] = dataset.describe()[columnName]["25%"]
        # → Find 25th percentile (lower quartile)
        descriptive[columnName]["Q2:50%"] = dataset.describe()[columnName]["50%"]
        # → Find 50th percentile (median)
        descriptive[columnName]["Q3:75%"] = dataset.describe()[columnName]["75%"]
        # → Find 75th percentile (upper quartile)
        descriptive[columnName]["99%"] = np.percentile(dataset[columnName],99)
        # → Find 99th percentile value
        descriptive[columnName]["Q4:100%"] = dataset.describe()[columnName]["max"]
        # → Find maximum value
        descriptive[columnName]["IQR"] = descriptive[columnName]["Q3:75%"] - descriptive[columnName]["Q1:25%"]
        # → Calculate spread of middle 50% data
        descriptive[columnName]["1.5rule"] = 1.5 * descriptive[columnName]["IQR"]
        # → Calculate threshold range for outlier detection
        descriptive[columnName]["Lesser"] = descriptive[columnName]["Q1:25%"] - descriptive[columnName]["1.5rule"]
        # → Minimum allowed value (lower outlier boundary)
        descriptive[columnName]["Greater"] = descriptive[columnName]["Q3:75%"] + descriptive[columnName]["1.5rule"]
        # → Maximum allowed value (upper outlier boundary)
        descriptive[columnName]["Min"] = dataset[columnName].min()
        # → Actual smallest value in data
        descriptive[columnName]["Max"] = dataset.describe()[columnName]["max"]
        # → Actual largest value in data
        descriptive[columnName]["kurtosis"]=dataset[columnName].kurtosis()
        # → kurtosis value in data
        descriptive[columnName]["skew"]=dataset[columnName].skew()
        # → skew largest value in data
        descriptive[columnName]["Variance"]=dataset[columnName].var()
        # → Variance
        descriptive[columnName]["StandardD"]=dataset[columnName].std()
        # → Standard Deviation
    return descriptive
    # → Return the full univariate summary table
    
    
    
    
    
def cap_outliers(dataset, descriptive, Quan):

    lesser = []
    greater = []

    # Step 1 → Find which columns have outliers
    for columnName in Quan:
        
        if dataset[columnName].min() < descriptive[columnName]["Lesser"]:
            lesser.append(columnName)

        if dataset[columnName].max() > descriptive[columnName]["Greater"]:
            greater.append(columnName)

    # Step 2 → Cap lower outliers
    for columnName in lesser:
        dataset[dataset[columnName] < descriptive[columnName]["Lesser"],columnName] = descriptive[columnName]["Lesser"]

    # Step 3 → Cap upper outliers
    for columnName in greater:
        dataset[dataset[columnName] > descriptive[columnName]["Greater"],columnName] = descriptive[columnName]["Greater"]

    return dataset