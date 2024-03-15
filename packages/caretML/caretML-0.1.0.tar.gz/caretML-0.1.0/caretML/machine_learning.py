import numpy as np
from numba import njit
from sklearn.cluster import SpectralClustering, KMeans, DBSCAN
from sklearn.svm import SVC
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from sklearn.mixture import GaussianMixture
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error, accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import roc_auc_score

@njit(parallel=True)
def spectral_clustering(adjacency_matrix, n_clusters):
    """
    Perform spectral clustering on a graph represented by its adjacency matrix.

    Parameters:
        adjacency_matrix (ndarray): The adjacency matrix of the graph.
        n_clusters (int): Number of clusters to form.

    Returns:
        ndarray: Array of cluster labels for each node.
    """
    model = SpectralClustering(n_clusters=n_clusters, affinity='precomputed', assign_labels='discretize')
    return model.fit_predict(adjacency_matrix)

def support_vector_machine_classification(X, y, kernel='rbf', C=1.0):
    """
    Perform support vector machine (SVM) classification.

    Parameters:
        X (array_like): Input features.
        y (array_like): Target labels.
        kernel (str, optional): Kernel function. Default is 'rbf'.
        C (float, optional): Regularization parameter. Default is 1.0.

    Returns:
        ndarray: Support vectors.
        ndarray: Dual coefficients.
        ndarray: Intercept.
        ndarray: Labels predicted by the model.
    """
    clf = SVC(kernel=kernel, C=C)
    clf.fit(X, y)
    return clf.support_vectors_, clf.dual_coef_, clf.intercept_, clf.predict(X)

def autoencoder(data, encoding_dim, epochs=50, batch_size=32):
    """
    Train an autoencoder model on the given data.

    Parameters:
        data (array_like): Input data for training.
        encoding_dim (int): Dimensionality of the encoded representation.
        epochs (int, optional): Number of training epochs. Default is 50.
        batch_size (int, optional): Batch size for training. Default is 32.

    Returns:
        ndarray: Encoded representations of input data.
        ndarray: Decoded representations of input data.
    """
    input_data = Input(shape=(data.shape[1],))
    encoded = Dense(encoding_dim, activation='relu')(input_data)
    decoded = Dense(data.shape[1], activation='sigmoid')(encoded)
    autoencoder = Model(input_data, decoded)
    autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
    autoencoder.fit(data, data, epochs=epochs, batch_size=batch_size, shuffle=True, verbose=0)
    encoder = Model(input_data, encoded)
    decoded_data = autoencoder.predict(data)
    return encoder.predict(data), decoded_data

@njit(parallel=True)
def k_means_clustering(data, n_clusters, max_iter=300):
    """
    Perform K-means clustering on the given dataset.

    Parameters:
        data (array_like): Input data to be clustered.
        n_clusters (int): Number of clusters to form.
        max_iter (int, optional): Maximum number of iterations. Default is 300.

    Returns:
        ndarray: Cluster centers.
        ndarray: Labels for each data point.
    """
    kmeans = KMeans(n_clusters=n_clusters, max_iter=max_iter)
    labels = kmeans.fit_predict(data)
    return kmeans.cluster_centers_, labels

def gaussian_mixture_model(data, n_components, max_iter=100):
    """
    Fit a Gaussian mixture model to the given data.

    Parameters:
        data (array_like): Input data to fit the model.
        n_components (int): Number of mixture components.
        max_iter (int, optional): Maximum number of EM iterations. Default is 100.

    Returns:
        ndarray: Means of the Gaussian components.
        ndarray: Covariance matrices of the Gaussian components.
        ndarray: Mixing coefficients of the Gaussian components.
        ndarray: Labels for each data point.
    """
    gmm = GaussianMixture(n_components=n_components, max_iter=max_iter)
    labels = gmm.fit_predict(data)
    return gmm.means_, gmm.covariances_, gmm.weights_, labels

def dynamic_time_warping(sequence1, sequence2, distance_function):
    """
    Perform dynamic time warping (DTW) between two sequences.

    Parameters:
        sequence1 (array_like): First sequence.
        sequence2 (array_like): Second sequence.
        distance_function (callable): Function to compute distance between elements of sequences.

    Returns:
        float: DTW distance between the two sequences.
    """
    n, m = len(sequence1), len(sequence2)
    dp = np.zeros((n + 1, m + 1))
    dp[0, 0] = 0
    for i in range(1, n + 1):
        dp[i, 0] = np.inf
    for j in range(1, m + 1):
        dp[0, j] = np.inf
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = distance_function(sequence1[i - 1], sequence2[j - 1])
            dp[i, j] = cost + min(dp[i - 1, j], dp[i, j - 1], dp[i - 1, j - 1])
    return dp[n, m]

