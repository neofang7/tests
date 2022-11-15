#!/bin/bash
# This file is only to simplify integration/kubernetes/init.sh
# to setup k8s environment.

#set -o errexit
set -o nounset
#set -o pipefail

SCRIPT_PATH=$(dirname "$(readlink -f "$0")")

source "lib/common.bash"
source "/etc/os-release" || source "/usr/lib/os-release"

# Running on baremetal.
# TODO: CI setting?
CI=${CI:-""}

untaint_k8s_node() {
	local node_name="$(hostname | awk '{print tolower($0)}')"
	info "Untaint the node so pods can be scheduled. ${node_name}"
	#kubectl taint nodes "${node_name}" node-role.kubernetes.io/master-
	kubectl taint nodes "${node_name}" node-role.kubernetes.io/control-plane-
}

wait_k8s_pods_ready() {
	# Master components provide the cluster’s control plane, including kube-apisever,
	# etcd, kube-scheduler, kube-controller-manager, etc.
	# We need to ensure their readiness before we run any container tests.
	local pods_status="kubectl get pods --all-namespaces"
	local apiserver_pod="kube-apiserver"
	local controller_pod="kube-controller-manager"
	local etcd_pod="etcd"
	local scheduler_pod="kube-scheduler"
	local dns_pod="coredns"
	local system_pod=($apiserver_pod $controller_pod $etcd_pod $scheduler_pod $dns_pod)

	local system_pod_wait_time=120
	local sleep_time=5
	local running_pattern=""
	for pod_entry in "${system_pod[@]}"; do
		running_pattern="${pod_entry}.*1/1.*Running"
		if ! waitForProcess "$system_pod_wait_time" "$sleep_time" \
			"$pods_status | grep "${running_pattern}""; then
			info "Some expected Pods aren't running after ${system_pod_wait_time} seconds." 1>&2
			${pods_status} 1>&2
			# Print debug information for the problematic pods.
			for pod in $(kubectl get pods --all-namespaces \
				-o jsonpath='{.items[*].metadata.name}'); do
				if [[ "$pod" =~ ${pod_entry} ]]; then
					echo "[DEBUG] Pod ${pod}:" 1>&2
					kubectl describe -n kube-system \
						pod $pod 1>&2 || true
				fi
			done
			die "Kubernetes is not fully ready. Bailing out..."
		fi
	done
}

wait_operator_pod_ready() {
	operator_pod=$1
	count=$2
	local pods_status="kubectl get pods -n confidential-containers-system"
	local system_pod_wait_time=120
	local sleep_time=10

	running_pattern="${operator_pod}*.*${count}/${count}.*Running"
	if ! waitForProcess "$system_pod_wait_time" "$sleep_time" \
		"$pods_status | grep "${running_pattern}""; then
		info "Some expected Pods ${operator_pod} aren't running after ${system_pod_wait_time} seconds." 1>&2
		${pods_status} 1>&2
		# Print debug information for the problematic pods.
		for pod in $(kubectl get pods -n confidential-containers-system \
			-o jsonpath='{.items[*].metadata.name}'); do
			if [[ "$pod" =~ ${operator_pod} ]]; then
				echo "[DEBUG] Pod ${pod}:" 1>&2
				kubectl describe -n confidential-containers-system \
					pod $pod 1>&2 || true
			fi
		done
		die "Operator pod is not ready . Bailing out..."
	fi
	info "Operator pod is ready."
}

