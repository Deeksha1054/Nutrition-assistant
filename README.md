
# AI Nutrition Assistant

![AI Nutrition Assistant](https://img.shields.io/badge/Status-Active-green)  
A web-based application that provides personalized nutrition insights using AI-powered classification and regression models. Users can query nutritional information (e.g., "How many calories in an apple?") and receive detailed analyses, including calorie predictions, macronutrient breakdowns, and food classifications (high/low calorie).

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Deployment](#deployment)
- [Challenges and Solutions](#challenges-and-solutions)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Overview
The AI Nutrition Assistant leverages machine learning to deliver actionable nutrition insights through a user-friendly web interface. Built with Flask and PyTorch, it processes natural language queries to classify foods and predict calorie content based on macronutrients (protein, fat, carbohydrates) from a nutritional dataset (`food.csv`). The responsive frontend, styled with Tailwind CSS, ensures accessibility across devices. The project demonstrates full-stack development, integrating AI models with web technologies, and is deployed on a cloud platform (e.g., Render).

## Features
- **Natural Language Queries**: Ask questions like "How many calories in pizza?" or "Is chicken high-calorie?"
- **Food Classification**: Labels foods as high-calorie (>200 kcal) or low-calorie using a PyTorch neural network.
- **Calorie Prediction**: Estimates calorie content per 100g with a regression model.
- **Macronutrient Breakdown**: Provides protein, fat, and carbohydrate details.
- **Responsive UI**: Clean, modern interface with Tailwind CSS and JavaScript interactivity.
- **Error Handling**: Robust logging and user-friendly error messages for invalid queries or server issues.
- **Potential Multimodality**: Extensible for image or voice inputs (future work).

## Tech Stack
- **Backend**: Python, Flask, PyTorch, Pandas, scikit-learn, flask-cors
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Dataset**: `food.csv` (nutritional data with columns: `Category`, `Data.Kilocalories`, `Data.Protein`, `Data.Fatt.Total Lipid`, `Data.Carbohydrate`)
- **Models**: Pre-trained PyTorch models (`classification_model.pth`, `regression_model.pth`)
- **Deployment**: Render (or Heroku), Gunicorn
- **Tools**: Git, GitHub, VS Code

## Installation
### Prerequisites
- Python 3.10+
- Git
- Virtual environment tool (e.g., `venv`)
- Optional: CUDA-enabled GPU for PyTorch (CPU works fine)

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/ai-nutrition-assistant.git
   cd ai-nutrition-assistant
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\Activate.ps1  # Windows (PowerShell)
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Files**:
   - Ensure `Data/food.csv`, `models/classification_model.pth`, and `models/regression_model.pth` are present.
   - Check `food.csv` columns: `Category`, `Data.Kilocalories`, `Data.Protein`, `Data.Fatt.Total Lipid`, `Data.Carbohydrate`.

5. **Run the Application**:
   ```bash
   python main.py
   ```
   - Open `http://localhost:5000` in a browser.

## Usage
1. **Navigate to the App**:
   - Access the homepage at `http://localhost:5000` (local) or your deployed URL (e.g., `https://your-app.onrender.com`).
2. **Query Nutrition**:
   - Go to the "AI Model Assistant" section.
   - Enter a query (e.g., "How many calories in an apple?") in the textarea.
   - Click "Get AI Response" to view results, including classification, calories, and macronutrients.
3. **Example Output**:
   ```
   🔍 Analysis Complete!
   Food: Apple
   Classification: Low-calorie
   Predicted Calories: 52.0 kcal per 100g
   Breakdown:
   • Protein: 0.3g
   • Fat: 0.2g
   • Carbohydrates: 14.0g
   Recommendation: Great healthy option!
   ```

## Directory Structure
```
ai-nutrition-assistant/
├── Data/
│   └── food.csv
├── models/
│   ├── classification_model.pth
│   ├── regression_model.pth
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── scripts.js
├── templates/
│   └── index.html
├── main.py
├── requirements.txt
├── Procfile
└── README.md
```

## Deployment
1. **Prepare Files**:
   - Ensure `Data/food.csv` and `models/*.pth` are committed to the repository.
   - Include `Procfile`:
     ```
     web: gunicorn main:app
     ```
2. **Update `requirements.txt`**:
   ```
   flask==2.3.2
   pandas==2.0.3
   numpy==1.24.3
   torch==2.0.1
   scikit-learn==1.3.0
   gunicorn==20.1.0
   flask-cors==4.0.1
   ```
3. **Deploy to Render**:
   - Create a new Web Service on Render.
   - Link your GitHub repository.
   - Set environment variables:
     - `PYTHON_VERSION`: 3.10
     - `PORT`: 5000
   - Deploy and access at `https://your-app.onrender.com`.
4. **Troubleshooting**:
   - Check Render logs for errors (e.g., missing files, CORS issues).
   - Verify `BACKEND_URL` in `static/js/scripts.js` matches the deployed URL.

## Challenges and Solutions
- **Challenge**: `KeyError: "Column 'Data.Fatt' not found in dataset"`.
  - **Cause**: Typo in `main.py` referencing `Data.Fatt` instead of `Data.Fatt.Total Lipid`.
  - **Solution**: Updated `main.py` to use correct column name after verifying `food.csv` columns.
- **Challenge**: Frontend-backend connectivity failure in deployment.
  - **Cause**: Relative `/ask` URL in `scripts.js` failed on separate domains; CORS issues.
  - **Solution**: Added dynamic `BACKEND_URL` in `scripts.js` and enabled CORS with `flask-cors` in `main.py`.
- **Challenge**: File path issues in deployment.
  - **Cause**: `food.csv` moved to `Data/` folder, causing path errors.
  - **Solution**: Used `os.path` for robust file paths in `main.py`.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

Please follow coding standards and include tests for new features.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contact
- **Author**: Deeksha R G
- **Email**: [deeksharng@gmail.com](mailto:deeksharng@gmail.com)
- **LinkedIn**: [Deeksha R G](https://www.linkedin.com/in/deeksha-r-g-6237b6280/)