def linear_regression(X_train, y_train, X_test):
    """
    Perform linear regression on the given data.

    Parameters:
        X_train (array_like): Training features.
        y_train (array_like): Training labels.
        X_test (array_like): Test features.

    Returns:
        array_like: Predicted values.
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model.predict(X_test)

def random_forest_classification(X_train, y_train, X_test, y_test):
    """
    Perform random forest classification on the given data.

    Parameters:
        X_train (array_like): Training features.
        y_train (array_like): Training labels.
        X_test (array_like): Test features.
        y_test (array_like): Test labels.

    Returns:
        float: Accuracy score of the model.
    """
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return accuracy_score(y_test, y_pred)

def principal_component_analysis(data, n_components):
    """
    Perform principal component analysis (PCA) on the given data.

    Parameters:
        data (array_like): Input data.
        n_components (int): Number of components to keep.

    Returns:
        array_like: Transformed data.
    """
    pca = PCA(n_components=n_components)
    return pca.fit_transform(data)

def mean_squared_error_metric(y_true, y_pred):
    """
    Calculate the mean squared error between true and predicted values.

    Parameters:
        y_true (array_like): True labels.
        y_pred (array_like): Predicted labels.

    Returns:
        float: Mean squared error.
    """
    return mean_squared_error(y_true, y_pred)

def calculate_accuracy(y_true, y_pred):
    """
    Calculate the accuracy of a classification model.

    Parameters:
        y_true (array_like): True labels.
        y_pred (array_like): Predicted labels.

    Returns:
        float: Accuracy score.
    """
    return accuracy_score(y_true, y_pred)

def calculate_precision(y_true, y_pred, average='binary'):
    """
    Calculate the precision of a classification model.

    Parameters:
        y_true (array_like): True labels.
        y_pred (array_like): Predicted labels.
        average (str, optional): Type of averaging performed. Possible values are 'binary', 'micro', 'macro', 'weighted'. Default is 'binary'.

    Returns:
        float: Precision score.
    """
    return precision_score(y_true, y_pred, average=average)

def calculate_recall(y_true, y_pred, average='binary'):
    """
    Calculate the recall of a classification model.

    Parameters:
        y_true (array_like): True labels.
        y_pred (array_like): Predicted labels.
        average (str, optional): Type of averaging performed. Possible values are 'binary', 'micro', 'macro', 'weighted'. Default is 'binary'.

    Returns:
        float: Recall score.
    """
    return recall_score(y_true, y_pred, average=average)

def calculate_f1_score(y_true, y_pred, average='binary'):
    """
    Calculate the F1 score of a classification model.

    Parameters:
        y_true (array_like): True labels.
        y_pred (array_like): Predicted labels.
        average (str, optional): Type of averaging performed. Possible values are 'binary', 'micro', 'macro', 'weighted'. Default is 'binary'.

    Returns:
        float: F1 score.
    """
    return f1_score(y_true, y_pred, average=average)

def dbscan_clustering(data, eps=0.5, min_samples=5):
    """
    Perform DBSCAN clustering on the given data.

    Parameters:
        data (array_like): Input data.
        eps (float, optional): The maximum distance between two samples for them to be considered as in the same neighborhood. Default is 0.5.
        min_samples (int, optional): The number of samples (or total weight) in a neighborhood for a point to be considered as a core point. Default is 5.

    Returns:
        ndarray: Cluster labels for each data point.
    """
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    return dbscan.fit_predict(data)

def standardize_data(X):
    """
    Standardize the input data.

    Parameters:
        X (array_like): Input data.

    Returns:
        array_like: Standardized data.
    """
    scaler = StandardScaler()
    return scaler.fit_transform(X)

def split_train_test_data(X, y, test_size=0.2, random_state=None):
    """
    Split the data into training and test sets.

    Parameters:
        X (array_like): Input features.
        y (array_like): Target labels.
        test_size (float, optional): The proportion of the dataset to include in the test split. Default is 0.2.
        random_state (int, RandomState instance, or None, optional): Controls the randomness of the training and testing indices produced. Default is None.

    Returns:
        tuple: Tuple containing train-test split of input features and target labels.
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def perform_grid_search(model, param_grid, X, y, cv=5):
    """
    Perform grid search to find the best hyperparameters for a model.

    Parameters:
        model (estimator): Model to optimize.
        param_grid (dict): Dictionary of hyperparameters to search.
        X (array_like): Input features.
        y (array_like): Target labels.
        cv (int, optional): Number of folds for cross-validation. Default is 5.

    Returns:
        GridSearchCV: Fitted grid search object.
    """
    grid_search = GridSearchCV(model, param_grid, cv=cv)
    grid_search.fit(X, y)
    return grid_search

def calculate_roc_auc_score(y_true, y_pred):
    """
    Calculate the ROC AUC score of predictions.

    Parameters:
        y_true (array_like): True labels.
        y_pred (array_like): Predicted labels.

    Returns:
        float: ROC AUC score.
    """
    return roc_auc_score(y_true, y_pred)

