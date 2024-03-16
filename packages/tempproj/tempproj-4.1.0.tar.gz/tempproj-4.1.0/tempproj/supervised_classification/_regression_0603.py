import pandas as pd
import numpy as np
import execdata as exe
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression


def Banglore_Home_Price_Prediction_0603(para_list):
    '''
        Linear Regression Model
        For Section6.Project03-Banglore_Home_Price_Prediction
        Github_Project:'https://github.com/bdfd/Section6.Project03-Real-Estate-Price-Prediction'
    '''
    dataset_url = 'https://raw.githubusercontent.com/bdfd/Section6.Project03-Real-Estate-Price-Prediction/main/1.0%20dataset/S603_Mugged_Data.csv'
    df = pd.read_csv(dataset_url, encoding='utf-8')
    target_feature = 'Price'
    location_dummies = pd.get_dummies(df.Location)
    df2 = pd.concat([df.drop(['Location', 'Price/Sqft'], axis='columns'),
                    location_dummies.drop('Others', axis='columns')],
                    axis='columns')
    X_train, X_test, y_train, y_test = exe.eda.sep_split(df2, target_feature)
    lr_clf = LinearRegression()

    model = make_pipeline(lr_clf)
    model.fit(X_train, y_train)

    input_sample = np.zeros(len(X_train.columns))
    loc_index = np.where(X_train.columns == para_list[3])[0][0]
    input_sample[0] = para_list[0]
    input_sample[1] = para_list[1]
    input_sample[2] = para_list[2]
    if loc_index >= 0:
        input_sample[loc_index] = 1
    # print(input_sample.shape)
    input_sample.reshape(1, 257)

    df_sample_columns = X_train.columns.tolist()
    # len(df_sample_columns)
    test_sample = pd.DataFrame(columns=df_sample_columns,
                               data=np.array(input_sample).reshape(1, len(df_sample_columns)))
    predict_price = model.predict(test_sample)[0]
    result = round(float(predict_price/100000), 2)
    return result
