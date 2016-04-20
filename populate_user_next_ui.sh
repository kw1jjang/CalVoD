username="alagu"
password="11111"
if [ ! -z "$1" ] ; then
    username=$1
fi
if [ ! -z "$2" ] ; then
    password=$2
fi








python ../../user_gui_tk.py ../../development.ini $username $password
cd "../.."
