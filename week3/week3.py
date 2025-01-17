import numpy as np
import pandas as pd
from matplotlib.ticker import MultipleLocator

from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import Lasso
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
df = pd.read_csv("week3.csv")
print(df.head())
x = np.array(df.iloc[:, 0:2])
x1 = np.array(df.iloc[:, 0]) #to plot the x_axis
x2 = np.array(df.iloc[:, 1])
y = np.array(df.iloc[:, 2])
#plot original data
fig1 = plt.figure(figsize=(17,12))
ax = fig1.add_subplot(111, projection='3d')
ax.scatter(x1, x2, y, label='original data', color='red')
plt.title("original data")
ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('y')
plt.legend(loc='upper right',fontsize=5)
#plt.show()

poly = PolynomialFeatures(degree=5, interaction_only=False,include_bias=False)
x_poly = poly.fit_transform(x)

#(c)
""" Because original data x1,x2 lies in (-1,1), 
so I choose to generate array of range (-1,1), and then use PolynomialFeatures to transform the Xtest."""
Xtest =[]
grid=np.linspace(-1.5,1.5) #Return evenly spaced numbers over a specified interval.
for i in grid:
    for j in grid:
        Xtest.append([i,j])
Xtest=np.array(Xtest)
poly_test = PolynomialFeatures(degree=5, interaction_only=False,include_bias=False)
x_poly_test = poly_test.fit_transform(Xtest)
fig2=plt.figure(figsize=(17,12))
"""Then I define a figure object to plot all the models using add_subplot function. 
The value of z axis is the prediction of lasso when input is the Xtest transformed ."""
#train the range of different alpha for linear lasso regression model
for inx,C in enumerate([0.001,0.01,0.1,1,10,100,1000]):
    alpha=1/C
    linlasso = Lasso(alpha=alpha,max_iter=9999).fit(x_poly, y)
    print('when C is {0},intercept is {1},coef is{2},the score is {3:.4f}\n'.format(C,
                                                                                    linlasso.intercept_, linlasso.coef_,
                                                                                    linlasso.score(x_poly, y)))
    y_pre_test = linlasso.predict(x_poly_test)
    y_pre_test = y_pre_test.reshape(1,-1)
    ax = fig2.add_subplot(2,4,inx+1,projection='3d')
    ax.scatter(Xtest[:,0], Xtest[:,1], y_pre_test, label="lasso regression", color='blue',s=1)
    ax.plot_surface(Xtest[:,0], Xtest[:,1], y_pre_test)
    ax.scatter(x1, x2, y, label="original data", color='red',s=1)
    plt.title("C={0}".format(C))
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('y')
    plt.legend(loc='upper right',fontsize=5)
#plt.show()
#d
fig3=plt.figure(figsize=(17,12))
for inx,C in enumerate([0.001,0.01,0.1,1,10,100,1000]):
    alpha=1/(2*C)
    rige = Ridge(alpha=alpha,max_iter=9999).fit(x_poly, y)
    print('when C is {0},intercept is {1},coef is{2},the score is {3:.4f}\n'.format(C,
                                                                                        rige.intercept_,
                                                                                        rige.coef_,
                                                                                        rige.score(x_poly, y)))
    y_pre_test = rige.predict(x_poly_test)
    y_pre_test = y_pre_test.reshape(1,-1)
    ax = fig3.add_subplot(2,4,inx+1,projection='3d')
    ax.scatter(Xtest[:,0], Xtest[:,1], y_pre_test, label="ridge regression", color='blue',s=1)
    ax.plot_surface(Xtest[:,0], Xtest[:,1], y_pre_test)
    ax.scatter(x1, x2, y, label="original data", color='red',s=1)
    plt.title("C={0}".format(C))
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('y')
    plt.legend(loc='upper right',fontsize=5)


from sklearn.model_selection import KFold
from  sklearn.model_selection import cross_val_score
#First I define 4 arrays in case to store the mean ,
# standard deviation , variance and the number of K perspectively.
mean_kfold_mse = []
standard_deviation_kfold_mse = []
variance_kfold_mse=[]
kfold1=[2,3,4,5,6,7,8,9,10,25,50,100]
mean_score_kfold=[]
linlasso1 = Lasso(alpha=1, max_iter=9999).fit(x_poly, y)
for i in kfold1:
    mean_score_kfold.append(cross_val_score(linlasso1,x_poly,y,cv=i).mean())
kfold=[2,5,10,25,50,100]
#And in each iteration of kfold , and inside the each split , get the list of value of mse, and outside each split
# get the variance, mean, standard deviation of each K-fold’s MSE.

for inx,n_splits in enumerate(kfold):
    kf = KFold(n_splits=n_splits)
    mse = []
    for train, test in kf.split(x_poly):
        linlasso = Lasso(alpha=1, max_iter=9999).fit(x_poly[train], y[train])
        ypred = linlasso.predict(x_poly[test])
        from sklearn.metrics import mean_squared_error
        mse.append(mean_squared_error(ypred, y[test]))
    print('{0} of folds,the mean of the mse:{1}, the var of the mse:{2}'.format(n_splits, np.mean(mse), np.var(mse)))
    variance_kfold_mse.append(np.var(mse))
    mean_kfold_mse.append(np.mean(mse))
    standard_deviation_kfold_mse.append(np.std(mse))
