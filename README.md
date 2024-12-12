#Building an E-commerce Product Recommender System: A Step-by-Step Guide

This project involves creating a recommender system for an e-commerce platform. We will cover the entire pipeline—from data preprocessing and model development to deployment and monitoring—using tools like Docker, AWS Free Tier, and public datasets. This guide assumes you have a basic understanding of Python, machine learning, and AWS services.

##Table of Contents

	0. 	Installation Guide
	1.	Project Overview
	2.	Dataset Selection
	3.	Deployment via AWS
	4. 	Monitoring


Installation Guide
Download repo and install requirements.txt, then run 
```bash
python app.py
```
Example usage with RESTful api: 
http://localhost/recommend?product_id=B00YQ6X8EO&num_recommendations=5



Project Overview

We aim to build a product recommendation system that suggests products to users based on their interaction history and product descriptions. The project will demonstrate:
	•	NLP Model Development: Analyzing product descriptions using NLP techniques.
	•	Model Evaluation: Assessing the performance of our recommender system.
	•	Deployment and Serving: Deploying the model as a RESTful API.
	•	Docker and AWS Basics: Containerizing the application and deploying it on AWS.
	•	Model Monitoring: Tracking the performance and usage of the deployed model.

Dataset Selection

We will use the Amazon Product Data available publicly for research purposes.

Below is a more detailed, step-by-step guide to deploying your application on an AWS EC2 instance. This process assumes you have already created an AWS account that is eligible for the Free Tier. If you haven’t, make sure you’ve signed up and completed all the verification steps, including adding a payment method and confirming your email and phone number.

Step-by-Step Guide for Deployment Via EC2

1. Log In to the AWS Management Console
	1.	Go to the AWS Management Console.
	2.	Sign in using the email and password associated with your AWS account.

You should now see the AWS Management Console home page, which provides a search bar and a list of services.

2. Navigate to the EC2 Service
	1.	In the “Find Services” search bar at the top of the page, type EC2.
	2.	Click on EC2 under the “Services” dropdown.

This will take you to the EC2 Dashboard, where you can manage virtual servers, also called instances.

3. Launch a New EC2 Instance
	1.	On the EC2 Dashboard, click on the “Launch instances” button.
Alternatively, you can go to the left-hand navigation menu and click on “Instances,” then “Launch instances.”
	2.	You’ll be taken to a “Launch an instance” page. Here, you need to configure the details of your virtual machine.

4. Choose an Amazon Machine Image (AMI)
	1.	Under the “Name and tags” section, give your instance a name, like recommender-system.
	2.	Scroll down to the “Application and OS Images (Amazon Machine Image)” section.
	3.	For a Free Tier-eligible machine, select an official Linux distribution:
	•	Amazon Linux 2 AMI (Free Tier eligible)
or
	•	Ubuntu Server 20.04 LTS (Free Tier eligible)

For simplicity, let’s choose Amazon Linux 2 AMI.

5. Choose an Instance Type
	1.	Under the “Instance type” section, pick t2.micro (Free Tier eligible).
	•	t2.micro comes with 1 vCPU and 1 GiB RAM, which is enough for small experiments.

6. Configure Key Pair (Login Credentials)
	1.	Under “Key pair (login)” select Create a new key pair if you don’t have one already.
	2.	Give the key pair a name, for example my-ec2-keypair.
	3.	Choose the key pair type (RSA) and file format (.pem for Linux/macOS or .ppk for Windows with PuTTY).
	4.	Click Create key pair. This will download a file to your local machine.

Keep this key file safe. You will need it to SSH into your instance.

7. Network Settings
	1.	Under “Network settings,” leave the defaults as is for now.
	2.	Security group rules: A default security group will be created allowing SSH (port 22) access.
If you plan to run a web server (such as the Flask app from our earlier discussion), you should also add a rule to allow inbound HTTP (port 80) traffic:
	•	Click “Edit” under the security group settings.
	•	Add a rule:
Type: HTTP
Source: Anywhere (0.0.0.0/0)
This allows external clients to access your API once it’s deployed.

