# Lab 6: Feature Engineering and Naive Bayes Classification

**Team Work:**  
This lab should be completed in pairs. Collaboration is encouraged!

**Objective:**  
- Understand and apply feature engineering techniques
- Implement text classification using Naive Bayes
- Work with categorical and text data
- Handle missing data through imputation
- Prepare a short presentation summarizing your work

---

## 1. Overview

In this lab, you will work with text data to build a document classification system using Naive Bayes. You will also practice various feature engineering techniques. The tasks include:

- **Feature Engineering:** Work with categorical and text data
- **Text Processing:** Convert text data into numerical features using techniques like TF-IDF
- **Model Building:** Implement Naive Bayes classification using Scikit-Learn
- **Model Evaluation:** Assess performance using metrics like accuracy and confusion matrix
- **Visualization:** Create plots to visualize results and feature importance
- **Presentation:** Prepare a short presentation (5 slides, maximum 5 minutes) summarizing your approach, results, and insights

---

## 2. Prerequisites

- Familiarity with Python and basic operations using NumPy and Pandas
- Basic understanding of feature engineering and Naive Bayes from our recent lecture
- Ensure you have installed the required Python libraries:
  ```bash
  pip install numpy pandas scikit-learn matplotlib seaborn nltk

## 3. The Dataset

We will use the 20 Newsgroups dataset, which is a collection of newsgroup documents. The dataset is available through Scikit-Learn's built-in datasets.
**Dataset Description:**  
- **Features:** Text documents from newsgroups
- **Labels:** Categories of newsgroups (e.g., sports, science, religion, etc.)
- The dataset will be loaded using `sklearn.datasets.fetch_20newsgroups`

---

## 4. Instructions

### 4.1. Feature Engineering Practice
- **Categorical Data:**
  - Create a small dataset with categorical variables
  - Practice one-hot encoding using `DictVectorizer` and `OneHotEncoder`
  - Visualize the transformed data

- **Text Processing:**
  - Load the 20 Newsgroups dataset
  - Implement basic text preprocessing (removing stopwords, punctuation)
  - Convert text to numerical features using both:
    - Count Vectorization (`CountVectorizer`)
    - TF-IDF Vectorization (`TfidfVectorizer`)

- **Missing Data:**
  - Create a dataset with some missing values
  - Practice different imputation strategies using `SimpleImputer`
  - Compare the effects of different imputation methods

### 4.2. Naive Bayes Classification
- **Data Preparation:**
  - Select a subset of categories from the 20 Newsgroups dataset
  - Split the data into training and testing sets
  - Apply TF-IDF vectorization

- **Model Building:**
  - Train a Multinomial Naive Bayes classifier
  - Create a pipeline combining TF-IDF and Naive Bayes
  - Experiment with different model parameters

- **Evaluation:**
  - Calculate accuracy, precision, recall, and F1-score
  - Create and visualize the confusion matrix
  - Analyze misclassified examples

### 4.3. Advanced Tasks (Optional)
- Implement cross-validation
- Try Gaussian Naive Bayes on numerical features
- Compare performance with other classifiers (e.g., SVM, Random Forest)
- Analyze feature importance and most predictive words

### 4.4. Presentation
- **Prepare a Short Presentation:**  
  - Create **5 min walkthrough** summarizing your work
  - **Duration:** 5 minutes or less
  - Include:
    - Overview of feature engineering techniques used
    - Text processing approach
    - Model performance and key findings
    - Challenges encountered and solutions
- **Presentation Delivery:** Be ready to present your walkthrough in class

---

## 5. Submission Instructions

1. **Repository Update:**  
   - Push your lab notebook/script and any supplementary files to your personal GitHub repository for the course by deadline, **13:00 on May 16, 2025**

2. **Email Submission:**  
   - Once completed, send an email with the subject:  
     ```
     [Your Name, Partner's Name] - Lab 6 Completed
     ```
   - Include a link to your GitHub repository
   - Send the email to: **eyuphan.koc@bogazici.edu.tr**

---

## 6. Additional Resources

- [Scikit-Learn Text Feature Extraction](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)
- [Scikit-Learn Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html)
- [NLTK Documentation](https://www.nltk.org/)
- [Feature Engineering Book](https://www.oreilly.com/library/view/feature-engineering-for/9781491953235/) 