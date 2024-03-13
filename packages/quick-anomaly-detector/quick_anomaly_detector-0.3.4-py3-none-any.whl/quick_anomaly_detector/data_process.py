import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, f1_score, roc_curve
import pandas as pd
import numpy as np
import torch, re, warnings, json


######################################
#       Load Data, combine Data      #
######################################
def combineDataFile(file_arr):
    df_arr = []
    for item in file_arr:
        df_arr.append(pd.read_csv(item))
    df = pd.concat(df_arr)
    return df


#########################################
#             Histogram graph           #
#########################################
def graph_multiple_histograms(df, columns, layout=(2, 2), bin_numbers=None):
    """
    Plot multiple histograms of specified columns from a DataFrame.

    :param df: The pandas DataFrame containing the data.
    :type df: pandas.DataFrame
        
    :param columns: List of column names to be plotted.
    :type columns: list
        
    :param layout: Tuple specifying the layout dimensions of subplots. Default is (2, 2).
    :type layout: tuple, optional
        
    :param bin_numbers: List of integers specifying the number of bins for each column.
    :type bin_numbers: list, optional

    :return: The generated matplotlib Figure object containing the histograms.
    :rtype: matplotlib.figure.Figure
    
    Example:
    
    .. code-block:: python

        from quick_anomaly_detector.data_process import graph_multiple_histograms

        columns_to_plot = ['a', 'b', 'c', 'd']
        bin_numbers = [10, 20, 15, 10]  # Example list of bin numbers corresponding to each column
        fig = graph_multiple_histograms(df, columns_to_plot, layout=(2, 2), bin_numbers=bin_numbers)
        plt.show()
    
    """
    num_plots = len(columns)
    num_rows, num_cols = layout
    total_plots = num_rows * num_cols

    if num_plots > total_plots:
        raise ValueError("Number of columns exceeds the available space in the layout.")

    if bin_numbers is None:
        bin_numbers = [10] * num_plots
    elif len(bin_numbers) != num_plots:
        raise ValueError("Length of bin_numbers must match the number of columns.")

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(14, 10))
    axes = axes.ravel()

    for i, (column, bins) in enumerate(zip(columns, bin_numbers)):
        ax = axes[i]
        ax.hist(df[column], bins=bins)
        ax.set_xlabel(column)
        ax.set_ylabel("Frequency")
        ax.set_title(f"Histogram of {column}")

    # Hide empty subplots
    for j in range(num_plots, total_plots):
        axes[j].axis('off')

    plt.tight_layout()
    return fig

def category_hist_graph(df, category_column):
    """
    This function is for plot the histograms of category feature
    """
    category_counts = df[category_column].value_counts()
    fig, ax = plt.subplots()
    category_counts.plot(kind='bar')
    ax.set_xlabel(category_column)
    ax.set_ylabel('Frequency')
    ax.set_title(f'Histogram of {category_column}')
    return fig, category_counts


##################################################
#                Scatter graph                   #
##################################################
def graph_scatter(df, x_column, y_column, color_column):
    """
    Create a scatter plot with color mapping based on a column of a DataFrame.

    :param df: The pandas DataFrame containing the data.
    :type df: pandas.DataFrame

    :return: The generated scatter plot figure.
    :rtype: matplotlib.figure.Figure

    :raises ValueError: If one or more specified columns do not exist in the DataFrame.

    Example: 

    .. code-block:: python

        from quick_anomaly_detector.data_process import graph_scatter

        df = pd.DataFrame({'x_column': [1, 2, 3], 'y_column': [4, 5, 6], 'color_column': ['red', 'blue', 'green']})
        fig = graph_scatter(df, 'x_column', 'y_column', 'color_column')
        plt.show()
    
    .. note:: 
    
        Ensure that the DataFrame contains the required columns for plotting.
    """
    # Validate input parameters
    if not all(col in df.columns for col in [x_column, y_column, color_column]):
        raise ValueError("One or more specified columns do not exist in the DataFrame.")

    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(df[x_column], df[y_column], c=df[color_column], cmap='viridis', alpha=0.7)
    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)
    ax.set_title(f"Scatter Chart (Color by {color_column})")
    cbar = plt.colorbar(ScalarMappable(norm=None, cmap='viridis'), ax=ax, label=color_column)
    return fig



