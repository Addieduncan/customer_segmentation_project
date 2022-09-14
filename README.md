#Final Project for M393C, Machine Learning with Pf. Rachle Ward

DATASET: (Kaggle) CreditCard_data.csv

SHORT SUMMARY OF HOW TO USE REPO 

## Business Problem: 
Suppose a mid-sized credit union is looking to target current customers for marketing of additional products like insurance policies, auto and home loans, banking accounts, or simply additional credit cards. As a mid-sized union, a miscalculated digital marketing strategy represents a significant cost, while successful marketing increases access to potential revenue. For such as business, efficient resource allocation for this marketing initiative is more important than for their global-scale competitors. 

To obtain a baseline for a cost-effective digital marketing strategy, such a credit union could run a customer segmentation analysis on their current customers, thereby obtaining insights into the wealth profiles, spending habits, credit reliability, and financial needs of credit union members. In our project we exhibit techniques of modern data science which take advantage of a full profile of customer features to identify intrinsic patterns in customer credit history that are generaly obscured by standard spreadsheet analysis.

Written in Python with a Jupyter Notebook format (no GPU compatibility required), our code exemplifies a low-cost starting point for a business with only modest computing architecture to deploy first-principles data science to grow their revenue by identifying customer behavior profiles. 

## Methods:
The basis of our customer segmentation is to cluster customers based on several credit card usage features. We use [data from Kaggle] that contains information on 14 different attributes for about 8,600 credit card customers over a 6 month period. 8 of these attributes contain information about size (in USD) of customer purchases, payments, balances, cash advances, and credit limits. The other 6 attributes contain information about the frequency of purchases, payments, and cash advances. 

The first challenge is to understand the [feature distribution](https://github.com/Addieduncan/m393c_project/blob/b9e4bd4bae46f2e8c05811dbf0396f99d9ec28e3/images/all_dist.png) of the data and remove outliers that could skew the resulting clusters. We removed the top and bottom 1% of customers for each feature resulting in about 8% of the customers being removed. Since there are 14 features and we are removing 2% of the data from each feature we would expect 28% of the data to be removed. Because we only observed an 8% loss, many of the customers being removed are outliers in more than one feature, further justifying their removal.

The second challenge is to understand the geometry of the data and standardize the features so that they can be accurately compared against each other. A naive approach to standardizing the data by normalizing the features to take values between 0 and 1 leads to a fundamentally flawed analysis. This is because some of the data are frequency amounts which are integer valued numbers and the rest of the data are USD amounts which are real-valued numbers. Comparing the distance between two points which are integer-valued is geometrically very different from the distance between two points which are real-valued. In other words, if we were to use a real-valued metric across all of our data values we would find that two integer-valued data points are seen as further away than they would be using a discrete notion of distance (2 and 3 are consecutive integers but there are lots of real numbers between 2 and 3). To remedy this geometric issue we divide the features into 11 quantiles by population percentage and assign each quantile an integer value; the first 10% of the data is assigned to quantile 1, the next 10% is given to quantile 2 and so on. Further, if the features in the first k number of quantiles contain data points all with value 0 we assign 0 to those quantiles and assign the first non-zero quantile the number k+1. This effectively standardizes our data so that each feature is weighted equally regardless of the types of values that it takes. Moreover, there is no longer a need for removing outliers when using quantization analysis since the influence of outliers is removed by funneling the outliers into a quantile with a fixed value assignment.

The first clustering analysis we run on our data is a k-means clustering. This type of clustering uses distance from the cluster means to group data points into spherical clusters. We also run a Gaussian mixture clustering on our data which clusters based on the probability that a data point belongs to a cluster. Gaussian mixture model clusters are not necessarily spherical and allow for different types of overlaps of clusters. We find that the Gaussian mixture clustering returns nearly the same clusters as our k-means analysis. Since the Gaussian mixture model is less dependent on the geometry of the data yet still finds the same clusters we can have confidence that our k-means analysis is capturing the intrinsic clusters of our data. We proceed with using our k-means clustering because it is the more cost efficient algorithm.

The next step is to tune the parameters of our k-means model. We use several [error metrics](https://github.com/Addieduncan/m393c_project/tree/master/images/Error%20metric%20analysis) including the sum of squares, Calinski-Harabasz index, Davies-Bouldin index, and silhouette score analysis to determine the optimal number of clusters for our data. We find that the optimal number of customer groups for our segmentation is 9. 

Now we have a robust process for determining 9 groups of customer types based on 14 credit card usage features. Using principal component analysis to project our data onto the first two principal components we can visually identify the [9 customer groupings](https://github.com/Addieduncan/m393c_project/blob/20248cd2e5e6b3e24c12b867e0e511fdb605165d/images/PCA%20clusters/q_km_9_pca.png) in our data. For each of our customer groups we can analyze the [feature distribution of the customers in each group](https://github.com/Addieduncan/m393c_project/tree/master/images/Individual_Feature/feature%20distributions) to learn information about their purchasing and payment habits. 

## Conclusions - Customer Behavior Profiles: 

Since both K-Means and GMM algorithms yielded an 'optimal' set of 9 clusters, with significant overlap between the K-Means and GMM clusters, we begin by using these clusters as 9 "natural" customer behavior profiles. To uncover information about these profiles, we examine the distributions of the original customer features (not their quantized modifications) within each fixed cluster, taking the K-Means clusters as a baseline. For example, look at cluster 7 
