#!/usr/bin/env bash

VMNAME='VNF1'
CPUS=4
RAM=8192
FILENAME='<baseISOfile>'
FILENAME2='<secondary mounted disk name>'
CONFIGDRV='configDrive.iso'
URL='<base location on disk>'
VMPATH='/run/media/sdb1' #vmstorage area
WGET_OPTS='--no-check-certificate'


if ! cd "$VMPATH"; then
  echo "ERROR: can't access working directory (VMPATH)" >&2
  exit 1
fi

if ! wget "$WGET_OPTS" "$URL"/"$FILENAME"; then
  echo "ERROR: can't get $FILENAME" >&2
  echo "wget "$WGET_OPTS" "$URL"/"$FILENAME""
  exit 1
fi

## Demo Layout
virt-install \
   --virt-type kvm \
   --name $VMNAME \
   --ram $RAM --vcpus $CPUS \
   --cpu host-passthrough \
   --os-type linux --os-variant ubuntu21.10 \
   --cdrom $CONFIGDRV \
   --network bridge=br3,model=virtio \
   --network bridge=br0,model=virtio \
   --network bridge=br1,model=virtio \
   --network bridge=br2,model=virtio \
   --disk path="$VMPATH"/"$FILENAME" \
   --disk path="$VMPATH"/"$FILENAME2",device=disk,bus=scsi,size=64 \
   --graphics vnc,listen=0.0.0.0 --noautoconsole \
   --noreboot \
   --import \
   --check-cpu

## Full Prod Layout
#virt-install \
#   --virt-type kvm \
#   --name $VMNAME \
#   --ram $RAM --vcpus $CPUS \
#   --cpu host-passthrough \
#   --os-type linux --os-variant ubuntu20.04 \
#   --network bridge=br0,model=e1000 \
#   --network bridge=br1,model=virtio \
#   --network bridge=br2,model=virtio \
#   --network bridge=br3,model=virtio \
#   --network bridge=lanbrd,model=virtio \
#   --disk path="$VMPATH"/"$FILENAME" \
#   --graphics vnc,listen=0.0.0.0 --noautoconsole \
#   --import \
#   --autostart --check-cpu