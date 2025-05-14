import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# 1. Load data from CSV file
# Make sure 'features.csv' is in the same directory as this script
df = pd.read_csv('features.csv')

# 2. Select numeric features (excluding any non-numeric columns like instance_name and source)
numeric_cols = df.select_dtypes(include=['number']).columns
X = df[numeric_cols]

# 3. Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Apply PCA to reduce to 2 components
pca = PCA(n_components=2)
components = pca.fit_transform(X_scaled)

# 5. Create a result DataFrame with PC scores and metadata
result = pd.DataFrame(components, columns=['PC1', 'PC2'])
if 'instance_name' in df.columns:
    result['instance_name'] = df['instance_name']
if 'source' in df.columns:
    result['source'] = df['source']

# 6. Show explained variance
print("Explained variance ratio:", pca.explained_variance_ratio_)

# 7. Plot the first two principal components
plt.figure(figsize=(8, 6))

# Plot google-hashcode instances
gh_mask = result['source'] == 'google-hashcode'
plt.scatter(result.loc[gh_mask, 'PC1'], result.loc[gh_mask, 'PC2'], 
            c='blue', label='Google Hashcode', alpha=0.7, edgecolor='k')

# Plot synthetic-real-world instances
srw_mask = result['source'] == 'synthetic-real-world'
plt.scatter(result.loc[srw_mask, 'PC1'], result.loc[srw_mask, 'PC2'], 
            c='red', label='Synthetic Real World', alpha=0.7, edgecolor='k')

# Plot random-synthetic instances
# srw_mask = result['source'] == 'synthetic-google-hashcode'
# plt.scatter(result.loc[srw_mask, 'PC1'], result.loc[srw_mask, 'PC2'], 
            # c='green', label='Synthetic Google Hashcode', alpha=0.7, edgecolor='k')

# srw_mask = result['source'] == 'synthetic-random'
# plt.scatter(result.loc[srw_mask, 'PC1'], result.loc[srw_mask, 'PC2'], 
#             c='yellow', label='Synthetic Random', alpha=0.7, edgecolor='k')

# srw_mask = result['source'] == 'initial-synthetic-random'
# plt.scatter(result.loc[srw_mask, 'PC1'], result.loc[srw_mask, 'PC2'], 
            # c='black', label='Initial Synthetic Random', alpha=0.7, edgecolor='k')

# Annotate points
for i, txt in enumerate(result['instance_name']):
    if txt in ['b_read_on.txt', 'c_incunabula.txt', 'd_tough_choices.txt', 'e_so_many_books.txt', 'f_libraries_of_the_world.txt']:
        plt.annotate(txt, (result.loc[i, 'PC1'], result.loc[i, 'PC2']), fontsize=14, alpha=1.0)
    else:
        plt.annotate('', (result.loc[i, 'PC1'], result.loc[i, 'PC2']), fontsize=3, alpha=0.2)

plt.title('PCA: PC1 vs PC2')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 8. (Optional) Save the result to CSV
result.to_csv('pca_result.csv', index=False)