#Then I create a new figure object to draw using plot and errorbar function for each subplot .
fig4=plt.figure(figsize=(17,12))
plt.subplot(131)
plt.plot(kfold, mean_kfold_mse,label='MSE',color='red')
plt.plot(kfold, variance_kfold_mse,label='variance',color='blue')
plt.title('Mean square error and variance')
plt.xlabel('K')
plt.legend(loc='upper right',fontsize=5)
plt.subplot(132)
plt.errorbar(kfold, mean_kfold_mse,label='MSE',color='red',yerr=standard_deviation_kfold_mse)
plt.title('Mean square error')
plt.xlabel('K')
plt.legend(loc='upper right',fontsize=5)
#plot the mean scores of each K
plt.subplot(133)
plt.plot(kfold1,mean_score_kfold,label='mean scores',color='red')
plt.xlabel('K')
plt.title('the scores of different K')
plt.legend(loc='upper right',fontsize=5)

fig5 = plt.figure(figsize=(17,12))
c_range=[0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.2,1.5,1.8,2]
c_mean_mse1 = []
c_std_mse1 = []
c_mean_mse2 = []
c_std_mse2 = []
#when K=5
for inx, C in enumerate(c_range):
    kf = KFold(n_splits=5)
    mse = []
    for train, test in kf.split(x_poly):
        linlasso = Lasso(alpha=1 / C, max_iter=9999).fit(x_poly[train], y[train])
        ypred = linlasso.predict(x_poly[test])
        from sklearn.metrics import mean_squared_error
        mse.append(mean_squared_error(ypred, y[test]))
    c_mean_mse1.append(np.mean(mse))
    c_std_mse1.append(np.std(mse))
#when K=10
for inx, C in enumerate(c_range):
    kf = KFold(n_splits=10)
    mse = []
    for train, test in kf.split(x_poly):
        linlasso = Lasso(alpha=1 / C, max_iter=9999).fit(x_poly[train], y[train])
        ypred = linlasso.predict(x_poly[test])
        from sklearn.metrics import mean_squared_error
        mse.append(mean_squared_error(ypred, y[test]))
    c_mean_mse2.append(np.mean(mse))
    c_std_mse2.append(np.std(mse))
plt.errorbar(c_range, c_mean_mse2, label='K=10', color='blue', yerr=c_std_mse2)
plt.errorbar(c_range, c_mean_mse1, label='K=5', color='red', yerr=c_std_mse1)
plt.ylabel('Mean square error')
plt.xlabel('C')
plt.legend(loc='upper right',fontsize=5)
#(ii)(d)
#ridge model
#when K=5
fig6=plt.figure(figsize=(17,12))
c_range1=[0.001,0.01,0.1,1,10,100,1000]
c_mean_mse3 = []
c_std_mse3 = []
c_mean_mse4 = []
c_std_mse4 = []
for inx, C in enumerate(c_range1):
    kf = KFold(n_splits=5)
    mse = []
    for train, test in kf.split(x_poly):
        ridge = Ridge(alpha=1 / (2*C), max_iter=9999).fit(x_poly[train], y[train])
        ypred = linlasso.predict(x_poly[test])
        from sklearn.metrics import mean_squared_error
        mse.append(mean_squared_error(ypred, y[test]))
    c_mean_mse3.append(np.mean(mse))
    c_std_mse3.append(np.std(mse))
#when K=10
for inx, C in enumerate(c_range1):
    kf = KFold(n_splits=10)
    mse = []
    for train, test in kf.split(x_poly):
        ridge = Ridge(alpha=1 / (2*C), max_iter=9999).fit(x_poly[train], y[train])
        ypred = linlasso.predict(x_poly[test])
        from sklearn.metrics import mean_squared_error
        mse.append(mean_squared_error(ypred, y[test]))
    c_mean_mse4.append(np.mean(mse))
    c_std_mse4.append(np.std(mse))
#draw the MSE with different C and K
plt.errorbar(c_range1, c_mean_mse4, label='K=10', color='blue', yerr=c_std_mse4)
plt.errorbar(c_range1, c_mean_mse3, label='K=5', color='red', yerr=c_std_mse3)
plt.ylabel('Mean square error')
plt.title('ridge regression model')
plt.xlabel('C')
plt.legend(loc='upper right',fontsize=5)
#draw the mean scores of different C using ridge model
fig7=plt.figure(figsize=(17,12))
mean_score_crange=[]
crange_ridge = [0.01,0.1,0.3,0.5,0.7,1,2,4,6,10]
for c in crange_ridge:
    ridge = Ridge(alpha=1/(2*c), max_iter=9999).fit(x_poly, y)
    mean_score_crange.append(cross_val_score(ridge, x_poly, y, cv=5).mean())
plt.plot(crange_ridge,mean_score_crange,label='mean scores',color='red')
plt.xlabel('C')
plt.title('the scores of different C')
plt.legend(loc='upper right',fontsize=5)

plt.show()

