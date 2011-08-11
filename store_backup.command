# Backup of store disk
# store_0 contains an entire copy of the store disk
# synced each time this script is run.

echo Start: `date` > store_0_info
echo
time /usr/local/bin/rsync --rsync-path=/usr/local/bin/rsync -aWx --eahfs --showtogo --delete --delete-excluded --exclude "/Volumes/store/.Trash*" --exclude "/Volumes/store/.Spotlight*" --exclude "/Volumes/store/Torrents*" "/Volumes/store/" "/Volumes/LaptopBackup/store_0/" 2>> store_0_info
chmod -R u+rX store_0
echo
echo End: `date` >> store_0_info

