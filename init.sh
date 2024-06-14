sysctl -w net.core.rmem_default=262144
sysctl -w net.core.rmem_max=262144
sudo sysctl -w net.core.wmem_max=8388608
sudo sysctl -w net.core.wmem_default=8388608
sysctl -w net.core.netdev_max_backlog=2000

systemctl status chronyd
systemctl start chronyd
systemctl enable chronyd
chronyc tracking
chronyc makestep

chmod +x start.sh
