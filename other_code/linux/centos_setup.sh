# This program was never finished


sudo yum update && yum upgrade
sudo dnf update && dnf upgrade
yum group -y install Server 'Security Tools' 'Graphical Administration Tools' 'Headless Management'
yum group -y install 'Mail Server' 'Basic Web Server' 'Performance Tools' 'Remote Management for linux' 'setools-console'
yum -y install git
sudo dnf -y install https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm
dnf -qy module disable postgresql
dnf -y install postgresql12
dnf -y install postgresql12-server
/usr/pgsql-12/bin/postgresql-12-setup initdb
sudo firewall-cmd --zone=public --permanent --add-service=postgresql
sudo firewall-cmd --zone=public --permanent --add-port=5432/tcp
systemctl enable postgresql-12
systemctl start postgresql-12
# Needs to add PSQL commands for scram-sha-256

sudo yum -y install vsftpd
echo 'y'
sudo systemctl start vsftpd
sudo systemctl enable vsftpd
sudo firewall-cmd --zone=public --permanent --add-port=21/tcp
sudo firewall-cmd --reload
sudo cp /etc/vsftpd/vsftpd.conf /etc/vsftpd/vsftpd.conf.default
sudo adduser magnusyep
sudo passwd magnusyep
cat << 'EOL' > /etc/vsftpd/vsftpd.conf
pam_service_name=vsftpd
userlist_enable=YES
userlist_file=/etc/vsftpd/user_list
userlist_deny=NO
EOL
rm -rf
cat << 'EOL' > /etc/vsftpd/ftpusers
bin
daemon
adm
lp
sync
shutdown
halt
mail
news
uucp
operator
games
nobody
EOL
rm -rf /etc/vsftpd/user_list
cat << 'EOL' > /etc/vsftpd/user_list
root
android
lilleslott
EOL
yum -y install cockpit*
systemctl enable --now cockpit.socket
sudo firewall-cmd --zone=public --permanent --add-port=80/tcp
sudo firewall-cmd --zone=public --permanent --add-service=http
sudo firewall-cmd --zone=public --permanent --add-port=443/tcp
sudo firewall-cmd --zone=public --permanent --add-service=https
sudo firewall-cmd --zone=public --permanent --add-service=ssh
