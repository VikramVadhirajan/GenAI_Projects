# AI-Powered Data Processing App 📊🤖

An interactive **Streamlit-based data processing and analysis application** that combines:

* Automated data cleaning
* Exploratory Data Analysis (EDA)
* Feature engineering
* AI-generated insights using LLMs

This tool allows users to upload datasets, perform preprocessing, visualize data, and generate intelligent summaries — all in one place.

---

# 🚀 Project Overview

This application provides a **complete end-to-end data processing pipeline** with an intuitive UI.

Users can:

* Upload datasets
* Explore and visualize data
* Clean and preprocess data
* Apply transformations (encoding, scaling, outlier treatment)
* Generate AI-powered dataset insights
* Download processed data and reusable pipeline artifacts

---

# 🧠 Key Features

### 📄 Data Handling

* Upload datasets dynamically
* View dataset preview and shape
* Maintain session state across operations

---

### 🤖 AI-Powered Insights

* Generate dataset summaries using LLMs
* Uses profiling + LLM for intelligent insights
* Requires API key (Groq / compatible)

---

### 📊 Data Profiling

* Automatic dataset profiling
* Summary statistics and structure overview

---

### 📈 Exploratory Data Analysis (EDA)

* Univariate, bivariate, and multivariate analysis
* Multiple chart types:

  * Histogram
  * Boxplot
  * Scatter plot
  * Violin plot
* Dynamic column selection

---

### ⚙️ Data Processing Pipeline

#### ✂️ Symbol Cleaning

* Remove punctuation and special characters from text columns

#### 🗑️ Column Removal

* Drop unwanted columns interactively

#### 🔍 Missing Value Analysis

* Summary and visualization of missing data
* Missing matrix visualization

#### 🧹 Row Filtering

* Remove rows based on missing value threshold

#### 🧠 Imputation

* Separate handling for:

  * Categorical columns
  * Numerical columns

#### 📊 Outlier Handling

* Outlier detection
* Boxplot visualization
* Selective outlier treatment

#### 🔤 Encoding

* Label Encoding
* One-Hot Encoding

#### 📏 Scaling

* Standard Scaling
* Min-Max Scaling
* Target column exclusion support

---

### 📦 Pipeline Artifact Generation

The app allows exporting reusable preprocessing components:

* Outlier bounds → `outlier.pkl`
* Encoders → `encoder.pkl`
* Scalers → `scaler.pkl`
* Imputers → `imputer.pkl`
* Symbol cleaner → `symbol_cleaner.pkl`

These can be reused in ML pipelines.

---

### ⬇️ Output

* Download processed dataset as CSV
* Download preprocessing artifacts

---

# 🧩 Application Structure

```id="app_struct"
005_Streamlit_DataAnalysis/
│
├── app.py
├── modules/
│   ├── llm.py
│   ├── uploader.py
│   ├── profiler.py
│   ├── preprocessing.py
│   ├── visualization.py
│   ├── missing_analysis.py
│   └── utils.py
│
├── requirements.txt
└── README.md
```

---

# 🔄 Application Workflow

1. Upload dataset
2. View data preview
3. Generate AI summary (optional)
4. Perform EDA
5. Apply preprocessing steps:

   * Cleaning
   * Missing value handling
   * Outlier treatment
   * Encoding
   * Scaling
6. View processed dataset
7. Download results and pipeline artifacts

---

# ⚙️ Technologies Used

* Python
* Streamlit
* Pandas
* Seaborn & Matplotlib
* Pickle (for pipeline artifacts)
* LLM API (Groq / compatible)

---

# ▶️ How to Run

### 1️⃣ Clone the repository

```bash
git clone https://github.com/VikramVadhirajan/Python_Scripts.git
```

---

### 2️⃣ Navigate to the project

```bash
cd 005_Streamlit_DataAnalysis
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run the app

```bash
streamlit run app.py
```

---

# 🧠 What Makes This Project Strong

* End-to-end data pipeline in a single UI
* Combines **Data Engineering + EDA + AI insights**
* Modular architecture (separate preprocessing modules)
* Exportable pipeline components (production-ready concept)
* Interactive and user-friendly

---

# 🔮 Future Enhancements

* Add model training & prediction module
* AutoML integration
* Dashboard export
* Cloud deployment (Streamlit Cloud / Azure)
* Data versioning support

---

# 👨‍💻 Author

**Vikram Vadhirajan**

Data Analyst | Machine Learning | Generative AI | Python

---

# ⭐ Support

If you find this project useful, consider giving it a ⭐
