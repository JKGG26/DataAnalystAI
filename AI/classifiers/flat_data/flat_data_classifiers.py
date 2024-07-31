import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC


class FlatDataClassifier:

    def __init__(self) -> None:
        self.__X_train = None
        self.__X_test = None
        self.__y_train = None
        self.__y_test = None

    def get_train_data(self, df):
        X = df.drop('Y', axis=1)
        y = df['Y']
        # Split data into training and testing sets
        self.__X_train, self.__X_test, self.__y_train, self.__y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    def normalize_data(self):
        scaler = StandardScaler()
        self.__X_train = scaler.fit_transform(self.__X_train)
        self.__X_test = scaler.transform(self.__X_test)

    
class RandomForestClassifier(FlatDataClassifier):
    def __init__(self) -> None:
        self.__rf_model = RandomForestClassifier(random_state=42)
        super().__init__()

    def train(self):
        # Train the Random Forest model
        self.__rf_model.fit(self.__X_train, self.__y_train)

    def prediction(self):
        # Predict and evaluate
        rf_predictions = self.__rf_model.predict(self.__X_test)
        print("Random Forest Classifier")
        print(f"Accuracy: {accuracy_score(self.__y_test, rf_predictions)}")
        print(classification_report(self.__y_test, rf_predictions))

    
class SVMClassifier(FlatDataClassifier):
    def __init__(self) -> None:
        self.__svm_model = SVC(random_state=42)
        super().__init__()

    def train(self):
        # Train the SVM model
        self.__svm_model.fit(self.__X_train, self.__y_train)

    def prediction(self):
        # Predict and evaluate
        svm_predictions = self.__svm_model.predict(self.__X_test)
        print("Support Vector Classifier")
        print(f"Accuracy: {accuracy_score(self.__y_test, svm_predictions)}")
        print(classification_report(self.__y_test, svm_predictions))
    