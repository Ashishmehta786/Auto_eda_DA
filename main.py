#import streamlit as st





import pandas as pd
from flask import Flask,render_template, request 
import csv 
import os
#import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
#import mpld3
#from pandas_profiling import ProfileReport
#from google.colab import files

app = Flask(__name__)

UPLOAD_FOLDER = 'csv'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
  return render_template('upload.html')



@app.route('/upload', methods=['POST'])
def upload():
    # Check if the POST request has the file part
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']

    # If the user does not select a file, the browser submits an empty part without filename
    if file.filename == '':
        return 'No selected file'

    if file:
        # Save the file to the uploads folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Process the CSV file
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            # You can process the CSV data here

        return 'File uploaded successfully'

def perform_eda(data):
    # Summary Information
    summary = {}

    # Data Information
    summary['Data Information'] = data.info()

    # Summary Statistics
    summary['Summary Statistics'] = data.describe()

    # Data Correlation - Heatmap
    correlation_matrix = data.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Matrix - Heatmap")
    plt.tight_layout()
    correlation_plot_path = "correlation_heatmap.png"
    plt.savefig(correlation_plot_path)
    plt.close()
    summary['Correlation Matrix - Heatmap'] = correlation_plot_path

    # Categorical Plots
    categorical_columns = data.select_dtypes(include='object').columns
    for column in categorical_columns:
        plt.figure(figsize=(8, 6))
        sns.countplot(x=column, data=data, palette='pastel')
        plt.title(f"{column} - Count Plot")
        plt.xticks(rotation=45)
        plt.tight_layout()
        count_plot_path = f"{column}_count_plot.png"
        plt.savefig(count_plot_path)
        plt.close()
        summary[f'{column} - Count Plot'] = count_plot_path

        # Count Plot Summary
        summary[f'{column} - Count Plot Summary'] = \
            f"The count plot displays the distribution of the '{column}' category. " \
            f"It shows the frequency of each category in the dataset."

    # Numerical Plots
    numerical_columns = data.select_dtypes(include=['int64', 'float64']).columns
    for column in numerical_columns:
        plt.figure(figsize=(8, 6))
        sns.histplot(data[column], kde=True, color='skyblue')
        plt.title(f"{column} - Histogram")
        plt.tight_layout()
        histogram_plot_path = f"{column}_histogram.png"
        plt.savefig(histogram_plot_path)
        plt.close()
        summary[f'{column} - Histogram'] = histogram_plot_path

        # Histogram Summary
        summary[f'{column} - Histogram Summary'] = \
            f"The histogram shows the distribution of '{column}' numerical data. " \
            f"It provides insights into the data's central tendency, spread, and skewness."

        # Log-Log Scaling Plot
        if data[column].min() > 0:
            plt.figure(figsize=(8, 6))
            plt.loglog(data[column], marker='o', linestyle='', markersize=4)
            plt.title(f"{column} - Log-Log Scaling Plot")
            plt.tight_layout()
            log_log_plot_path = f"{column}_log_log_scaling_plot.png"
            plt.savefig(log_log_plot_path)
            plt.close()
            summary[f'{column} - Log-Log Scaling Plot'] = log_log_plot_path

            # Log-Log Scaling Plot Summary
            summary[f'{column} - Log-Log Scaling Plot Summary'] = \
                f"The log-log scaling plot visualizes '{column}' numerical data on " \
                f"a logarithmic scale on both the x-axis and y-axis. It is useful for " \
                f"visualizing relationships that might not be evident in linear plots."

        # Additional Numerical Plots
        plt.figure(figsize=(8, 6))
        sns.boxplot(x=column, data=data, palette='pastel')
        plt.title(f"{column} - Box Plot")
        plt.tight_layout()
        box_plot_path = f"{column}_box_plot.png"
        plt.savefig(box_plot_path)
        plt.close()
        summary[f'{column} - Box Plot'] = box_plot_path

        # Box Plot Summary
        summary[f'{column} - Box Plot Summary'] = \
            f"The box plot displays the distribution of '{column}' numerical data through " \
            f"quartiles, showing the median, interquartile range (IQR), and potential outliers."

        plt.figure(figsize=(8, 6))
        sns.violinplot(x=column, data=data, palette='pastel')
        plt.title(f"{column} - Violin Plot")
        plt.tight_layout()
        violin_plot_path = f"{column}_violin_plot.png"
        plt.savefig(violin_plot_path)
        plt.close()
        summary[f'{column} - Violin Plot'] = violin_plot_path

        # Violin Plot Summary
        summary[f'{column} - Violin Plot Summary'] = \
            f"The violin plot combines box plots and kernel density plots to show " \
            f"the distribution and density of '{column}' numerical data. It is useful " \
            f"for comparing the distribution of multiple categories."

        plt.figure(figsize=(8, 6))
        sns.kdeplot(data[column], shade=True, color='skyblue')
        plt.title(f"{column} - KDE Plot")
        plt.tight_layout()
        kde_plot_path = f"{column}_kde_plot.png"
        plt.savefig(kde_plot_path)
        plt.close()
        summary[f'{column} - KDE Plot'] = kde_plot_path

        # KDE Plot Summary
        summary[f'{column} - KDE Plot Summary'] = \
            f"The KDE plot shows the probability density function of '{column}' numerical data. " \
            f"It provides a smooth estimate of the underlying data distribution."

        plt.figure(figsize=(8, 6))
        sns.lineplot(x=data.index, y=data[column])
        plt.title(f"{column} - Line Plot")
        plt.tight_layout()
        line_plot_path = f"{column}_line_plot.png"
        plt.savefig(line_plot_path)
        plt.close()
        summary[f'{column} - Line Plot'] = line_plot_path

        # Line Plot Summary
        summary[f'{column} - Line Plot Summary'] = \
            f"The line plot displays the trend or relationship between the index and '{column}' " \
            f"numerical data. It is useful for identifying patterns and trends in time series data."

            # Additional Categorical Plots
        for column in categorical_columns:
            plt.figure(figsize=(8, 6))
            sns.barplot(x=data[column].value_counts().index, y=data[column].value_counts(), palette='pastel')
            plt.title(f"{column} - Bar Plot")
            plt.xticks(rotation=45)
            plt.tight_layout()
            bar_plot_path = f"{column}_bar_plot.png"
            plt.savefig(bar_plot_path)
            plt.close()
            summary[f'{column} - Bar Plot'] = bar_plot_path

            # Bar Plot Summary
            summary[f'{column} - Bar Plot Summary'] = \
                f"The bar plot displays the distribution of '{column}' categorical data using bars. " \
                f"It is useful for comparing the frequency or count of categories across different groups."

    return summary

