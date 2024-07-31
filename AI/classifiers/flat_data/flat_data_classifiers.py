import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC


class FlatDataClassifier:

    def __init__(self) -> None:
        self._X_train = None
        self._X_test = None
        self._y_train = None
        self._y_test = None

    def get_train_data(self, df):
        X = df.drop('Y', axis=1)
        y = df['Y']
        # Split data into training and testing sets
        self._X_train, self._X_test, self._y_train, self._y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    def normalize_data(self):
        scaler = StandardScaler()
        self._X_train = scaler.fit_transform(self._X_train)
        self._X_test = scaler.transform(self._X_test)

    
class RFClassifier(FlatDataClassifier):
    def __init__(self) -> None:
        super().__init__()
        self.__rf_model = RandomForestClassifier(random_state=42)

    def train(self):
        # Train the Random Forest model
        self.__rf_model.fit(self._X_train, self._y_train)

    def prediction(self):
        # Predict and evaluate
        rf_predictions = self.__rf_model.predict(self._X_test)
        print("Random Forest Classifier")
        print(f"Accuracy: {accuracy_score(self._y_test, rf_predictions)}")
        print(classification_report(self._y_test, rf_predictions))

    
class SVMClassifier(FlatDataClassifier):
    def __init__(self) -> None:
        super().__init__()
        self.__svm_model = SVC(random_state=42)

    def train(self):
        # Train the SVM model
        self.__svm_model.fit(self._X_train, self._y_train)

    def prediction(self):
        # Predict and evaluate
        svm_predictions = self.__svm_model.predict(self._X_test)
        print("Support Vector Classifier")
        print(f"Accuracy: {accuracy_score(self._y_test, svm_predictions)}")
        print(classification_report(self._y_test, svm_predictions))
    