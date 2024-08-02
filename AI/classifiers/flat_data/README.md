# FlatDataClassifier README

## Overview

This project provides a set of classes for training and evaluating classification models on tabular data. It includes a base class `FlatDataClassifier` with common functionality and two subclasses: `RFClassifier` for Random Forest classification and `SVMClassifier` for Support Vector Classification.

## Classes

### `FlatDataClassifier`

A base class for classification models. It handles data splitting, normalization, training, prediction, and performance evaluation.

#### Methods

- **`__init__()`**: Initializes the class with placeholder attributes for training/testing data, the model, predictions, and accuracy.

- **`set_train_data(df: pd.DataFrame)`**: Prepares the training and testing data from a DataFrame. Expects the target variable to be in a column named 'Y'.

- **`normalize_data(X_df: pd.DataFrame) -> pd.DataFrame`**: Normalizes the feature data using `StandardScaler`.

- **`train() -> pd.DataFrame`**: Trains the model on the normalized training data and sets predictions. Returns a DataFrame with prediction statistics.

- **`prediction(X_df: pd.DataFrame)`**: Predicts the labels for the given data and stores them.

- **`prediction_stats(y_labels: pd.Series) -> pd.DataFrame`**: Computes and prints the accuracy and detailed classification report of predictions. Returns a DataFrame with the prediction statistics.

- **`save_model(output_path: str = 'data/model.pkl')`**: Saves the trained model to the specified path using `pickle`.

- **`load_model(input_path: str = 'data/model.pkl')`**: Loads a model from the specified path using `pickle`.

### `RFClassifier`

A subclass of `FlatDataClassifier` that uses a Random Forest Classifier.

#### Methods

- **`__init__(file_path: str = None)`**: Initializes the Random Forest Classifier. If a file path is provided, it loads the model from the file.

### `SVMClassifier`

A subclass of `FlatDataClassifier` that uses a Support Vector Classifier.

#### Methods

- **`__init__(file_path: str = None)`**: Initializes the Support Vector Classifier. If a file path is provided, it loads the model from the file.

## Usage

### Installation

Ensure you have the required packages installed:

```sh
pip install pandas scikit-learn
```

### Example

Here's an example of how to use these classes:

```python
from your_module import RFClassifier, SVMClassifier  # Replace 'your_module' with the actual module name

# Example with Random Forest Classifier
rf_classifier = RFClassifier()
df = pd.read_csv('path/to/your/data.csv')  # Load your data
rf_classifier.set_train_data(df)
rf_classifier.train()
report = rf_classifier.prediction_stats(df['Y'])
rf_classifier.save_model('path/to/save/model.pkl')

# Example with Support Vector Classifier
svm_classifier = SVMClassifier()
df = pd.read_csv('path/to/your/data.csv')  # Load your data
svm_classifier.set_train_data(df)
svm_classifier.train()
report = svm_classifier.prediction_stats(df['Y'])
svm_classifier.save_model('path/to/save/model.pkl')
```

### Notes

- Ensure the target variable is named 'Y' in the DataFrame.
- Adjust file paths and model file names as needed.
- The `train()` method normalizes the data and trains the model, which requires data to be provided via `set_train_data()`.