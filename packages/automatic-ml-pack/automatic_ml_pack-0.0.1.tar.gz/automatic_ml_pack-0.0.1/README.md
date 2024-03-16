## Malaria Incidence Prediction


https://feature-engine.trainindata.com/en/latest/user_guide/index.html#transformation

python ./modules/pipeline/train_pipeline.py --input_file notebooks/data/heart.csv --target_column HeartDisease --input_type csv --training_type clf --engineer_new_features --output_base test --test_size 0.2 --standard_scaling --feature_selection --feature_selection_method addition --selectkbest_num_features 32