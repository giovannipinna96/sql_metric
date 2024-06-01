#!/bin/bash

echo "Start to colled BIRD data"

cd /mnt/data/gpinna/lisbona_sql_metric/sql_metric/data

mkdir ./raw_data_zip
mkdir ./raw_data

echo "Downloading dev data"
wget -P ./raw_data_zip https://bird-bench.oss-cn-beijing.aliyuncs.com/dev.zip
# echo "Downloading train data"
# wget -P ./raw_data https://bird-bench.oss-cn-beijing.aliyuncs.com/train.zip

echo "Unzipping dev data"
unzip ./raw_data_zip/dev.zip -d ./raw_data -x '__MACOSX/*'
# echo "Unzipping train data"
# unzip ./raw_data_zip/train.zip -d ./raw_data

echo "Unzipping databases inside dev folder"
unzip ./raw_data/dev/dev_databases.zip -d ./raw_data/dev -x '__MACOSX/*'

echo "Finish"