##################################################
#        Check Wrongly-Predicted Data           #
##################################################
def check_wrong(df, predict='predict', label='label'):
    """
    `check_wrong` is a function to calculate the predicted wrongly df

    :param df: The pandas DataFrame containing the data.
    :type df: pandas.DataFrame

    :param predict: the column name of predict 
    :type predict: string

    :param label: the column name of label 
    :type label: string

    :return: df_tn, df_fn, df_tp, df_fp dataframe
    :rtype: [pandas.DataFrame, pandas.DataFrame, pandas.DataFrame, pandas.DataFrame]

    """
    df_tn = df[(df[predict] == 0) & (df[label] == 0)]
    df_fp = df[(df[predict] == 1) & (df[label] == 0)]
    df_fn = df[(df[predict] == 0) & (df[label] == 1)]
    df_tp = df[(df[predict] == 1) & (df[label] == 1)]
    return df_tn, df_fn, df_tp, df_fp



##################################################
#         Log Sqaure feature transform           #
##################################################
def apply_transformations(df, column_name):
    """
    Apply logarithm and square transformations to a column in a DataFrame.

    :param df: The pandas DataFrame containing the data.
    :type df: pandas.DataFrame
        
    :param column_name: The name of the column to transform.
    :type column_name: str

    :return: A list of column names including the original column and the transformed columns.
    :rtype: list
        
    Example

    .. code-block:: python

        from quick_anomaly_detector.data_process import apply_transformations

        columns_to_plot = log_sqaure(df, 'column_name')
    """
    # Apply transformations
    df[f'log_{column_name}'] = df[column_name].apply(lambda x: np.log(x + 0.001))
    df[f'square2_{column_name}'] = df[column_name].apply(lambda x: x ** 2)
    df[f'square0.5_{column_name}'] = df[column_name].apply(lambda x: x ** 0.5)
    
    # Define columns to plot
    transformed_columns = [column_name, f'log_{column_name}', f'square2_{column_name}', f'square0.5_{column_name}']
    
    return transformed_columns



##################################################
#         check valid tensor                     #
##################################################
def check_valid_tensor_data(input_tensor):
    """
    Perform checks on the input tensor.
    
    :param input_tensor: Input tensor to be checked.
    :type input_tensor: torch.Tensor
    
    :return: A tuple containing a boolean indicating whether the input passes all checks and a message indicating the result of the checks.
    :rtype: tuple[bool, str]

    
    Example: 

    .. code-block:: python

        from quick_anomaly_detector.data_process import check_valid_tensor_data

        input_tensor = torch.tensor([1.0, 2.0, float('nan'), 4.0])  # Example tensor with NaN
        valid, message = check_valid_tensor_data(input_tensor)
        print(valid, message)
    """
    # Check if input_tensor is a torch.Tensor
    if not isinstance(input_tensor, torch.Tensor):
        return False, "Input is not a torch.Tensor"
    
    # Check if input_tensor contains NaN or infinite values
    if torch.isnan(input_tensor).any() or torch.isinf(input_tensor).any():
        return False, "Input contains NaN or infinite values"
    
    # Check if input_tensor is of floating-point data type
    if input_tensor.dtype not in [torch.float32, torch.float64]:
        return False, "Input is not of floating-point data type"
    
    # Check if input_tensor has a valid shape (not empty)
    if input_tensor.numel() == 0:
        return False, "Input tensor has an empty shape"
    
    return True, "Input passes all checks"



