from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import joblib

import joblib
import os

class TextClassifier:
    def __init__(self):
        models_dir = os.path.dirname(os.path.abspath(__file__))
        self.models = {}
        for filename in os.listdir(models_dir):
            if filename.endswith('.joblib'):
                model_name = os.path.splitext(filename)[0]
                model_path = os.path.join(models_dir, filename)
                self.models[model_name] = joblib.load(model_path)

    def pred_logreg(self, text):
        return self.models['logreg'].predict([text])[0]

    def pred_tree(self, text):
        return self.models['ds_tree'].predict([text])[0]

    def pred_forest(self, text):
        return self.models['rd_forest'].predict([text])[0]
