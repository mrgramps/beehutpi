#! /bin/bash

dbox_dir=/home/pi/dboxshare
uploader_script=/home/pi/dboxshare/Dropbox-Uploader/dropbox_uploader.sh
dbox_conf=/home/pi/beehutpi/dboxsync.conf

var=$( cat $dbox_conf )

if [ $var == "enable" ]
then
  cd ${dbox_dir}
  last_file=$(ls -t *.avi | head -n 1 | xargs -I out echo out)
  bash ${uploader_script} upload ${dbox_dir}/${last_file} ${last_file}
  echo "Uploaded" ${last_file} "on" $(date) >> ${dbox_dir}/dboxsync.log
fi
