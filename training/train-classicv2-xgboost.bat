(gcloud ai-platform jobs submit training return_signals_model_23_10_2020_7__target_1m ^
    --module-name=classicv2.xgboost ^
    --package-path=./classicv2 ^
    --staging-bucket=gs://algo-trading ^
    --region=us-east1 ^
    --scale-tier=CUSTOM ^
    --master-machine-type=n1-standard-16 ^
    --python-version=3.7 ^
    --runtime-version=2.2 ^
    -- ^
    --version=v3-scaled ^
    --target=Forward_Return_1m

gcloud ai-platform jobs submit training return_signals_model_23_10_2020_7__target_2m ^
    --module-name=classicv2.xgboost ^
    --package-path=./classicv2 ^
    --staging-bucket=gs://algo-trading ^
    --region=us-east1 ^
    --scale-tier=CUSTOM ^
    --master-machine-type=n1-standard-16 ^
    --python-version=3.7 ^
    --runtime-version=2.2 ^
    -- ^
    --version=v3-scaled ^
    --target=Forward_Return_2m

gcloud ai-platform jobs submit training return_signals_model_23_10_2020_7__target_3m ^
    --module-name=classicv2.xgboost ^
    --package-path=./classicv2 ^
    --staging-bucket=gs://algo-trading ^
    --region=us-east1 ^
    --scale-tier=CUSTOM ^
    --master-machine-type=n1-standard-16 ^
    --python-version=3.7 ^
    --runtime-version=2.2 ^
    -- ^
    --version=v3-scaled ^
    --target=Forward_Return_3m

gcloud ai-platform jobs submit training return_signals_model_23_10_2020_7__target_1w ^
    --module-name=classicv2.xgboost ^
    --package-path=./classicv2 ^
    --staging-bucket=gs://algo-trading ^
    --region=us-east1 ^
    --scale-tier=CUSTOM ^
    --master-machine-type=n1-standard-16 ^
    --python-version=3.7 ^
    --runtime-version=2.2 ^
    -- ^
    --version=v3-scaled ^
    --target=Forward_Return_1w)