8. Configure Storage
	1.	By default, the instance will come with an 8 GB EBS volume. This should be sufficient for starting out. You can leave the defaults.

9. Review and Launch
	1.	Review all the settings you selected.
	2.	Click Launch instance at the bottom-right corner of the page.
	3.	AWS will now provision your instance. This usually takes a couple of minutes.

10. View Your Running EC2 Instance
	1.	Click on “View all instances” after launching.
	2.	You will see your new instance in a “pending” state. Wait until the “Instance state” shows running and the “Status checks” shows 2/2 checks passed.

Once the instance is running, you have a virtual machine (VM) in the cloud that you can remotely connect to and set up your recommender system application.

Connecting to Your EC2 Instance

1. Locate Your Instance’s Public DNS or IP
	1.	In the EC2 Console, click on Instances in the left navigation panel.
	2.	Select the instance you just launched.
	3.	In the “Description” tab at the bottom, look for the Public IPv4 address or Public IPv4 DNS. This is what you’ll use to connect to your instance.

2. SSH into Your EC2 Instance (Linux/Mac)
	1.	Open a terminal on your local machine.
	2.	Navigate to the directory where your downloaded .pem key is located.
	3.	Change the permissions of the key file to be more secure:

chmod 400 my-ec2-keypair.pem


	4.	Connect to the instance:

ssh -i "my-ec2-keypair.pem" ec2-user@<your-instance-public-dns>

Replace <your-instance-public-dns> with the value from the EC2 console (something like ec2-3-122-50-33.compute-1.amazonaws.com).

For Ubuntu instances, the default user is ubuntu instead of ec2-user:

ssh -i "my-ec2-keypair.pem" ubuntu@<your-instance-public-dns>

3. SSH into Your EC2 Instance (Windows)
	•	If you’re using Windows, you can use PuTTY or Windows Subsystem for Linux (WSL).
	•	For PuTTY:
	1.	Convert .pem to .ppk using PuTTYgen.
	2.	Open PuTTY, enter <your-instance-public-dns> in the Host Name field.
	3.	Under SSH > Auth in the sidebar, browse to your .ppk file.
	4.	Click Open to connect.

Setting Up Your Environment on EC2

Once logged in, you can:
	1.	Update the instance:

sudo yum update -y

(If using Amazon Linux; if Ubuntu, use sudo apt update && sudo apt upgrade -y)

	2.	Install Docker if needed:

sudo amazon-linux-extras install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
# Log out and back in for this to take effect


	3.	Clone your repository or upload files:

git clone https://github.com/yourusername/recommender-system.git


	4.	Build and run your Docker container:

cd recommender-system
docker build -t recommender-system .
docker run -d -p 80:80 recommender-system



Your Flask app (if it listens on port 80) is now accessible via http://<your-instance-public-dns>/recommend.

Testing Your Deployed Application
	1.	In your local web browser, go to:

http://<your-instance-public-dns>/recommend?product_id=B001E4KFG0&num_recommendations=5

If everything is set up correctly, you should receive a JSON response with the recommended products.

Additional Tips
	•	Security: Avoid opening SSH from anywhere (0.0.0.0/0) in production. Restrict to your IP for better security.
	•	Costs: EC2 Free Tier is free for 750 hours per month of t2.micro usage, but watch out for other services you enable that might incur costs.
	•	Scaling: If you need more resources later, you can stop your instance and change its type to a larger one (not free tier).
	•	Stopping the Instance: When not in use, you can stop the instance to avoid charges for associated services like EBS storage (although EBS under free tier might be partially covered).

Conclusion

Launching an EC2 instance on AWS involves logging into the AWS Management Console, navigating to EC2, configuring an instance with a Free Tier eligible AMI and instance type, setting up security groups, and then launching it. With these steps, you can access the instance via SSH, set up your application, and run it live on the internet. As you grow more comfortable with the AWS environment, you can explore more advanced features such as load balancing, auto-scaling, and continuous deployment pipelines.