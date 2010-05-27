# Backup of scratch disk
# scratch_0 contains an entire copy of the scratch disk
# synced each time this script is run.

echo Start: `date` > scratch_0_info
echo
time /usr/local/bin/rsync --rsync-path=/usr/local/bin/rsync -aWx --eahfs --showtogo --delete --delete-excluded --exclude "/Volumes/scratch/.Trash*" --exclude "/Volumes/scratch/.Spotlight*" --exclude "/Volumes/scratch/Torrents*" "/Volumes/scratch/" "/Volumes/LaptopBackup/scratch_0/" 2>> scratch_0_info
chmod -R u+rX scratch_0
echo
echo End: `date` >> scratch_0_info

