Customer Churn Prediction

This project aims to predict customer churn for GlobalMart using a logistic regression model. The goal is to identify which customers are likely to leave the service, allowing the company to offer incentives and retain them.

Dataset

The dataset used for this project is the Telco Customer Churn dataset from Kaggle, which contains information about customers, including their demographics, service usage, and whether they churned or not.

Project Steps
1. Data Preprocessing

Cleaned the data by handling missing values.

Converted categorical variables into numeric format using One-Hot Encoding.

Scaled numerical features using StandardScaler to improve model performance.

2. Train-Test Split

The data was split into 80% training and 20% testing using the train_test_split method from sklearn.

3. Model Training

A Logistic Regression model was trained to classify customers as either likely to churn or not.

Used max_iter=200 to ensure the model converges properly.

4. Model Evaluation

Evaluated the model's performance using accuracy, precision, recall, and F1 score.

A confusion matrix was generated to visualize the true positives, false positives, true negatives, and false negatives.

5. Performance Results

The model achieved an accuracy of 82.47% with the following evaluation metrics:

Precision: 0.70

Recall: 0.60

F1 Score: 0.64

How to Run the Code

Clone the repository:

git clone https://github.com/yourusername/customer-churn-prediction.git


Install the required libraries:

pip install -r requirements.txt


Run the notebook to train the model:

jupyter notebook churn_prediction.ipynb