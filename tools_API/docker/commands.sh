# Install Docker on AWS linux AMI
yum update -y
amazon-linux-extras install docker -y
service docker start
usermod -a -G docker ec2-user

# Install Swarm Manager
docker swarm init --advertise-addr IP_MANAGER_ADDRESS
# TCP 2377 for cluster management communications
# TCP and UDP port 7946 for communication among nodes
# UDP port 4789 for overlay network traffic

# Get Swarm Manager Token
docker swarm join-token worker