def perform_cross_validation(model, X, y, cv=5, scoring=None):
    """
    Perform cross-validation to evaluate a model's performance.

    Parameters:
        model: Machine learning model to be evaluated.
        X (array_like): Input features.
        y (array_like): Target labels.
        cv (int, cross-validation generator, or an iterable, optional):
            Determines the cross-validation strategy. Default is 5-fold cross-validation.
        scoring (str or callable, optional): Scoring method. Default is None (uses model's default scoring).

    Returns:
        array_like: Array of scores obtained from cross-validation.
    """
    return cross_val_score(model, X, y, cv=cv, scoring=scoring)

def select_best_features(X, y, k=10):
    """
    Select the k best features based on mutual information between features and target.

    Parameters:
        X (array_like): Input features.
        y (array_like): Target labels.
        k (int, optional): Number of features to select. Default is 10.

    Returns:
        array_like: Transformed input features with selected features.
    """
    selector = SelectKBest(score_func=mutual_info_classif, k=k)
    X_selected = selector.fit_transform(X, y)
    return X_selected

def perform_dimensionality_reduction(X, method='PCA', n_components=None):
    """
    Perform dimensionality reduction on the input features.

    Parameters:
        X (array_like): Input features.
        method (str, optional): Dimensionality reduction method ('PCA', 't-SNE', etc.). Default is 'PCA'.
        n_components (int, optional): Number of components to keep. Default is None.

    Returns:
        ndarray: Transformed features with reduced dimensionality.
    """
    if method == 'PCA':
        pca = PCA(n_components=n_components)
        return pca.fit_transform(X)
    elif method == 't-SNE':
        tsne = TSNE(n_components=n_components)
        return tsne.fit_transform(X)
    # Add more dimensionality reduction methods as needed
    else:
        raise ValueError("Unsupported dimensionality reduction method.")

def build_model_pipeline(model, scaler=True, feature_selection=False, n_features=None):
    """
    Build a pipeline for the machine learning model.

    Parameters:
        model: Machine learning model.
        scaler (bool, optional): Whether to include feature scaling. Default is True.
        feature_selection (bool, optional): Whether to include feature selection. Default is False.
        n_features (int, optional): Number of features to select. Default is None.

    Returns:
        Pipeline: Pipeline object containing preprocessing steps and the model.
    """
    steps = []
    if scaler:
        steps.append(('scaler', StandardScaler()))
    if feature_selection:
        steps.append(('feature_selection', SelectKBest(mutual_info_classif, k=n_features)))
    steps.append(('model', model))
    return Pipeline(steps)

def tune_hyperparameters(model, param_grid, X_train, y_train, scoring='accuracy', cv=5):
    """
    Tune hyperparameters of the given model using grid search or randomized search.

    Parameters:
        model: Machine learning model.
        param_grid (dict): Dictionary of hyperparameters and their values for grid/randomized search.
        X_train (array_like): Input features for training.
        y_train (array_like): Target labels for training.
        scoring (str or callable, optional): Scoring metric for evaluation. Default is 'accuracy'.
        cv (int, cross-validation generator, or an iterable, optional): Cross-validation strategy. Default is 5.

    Returns:
        GridSearchCV or RandomizedSearchCV: Tuned model with best hyperparameters.
    """
    if isinstance(scoring, str):
        scoring = make_scorer(scoring)
    if len(param_grid) < 20:  # Use grid search for smaller parameter grids
        grid_search = GridSearchCV(model, param_grid, scoring=scoring, cv=cv)
    else:  # Use randomized search for larger parameter grids
        grid_search = RandomizedSearchCV(model, param_grid, scoring=scoring, cv=cv)
    grid_search.fit(X_train, y_train)
    return grid_search

def ensemble_model(X_train, y_train, estimators=None):
    """
    Train an ensemble model using a combination of base estimators.

    Parameters:
        X_train (array_like): Input features for training.
        y_train (array_like): Target labels for training.
        estimators (list of tuples, optional): List of base estimators and their weights. Default is None.

    Returns:
        object: Trained ensemble model.
    """
    if not estimators:
        estimators = [('rf', RandomForestClassifier()), ('gb', GradientBoostingRegressor())]
    from sklearn.ensemble import VotingClassifier, VotingRegressor
    if all(isinstance(estimator[1], RandomForestClassifier) for estimator in estimators):
        ensemble = VotingClassifier(estimators)
    else:
        ensemble = VotingRegressor(estimators)
    ensemble.fit(X_train, y_train)
    return ensemble

def custom_model_evaluation(y_true, y_pred):
    """
    Perform custom evaluation of model predictions.

    Parameters:
        y_true (array_like): True target labels.
        y_pred (array_like): Predicted target labels.

    Returns:
        float: Custom evaluation metric.
    """
    # Example of custom evaluation metric
    return precision_score(y_true, y_pred) * recall_score(y_true, y_pred)
