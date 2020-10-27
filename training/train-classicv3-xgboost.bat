(gcloud ai-platform jobs submit training classicv3_xgboost__no_currency_no_scaled_basic_261020202347__target_1m ^
    --module-name=classicv3.xgboost ^
    --package-path=./classicv3 ^
    --staging-bucket=gs://algo-trading ^
    --region=us-east1 ^
    --scale-tier=CUSTOM ^
    --master-machine-type=n1-standard-16 ^
    --python-version=3.7 ^
    --runtime-version=2.2 ^
    -- ^
    --version=only-usd-no-scaled-continuous-no-currency ^
    --target=Forward_Return_1m

gcloud ai-platform jobs submit training classicv3_xgboost__no_currency_no_scaled_basic_261020202347__target_2m ^
    --module-name=classicv3.xgboost ^
    --package-path=./classicv3 ^
    --staging-bucket=gs://algo-trading ^
    --region=us-east1 ^
    --scale-tier=CUSTOM ^
    --master-machine-type=n1-standard-16 ^
    --python-version=3.7 ^
    --runtime-version=2.2 ^
    -- ^
    --version=only-usd-no-scaled-continuous-no-currency ^
    --target=Forward_Return_2m

gcloud ai-platform jobs submit training classicv3_xgboost__no_currency_no_scaled_basic_261020202347__target_3m ^
    --module-name=classicv3.xgboost ^
    --package-path=./classicv3 ^
    --staging-bucket=gs://algo-trading ^
    --region=us-east1 ^
    --scale-tier=CUSTOM ^
    --master-machine-type=n1-standard-16 ^
    --python-version=3.7 ^
    --runtime-version=2.2 ^
    -- ^
    --version=only-usd-no-scaled-continuous-no-currency ^
    --target=Forward_Return_3m

gcloud ai-platform jobs submit training classicv3_xgboost__no_currency_no_scaled_basic_261020202347__target_1w ^
    --module-name=classicv3.xgboost ^
    --package-path=./classicv3 ^
    --staging-bucket=gs://algo-trading ^
    --region=us-east1 ^
    --scale-tier=CUSTOM ^
    --master-machine-type=n1-standard-16 ^
    --python-version=3.7 ^
    --runtime-version=2.2 ^
    -- ^
    --version=only-usd-no-scaled-continuous-no-currency ^
    --target=Forward_Return_1w)