def save_summary_to_html(summary, output_html):
    with open(output_html, 'w') as f:
        f.write("<html>")
        f.write("<head><title>EDA Summary</title></head>")
        f.write("<body>")

        # Write the summary for each plot and include the image links
        for section, info in summary.items():
            f.write(f"<h3>{section}</h3>")
            if section.startswith(('Correlation Matrix', 'Count Plot', 'Histogram', 'Box Plot', 'Violin Plot', 'KDE Plot', 'Line Plot', 'Bar Plot')):
                f.write(f"<img src='{info}' alt='{section}'><br><br>")
            else:
                f.write(f"<p>{info}</p>")

        f.write("</body>")
        f.write("</html>")


def main():
  # Upload the CSV file
  print("Upload a CSV file:")
  csv_file = upload()

  # Load the data from the uploaded CSV file
  data = pd.read_csv("dlf.csv")

  # Perform EDA and generate plots
  summary = perform_eda(data)

  # Convert the summary to an HTML file
  output_html = "eda_summary.html"
  save_summary_to_html(summary, output_html)

   # Print the EDA summary
  print("\nEDA Summary:")
  for section, info in  summary.items():
    print(f"\n{section}:\n{info}")

  # Display link to download the HTML file
  print(f"\nEDA Summary saved as '{output_html}'")


  
app.run(port=5000 )