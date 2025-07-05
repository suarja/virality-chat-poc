# 📚 Machine Learning Glossary - TikTok Virality Prediction

## 🎯 **Purpose**

This glossary explains all Machine Learning concepts used in our TikTok virality prediction project. Each concept is explained with:

- **Simple Definition** - Easy to understand explanation
- **Real-World Context** - How it applies to our TikTok project
- **Mathematical Foundation** - Basic formulas and theory
- **Practical Examples** - Code examples from our project
- **Further Reading** - Links to detailed explanations

---

## 📊 **Core ML Concepts**

### **R² Score (Coefficient of Determination)**

**📖 Definition**: A statistical measure that represents the proportion of variance in the dependent variable that's predictable from the independent variable(s).

**🎯 In Our Context**:

- R² = 0.457 means our model explains 45.7% of the variance in TikTok view counts
- Range: 0 to 1 (higher is better)
- Our result: Good for a small dataset (8 videos)
- Interpretation: 45.7% of view count variation is predictable from our features

**🧮 Formula**:

```
R² = 1 - (SS_res / SS_tot)
```

- SS_res = Sum of squared residuals (prediction errors)
- SS_tot = Total sum of squares (total variance)

**💻 Example from Our Code**:

```python
from sklearn.metrics import r2_score
r2 = r2_score(y_true, y_pred)  # 0.457 in our case
```