# Normally, we do not cleanup kubeadm and cni.
# Delete the CNI configuration files and delete the interface.
# That's needed because `kubeadm reset` (ran on clean up) won't clean up the
# CNI configuration and we must ensure a fresh environment before starting
# Kubernetes.
cleanup_k8s_cni_configuration() {
	# Remove existing CNI configurations:
	local cni_config_dir="/etc/cni"
	local cni_interface="cni0"
	sudo rm -rf /var/lib/cni/networks/*
	sudo rm -rf "${cni_config_dir}"/*
	if ip a show "$cni_interface"; then
		sudo ip link set dev "$cni_interface" down
		sudo ip link del "$cni_interface"
	fi
}

wait_coredns_pod_ready() {
	local pods_status="kubectl get pods --all-namespaces"
	local coredns_pod="kube-flannel-ds"
	local system_pod_wait_time=60
	local sleep_time=5

	running_pattern="${coredns_pod}*.*1/1.*Running"
	if ! waitForProcess "$system_pod_wait_time" "$sleep_time" \
		"$pods_status | grep "${running_pattern}""; then
		info "Some expected Pods aren't running after ${system_pod_wait_time} seconds." 1>&2
		${pods_status} 1>&2
		# Print debug information for the problematic pods.
		for pod in $(kubectl get pods --all-namespaces \
			-o jsonpath='{.items[*].metadata.name}'); do
			if [[ "$pod" =~ ${coredns_pod} ]]; then
				echo "[DEBUG] Pod ${pod}:" 1>&2
				kubectl describe --all-namespaces \
					pod $pod 1>&2 || true
			fi
		done
		die "Coredns is not fully ready. Bailing out..."
	fi
	info "Flannel core dns ready."
}

# Configure network: Use flannel by default.
configure_k8s_network() {
	local network_plugin_config="https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml"
	kubectl apply -f ${network_plugin_config}
	#check network configuration
	wait_coredns_pod_ready
}

# Stop Kubernetes
stop_metrics_kubernetes() {
	local cri_socket_path="$1"
	info "Clean kubernetes since testing is completed."
	kubeadm init --cri-socket "${cri_socket_path}"
}

# Start Kubernetes
start_metrics_kubernetes() {
	local cri_socket_path="$1"
	local cgroup_driver="$2"
	local kubelet_wait="240"
	local kubelet_sleep="10"

	info "Init cluster using ${cri_socket_path}"

	# # This should be global otherwise the clean up fails.
	# kubeadm_config_file="$(mktemp --tmpdir kubeadm_config.XXXXXX.yaml)"
	# trap 'sudo -E sh -c "rm -r "${kubeadm_config_file}""' EXIT

	# sed -e "s|CRI_RUNTIME_SOCKET|${cri_socket_path}|" "${kubeadm_config_template}" > "${kubeadm_config_file}"
	# sed -i "s|CGROUP_DRIVER|${cgroup_driver}|" "${kubeadm_config_file}"

	if [ "${CI}" == true ] && [[ $(wc -l /proc/swaps | awk '{print $1}') -gt 1 ]]; then
		grep -q zram /proc/swaps && echo "# zram swap disabled" | sudo tee /etc/systemd/zram-generator.conf
		sudo swapoff -a || true
	fi

	# sudo -E kubeadm init --config "${kubeadm_config_file}"
	kubeadm init --cri-socket "${cri_socket_path}" --pod-network-cidr=10.244.0.0/16
	mkdir -p "$HOME/.kube"
	sudo cp "/etc/kubernetes/admin.conf" "$HOME/.kube/config"
	sudo chown $(id -u):$(id -g) "$HOME/.kube/config"
	export KUBECONFIG="$HOME/.kube/config"

	info "Probing kubelet (timeout=${kubelet_wait}s)"
	waitForProcess "$kubelet_wait" "$kubelet_sleep" \
		"kubectl get nodes"
}

install_operator() {
	kubectl apply -f operator/deploy.yaml
	wait_operator_pod_ready "cc-operator-controller-manager" 2
	kubectl apply -f https://raw.githubusercontent.com/confidential-containers/operator/v0.1.0/config/samples/ccruntime.yaml
	wait_operator_pod_ready "cc-operator-daemon-install" 1
}

main() {
	local cri_runtime_socket="/run/containerd/containerd.sock"
	local cgroup_driver="cgroupfs"

	info "Check there aren't dangling processes from previous tests"
	installed=$(ps aux | grep 'kubelet' | grep -v grep)
	info "check k8s installation"
	if [ -z "${installed}" ]; then
		#check_processes
		info "Start kubernets"
		start_metrics_kubernetes "${cri_runtime_socket}" "${cgroup_driver}"
		info "Configure the cluster network"
		configure_k8s_network
		info "Wait for system's pods be ready and running"
		wait_k8s_pods_ready
		untaint_k8s_node
	else
		info "K8S has already installed."
	fi

	info "Install CCRuntime operator"
	if eval kubectl get runtimeclass | grep kata; then
		info "CCRuntime operator already installed."
	else
		local node_name="$(hostname | awk '{print tolower($0)}')"
		kubectl label node "${node_name}" node-role.kubernetes.io/worker=
		install_operator
	fi
}

main "$@"
#install_operator
