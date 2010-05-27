# Backup of sys disk
# sys_0 always contains an entire copy of the sys disk
# synced each time this script is run.

echo Start: `date` > sys_0_info
echo
time /usr/local/bin/rsync --rsync-path=/usr/local/bin/rsync -aWx --eahfs --showtogo --delete --delete-excluded --exclude "*/tmp/*" --exclude "*/var/vm/*" --exclude "/Volumes/sys/.Trash*" --exclude "/Volumes/sys/.Spotlight*" "/Volumes/sys/" "/Volumes/LaptopBackup/sys_0/" 2>> sys_0_info
chmod -R u+rX sys_0
echo
echo End: `date` >> sys_0_info
