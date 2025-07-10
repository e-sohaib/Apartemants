from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import pandas
import matplotlib.pyplot as plt
def regr(df : pandas.DataFrame):
    X = df.drop(['price_total' ,'location_lat', 'location_lon',],axis=1)
    #X = df[['meterage', 'room_count' , 'age' , 'floor_number' , 'total_floors' , 'has_elevator']]
    #X = df[['meterage', 'room_count' , 'age']]
    y = df['price_total']
    print(X.columns)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    return r2,model.coef_ ,model.intercept_
def ploter(df:pandas.DataFrame):
    x = df['meterage']
    y = df['price_total']
    plt.scatter(x,y,color='blue')
    plt.show()