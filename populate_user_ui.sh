username="alagu"
password="11111"
if [ ! -z "$1" ] ; then
    username=$1
fi
if [ ! -z "$2" ] ; then
    password=$2
fi

./kill_users.sh
mkdir -p users
rm -rf users/user001
#rm -rf users/.user001
cp "black.jpg" "users"
cp "pic.jpg" "users"
cp "vlctk.py" "users"
cp "vlc.py" "users"
cp "play_vlc.sh" "users"
cp "user_data_display.sh" "users"
cp "populate_user_next_ui.sh" "users"
cd "users"
mkdir -p user001
cp "black.jpg" "user001"
cp "pic.jpg" "user001"
cp "vlctk.py" "user001"
cp "vlc.py" "user001"
cp "play_vlc.sh" "user001"
cp "user_data_display.sh" "user001"
cp "populate_user_next_ui.sh" "user001"
cd "user001"
# mkdir -p .user001
# cd ".user001"
rm -rf video*
python ../../user_gui_tk.py ../../development.ini $username $password
cd "../.."
