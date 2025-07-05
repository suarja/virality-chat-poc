# 🧪 Test Suite - TikTok Virality Prediction

## 🎯 **Purpose**

This directory contains the comprehensive test suite for our TikTok virality prediction system. Tests are organized by functionality to ensure proper coverage and maintainability.

## 📚 **Key Concepts**

- **Unit Testing**: Testing individual components in isolation
- **Integration Testing**: Testing how components work together
- **Test Coverage**: Percentage of code executed by tests
- **Test-Driven Development (TDD)**: Writing tests before implementation

## 🔗 **Related Documentation**

- [`docs/educational/ml_glossary.md`](../docs/educational/ml_glossary.md) - ML concepts glossary
- [`docs/reflection/iterations/`](../docs/reflection/iterations/) - Scientific documentation

## 🚀 **Getting Started**

### **Running All Tests**

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test category
python -m pytest tests/features/
python -m pytest tests/scraping/
```

### **Test Structure**

```
tests/
├── features/              # Feature engineering tests
│   ├── test_data_processor.py
│   └── test_feature_extractor.py
├── scraping/              # Data collection tests
│   └── test_scraping.py
├── utils/                 # Utility function tests
│   └── test_batch_tracker.py
├── pipeline/              # Pipeline integration tests
│   └── test_pipeline.py
└── test_gemini_analysis.py  # Gemini AI analysis tests
```

## 📈 **Educational Path**

### **Beginner Level**

1. **Understanding Test Structure** - How tests are organized
2. **Basic Test Concepts** - Unit vs Integration testing
3. **Running Tests** - How to execute the test suite

### **Intermediate Level**

1. **Writing Tests** - Creating new test cases
2. **Test Coverage** - Ensuring comprehensive testing
3. **Test Maintenance** - Keeping tests up to date

### **Advanced Level**

1. **Test-Driven Development** - Writing tests first
2. **Performance Testing** - Testing model and API performance
3. **Continuous Integration** - Automated testing in CI/CD

## 🎓 **Test Categories Explained**

### **Features Tests** (`tests/features/`)

**Purpose**: Test feature engineering components
**Key Concepts**: Feature Engineering, Data Preprocessing, Feature Selection
**Examples**:

- Test feature extraction from video metadata
- Test Gemini AI feature integration
- Test feature validation and cleaning

### **Scraping Tests** (`tests/scraping/`)

**Purpose**: Test data collection functionality
**Key Concepts**: Web Scraping, Data Validation, API Integration
**Examples**:

- Test TikTok data extraction
- Test rate limiting and error handling
- Test data format validation

### **Utils Tests** (`tests/utils/`)

**Purpose**: Test utility functions and helpers
**Key Concepts**: Utility Functions, Batch Processing, Data Management
**Examples**:

- Test batch processing system
- Test data validation utilities
- Test logging and monitoring

### **Pipeline Tests** (`tests/pipeline/`)

**Purpose**: Test end-to-end pipeline functionality
**Key Concepts**: Integration Testing, Pipeline Orchestration, Data Flow
**Examples**:

- Test complete data processing pipeline
- Test model training and evaluation
- Test feature aggregation workflows

## 📊 **Test Coverage Goals**

### **Current Coverage**

- **Features**: ~80% (Core functionality tested)
- **Scraping**: ~70% (Basic functionality tested)
- **Utils**: ~60% (Key utilities tested)
- **Pipeline**: ~50% (Integration points tested)

### **Target Coverage**

- **Features**: 90% (All feature extraction tested)
- **Scraping**: 85% (All scraping scenarios tested)
- **Utils**: 80% (All utility functions tested)
- **Pipeline**: 75% (All pipeline stages tested)

## 🔧 **Test Dependencies**

### **Required Packages**

```python
# Testing framework
pytest>=7.0.0
pytest-cov>=4.0.0

# Mocking and fixtures
pytest-mock>=3.10.0
factory-boy>=3.2.0

# Data testing
pandas>=1.5.0
numpy>=1.21.0
```

### **Test Data**

- **Mock Data**: Generated test data for unit tests
- **Sample Videos**: Real TikTok video data for integration tests
- **Gemini Responses**: Mocked AI analysis responses

## 📝 **Writing New Tests**

### **Test File Template**

```python
"""
📊 Test File: test_[module_name].py
🎯 Purpose: Tests for [module functionality]
📚 Concepts: [ML concepts being tested]
🔗 Related: [Links to related documentation]
"""

import pytest
from src.[module] import [function_to_test]

class Test[ModuleName]:
    """Test suite for [module name]."""

    def test_[specific_functionality](self):
        """Test [specific functionality description]."""
        # Arrange
        input_data = "test_input"

        # Act
        result = function_to_test(input_data)

        # Assert
        assert result == expected_output
```

### **Test Naming Conventions**

- **Test files**: `test_[module_name].py`
- **Test classes**: `Test[ModuleName]`
- **Test methods**: `test_[specific_functionality]`
- **Fixtures**: `[fixture_name]_fixture`

## 🚨 **Common Test Patterns**

### **Mocking External APIs**

```python
@pytest.fixture
def mock_gemini_api(mocker):
    """Mock Gemini API responses."""
    return mocker.patch('src.features.gemini_analyzer.analyze_video')
```

### **Data Validation Tests**

```python
def test_feature_validation(self, sample_video_data):
    """Test feature validation logic."""
    # Test valid data
    assert validate_features(sample_video_data) is True

    # Test invalid data
    invalid_data = sample_video_data.copy()
    invalid_data['duration'] = -1
    assert validate_features(invalid_data) is False
```

### **Integration Tests**

```python
def test_end_to_end_pipeline(self, sample_dataset):
    """Test complete pipeline from data to prediction."""
    # Run complete pipeline
    result = run_pipeline(sample_dataset)

    # Verify output structure
    assert 'predictions' in result
    assert 'features' in result
    assert 'model_performance' in result
```

## 🔍 **Debugging Tests**

### **Running Tests in Debug Mode**

```bash
# Run with verbose output
python -m pytest tests/ -v

# Run specific test with debug output
python -m pytest tests/features/test_feature_extractor.py::TestFeatureExtractor::test_extract_metadata -v -s

# Run with print statements
python -m pytest tests/ -s
```

### **Common Issues**

1. **Import Errors**: Check Python path and module structure
2. **Mock Issues**: Ensure mocks are properly configured
3. **Data Issues**: Verify test data format and availability
4. **Environment Issues**: Check API keys and dependencies

## 📈 **Performance Testing**

### **Model Performance Tests**

```python
def test_model_performance_benchmark(self):
    """Test model performance meets benchmarks."""
    model = load_trained_model()
    test_data = load_test_dataset()

    # Measure prediction time
    start_time = time.time()
    predictions = model.predict(test_data)
    prediction_time = time.time() - start_time

    # Assert performance requirements
    assert prediction_time < 1.0  # Less than 1 second
    assert len(predictions) == len(test_data)
```

### **API Performance Tests**

```python
def test_api_response_time(self, client):
    """Test API endpoint response times."""
    response = client.post("/api/v1/predict", json=test_video_data)

    # Assert response time
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 2.0  # Less than 2 seconds
```

---

_Test documentation created on July 5, 2025 - Comprehensive test suite for TikTok Virality Prediction POC_
