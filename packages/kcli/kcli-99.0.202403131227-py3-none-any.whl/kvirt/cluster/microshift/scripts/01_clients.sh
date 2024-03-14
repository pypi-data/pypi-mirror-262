#!/usr/bin/env bash

MAJOR={{ 8 if 'rhel8' in image else 9 }}
{% set tag_str = tag|string %}

TAG={{ tag }}
subscription-manager repos --enable rhocp-$TAG-for-rhel-$MAJOR-$(uname -i)-rpms --enable fast-datapath-for-rhel-$MAJOR-$(uname -i)-rpms
dnf -y install openshift-clients lvm2 podman

test -f /root/auth.json && podman login registry.redhat.io --authfile /root/auth.json

DEVICE=/dev/$(lsblk -o name | tail -1)
pvcreate $DEVICE
vgcreate rhel $DEVICE
