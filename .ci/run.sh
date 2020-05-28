#!/bin/bash
#
# Copyright (c) 2017-2020 Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0
#

# This script will execute the Kata Containers Test Suite.

set -e

cidir=$(dirname "$0")
source "${cidir}/lib.sh"

export RUNTIME="kata-runtime"

export CI_JOB="${CI_JOB:-default}"

case "${CI_JOB}" in
	"CRI_CONTAINERD_K8S")
		echo "INFO: Containerd checks"
		sudo -E PATH="$PATH" bash -c "make cri-containerd"
		sudo -E PATH="$PATH" CRI_RUNTIME="containerd" bash -c "make kubernetes"
		;;
	"FIRECRACKER")
		echo "INFO: Running docker integration tests"
		sudo -E PATH="$PATH" bash -c "make docker"
		echo "INFO: Running soak test"
		sudo -E PATH="$PATH" bash -c "make docker-stability"
		echo "INFO: Running oci call test"
		sudo -E PATH="$PATH" bash -c "make oci"
		echo "INFO: Running networking tests"
		sudo -E PATH="$PATH" bash -c "make network"
		echo "INFO: Running crio tests"
		sudo -E PATH="$PATH" bash -c "make crio"
		;;
	"CLOUD-HYPERVISOR")
		echo "INFO: Containerd checks"
		sudo -E PATH="$PATH" bash -c "make cri-containerd"

		echo "INFO: Running kubernetes tests"
		sudo -E PATH="$PATH" bash -c "make kubernetes"

		echo "INFO: Running docker integration tests"
		sudo -E PATH="$PATH" bash -c "make docker"

		echo "INFO: Running soak test"
		sudo -E PATH="$PATH" bash -c "make docker-stability"

		echo "INFO: Running oci call test"
		sudo -E PATH="$PATH" bash -c "make oci"

		echo "INFO: Running networking tests"
		sudo -E PATH="$PATH" bash -c "make network"
		;;
	"PODMAN")
		export TRUSTED_GROUP="kvm"
		newgrp "${TRUSTED_GROUP}" << END
		echo "This is running as group $(id -gn)"
END
		echo "INFO: Running podman integration tests"
		bash -c "make podman"
		;;
	*)
		echo "INFO: Running checks"
		sudo -E PATH="$PATH" bash -c "make check"

		echo "INFO: Running functional and integration tests ($PWD)"
		sudo -E PATH="$PATH" bash -c "make test"
		;;
esac
