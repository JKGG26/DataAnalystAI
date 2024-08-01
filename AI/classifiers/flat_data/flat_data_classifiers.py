import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import pickle


class FlatDataClassifier:

    def __init__(self) -> None:
        self._X_train = None
        self._X_test = None
        self._y_train = None
        self._y_test = None

        self._model = None
        self.data_predictions = None
        self.accuracy = 0

    def set_train_data(self, df):
        X = df.drop('Y', axis=1)
        y = df['Y']
        # Split data into training and testing sets
        self._X_train, self._X_test, self._y_train, self._y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    def normalize_data(self, X_df):
        scaler = StandardScaler()
        return scaler.fit_transform(X_df)

    def train(self):
        # Normalize data
        self._X_train = self.normalize_data(self._X_train)
        self._X_test = self.normalize_data(self._X_test)
        # Train the SVM model
        self._model.fit(self._X_train, self._y_train)
        # Set predictions
        self.prediction(self._X_test)
        # Get prediction stats
        return self.prediction_stats(self._y_test)

    def prediction(self, X_df):
        # Predict and evaluate
        self.data_predictions = self._model.predict(X_df)

    def prediction_stats(self, y_labels):
        self.accuracy = int(accuracy_score(y_labels, self.data_predictions) * 1000000) / 1000000
        print(f"Accuracy: {self.accuracy} = {self.accuracy * 100} %")
        predict_report = classification_report(y_labels, self.data_predictions, output_dict=True)
        del predict_report['accuracy']
        prediction_report = []
        for y, stats in predict_report.items():
            stats['accuracy'] = self.accuracy
            stats['class'] = y
            prediction_report.append(stats)

        report = pd.DataFrame(prediction_report)
        report_cols = ['class'] + list(report.keys())[:-1]
        report = report[report_cols]
        return report

    def save_model(self, output_path: str = 'data/model.pkl'):
        with open(output_path, 'wb') as file:
            pickle.dump(self._model, file)

        print(f"\nModel saved in '{output_path}'")

    def load_model(self, input_path: str = 'data/model.pkl'):
        # Load the model from the file
        with open(input_path, 'rb') as file:
            self._model = pickle.load(file)

    
class RFClassifier(FlatDataClassifier):
    def __init__(self) -> None:
        super().__init__()
        self._model = RandomForestClassifier(random_state=42)
        print("\nRANDOM FOREST CLASSIFIER:\n")

    
class SVMClassifier(FlatDataClassifier):
    def __init__(self) -> None:
        super().__init__()
        self._model = SVC(random_state=42)
        print("\nSUPPORT VECTOR CLASSIFIER:\n")
    