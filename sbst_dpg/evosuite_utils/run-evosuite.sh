#!/bin/sh
FQ_CLASS_NAME=$1
PROJ_CLASSPATH=$2
SEARCH_BUDGET=$3
COVERED_GOALS_PATH=$4
TESTS_DIR=$5
REPORT_DIR=$6
ASSERTION_TIMEOUT=$7
JUNIT_CHECK_TIMEOUT=$8
WRITE_JUNIT_TIMEOUT=$9
MEM=${10}
EVOSUITE_LOGS_OUT=${11}
EVOSUITE_JAR_DIR=${12}

if [ -z $EVO ] 
then export EVO="java -Xms4000m -Xmx4000m -jar $EVOSUITE_JAR_DIR/evosuite-master-1.0.7-SNAPSHOT.jar"
fi

$EVO -mem $MEM -permSize 256 -class $FQ_CLASS_NAME -projectCP $PROJ_CLASSPATH -criterion branch -Dstrategy=MOSuite -Dalgorithm=DynaMOSA -Dselection_function=RANK_CROWD_DISTANCE_TOURNAMENT -Dsearch_budget=$SEARCH_BUDGET -Dassertion_strategy=ALL -Dminimize=true -Dwrite_covered_goals_file=true -Dstop_zero=true -Dcoverage=false -Dnew_statistics=false -Dwrite_junit_timeout=$WRITE_JUNIT_TIMEOUT -Dassertion_timeout=$ASSERTION_TIMEOUT -Djunit_check_timeout=$JUNIT_CHECK_TIMEOUT -Dmax_loop_iterations=-1 -Dcovered_goals_file=$COVERED_GOALS_PATH -Dtest_dir=$TESTS_DIR -Dreport_dir=$REPORT_DIR -Dlog_time_taken=true -Dnum_test_files=8 -Dlog_age=true -Dbalance_test_cov=false -Dremove_covered_targets=true -Darchive_all=false -Dlog_balance_test_cov=true > $EVOSUITE_LOGS_OUT
