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