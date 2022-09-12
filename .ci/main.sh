#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
set -o errtrace

cidir=$(dirname "$0")
source "/etc/os-release" || source "/usr/lib/os-release"

export WORKSPACE=${WORKSPACE:-$HOME}
# export WORKSPACE=$1
export GOPATH="${WORKSPACE}/go"

#necessary variables.
export CRI_CONTAINERD="yes"
export CRI_RUNTIME="containerd"
export KATA_HYPERVISOR="qemu"
export KATA_BUILD_CC="yes"
#export TEE_TYPE="tdx"
#export TEE_CONFIDENTIAL_GUEST="false"
#export KATA_BUILD_KERNEL_TYPE="tdx"
#export KATA_BUILD_QEMU_TYPE="tdx"
export KUBERNETES="yes"

export USE_DOCKER="true"
export CRIO="false"
export CRI_CONTAINERD="true"
export CRI_RUNTIME="containerd"
#export CI_JOB="CRI_CONTAINERD_K8S_MINIMAL"
export CCV0="yes"
export CI_JOB="METRICS"
export METRICS_CI="yes"

ci_dir_name=".ci"

export GOROOT="/usr/local/go"
export GOPATH=${WORKSPACE}/go
mkdir -p "${GOPATH}"

export PATH=${GOPATH}/bin:/usr/local/go/bin:/usr/sbin:/sbin:${PATH}

export GO111MODULE="auto"

kata_repo="github.com/kata-containers/kata-containers"
tests_repo="github.com/kata-containers/tests"

kata_repo_dir="${GOPATH}/src/${kata_repo}"
tests_repo_dir="${GOPATH}/src/${tests_repo}"

#Do not git clone tests from upstream repo
#[ -d "${tests_repo_dir}" ] || git clone "https://github.com/neofang7/tests.git" "${tests_repo_dir}"
#assume tests_repo has already cloned from neofang7/tests.git
[ -d "${kata_repo_dir}" ] || git clone -b CCv0 "https://${kata_repo}.git" "${kata_repo_dir}"
arch=$("${tests_repo_dir}/.ci/kata-arch.sh")

# container_id=$(docker ps| grep kata-registry | awk '{print $1}')
# if [ ! ${container_id} == "" ]; then
#         docker stop ${container_id}
#         docker rm ${container_id}
#         kubeadm reset -f --cri-socket /run/containerd/containerd.sock
# fi

# Get the repository of the PR to be tested
#mkdir -p $(dirname "${kata_repo_dir}")
#[ -d "${kata_repo_dir}" ] || git clone "https://${kata_repo}.git" "${kata_repo_dir}"

#Clean up the environment before running tests.
#tests_repo="${tests_repo}" "${tests_repo_dir}/.ci/clean_up.sh"

#install kata tools under ${kata_repo_dir}
pushd "${kata_repo_dir}"
"${GOPATH}/src/${tests_repo}/.ci/install_go.sh" -p -f
popd

# Resolve kata dependencies
"${GOPATH}/src/${tests_repo}/.ci/resolve-kata-dependencies.sh"

#skip static anlysis tools here.

pushd "${GOPATH}/src/${tests_repo}"
source ".ci/ci_job_flags.sh"
source "${cidir}/lib.sh"

echo "run setup.sh from $PWD"
".ci/setup.sh"

pushd ${tests_repo_dir}/cmd/checkmetrics/ci_worker/
cp checkmetrics-json-qemu-sv-c1-small-x86-01.toml checkmetrics-json-qemu-$(uname -n).toml
cp checkmetrics-json-cloud-hypervisor-sv-c1-small-x86-01.toml checkmetrics-json-cloud-hypervisor-$(uname -n).toml
popd

echo "Running the metrics tests:"
".ci/run.sh"

if [ ${TEE_CONFIDENTIAL_GUEST} == "false" ]
then
	mv metrics/results metrics/legacy-results
else
	mv metrics/results metrics/tdx-results
fi	

echo "TEE_CONFIDENTIAL_GUEST == ${TEE_CONFIDENTIAL_GUEST}"

sudo chown jenkins -R metrics/results

if [ ${TEE_CONFIDENTIAL_GUEST} == "false" ]
then
       mv metrics/results metrics/legacy-results
else
       mv metrics/results metrics/tdx-results
fi

mkdir -p metrics/results

sudo kubeadm reset -f --cri-socket /run/containerd/containerd.sock

echo "Test Completed."

popd
