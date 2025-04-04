
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        print("Data loaded successfully.")
        print(df.head())
        print("\nSummary statistics:")
        print(df.describe())
        print("\nMissing values:")
        print(df.isnull().sum())
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None


def fill_missing_values(df):
    filled_df = df.copy()
    age_col = filled_df.columns[7]
    for age in filled_df[age_col].unique():
        age_group = filled_df[filled_df[age_col] == age]
        means = age_group.mean()
        filled_df.loc[filled_df[age_col] == age] = age_group.fillna(means)
    return filled_df


def visualize_data(df):
    age_col = df.columns[7]
    strength_col = df.columns[8]
    features = df.columns[:7]

    plt.figure(figsize=(8, 6))
    df.groupby(age_col)[strength_col].mean().plot(marker='o')
    plt.xlabel('Age (days)')
    plt.ylabel('Strength (MPa)')
    plt.title('Concrete Compressive Strength vs. Age')
    plt.grid(True)
    plt.show()

    df_28 = df[df[age_col] == 28]
    fig, axs = plt.subplots(2, 4, figsize=(16, 8))
    axs = axs.flatten()

    for i, feature in enumerate(features):
        axs[i].scatter(df_28[feature], df_28[strength_col], alpha=0.6)
        axs[i].set_title(f'Strength vs. {feature}', fontsize=10)
        axs[i].set_xlabel(feature)
        axs[i].set_ylabel('Strength (MPa)')
        axs[i].grid(True)

    fig.delaxes(axs[-1])
    plt.tight_layout()
    plt.show()


def split_data(df):
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    return train_test_split(X, y, test_size=0.2, random_state=42)


def train_evaluate_visualize(X_train, X_test, y_train, y_test):
    model = LinearRegression().fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Squared Error: {mse:.4f}")
    print(f"R² Score: {r2:.4f}")

    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred, alpha=0.6)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    plt.xlabel("Actual Strength (MPa)")
    plt.ylabel("Predicted Strength (MPa)")
    plt.title("Predicted vs. Actual Strength")
    plt.grid(True)
    plt.show()

    residuals = y_test - y_pred
    plt.figure(figsize=(8, 6))
    sns.histplot(residuals, kde=True)
    plt.axvline(0, linestyle='--', color='red')
    plt.xlabel("Residuals")
    plt.title("Residual Distribution")
    plt.grid(True)
    plt.show()

    return model


def main():
    file_path = '../../datasets/concrete_strength/Concrete_Data.xls'
    df = load_data(file_path)
    if df is not None:
        df = fill_missing_values(df)
        visualize_data(df)
        X_train, X_test, y_train, y_test = split_data(df)
        train_evaluate_visualize(X_train, X_test, y_train, y_test)


if __name__ == '__main__':
    main()