**🔗 Related**: [Mean Squared Error](#mean-squared-error-mse), [Feature Importance](#feature-importance)

---

### **Feature Engineering**

**📖 Definition**: The process of creating new features from raw data to improve model performance.

**🎯 In Our Context**:

- Converting video metadata into numerical features
- Extracting visual features using Gemini AI
- Creating temporal features (hour, day, weekend)
- Combining multiple features into composite scores

**🧮 Process**:

```
Raw Data → Feature Extraction → Feature Selection → Model Training
```

**💻 Example from Our Code**:

```python
# Temporal feature engineering
df['hour_of_day'] = df['created_at'].dt.hour
df['is_weekend'] = df['created_at'].dt.weekday >= 5
```

**🔗 Related**: [Feature Importance](#feature-importance), [Data Preprocessing](#data-preprocessing)

---

### **Feature Importance**

**📖 Definition**: A measure of how much each feature contributes to the model's predictions.

**🎯 In Our Context**:

- audience_connection_score (0.124) - Most important feature
- hour_of_day (0.108) - Timing is crucial
- video_duration_optimized (0.101) - Duration matters
- Shows which features to focus on for improvement

**🧮 Calculation**:

- Random Forest: Based on Gini impurity reduction
- Linear Models: Based on coefficient magnitudes
- Our project: Uses Random Forest feature importance

**💻 Example from Our Code**:

```python
# Feature importance from Random Forest
feature_importance = model.feature_importances_
# audience_connection_score: 0.124
# hour_of_day: 0.108
# video_duration_optimized: 0.101
```

**🔗 Related**: [Feature Engineering](#feature-engineering), [Model Training](#model-training)

---

### **Cross-Validation**

**📖 Definition**: A technique to assess how well a model will generalize to new, unseen data.

**🎯 In Our Context**:

- Essential for small datasets (8 videos)
- Prevents overfitting to specific videos
- Validates model performance across different data splits
- Critical for reliable performance estimates

**🧮 Process**:

```
Dataset → Split into K folds → Train on K-1, test on 1 → Repeat K times → Average results
```

**💻 Example from Our Code**:

```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5)  # 5-fold cross-validation
mean_score = scores.mean()  # Average performance
```

**🔗 Related**: [Overfitting](#overfitting), [Model Evaluation](#model-evaluation)

---

### **Overfitting**

**📖 Definition**: When a model learns the training data too well, including noise, and performs poorly on new data.

**🎯 In Our Context**:

- Risk with small dataset (8 videos)
- Model might memorize specific video characteristics
- Cross-validation helps detect overfitting
- Need more data for robust model

**🧮 Indicators**:

- High training accuracy, low test accuracy
- Large gap between training and validation scores
- Unstable feature importance

**💻 Example Detection**:

```python
# Check for overfitting
train_score = model.score(X_train, y_train)  # 0.95
test_score = model.score(X_test, y_test)     # 0.45
overfitting = train_score - test_score > 0.1  # True
```

**🔗 Related**: [Cross-Validation](#cross-validation), [Regularization](#regularization)

---

### **Data Preprocessing**

**📖 Definition**: The process of cleaning and transforming raw data into a format suitable for machine learning.

**🎯 In Our Context**:

- Converting dates to numerical features
- Handling missing values in Gemini analysis
- Normalizing feature scales
- Encoding categorical variables

**🧮 Steps**:

```
Raw Data → Cleaning → Transformation → Scaling → Feature Engineering
```

**💻 Example from Our Code**:

```python
# Date preprocessing
df['hour_of_day'] = pd.to_datetime(df['created_at']).dt.hour
df['day_of_week'] = pd.to_datetime(df['created_at']).dt.dayofweek

# Feature scaling
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

**🔗 Related**: [Feature Engineering](#feature-engineering), [Model Training](#model-training)

---

## 🎯 **Model-Specific Concepts**

### **Random Forest**

**📖 Definition**: An ensemble learning method that constructs multiple decision trees and outputs the mean prediction.

**🎯 In Our Context**:

- Our primary model for virality prediction
- Handles both numerical and categorical features
- Provides feature importance scores
- Robust to overfitting

**🧮 Algorithm**:

```
1. Create multiple decision trees with random subsets of data
2. Each tree makes a prediction
3. Final prediction = average of all tree predictions
```

**💻 Example from Our Code**:

```python
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

**🔗 Related**: [Feature Importance](#feature-importance), [Ensemble Methods](#ensemble-methods)

---

### **Linear Regression**

**📖 Definition**: A statistical method that models the relationship between a dependent variable and one or more independent variables.

**🎯 In Our Context**:

- Baseline model for comparison
- Simple and interpretable
- Assumes linear relationships
- Good starting point for understanding data

**🧮 Formula**:

```
y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ + ε
```

- y = dependent variable (view count)
- β = coefficients (feature weights)
- x = independent variables (features)
- ε = error term

**💻 Example from Our Code**:

```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
coefficients = model.coef_  # Feature weights
```

**🔗 Related**: [R² Score](#r²-score-coefficient-of-determination), [Feature Importance](#feature-importance)

---

### **Mean Squared Error (MSE)**

**📖 Definition**: The average squared difference between predicted and actual values.

**🎯 In Our Context**:

- Measures prediction accuracy
- Penalizes large errors more heavily
- Used for model comparison
- Lower values indicate better performance

**🧮 Formula**:

```
MSE = (1/n) * Σ(y_pred - y_true)²
```

**💻 Example from Our Code**:

```python
from sklearn.metrics import mean_squared_error
mse = mean_squared_error(y_true, y_pred)
rmse = np.sqrt(mse)  # Root Mean Squared Error
```

**🔗 Related**: [R² Score](#r²-score-coefficient-of-determination), [Model Evaluation](#model-evaluation)

---

## 🔬 **Advanced Concepts**

### **Ensemble Methods**

**📖 Definition**: Techniques that combine multiple models to improve prediction accuracy and robustness.

**🎯 In Our Context**:

- Random Forest is an ensemble method
- Could combine different feature sets
- Improves stability and performance
- Reduces overfitting risk

**🧮 Types**:

- **Bagging**: Random Forest (our current approach)
- **Boosting**: Gradient Boosting, XGBoost (future consideration)
- **Stacking**: Combining multiple models

**💻 Example from Our Code**:

```python
# Random Forest (Bagging)
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators=100)

# Future: Gradient Boosting
from sklearn.ensemble import GradientBoostingRegressor
gb_model = GradientBoostingRegressor()
```

**🔗 Related**: [Random Forest](#random-forest), [Model Training](#model-training)

---

### **Regularization**

**📖 Definition**: Techniques to prevent overfitting by adding constraints to the model.

**🎯 In Our Context**:

- Important for small datasets
- Prevents model from memorizing training data
- Improves generalization to new videos
- Can be applied to various models

**🧮 Types**:

- **L1 (Lasso)**: Adds absolute value penalty
- **L2 (Ridge)**: Adds squared penalty
- **Elastic Net**: Combines L1 and L2

**💻 Example from Our Code**:

```python
# Ridge Regression (L2 regularization)
from sklearn.linear_model import Ridge
model = Ridge(alpha=1.0)  # alpha controls regularization strength

# Lasso Regression (L1 regularization)
from sklearn.linear_model import Lasso
model = Lasso(alpha=0.1)
```

**🔗 Related**: [Overfitting](#overfitting), [Model Training](#model-training)

---

### **Hyperparameter Tuning**

**📖 Definition**: The process of finding the optimal parameters for a machine learning model.

**🎯 In Our Context**:

- Optimizing Random Forest parameters
- Finding best feature combinations
- Improving model performance
- Essential for small datasets

**🧮 Methods**:

- **Grid Search**: Try all parameter combinations
- **Random Search**: Random parameter sampling
- **Bayesian Optimization**: Smart parameter search

**💻 Example from Our Code**:

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(RandomForestRegressor(), param_grid, cv=5)
grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_
```

**🔗 Related**: [Cross-Validation](#cross-validation), [Model Training](#model-training)

---

## 📈 **Evaluation Metrics**

### **Model Evaluation**

**📖 Definition**: The process of assessing how well a model performs on unseen data.

**🎯 In Our Context**:

- Critical for validating predictions
- Ensures model reliability
- Guides model improvements
- Essential for business decisions

**🧮 Metrics Used**:

- **R² Score**: Overall model performance
- **MSE/RMSE**: Prediction accuracy
- **Feature Importance**: Model interpretability
- **Cross-validation**: Generalization ability

**💻 Example from Our Code**:

```python
# Comprehensive model evaluation
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"R² Score: {r2:.3f}")
print(f"RMSE: {rmse:.0f} views")
```

**🔗 Related**: [R² Score](#r²-score-coefficient-of-determination), [Cross-Validation](#cross-validation)

---

## 🔗 **Cross-References**

### **Concept Relationships**

- **R² Score** ↔ **MSE** ↔ **Model Evaluation**
- **Feature Engineering** ↔ **Feature Importance** ↔ **Model Training**
- **Cross-Validation** ↔ **Overfitting** ↔ **Regularization**
- **Random Forest** ↔ **Ensemble Methods** ↔ **Hyperparameter Tuning**

### **Learning Path**

1. **Beginner**: R² Score, Feature Engineering, Data Preprocessing
2. **Intermediate**: Cross-Validation, Overfitting, Random Forest
3. **Advanced**: Ensemble Methods, Regularization, Hyperparameter Tuning

### **File References**

- `scripts/analyze_existing_data.py` - Implementation of these concepts
- `src/features/modular_feature_system.py` - Feature engineering examples
- `docs/reflection/iterations/iteration_1_scientific_documentation.md` - Results using these concepts

---

## 📚 **Further Reading**

### **Online Resources**

- [Scikit-learn Documentation](https://scikit-learn.org/stable/)
- [Machine Learning Mastery](https://machinelearningmastery.com/)
- [Towards Data Science](https://towardsdatascience.com/)

### **Books**

- "Introduction to Statistical Learning" by James et al.
- "Hands-On Machine Learning" by Aurélien Géron
- "Python Machine Learning" by Sebastian Raschka

### **Our Project Resources**

- [`docs/reflection/iterations/`](../reflection/iterations/) - Scientific documentation
- [`notebooks/`](../../notebooks/) - Interactive examples
- [`tests/`](../../tests/) - Code examples and tests

---

_Glossary created on July 5, 2025 - Educational resource for TikTok Virality Prediction POC_
