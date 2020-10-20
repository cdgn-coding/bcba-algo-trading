(gcloud ai-platform jobs submit training return_1m_20_10_2020__4 ^
    --module-name=classic.model ^
    --package-path=./classic ^
    --staging-bucket=gs://algo-trading ^
    --region=us-east1 ^
    --scale-tier=CUSTOM ^
    --master-machine-type=n1-standard-4 ^
    --python-version=3.7 ^
    --runtime-version=2.1 ^
    -- ^
    --target=Forward_Return_1m

gcloud ai-platform jobs submit training return_2m_20_10_2020__4 ^
    --module-name=classic.model ^
    --package-path=./classic ^
    --staging-bucket=gs://algo-trading ^
    --region=us-east1 ^
    --scale-tier=CUSTOM ^
    --master-machine-type=n1-standard-4 ^
    --python-version=3.7 ^
    --runtime-version=2.1 ^
    -- ^
    --target=Forward_Return_2m

gcloud ai-platform jobs submit training return_3m_20_10_2020__4 ^
    --module-name=classic.model ^
    --package-path=./classic ^
    --staging-bucket=gs://algo-trading ^
    --region=us-east1 ^
    --scale-tier=CUSTOM ^
    --master-machine-type=n1-standard-4 ^
    --python-version=3.7 ^
    --runtime-version=2.1 ^
    -- ^
    --target=Forward_Return_3m

gcloud ai-platform jobs submit training return_1w_20_10_2020__4 ^
    --module-name=classic.model ^
    --package-path=./classic ^
    --staging-bucket=gs://algo-trading ^
    --region=us-east1 ^
    --scale-tier=CUSTOM ^
    --master-machine-type=n1-standard-4 ^
    --python-version=3.7 ^
    --runtime-version=2.1 ^
    -- ^
    --target=Forward_Return_1w)