#!/usr/bin/env bash

# CAUCTION! THIS SCRIPT IS SET UP TO WIPE /dev/sda BEFORE EXECUTION.

# Loads Norwegian keyboard
loadkeys no-latin1

# Sets timeserver
timedatectl set-ntp true

# Enables pacman
pacman -Sy

# Make desired disk gpt format
parted /dev/sda -s mklabel gpt

# Create partitions
(
# Create EFI partition
echo n
echo
echo
echo +1G
echo t
echo 1

# Create boot partition
echo n
echo
echo
echo +1G
echo t
echo
echo 4

# Create LVM partition for remaining disk
echo n
echo
echo
echo
echo t
echo
echo 30

# Save partition
echo w
) | fdisk /dev/sda

# create LVM partitions
pvcreate /dev/sda3
vgcreate archlinux /dev/sda3
lvcreate -L 10G -n swap archlinux
lvcreate -L 30G -n root archlinux
lvcreate -l +100%FREE -n data archlinux

# Formatting disks
mkfs.ext4 /dev/archlinux/root
mkfs.ext4 /dev/archlinux/data
mkfs.fat -F 32 /dev/sda1
mkfs.ext2 /dev/sda2

# enable swap
mkswap /dev/archlinux/swap
swapon /dev/archlinux/swap

# Mount root
mount /dev/archlinux/root /mnt

# Create mountpoints
mkdir /mnt/home
mkdir /mnt/boot
mkdir /mnt/efi

# Mount disks
mount /dev/archlinux/data /mnt/home
mount /dev/sda1 /mnt/efi
mount /dev/sda2 /mnt/boot

# Install dependencies
pacstrap /mnt base linux linux-firmware lvm2 dhcpcd grub efibootmgr intel-ucode amd-ucode

# Generate fstab
genfstab -U /mnt >> /mnt/etc/fstab

# Creating script to be run inside arch-chroot
touch /mnt/root/part2.sh && chmod +x /mnt/root/part2.sh
cat << 'EOF' > /mnt/root/part2.sh
# Adding lvm to /etc/mkinitcpio.conf
sed '52 c\HOOKS=(base udev autodetect modconf block lvm2 filesystems keyboard fsck)' /etc/mkinitcpio.conf >> output.txt
mv output.txt /etc/mkinitcpio.conf
# Setting timezone
ln -sf /usr/share/zoneinfo/Europe/Oslo /etc/localtime
hwclock --systohc
# Generate and set locales
locale-gen
touch /etc/locale.conf
echo LANG=en_US.UTF-8 >> /etc/locale.conf
touch /etc/vconsole.conf
echo KEYMAP=no-latin1 >> /etc/vconsole.conf
touch /etc/hostname
echo archlinux >> /etc/hostname
echo '127.0.0.1 localhost' >> /etc/hosts
echo '::1       localhost' >> /etc/hosts
echo '127.0.1.1 archlinux.localdomain   archlinux' >> /etc/hosts
mkinitcpio -P
# Set root password
(
echo toor
echo toor
) | passwd
# Microcode settings
CONFIG_BLK_DEV_INITRD=Y
CONFIG_MICROCODE=y
CONFIG_MICROCODE_INTEL=Y
CONFIG_MICROCODE_AMD=y
# Install Grub
grub-install --target=x86_64-efi --efi-directory=efi --bootloader-id=GRUB --removable
sed '3 i\GRUB_PRELOAD_MODULES="lvm"' /etc/default/grub >> output.txt
mv output.txt /etc/default/grub
touch /boot/grub/grub.cfg
grub-mkconfig -o /boot/grub/grub.cfg
EOF

# Run script inside arch-chroot
arch-chroot /mnt /root/./part2.sh

# Remove script after finished
arch-chroot /mnt rm -rf /root/part2.sh

# Unmount disks
umount -R /mnt
poweroff
