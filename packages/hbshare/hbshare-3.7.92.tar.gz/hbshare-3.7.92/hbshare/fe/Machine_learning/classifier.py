import pandas as pd
import numpy as np
#ploting
import matplotlib.pyplot as plt

# Modeling
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler



# Metrics validation
from sklearn.metrics import confusion_matrix, \
    precision_score, recall_score, f1_score, \
    confusion_matrix, precision_recall_curve, \
    accuracy_score

def set_metrics_method(y_pred,y_test):

    if(len(set(y_test))>2):
        method='weighted'
    else:
        method='binary'
    return method

def metrics(actuals, predictions,method):
    print("Accuracy: {:.5f}".format(accuracy_score(actuals.tolist(), predictions.tolist())))
    print("Precision: {:.5f}".format(precision_score(actuals.tolist(), predictions.tolist(),average=method)))
    print("Recall: {:.5f}".format(recall_score(actuals.tolist(), predictions.tolist(),average=method)))
    print("F1-score: {:.5f}".format(f1_score(actuals.tolist(), predictions.tolist(),average=method)))
    return f1_score(actuals.tolist(), predictions.tolist(),average=method)

def train_model (model, x_train, y_train):

    model.fit(x_train, y_train)

    return model

def evluation(model,x_test,y_test):

    y_pred = model.predict(x_test)

    if (type(y_pred[0]) == np.float32 or type(y_pred[0]) == np.float64):
        y_pred = y_pred.round().astype(int)

    test = y_test.to_frame('real')
    test['pre'] = y_pred
    if(len(test[test['pre']==0])>0):
        print(len(test[(test['pre']==0)&(test['real']==0)])/len(test[test['pre']==0]))
    else:
        print('find no target')

    # method = set_metrics_method(y_pred,y_test)
    # f1_score = metrics(y_test, y_pred, method)
    f1_score=1

    #cnf_matrix = confusion_matrix(y_test, y_pred)

    # sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu", fmt='g')
    # plt.ylabel('Actual Label')
    # plt.xlabel('Predicted Label')

    return f1_score

def load_local_data(dir):

    df = pd.read_csv(dir)
    return  df

def standardlize(df,col_list):
    # rs_list=[]
    rs = RobustScaler()
    for col in col_list:
        # tempfit=rs.fit((df[col].values.reshape(-1,1)))
        # df[col] = tempfit.transform((df[col].values.reshape(-1, 1)))
        df[col]=rs.fit_transform ((df[col].values.reshape(-1,1)))
        # rs_list.append(tempfit)
        #dict(zip(col_list,rs_list))
    return df

def split_train_test(x,y,test_ratio):
    (x_train, x_test, y_train, y_test) = train_test_split(x, y, test_size= test_ratio, random_state= 42)
    # print("Shape of train_X: ", x_train.shape)
    # print("Shape of test_X: ", x_test.shape)
    return x_train, x_test, y_train, y_test

def model_built_up(df,lable_col,model_name,standardlize_col,test_ratio):

    df=standardlize(df,standardlize_col)

    x = df.drop([lable_col], axis= 1)
    y = df[lable_col]

    if(test_ratio>0):
        # x_train, x_test, y_train, y_test=split_train_test(x,y,test_ratio)

        x_train=x.iloc[0:test_ratio]
        y_train=y.iloc[0:test_ratio]
        x_test=x.iloc[test_ratio:]
        y_test=y.iloc[test_ratio:]
    else:

        x_train=x
        y_train=y



    if(model_name.lower()=='xgboost'):

        # map_list=y_train.unique()
        #         # map_list.sort()
        #         # for i in range(len(map_list)):
        #         #     y_train[y_train==map_list[i]]=i
        #         #     if(test_ratio>0):
        #         #         y_test[y_test == map_list[i]] = i
        from xgboost import XGBRegressor
        # if(len(map_list)>2):
        #     trained_model=train_model(XGBRegressor(objective='multi:softmax',num_class=len(map_list)), x_train, y_train)
        # else:
        # for i in range(1,50,1):
        #     print('max_depth is {}'.format(i))
        #     #min_child_weight = i / 10
        #     trained_model = train_model(XGBRegressor(max_depth =3,min_child_weight=i)
        #                                 , x_train, y_train)
        #     f1_score = evluation(trained_model, x_train, y_train)
        #     f1_score = evluation(trained_model, x_test, y_test)

        trained_model = train_model(XGBRegressor(max_depth=3, min_child_weight=39)
                                    , x_train, y_train)

    elif(model_name.lower()=='randomforest'):
        from sklearn.ensemble import RandomForestClassifier
        for i in range(1,20,1):

            #print('n_estimators is {}'.format(i))
            print('max_depth is {}'.format(i))
            trained_model=train_model(RandomForestClassifier(n_estimators=31+1,max_depth=i), x_train, y_train)
            f1_score = evluation(trained_model, x_train, y_train)
            f1_score = evluation(trained_model, x_test, y_test)



    elif(model_name.lower()=='svm'):
        from sklearn.svm import SVC
        trained_model = train_model(SVC(), x_train, y_train)
    elif(model_name.lower()=='kmeans'):
        from sklearn.cluster import KMeans
        n_clusters=len(set(y))
        trained_model=train_model(KMeans(n_clusters=n_clusters), x_train, x_test, y_test)
        f1_score=0
    else:
        raise Exception
        print('the input model name is not acceptable,')

    if(test_ratio>0 and model_name.lower()!='kmeans'):
        print('Evaluation of {0}'.format(model_name))
        f1_score=evluation(trained_model,x_test,y_test)
    else:
        f1_score=0

    return trained_model,f1_score

if __name__ == '__main__':

    df=load_local_data('creditcard.csv')
    model, f1_score=model_built_up(df,'Class','randomforest',['Amount','Time'],0.2)