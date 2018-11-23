from sklearn.linear_model import LogisticRegression
import pandas as pd

def linear(X_train, y_train, X_test, y_test):
    """
    define a simple linear model, train it and return model stats
    """
    clf=LogisticRegression().fit(X_train,y_train)
    
    train_score=clf.score(X_train, y_train)
    test_score =clf.score(X_test, y_test)
    return(train_score, test_score)