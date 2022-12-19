#!/bin/bash

#rootfs_image=/opt/confidential-containers.metrics/share/kata-containers/kata-ubuntu-latest.image
rootfs_image=$1
if [ ! -f ${rootfs_image} ]; then
    echo "${rootfs_image} not exists."
    exit 1
fi

cert_file=$2
if [ ! -f ${cert_file} ]; then
    echo "${cert_file} does not exist."
    exit 1
fi

mnt_dir=/mnt/kata_containers
mkdir -p ${mnt_dir}
start_sector=$(fdisk -l ${rootfs_image}|grep kata-ubuntu-latest.image1|awk '{print $3}')

losetup -f ${rootfs_image}
device=$(losetup -l | grep ${rootfs_image} | awk '{print $1}')
echo "mount -ooffset=$((512*${start_sector})) ${device} ${mnt_dir}"
mount -ooffset=$((512*${start_sector})) ${device} ${mnt_dir}

user=$(whoami)
chown ${user} ${mnt_dir}/etc/ssl/certs/ca-certificates.crt
lines=$(cat ${cert_file} | awk 'BEGIN{ RS = ""; FS = "\n" }{print $2}')
isexist=$(grep "${lines}" ${mnt_dir}/etc/ssl/certs/ca-certificates.crt)
if [ -z "${isexist}" ]; then
    echo "${isexist} Write certs into rootfs."
    cat ${cert_file} >> ${mnt_dir}/etc/ssl/certs/ca-certificates.crt
else
    echo "Certs exists in ${mnt_dir}/etc/ssl/certs/ca-certificates.crt"
fi

chown root ${mnt_dir}/etc/ssl/certs/ca-certificates.crt

umount ${mnt_dir}
echo "umount and detach.."
losetup -d ${device}
rm -rf ${mnt_dir}
