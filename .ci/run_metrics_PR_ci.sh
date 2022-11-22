#!/bin/bash
# Copyright (c) 2017-2021 Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0

# Note - no 'set -e' in this file - if one of the metrics tests fails
# then we wish to continue to try the rest.
# Finally at the end, in some situations, we explicitly exit with a
# failure code if necessary.

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
source "${SCRIPT_DIR}/../metrics/lib/common.bash"
RESULTS_DIR=${SCRIPT_DIR}/../metrics/results
CHECKMETRICS_DIR=${SCRIPT_DIR}/../cmd/checkmetrics
# Where to look by default, if this machine is not a static CI machine with a fixed name.
CHECKMETRICS_CONFIG_DEFDIR="/etc/checkmetrics"
# Where to look if this machine is a static CI machine with a known fixed name.
CHECKMETRICS_CONFIG_DIR="${CHECKMETRICS_DIR}/ci_worker"
CM_DEFAULT_DENSITY_CONFIG="${CHECKMETRICS_DIR}/baseline/density-CI.toml"
KATA_HYPERVISOR="${KATA_HYPERVISOR:-qemu}"
METRICS_IPERF="${METRICS_IPERF:-false}"
METRICS_LEGACY="${METRICS_LEGACY:-true}"

# Set up the initial state
init() {
	metrics_onetime_init
}

# Execute metrics scripts
run() {
	pushd "$SCRIPT_DIR/../metrics"

	if [ $METRICS_MLC == "true" ]; then
		#mlc/mlc_test_ctr.sh 60
		mlc/mlc_full.sh 60
	fi

	if [ $METRICS_FIO == "true" ]; then
		bash storage/fio-k8s/scripts/fio-test/fio-test.sh
	fi


	if [ $METRICS_LEGACY == "true" ]; then
		# Cloud hypervisor tests are being affected by kata-containers/kata-containers/issues/1488
		if [ "${KATA_HYPERVISOR}" != "cloud-hypervisor" ]; then
		# If KSM is available on this platform, let's run any tests that are
		# affected by having KSM on/orr first, and then turn it off for the
		# rest of the tests, as KSM may introduce some extra noise in the
		# results by stealing CPU time for instance.
			if [[ -f ${KSM_ENABLE_FILE} ]]; then
				save_ksm_settings
				trap restore_ksm_settings EXIT QUIT KILL
				set_ksm_aggressive

				# Run the memory footprint test - the main test that
				# KSM affects.
				bash density/memory_usage.sh 20 300 auto
			fi
		fi

		restart_docker_service

		# Run the density tests - no KSM, so no need to wait for settle
		# (so set a token 5s wait)
		# disable_ksm
		# bash density/memory_usage.sh 20 5

		# Run storage tests
		# bash storage/blogbench.sh

		# Run the density test inside the container
		# bash density/memory_usage_inside_container.sh

		# Run the time tests
		#bash time/launch_times.sh -i public.ecr.aws/ubuntu/ubuntu:latest -n 20
	fi

	if [ $METRICS_IPERF == "true" ]; then
		# Run the cpu statistics test
		bash network/iperf3_kubernetes/k8s-network-metrics-iperf3.sh -b
	fi

	echo "Start to generate csv and pdf."
	sh statis/statis.sh
	popd
}

init
run

