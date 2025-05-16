#!/bin/sh

work_dir=$(dirname $(readlink -f $0))/..
log_dir=/data3/E03SubData/trigger_2020dec

data_dir=(
    # /mnt/hdd1/bench_e03_2020
    /mnt/hdd1/e03_2020dec
    # /misc/eb1_ssd1/e40_2019feb
    # /misc/eb1_ssd2/e40_2019feb
    # /misc/e40_ssd1/e40_2018jun
    # /misc/e40_ssd2/e40_2018jun
    # /misc/e40_ssd1/bench_e40
    # /misc/e40_ssd2/bench_e40
)

if [ $$ -ne $(pgrep -fo $0) ]; then
    echo "$0 is already running."
    exit 1
fi

last_log=$work_dir/last.log

while true
do
    for d in ${data_dir[@]}
    do
	run=`cat $d/misc/runno.txt 2>/dev/null`
	if [ $? != 0 -o -z "$run" ]; then
	    continue
	    #exit
	fi
	run=`printf %05d $run`
	log=$log_dir/trigger_$run.log
	if [ ! -f $log ]; then
	    echo "RUN $run"
	    cat $last_log >$log 2>&1
	fi
    done
    sleep 30
done
