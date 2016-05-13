#To pop up the VLC media player

video_name="none"
folder_name="none"
if [ ! -z "$1" ] ; then
    video_name=$1
fi
if [ ! -z "$2" ] ; then
    folder_name=$2
fi
cp "vlctk.py" "$folder_name"
cp "vlc.py" "$folder_name"
cp "pic.jpg" "$folder_name"
cd "$folder_name"

python vlctk.py "$video_name"
