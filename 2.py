#%% imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#%% data loading
df = pd.read_csv('powerlifting_cleaned.csv', low_memory=False)
print(df[['Name', 'Best3SquatKg', 'Best3BenchKg', 'Best3DeadliftKg', 'TotalKg']].head())

# %% ratio calc
df= df.sort_values(by='TotalKg', ascending=False).drop_duplicates(subset='Name')
def calculate_ratios(df):
    df['Squat Ratio'] = df['Best3SquatKg'] / df['TotalKg']
    df['Bench Press Ratio'] = df['Best3BenchKg'] / df['TotalKg']
    df['Deadlift Ratio'] = df['Best3DeadliftKg'] / df['TotalKg']
    return df
calculate_ratios(df)
# %% filter
df_female = df[df['Sex'] == 'F'][['Name', 'Squat Ratio', 'Bench Press Ratio', 'Deadlift Ratio', 'Dots']].dropna()
df_male = df[df['Sex'] == 'M'][['Name', 'Squat Ratio', 'Bench Press Ratio', 'Deadlift Ratio', 'Dots']].dropna()

#%% sklearn imports
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# %% scaling
X1 = df_female[['Squat Ratio', 'Bench Press Ratio', 'Deadlift Ratio', 'Dots']]
X2 = df_male[['Squat Ratio', 'Bench Press Ratio', 'Deadlift Ratio', 'Dots']]
scaler = StandardScaler()
X1_scaled = scaler.fit_transform(X1)
X2_scaled = scaler.fit_transform(X2)

#%% clustering
def k_means_clust(scaled_df) :
    wcss = []
    shilhouette_scores = []
    for k in range(2, 11):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(scaled_df)
        wcss.append(kmeans.inertia_)
        shilhouette_scores.append(silhouette_score(scaled_df, kmeans.labels_))
    return wcss, shilhouette_scores

def plot_wcss(wcss, shilhouette_scores):
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(range(2, 11), wcss, marker='o')
    plt.title('WCSS vs Number of Clusters')
    plt.xlabel('Number of Clusters')
    plt.ylabel('WCSS')

    plt.subplot(1, 2, 2)
    plt.plot(range(2, 11), shilhouette_scores, marker='o')
    plt.title('Silhouette Score vs Number of Clusters')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Silhouette Score')

    plt.tight_layout()
    plt.show()

# %% women
k_means_clust(X1_scaled)
plot_wcss(*k_means_clust(X1_scaled)) #decided on 4 clusters

# %% men
k_means_clust(X2_scaled)
plot_wcss(*k_means_clust(X2_scaled)) #again, decided on 4 clusters

# %% assign clusters
def assign_clusters(df, scaled_df, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['Cluster'] = kmeans.fit_predict(scaled_df)
    return df
assign_clusters(df_female, X1_scaled, 4)
assign_clusters(df_male, X2_scaled, 4)

#%% women clusters analysis
variables = ['Squat Ratio', 'Bench Press Ratio', 'Deadlift Ratio', 'Dots']

def get_cluster_stats(df, column):
    return df.groupby('Cluster')[column].agg(
        Mean='mean',
        Median='median',
        Std='std',
        Min='min',
        Q1=lambda x: x.quantile(0.25),
        Q3=lambda x: x.quantile(0.75),
        Max='max'
    ).round(2)
#%% print cluster stats - women
for var in variables:
    print(f"\n===== {var} =====")
    print(get_cluster_stats(df_female, var))

# cluster explanation - women
# Cluster 0: Strong deadlift, moderate squat and bench press, moderate dots - Deadlift specialists
# Cluster 1: Strong bench press, moderate squat, weaker deadlift, moderate dots - Bench Press specialists
# Cluster 2: Strong SBD, highest dots - All-rounders
# Cluster 3: Strong deadlift, lower squat and bench press, moderate dots - Elite Deadlifters

#%% print cluster stats - men
for var in variables:
    print(f"\n===== {var} =====")
    print(get_cluster_stats(df_male, var))

# cluster explanation - men
# Cluster 0: Strong benchpress and deadlift, moderate squat, modeate dots - Bench Press specialists
# Cluster 1: Well-rounded lifters, strong SBD, modearte-high dots - Well-rounded mid-level lifters
# Cluster 2: Highest Dots, strong SBD, moderate ratios - Elite All-rounders
# Cluster 3: Strong deadlift, lower squat and bench press, moderate dots - Deadlift specialists