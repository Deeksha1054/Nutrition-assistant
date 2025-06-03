from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler
import re
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define the model architecture
class NutritionModel(nn.Module):
    def __init__(self, input_size, hidden_size=64):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
        self.fc3 = nn.Linear(hidden_size // 2, 1)
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Load dataset and models
def load_resources():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_dir, 'Data', 'food.csv')
        logger.info(f"Loading dataset from: {data_path}")
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Dataset not found at {data_path}")
        
        df = pd.read_csv(data_path)
        required_columns = ['Category', 'Data.Kilocalories', 'Data.Protein', 'Data.Fatt', 'Data.Carbohydrate']
        logger.info(f"Available columns in dataset: {list(df.columns)}")
        for col in required_columns:
            if col not in df.columns:
                raise KeyError(f"Column '{col}' not found in dataset")
        
        df = df[required_columns].dropna()
        for col in required_columns[1:]:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        logger.info(f"Dataset shape: {df.shape}")
        
        input_size = 3
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Using device: {device}")
        classification_model = NutritionModel(input_size).to(device)
        regression_model = NutritionModel(input_size).to(device)
        
        class_model_path = os.path.join(base_dir, 'models', 'classification_model.pth')
        reg_model_path = os.path.join(base_dir, 'models', 'regression_model.pth')
        logger.info(f"Loading models from: {class_model_path}, {reg_model_path}")
        if not os.path.exists(class_model_path):
            raise FileNotFoundError(f"Classification model not found at {class_model_path}")
        if not os.path.exists(reg_model_path):
            raise FileNotFoundError(f"Regression model not found at {reg_model_path}")
        classification_model.load_state_dict(torch.load(class_model_path, map_location=device))
        regression_model.load_state_dict(torch.load(reg_model_path, map_location=device))
        classification_model.eval()
        regression_model.eval()
        
        features = df[['Data.Protein', 'Data.Fatt', 'Data.Carbohydrate']].values
        scaler = StandardScaler()
        scaler.fit(features)
        logger.info("Scaler fitted successfully")
        
        return df, classification_model, regression_model, scaler, device
    except Exception as e:
        logger.error(f"Error loading resources: {str(e)}")
        raise

df, classification_model, regression_model, scaler, device = load_resources()

def extract_food_name(query):
    try:
        common_words = ['how', 'many', 'calories', 'in', 'is', 'are', 'high', 'low', 'calorie', 'of', '100g', 'per', 'gram', 'grams']
        query = query.lower().strip()
        words = re.findall(r'\b\w+\b', query)
        food_words = [word for word in words if word not in common_words]
        if food_words:
            food_name = ' '.join(food_words)
            logger.debug(f"Extracted food name: {food_name}")
            return food_name
        potential_food = re.search(r'\b([a-z\s]+)\b', query)
        if potential_food:
            food_name = potential_food.group(1).strip()
            logger.debug(f"Fallback extracted food name: {food_name}")
            return food_name
        logger.warning("No food name extracted")
        return ''
    except Exception as e:
        logger.error(f"Error extracting food name: {str(e)}")
        return ''

@app.route('/')
def index():
    logger.debug("Serving homepage")
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        query = request.json.get('query', '').strip()
        logger.info(f"Received query: {query}")
        if not query:
            logger.warning("Empty query received")
            return jsonify({'error': 'Please enter a nutrition question!'}), 400
        
        food_name = extract_food_name(query)
        if not food_name:
            logger.warning("No food item identified in query")
            return jsonify({'response': 'Could not identify a food item in your query. Please specify a food (e.g., "apple", "chicken").'}), 400
        
        food_data = df[df['Category'].str.contains(food_name, case=False, na=False)]
        if food_data.empty:
            logger.warning(f"No data found for food: {food_name}")
            return jsonify({'response': f'Food "{food_name}" not found in dataset. Try another food!'}), 404
        
        features = df[['Data.Protein', 'Data.Fatt', 'Data.Carbohydrate']].values
        logger.debug(f"Features shape: {features.shape}")
        features_scaled = scaler.transform(features)
        features_tensor = torch.tensor(features_scaled, dtype=torch.float32).to(device)
        
        with torch.no_grad():
            class_output = classification_model(features_tensor).squeeze()
            class_prob = torch.sigmoid(class_output).mean().item()
            classification = 'High-calorie (>200 kcal)' if class_prob >= 0.5 else 'Low-calorie'
            logger.debug(f"Classification: {classification}, Probability: {class_prob}")
        
        with torch.no_grad():
            reg_output = regression_model(features_tensor).squeeze()
            predicted_calories = reg_output.mean().item()
            logger.debug(f"Predicted calories: {predicted_calories}")
        
        avg_protein = food_data['Data.Protein'].mean()
        avg_fat = food_data['Data.Fatt'].mean()
        avg_carbs = food_data['Data.Carbohydrate'].mean()
        
        response = (
            f"🔍 **Analysis Complete!**\n\n"
            f"**Food**: {food_name.capitalize()}\n"
            f"**Classification**: {classification}\n"
            f"**Predicted Calories**: {predicted_calories:.1f} kcal per 100g\n"
            f"**Breakdown**:\n"
            f"• Protein: {avg_protein:.1f}g\n"
            f"• Fat: {avg_fat:.1f}g\n"
            f"• Carbohydrates: {avg_carbs:.1f}g\n\n"
            f"**Recommendation**: {'Enjoy in moderation' if class_prob >= 0.5 else 'Great healthy option!'}"
        )
        logger.info("Response generated successfully")
        return jsonify({'response': response})
    
    except Exception as e:
        logger.error(f"Error in /ask: {str(e)}")
        return jsonify({'response': f'❌ Error processing request: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Flask app on port {port}")
    app.run(debug=False, host='0.0.0.0', port=port)