#########################################
#              Eval Metics              #
#########################################
def calculate_metrics(actual_labels, predicted_labels):
    """
    Calculate various evaluation metrics for binary classification.

    :param actual_labels: Ground truth labels.
    :type actual_labels: array-like

    :param predicted_labels: Predicted labels.
    :type predicted_labels: array-like

    :return: Dictionary containing the following evaluation metrics:
        - precision (float): Precision score.
        - recall (float): Recall score.
        - label_pass_rate (float): Proportion of samples labeled as negative class in the ground truth.
        - predict_pass_rate (float): Proportion of samples predicted as negative class.
        - ks (float): Kolmogorov-Smirnov statistic.
        - gini (float): Gini coefficient.
        - f1 (float): F1 score.
        - auc_roc (float): Area under the ROC curve.
        - accuracy (float): Accuracy score.
    :rtype: dict
    """
    # Precision
    precision = precision_score(actual_labels, predicted_labels)
    # Recall
    recall = recall_score(actual_labels, predicted_labels)
    # Pass Rate
    label_pass_rate = np.mean(actual_labels == 0)
    predict_pass_rate = np.mean(predicted_labels == 0)
    # KS statistic
    fpr, tpr, _ = roc_curve(actual_labels, predicted_labels)
    ks_statistic = max(tpr - fpr)
    # F1 Score
    f1 = f1_score(actual_labels, predicted_labels)
    # AUC-ROC
    auc_roc = roc_auc_score(actual_labels, predicted_labels)
    # Gini coefficient
    gini = 2 * auc_roc - 1
    # Accuracy
    accuracy = accuracy_score(actual_labels, predicted_labels)
    metrics = {
      'precision': precision, 'recall': recall, 
      'label_pass_rate': label_pass_rate, 'predict_pass_rate': predict_pass_rate,
      'ks': ks_statistic, 'gini': gini, 'f1': f1, 'auc_roc': auc_roc, 'accuracy': accuracy
    }
    return metrics



#########################################
#  format dataframe column              #
#########################################
# Example usage:
# parse_dates(df, 'date_column')
# parse_dates(df, 'date_column', format='%d/%m/%Y %H:%M:%S')
def parse_dates(df, date_column_name, format=None):
    """
    Example:

    .. code-block:: python

        parse_dates(df, 'date_column')
        parse_dates(df, 'date_column', format='%d/%m/%Y %H:%M:%S')
    """
    if date_column_name not in df.columns:
        raise ValueError(f"'{date_column_name}' column not found in the DataFrame.")
    def apply_date_parser(date_parser, format=None):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                df['date_column'] = date_parser(df[date_column_name], errors='coerce', format=format)
            return df['date_column'].values
        except Exception as e:
            print(e)
            return None

    if format is None:
        try:
            # Attempt parsing with default settings
            return apply_date_parser(pd.to_datetime)
        except Exception as e:
            # If default parsing fails, try to extract and use the format from the error
            match = re.search(r'Parsing dates in (.+?) format', str(e))
            if match:
                date_format = match.group(1)
                return apply_date_parser(pd.to_datetime, format=date_format)
            else:
                print(e)
                return None
    else:
        # Parse with the specified format
        return apply_date_parser(pd.to_datetime, format=format)

#########################################
#  format numeric column              #
#########################################
def format_numeric_column(df, numeric_column_name):
    try:
        df['numric_column'] = df[numeric_column_name].apply(lambda x: int(x) if x.isdigit() else 0)
        return df['numric_column'].values
    except Exception as e:
        print(e)
        return None

################################################################
#              Get value from df's json column                 #
################################################################
# function to get value of node in json
def process_json(row, key_names):
    try:
        parsed_json = json.loads(row)
        value = parsed_json
        for key in key_names:
            if key in value:
                value = value[key]
            else:
                return None
        return value
    except (json.JSONDecodeError, TypeError, KeyError):
        return None

def get_feature_from_json(df, json_column_name, key_names):
    """ get value of json columns by keys"""
    df_copy = df.copy()
    df_copy.loc[:, 'json_feature'] = df[json_column_name].apply(process_json, args=(key_names,))
    return df_copy['json_feature'].values


###############################################################
#                                                             #
#       get email domain and predix from email column         #
#                                                             #
###############################################################
def get_email_host(df, email_column='email'):
    if email_column not in df.columns:
        raise ValueError(f"'{email_column}' column not found in the DataFrame.")
    df[email_column] = df[email_column].fillna('').str.lower()
    df['email_domain'] = ''
    df['email_prefix'] = ''
    # check for non-empty email addresses
    mask_non_empty_email = df[email_column] != ''
    df.loc[mask_non_empty_email, 'email_domain'] = df[mask_non_empty_email][email_column].str.split('@').str[1]
    df.loc[mask_non_empty_email, 'email_prefix'] = df[mask_non_empty_email][email_column].str.split('@').str[0]
    df['email_domain'] = df['email_domain'].str.lower()
    df['email_prefix'] = df['email_prefix'].str.lower()
    return df['email_prefix'].values, df['email_domain'].values