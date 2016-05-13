#To run the UI after watching a movie, that is it displays the list of movies

username="alagu"
password="11111"
if [ ! -z "$1" ] ; then
    username=$1
fi
if [ ! -z "$2" ] ; then
    password=$2
fi

python ../../user_tk.py ../../development.ini $username $password
cd "../.."
