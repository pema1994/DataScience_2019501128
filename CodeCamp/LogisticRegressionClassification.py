#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 15:03:51 2020

@author: arunkp
"""
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.impute import KNNImputer
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.neural_network import MLPClassifier
#from sklearn.metrics import balanced_accuracy_score
#read train and test datasets into pandas DataFrames trainx_df, trainy_df,testx_df
def readDataSets(train_path, test_path,predict_col,index_col=None):
    if index_col==None:
        trainx_df=pd.read_csv(train_path)
        trainy_df=trainx_df[predict_col]
        trainy_df.hist()
        trainx_df.drop(predict_col,axis=1,inplace=True)
        testx_df=pd.read_csv(test_path)
    else:
        trainx_df=pd.read_csv(train_path,index_col='Id')
        trainy_df=trainx_df[predict_col]
        trainx_df.drop(predict_col,axis=1,inplace=True)
        testx_df=pd.read_csv(test_path,index_col='Id')
    return trainx_df,trainy_df,testx_df
# As a first step of pre-processing remove columns with null value ratio greater than provided limit
def dropFeturesWithNullValuesGreaterThanALimit(trainx_df, testx_df,null_ratio=0.3):
    sample_size=len(trainx_df)
    columns_with_null_values=[[col,float(trainx_df[col].isnull().sum())/float(sample_size)] for col in trainx_df.columns if trainx_df[col].isnull().sum()]
    columns_to_drop=[x for (x,y) in columns_with_null_values if y>null_ratio]
    trainx_df.drop(columns_to_drop,axis=1,inplace=True)
    testx_df.drop(columns_to_drop,axis=1,inplace=True)
    return trainx_df,testx_df
# As a second pre-processing step find all categorical columns and one hot  encode them. Before one hot encode fill all null values with dummy in those columns.  Some categorical columns in trainx_df may not have null values in trainx_df but have null values in testx_df. To overcome this problem we will add a row to the trainx_df with all dummy values for categorical values. Once one hot encoding is complete drop the added dummy column
def oneHotEncode(trainx_df,testx_df):
    categorical_columns=[col for col in trainx_df.columns if            trainx_df[col].dtype==object]
    ordinal_columns=[col for col in trainx_df.columns if col not in categorical_columns]
    dummy_row=list()
    for col in trainx_df.columns:
        if col in categorical_columns:
            dummy_row.append("dummy")
        else:
            dummy_row.append("")
    new_row=pd.DataFrame([dummy_row],columns=trainx_df.columns)
    trainx_df=pd.concat([trainx_df,new_row],axis=0, ignore_index=True)
    testx_df=pd.concat([testx_df],axis=0,ignore_index=True)
    for col in categorical_columns:
        trainx_df[col].fillna(value="dummy",inplace=True)
        testx_df[col].fillna(value="dummy",inplace=True)
    enc = OneHotEncoder(drop='first',sparse=False)
    enc.fit(trainx_df[categorical_columns])
    trainx_enc=pd.DataFrame(enc.transform(trainx_df[categorical_columns]))
    testx_enc=pd.DataFrame(enc.transform(testx_df[categorical_columns]))
    trainx_enc.columns=enc.get_feature_names(categorical_columns)
    testx_enc.columns=enc.get_feature_names(categorical_columns)
    trainx_df=pd.concat([trainx_df[ordinal_columns],trainx_enc],axis=1,ignore_index=True)
    testx_df=pd.concat([testx_df[ordinal_columns],testx_enc],axis=1,ignore_index=True)
    trainx_df.drop(trainx_df.tail(1).index,inplace=True)
    return trainx_df,testx_df
# As a third step of pre-processing fill all missing values for ordinal features
def fillMissingValues(trainx_df,testx_df):
    imputer = KNNImputer(n_neighbors=2)
    imputer.fit(trainx_df)
    trainx_df_filled = imputer.transform(trainx_df)
    trainx_df_filled=pd.DataFrame(trainx_df_filled,columns=trainx_df.columns)
    testx_df_filled = imputer.transform(testx_df)
    testx_df_filled=pd.DataFrame(testx_df_filled,columns=testx_df.columns)
    testx_df_filled.reset_index(drop=True,inplace=True)
    return trainx_df_filled,testx_df_filled
# As a fourth step of pre-processing scale all the features either through Standard scores or MinMax scaling
def scaleFetures(trainx_df,testx_df,scale='Standard'):
    if scale == 'Standard':
        scaler = preprocessing.StandardScaler().fit(trainx_df)
        trainx_df=scaler.transform(trainx_df)
        testx_df=scaler.transform(testx_df)
    elif scale == 'MinMax':
        scaler=preprocessing.MinMaxScaler().fit(trainx_df)
        trainx_df=scaler.transform(trainx_df)
        testx_df=scaler.transform(testx_df)
    return trainx_df,testx_df
#As fifth step of preprocessing apply PCA
def findPrincipalComponents(trainx_df, testx_df):
    pca = PCA().fit(trainx_df)
    itemindex = np.where(np.cumsum(pca.explained_variance_ratio_)>0.9999)
    print('np.cumsum(pca.explained_variance_ratio_)',      np.cumsum(pca.explained_variance_ratio_))
    #Plotting the Cumulative Summation of the Explained Variance
    plt.figure(np.cumsum(pca.explained_variance_ratio_)[0])
    plt.plot(np.cumsum(pca.explained_variance_ratio_))
    plt.xlabel('Number of Components')
    plt.ylabel('Variance (%)') #for each component
    plt.title('Principal Components Explained Variance')
    plt.show()
    pca_std = PCA(n_components=itemindex[0][0]).fit(trainx_df)
    trainx_df = pca_std.transform(trainx_df)
    testx_df = pca_std.transform(testx_df)
    return trainx_df,testx_df


# Change labels into 0 and 1
def encodeLabelsToZeroAndOne(trainy_df):
    le = preprocessing.LabelEncoder()
    trainy_df=le.fit_transform(trainy_df)
    return trainy_df


# As a fifth step of pre-processing split the trainx_df into two parts to build a model and test how is it working to pick best model
def splitTrainAndTest(trainx_df, trainy_df,split_ratio=0.3):
    X_train, X_test, y_train, y_test = train_test_split(trainx_df, trainy_df, test_size=split_ratio, random_state=42)
    return X_train, X_test, y_train, y_test

# Fit Logistic Regression 
def getLogisticRegressionModel(X_train, y_train,reg_par=0.00001, max_iterations=1000000):
    logreg=LogisticRegression(class_weight="balanced",C=reg_par,max_iter=max_iterations)
    logreg.fit(X_train, y_train)
    return logreg

#Fit SVM Classification Model
def getSVClassificationModel(X_train, y_train,reg_par=1.0,deg=3,ker='rbf'):
    svcmodel=SVC(C=reg_par,degree=deg,kernel=ker)
    svcmodel.fit(X_train, y_train)
    return svcmodel

#get BackPropagation Model
def getBackPropagationModel(X_train, y_train,sol='lbfgs', reg_par=1e-5, hid_layer_sizes=(5, ), random_state=1,maxi_iter=1000):
    nn_bp_model = MLPClassifier(solver=sol, alpha=reg_par, hidden_layer_sizes=hid_layer_sizes, random_state=1,max_iter=maxi_iter)
    nn_bp_model.fit(X_train, y_train)
    return nn_bp_model

#get results from model
def getScores(model,X_train, X_test, y_train, y_test):
    '''THRESHOLD = 0.5
    yhat = np.where(model.predict_proba(X_test)[:,1] > THRESHOLD, 1, 0)'''
    yprobs= model.predict_log_proba(X_test)
    yprobs=yprobs[:,1]
    ras=roc_auc_score(y_test,yprobs,average = 'weighted')
    print(ras)
    yhat = model.predict(X_test)
    
    #pd.DataFrame(yhat).to_csv(model)
    TP, TN, FP, FN =0,0,0,0
    for i in range(len(yhat)):
        if yhat[i]==0:
            if y_test[i]==0:
                TN+=1
            else:
                FN+=1
        else:
            if y_test[i]==1:
                TP+=1
            else:
                FP+=1
    print(classification_report(y_test,yhat))
    print(classification_report(y_test,yhat,output_dict=True)['1']['precision'], classification_report(y_test,yhat,output_dict=True)['1']['recall'])
    fpr, tpr, threshold = roc_curve(y_test, yprobs)
    roc_auc = auc(fpr, tpr)
    
    plt.title('Receiver Operating Characteristic')
    plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
    plt.legend(loc = 'lower right')
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()
    return([TP, TN,FP,FN,TP/(TP+FN), TN/(TN+FP)])
# get Scores for SVC
def getScoresForSVC(model,X_train, X_test, y_train, y_test):
    yhat = model.predict(X_test)
    
    #pd.DataFrame(yhat).to_csv(model)
    TP, TN, FP, FN =0,0,0,0
    for i in range(len(yhat)):
        if yhat[i]==0:
            if y_test[i]==0:
                TN+=1
            else:
                FN+=1
        else:
            if y_test[i]==1:
                TP+=1
            else:
                FP+=1
    print(classification_report(y_test,yhat))
    print(classification_report(y_test,yhat,output_dict=True)['1']['precision'], classification_report(y_test,yhat,output_dict=True)['1']['recall'])
    return([TP, TN,FP,FN,TP/(TP+FN), TN/(TN+FP)])
# Tune regularization Parameter based on f1 value or mse

def predictTestx(Model, testx_df):
    testpred=pd.DataFrame(Model.predict(testx_df))
    testpred.to_csv("test_pred.csv")

trainx_df,trainy_df,testx_df=readDataSets("/Users/pemawangmo/Desktop/DS_Notes/log_reg/marketing_training.csv","/Users/pemawangmo/Desktop/DS_Notes/log_reg/marketing_test.csv", predict_col='responded')
trainx_df,testx_df=dropFeturesWithNullValuesGreaterThanALimit(trainx_df, testx_df,null_ratio=0.5)
trainx_df,testx_df=oneHotEncode(trainx_df,testx_df)
trainx_df,testx_df=fillMissingValues(trainx_df,testx_df)
trainx_df,testx_df=scaleFetures(trainx_df,testx_df,scale='Standard')
trainy_df=encodeLabelsToZeroAndOne(trainy_df)
trainx_df,testx_df=findPrincipalComponents(trainx_df, testx_df)
X_train, X_test, y_train, y_test=splitTrainAndTest(trainx_df, trainy_df,split_ratio=0.3)
print("Results for Logistic Regression")
LogRegModel=getLogisticRegressionModel(X_train, y_train)
getScores(LogRegModel,X_train, X_test, y_train, y_test)
print("Results for SVM Classifier")
svcmodel=getSVClassificationModel(X_train, y_train,reg_par=0.5,deg=2,ker='poly')
getScoresForSVC(svcmodel,X_train, X_test, y_train, y_test)
print("Results for Back Propagation Classifier")
nn_bp_model=getBackPropagationModel(X_train, y_train,sol='lbfgs', reg_par=0.01, hid_layer_sizes=(7, ), random_state=1,maxi_iter=10000)
getScores(nn_bp_model,X_train, X_test, y_train, y_test)
'''LRModel=getLinearRegressionModel(X_train, y_train)
RidgeModel=getRidgeRegressionModel(X_train, y_train,tolerence=0.0001,reg_par=0.5)
getRSqureandMSEVsAlphaPlots(X_train, X_test, y_train, y_test,alpha_start=130,alpha_end=146,jumps=10)'''




