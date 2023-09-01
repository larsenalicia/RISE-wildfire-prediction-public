# RISE-wildfire-prediction-public 🔥

#### Abstract
This study aims to predict wildfires in Sweden using only satellite data in combination with different machine learning methods. The features used include land surface temperature, normalised difference vegetation index, and enhanced vegetation index. The target was thermal anomalies and fire. The data was filtered and aggregated in 16 different ways, which were used for training separate models. Evaluation was based on F1 scores. The results showed that the best performance was obtained by using a more restricted data-filtering and an area larger than 20 by 20 kilometers. However, additional statistical tests are required for general conclusions. Another challenge was imbalanced data-sets. This was combated by exploring over- and under sampling. The F1 scores showed these sampling techniques had an effect, but also needs further investigations before generality. While there are areas of improvement in the methodology, the study aims to guide future research in combating destructive wildfires.

#### Tutorial
This repository contains tutorials on all steps from data procurement to analysis, regarding wildfire prediction. These are the steps to get you started:

1. Download the requirements in the requirements.txt file. 
2. Modify the variables in globals/global_vars.py file, to suit the location, time period, area etc. of interest.
3. Run <code>0_set_up.pyinb</code> to create all the necessary folders for the data storage.
4. Run <code>1_data_procurement.pyinb</code> to acquire the data specified in the globals/global_vars.py file.
5. Run <code>2_data_qc_filtering.pyinb</code> to filter the data based on the quality control dataset. Note that this notebook requires manual modification of the filtering requirements to suit the datasets of interest.
6. Run  <code>3_data_aggregation.pyinb</code> to pre-process the data, e.g., standardise the spatial and temporal resolution, make derivations, and normalise the data.
7. Run <code>4_exploratory_data_analysis.pyinb</code> and get aquatinted with the data.
8. Run <code>5_ml_performance_results.pyinb</code> and iterate through a number of machine learning models and differently aggregated datasets.
9. Finally, run <code>5_finetuning_rf.pyinb</code> and explore under- and oversampling with random forest algorithms.

Hope you found this tutorial useful! Have a nice day!

