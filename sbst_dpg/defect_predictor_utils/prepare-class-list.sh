#!/bin/sh
REPO_PATH=$1
SRC_PATH=$2
WORKSPACE=$3


cd $REPO_PATH/$SRC_PATH
find . -type f | grep .java >> $WORKSPACE/all_classes.log
sed -i 's+\./++g' $WORKSPACE/all_classes.log
sed -i 's+\.java++g' $WORKSPACE/all_classes.log
sed -i 's+/+\.+g' $WORKSPACE/all_classes.log

sed -i "s+$SRC_PATH/++g" $WORKSPACE/schwa_results.csv
sed -i 's+\.java++g' $WORKSPACE/schwa_results.csv
sed -i 's+/+\.+g' $WORKSPACE/schwa_results.csv
