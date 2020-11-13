
import subprocess as sp
import json
import os
import getpass
import time

def prRed(skk): print("\033[91m {}\033[00m" .format(skk)) 
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk)) 
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk)) 
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk)) 
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk),end=" ") 
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk)) 
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk)) 
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))

def hadoopf(op1,ip,key,un):
    ssh = "ssh -l {0} {1} -i {2} sudo ".format(un,ip,key)
    while(op1!="7"):
        if op1=="0":
            prCyan("""\nWhat you want to do in hadoop
[To enter multiple option seprate it with ","]\n
        1. Install hadoop software\n
        2. Configure named node\n
        3. Configure data node\n
        4. Start named node\n
        5. Start data node\n
        6. Check dfsadmin report\n
        7. Exit hadoop menu\n""")
            op1=input("enter ur option: ")
        if op1=="7":
            prLightGray("Quiting HADOOP MENU....")
        else:
            if ("2" in op1)or("3" in op1)or("4" in op1)or("5" in op1)or("6" in op1)or("1" in op1):
                output = sp.getstatusoutput(ssh+"hadoop version")
                if (output[0]!=0) and not("1" in op1):
                    prRed(">>>>>>>Hadoop is not installed in this OS<<<<<<<<")
                    op1="0"
                elif (output[0]==0) and ("1" in op1):
                    prYellow(">>>>>>>HADOOP IS ALREADY INSTALLED<<<<<<<")
                    op1="0"
            if "1" in op1:
                prLightPurple(">>>>>>>>INSTALLING HADOOP PLEASE WAIT.....")
                output = sp.getstatusoutput(ssh+"yum install wget -y")
                output = sp.getstatusoutput(ssh+"wget http://35.244.242.82/yum/java/el7/x86_64/jdk-8u171-linux-x64.rpm")
                output = sp.getstatusoutput(ssh+"rpm -i jdk-8u171-linux-x64.rpm")
                print(output)
                output = sp.getstatusoutput(ssh+"wget https://archive.apache.org/dist/hadoop/core/hadoop-1.2.1/hadoop-1.2.1-1.x86_64.rpm")
                output = sp.getstatusoutput(ssh+"rpm -i hadoop-1.2.1-1.x86_64.rpm --force")
                print(output)
                output = sp.getstatusoutput(ssh+"echo 3 > /proc/sys/vm/drop-caches")
                prGreen(">>>>>>>>>HADOOP SOFTWARE IS SUCESSFULLY INSTALLED<<<<<<<<<<<<<")
            if ("2" in op1)or("3" in op1)or("4" in op1)or("5" in op1)or("6" in op1):
                output = sp.getstatusoutput(ssh+"hadoop version")
                if output[0]!=0:
                    prRed(">>>>>>>Hadoop is not installed in this OS<<<<<<<<")
                    op1="0"
            if ("2" in op1)or("3" in op1)or("4" in op1)or("5" in op1):
                output = sp.getstatusoutput(ssh+"jps")
                if "NameNode" in output[1]:
                    prYellow(">>>>>>>>>>Namenode is already running....<<<<<<")
                    op1="0"
                if "DataNode" in output[1]:
                    prYellow(">>>>>>>>>>Datanode is already running....<<<<<<")
                    op1="0"
            if ("2" in op1) and not("3" in op1):
                prLightPurple(">>>>>>>>>Coniguring named node.....")
                output = sp.getstatusoutput(ssh+"mkdir /nn")
                output = sp.getstatusoutput("scp -i {0} hadoopfiles/name-hdfs.xml {1}@{2}:/home/{1}/hdfs-site.xml".format(key,un,ip))
                output = sp.getstatusoutput(ssh+"cp hdfs-site.xml /etc/hadoop/hdfs-site.xml")
                output = sp.getstatusoutput("scp -i {0} hadoopfiles/name-core.xml {1}@{2}:/home/{1}/core-site.xml".format(key,un,ip))
                output = sp.getstatusoutput(ssh+"cp core-site.xml /etc/hadoop/core-site.xml")
                op2 = input("hdfs-site and core-file configured sucesfully with /nn as named node directory do you want to format /nn. y/n?")
                if op2=="y":
                    output = sp.getstatusoutput(ssh+"hadoop namenode -format -force")
                prGreen(">>>>>>>>NAMED NODE IS NOW CONFIGURED READY TO START<<<<<<<<")
            if ("3" in op1) and not("2" in op1):
                prLightPurple(">>>>>>>>Coniguring data node.....")
                output = sp.getstatusoutput(ssh+"mkdir /dn")
                output = sp.getstatusoutput("scp -i {0} hadoopfiles/data-hdfs.xml {1}@{2}:/home/{1}/hdfs-site.xml".format(key,un,ip))
                output = sp.getstatusoutput(ssh+"cp hdfs-site.xml /etc/hadoop/hdfs-site.xml")
                name_ip = input("Enter your namednode IP: ")
                output = sp.getstatusoutput("rm hadoopfiles/data-core.xml")
                output = sp.getstatusoutput("touch hadoopfiles/data-core.xml")
                f = open("hadoopfiles/data-core.xml","a")
                f.write("""<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{0}:9001</value>
</property>
</configuration>""".format(name_ip))
                f.close()
                output = sp.getstatusoutput("scp -i {0} hadoopfiles/data-core.xml {1}@{2}:/home/{1}/core-site.xml".format(key,un,ip))
                output = sp.getstatusoutput(ssh+"cp core-site.xml /etc/hadoop/core-site.xml")
                prGreen(">>>>>>>>>>HADOOP DATA NODE IS CONFIGURED AND READY TO START<<<<<<<<<<")
            if ("4" in op1) and not("5" in op1):
                prLightPurple(">>>>>>>STARTING NAME NODE.....")
                output = sp.getstatusoutput(ssh+"hadoop-daemon.sh start namenode")
                if output[0]==0:
                    output = sp.getstatusoutput(ssh+"jps")
                    if "NameNode" in output[1]:
                        prGreen(">>>>>>>>NAME NODE IS SUCESSFULLY STARTED<<<<<<<<<")
                    else:
                        prRed(">>>>>>>>NAME NODE COULD NOT START<<<<<<<<")
                else:
                    prRed(">>>>>>>>NAME NODE COULD NOT START<<<<<<<<")
            if ("5" in op1) and not("4" in op1):
                prLightPurple(">>>>>>>STARTING DATA NODE.....")
                output = sp.getstatusoutput(ssh+"hadoop-daemon.sh start datanode")
                if output[0]==0:
                    output = sp.getstatusoutput(ssh+"jps")
                    if "DataNode" in output[1]:
                        prGreen(">>>>>>>>DATA NODE IS SUCESSFULLY STARTED<<<<<<<<<")
                    else:
                        prRed(">>>>>>>>DATA NODE COULD NOT START<<<<<<<<")
                else:
                    prRed(">>>>>>>>DATA NODE COULD NOT START<<<<<<<<")
            if "6" in op1:
                prLightPurple(">>>>>PRINTING HADOOP REPORT.......")
                output = sp.getstatusoutput(ssh+"hadoop dfsadmin -report")
                prLightGray(output[1])
            op1="0"

def awsf():
    prLightPurple("NOTE:IT IS ASSUMED THAT AWS CLI IS ALREADY CONFIGURED\n")
    prCyan("""What you want to do in AWS?
[To enter multiple option seprate it with ","]

        1. Create keypair.\n
        2. Create Security group\n
        3. Launch an EC2 instance.\n
        4. Create EBS volume.\n
        5. Attach EBS volume to EC2 instance.\n
        6. Install webserver on EC2 instance.\n
        7. Create Partition and mount it.\n
        8. Create S3 bucket\n
        9. Upload files in S3 bucket\n
        10. Reset this MENU\n
        11. EXIT AWS MENU\n""")

    op1 = input("Enter your option: ")
    kn = None
    nd = None
    sg_name = None
    ec2_az = None
    ec2_id = None
    ebs_id = None
    sg_name = None
    st1 = 0
    st2 = 0
    st3 = 0
    st4 = 0
    st5 = 0
    st6 = 0
    st7 = 0
    while(op1!="11"):
        if op1=="0":
            prCyan("""What you want to do in AWS?
[To enter multiple option seprate it with ","]\n""")
            if st1==1:
                prYellow("       1. Create keypair.✅\n")
            else:
                prCyan("       1. Create keypair.\n")
            if st2==1:
                prYellow("       2. Create Security group.✅\n")
            else:
                prCyan("       2. Create Security group.\n")
            if st3==1:
                prYellow("       3. Launch an EC2 instance.✅\n")
            else:
                prCyan("       3. Launch an EC2 instance.\n")
            if st4==1:
                prYellow("       4. Create EBS volume.✅\n")
            else:
                prCyan("       4. Create EBS volume.\n")
            if st5==1:
                prYellow("       5. Attach EBS volume to EC2 instance.✅\n")
            else:
                prCyan("       5. Attach EBS volume to EC2 instance.\n")
        
            prCyan("""       6. Install webserver on EC2 instance.\n
        7. Create Partition and mount it.\n
        8. Create S3 Bucket\n
        9. Upload files in S3 Bucket\n
        10. RESET THIS MENU\n
        11. EXIT AWS MENU\n""")
            op1 = input("Enter your option: ")

        if op1=="11":
            prLightGray("Quiting AWS MENU....")
        else:
            if op1=="10":
                os.system("clear")
                prYellow("\n>>>>>>>>>>>>> AWS MENU IS NOW RESET <<<<<<<<<<<<<<<<<\n")
                st1 = 0
                st2 = 0
                st3 = 0
                st4 = 0
                st5 = 0
                st6 = 0
                st7 = 0
                nd = None
                kn = None
                sg_name = None
                ec2_az = None
                ec2_id = None
                ebs_id = None
                sg_name = None
                op1 = "0"
            if ("1" in op1) and (st1!=1):
                kn = input("ENTER KEYPAIR NAME: ")
                output = sp.getstatusoutput("aws ec2 create-key-pair --key-name {0}".format(kn))
                if output[0]==0:
                    outpout = sp.getstatusoutput("touch awsfiles/{0}.pem".format(kn))
                    key_op = json.loads(output[1])
                    f = open("awsfiles/{0}.pem".format(kn),"a")
                    f.write(key_op["KeyMaterial"])
                    f.close()
                    outpout = sp.getstatusoutput("chmod 400 awsfiles/{0}.pem".format(kn)) 
                    st1=1
                    prGreen(">>>>>>>>>KEY PAIR NAMED *{0}* IS SUCESSFULLY CREATED and saved in folder awsfiles/ <<<<<<<<".format(kn))
                    
                else:
                    prRed(">>>>>>>>>FAILED TO CREATE KEY PAIR TRY AGAIN<<<<<<<<<\n"+output[1])
                    op1="0"
                    st1=0

            if ("2" in op1) and (st2!=1):
                sg_name = input("Enter Security group name: ")
                sg_dicp = input("Enter Security group Description: ")
                output = sp.getstatusoutput("aws ec2 create-security-group --group-name {0} --description '{1}'".format(sg_name,sg_dicp))
                if output[0]==0:
                    prGreen(output[1]+"\n>>>>>>>>>SECURITY GROUP NAMED *{0}* SECUSSFULLY CREATED<<<<<<<<<".format(sg_name))
                    st2=1
                    prLightPurple("""\n Which ingress rulls you want to add??
 [To enter multiple option seprate it with ","]
        1. Allow any IP HTTP ingress
        2. Allow any IP SSH ingress
        3. Allow all traffic to anywhere \n""")
                    sg_ing = input("Enter your options: ")
                    if "1" in sg_ing:
                        output = sp.getstatusoutput("aws ec2 authorize-security-group-ingress  --group-name {0} ".format(sg_name)+"--ip-permissions IpProtocol=tcp,FromPort=80,ToPort=80,Ipv6Ranges='[{CidrIpv6=::/0}]',IpRanges='[{CidrIp=0.0.0.0/0}]'")
                        if output[0]==0:
                            prGreen(">>>>>>>>>>HTTP ingress rule added sucesfully<<<<<<<<<<")
                        else:
                            prRed(">>>>>>>>>FAILED TO ADD HTTP ingress rule<<<<<<<<")
                    if "2" in sg_ing:
                        output = sp.getstatusoutput("aws ec2 authorize-security-group-ingress  --group-name {0} ".format(sg_name)+"--ip-permissions IpProtocol=tcp,FromPort=22,ToPort=22,Ipv6Ranges='[{CidrIpv6=::/0}]',IpRanges='[{CidrIp=0.0.0.0/0}]'")
                        if output[0]==0:
                            prGreen(">>>>>>>>>>SSH ingress rule added sucesfully<<<<<<<<<<")
                        else:
                            prRed(">>>>>>>>>FAILED TO ADD SSH ingress rule<<<<<<<<")
                    if "3" in sg_ing:
                        output = sp.getstatusoutput("aws ec2 authorize-security-group-ingress  --group-name {0} ".format(sg_name)+"--ip-permissions IpProtocol=-1,Ipv6Ranges='[{CidrIpv6=::/0}]',IpRanges='[{CidrIp=0.0.0.0/0}]'")
                        if output[0]==0:
                            prGreen(">>>>>>>>>>ALLOW ALL TRAFFIC ingress rule added sucesfully<<<<<<<<<<")
                        else:
                            prRed(">>>>>>>>>FAILED TO ADD ALLOW ALL TRAFFIC ingress rule<<<<<<<<")
                else:
                    ("\n>>>>>>>>>>>>>>FAILED TO CREATE SECURITY GROUP <<<<<<<<<<\n")
                    op1="0"
                    st2=0

            if ("3" in op1)and(st3!=1):
                prYellow("\n********************LAUNCHING EC2 INSTANCE*****************")
                prLightPurple("""Choose your AMI type:
[The default AMI is Red Hat Enterprise Linux 8]
            1. Amazon Linux 2 AMI (HVM), SSD Volume Type (64-bit x86)
            2. Red Hat Enterprise Linux 8 (64-bit x86)""")
                op2 = input("     Enter your choice: ")
                if op2=="1":
                    ec2_img = "ami-0e306788ff2473ccb"
                else:
                    ec2_img = "ami-052c08d70def0ac62"
                prLightPurple("""Choose your Availability Zone :
[The default AvailabilityZone is ap-south1a ]
            1. ap-south-1a
            2. ap-south-1b
            3. ap-south-1c""")
                op2 = input("     Enter your choice: ")
                if op2=="2":
                    ec2_az = "ap-south-1b"
                elif op2=="3":
                    ec2_az = "ap-south-1c"
                else:
                    ec2_az = "ap-south-1a"
                ec2_name =  input("     Enter your instance name: ")
                if kn!=None:
                    ec2_key=kn
                    prYellow("****Using the previously created keypair****")
                else:
                    ec2_key = input("     Enter your keyPair name: ")
                if sg_name!=None:
                    ec2_sg=sg_name
                    prYellow("****Using the previously created Security Group****")
                else:
                    ec2_sg = input("     Enter your security group name: ")
                output = sp.getstatusoutput("""aws ec2 run-instances \
--count 1 \
--image-id {0} \
--instance-type t2.micro \
--key-name {1} \
--security-groups {2} \
--placement 'AvailabilityZone={3}' \
--tag-specifications """.format(ec2_img,ec2_key,ec2_sg,ec2_az)+"'ResourceType=instance,Tags=[{Key=Name,Value="+ec2_name+"}]'")
                if output[0]==0:
                    prLightGray(output[1])
                    op_json = json.loads(output[1])
                    ec2_id = op_json["Instances"][0]["InstanceId"]
                    x=1
                    prLightPurple("\n>>>>>>>>>>>>>>>>>>> WAITING FOR PUBLIC IP ADDRESS <<<<<<<<<<<<<<<<<")
                    while x!=0:
                        ec2_des = sp.getstatusoutput("aws ec2 describe-instances --instance-ids "+ec2_id+" | grep PublicIp")
                        x=ec2_des[0]
                    ec2_des = sp.getstatusoutput("aws ec2 describe-instances --instance-ids "+ec2_id)
                    op_json2 = json.loads(ec2_des[1])
                    ec2_pubip = op_json2["Reservations"][0]["Instances"][0]["PublicIpAddress"]
                    prYellow("\n ####################################################")
                    prGreen(""">>>>>>>>>>EC2 INSTANCE SUCESFULLY LAUNCHED<<<<<<<<<<
        1. INSTANCE ID = {0}
        2. Public IP ADDRESS = {1}""".format(ec2_id,ec2_pubip))
                    prYellow("####################################################")
                    st3=1
                else:
                    prRed(output[1])
                    prRed(">>>>>>>>>>>>>EC2 INSTANCE FAILED TO LAUNCH<<<<<<<<<<<<")
                    op1="0"
                    st3=0

            if ("4" in op1)and(st4!=1):
                prLightPurple("\n*********CREATING AWS EBS***********")
                if ec2_az!=None:
                    ebs_az=ec2_az
                else:
                    prLightPurple("""Choose your Availability Zone :
[The default AvailabilityZone is ap-south1a ]
            1. ap-south-1a
            2. ap-south-1b
            3. ap-south-1c""")
                    op2 = input("     Enter your choice: ")
                    if op2=="2":
                        ebs_az = "ap-south-1b"
                    elif op2=="3":
                        ebs_az = "ap-south-1c"
                    else:
                        ebs_az = "ap-south-1a"
                ebs_size = input("     Enter EBS volume size in GiB: ")
                ebs_name = input("     Enter EBS volume NAME: ")
                output = sp.getstatusoutput("""aws ec2 create-volume \
--availability-zone {0} \
--volume-type gp2 \
--size {1} \
--tag-specifications """.format(ebs_az,ebs_size)+"'ResourceType=volume,Tags=[{Key=Name,Value="+ebs_name+"}]'")
                if output[0]==0:
                    prLightGray(output[1])
                    op_json = json.loads(output[1])
                    ebs_id = op_json["VolumeId"]
                    prYellow("\n ####################################################")
                    prGreen(""">>>>>>>>>>EBS VOLUME CREATED SUCESFULLY<<<<<<<<<<
        1. VOLUME ID = {0}""".format(ebs_id))
                    prYellow("####################################################")
                    st4=1
                else:
                    prRed(output[1])
                    prRed(">>>>>>>>>>>FAILED TO CREATE EBS VOLUME<<<<<<<<<<")
                    op1="0"
                    st4=0

            if ("5" in op1)and(st5!=1):
                prLightPurple("*********ATTACHING AWS EBS TO EC2 INSTANCE***********")
                if ec2_id==None:
                    ec2_id = input("     Enter EC2 instance ID: ")
                if ebs_id==None:
                    ebs_id = input("     Enter EBS Volume ID: ")
                x=1
                while x!=0:
                    output = sp.getstatusoutput("aws ec2 describe-volumes --volume-id "+ebs_id+" | grep available")
                    x = output[0]
                output = sp.getstatusoutput("aws ec2 attach-volume --device /dev/sdf --instance-id {0} --volume-id {1}".format(ec2_id,ebs_id))
                if output[0]==0:
                    prGreen("\n>>>>>>>>>> EBS VOLUME ATTACHED SUCESFULLY <<<<<<<<<<\n")
                    st5=1
                else:
                    prRed(output[1])
                    prRed("\n>>>>>>>>>> EBS VOLUME ATTACHMENT FAILED <<<<<<<<<<<\n")
                    op1="0"
                    st5=0

            if "6" in op1:
                prLightPurple("********* CONFIGURING WEBSERVER ON EC2 INSTANCE***********\n")
                if ec2_id==None:
                    ec2_pubip = input(" Enter the ip address: ")
                    ec2_key = input(" Enter the KeyPair file with path: ")
                else:
                    prLightPurple(">>>>>> Checking connection with {} Please Wait<<<<<<<<<<".format(ec2_pubip))
                    time.sleep(10)
                    output =  sp.getstatusoutput("ping {} -c 5".format(ec2_pubip))
                nd = linuxf("1",ec2_pubip,"ec2-user","awsfiles/{0}.pem".format(ec2_key))
            if "7" in op1:
                prLightPurple("********* CREATION OF PARTITION AND MOUNTING***********")
                if ec2_id==None:
                    ec2_pubip = input("\n    Enter the ip address: ")
                    ec2_key = input("    Enter the KeyPair file with path: ")
                part = linuxf("6",ec2_pubip,"ec2-user","awsfiles/{0}.pem".format(ec2_key))
                if nd == None:
                    nd = input("\n    Enter the folder to mount with path: ")
                linuxf("7",ec2_pubip,"ec2-user","awsfiles/{0}.pem".format(ec2_key),nd,part)

            op1="0"






def linuxf(op1="0",ip_ad=None,un=None,ky=None,nd=None,part=None):
    exclusive = 1
    prCyan("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> REMOTE LINUX AUTOMATION USING SSH <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
    if ip_ad==None:
        ip_ad = input("     Enter your target IP Address: ")
    else:
        prYellow("      Your IP address is "+ip_ad)
    if un==None:
        un = input("     Enter your target UserName: ")
    else:
        prYellow("      Your User Name is "+un)
    if ky==None:
        ky = input("     Enter your key file with path[Ex. awsfiles/key.pem] : ")
    else:
         prYellow("      Your key file is "+ky)
    ssh = "ssh -l {0} {1} -i {2} sudo ".format(un,ip_ad,ky)
    st1=0
    while(op1!="10"):
        if op1=="0":
            exclusive = 0
            op8 = "0"
            prCyan("""What you want to do in AWS?
[To enter multiple option seprate it with ","]\n""")
            if st1==1:
                prYellow("       1. WebServer is configured.✅\n")
            else:
                prCyan("       1. WebServer Configuration.\n")
            prCyan("""       2. Start any service.\n
        3. Stop any service.\n
        4. SCP file transfer. \n
        5. Create an USER. \n
        6. Create STATIC partition and Format it.\n 
        7. Mount Directory to a partition.\n
        8. LVM dynamic partition.\n
        9. SSH Remote Login .\n
       10. EXIT This MENU\n""")
            op1 = input("Enter your option: ")
        if op1=="10":
            prLightGray("QUITING LINUX AUTOMATION MENU............")
        else:
            if "1" in op1:
                prYellow("\n>>>>>>>>>>>>>>>>>>>>>>>>>> WEB SERVER CONFIGURATION <<<<<<<<<<<<<<<<<<")
                print(ssh+"yum install httpd -y")
                output = sp.getstatusoutput(ssh+"yum install httpd -y")
                if output[0]==0:
                    print(output[1])
                    prGreen("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>> HTTPD SOFTWARE INSTALLED SUCESSFULLY <<<<<<<<<<<<<<<<<<<\n")
                    op2 = input("    Do you want to download your HTML file into /var/www/html ? (y/n): ")
                    if op2=="y" or op2=="Y":
                        link = input("\nEnter the URL of html file: ")
                        output = sp.getstatusoutput(ssh+"yum install wget -y")
                        output = sp.getstatusoutput(ssh+"wget {0} -P /var/www/html/".format(link))
                        if output[0]==0:
                            print(output[1])
                            prGreen("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>> HTML FILE DOWNLOADED SUCESSFULLY <<<<<<<<<<<<<<<<<<<")
                        else:
                            prRed("\n>>>>>>>>>>>>>>>>>>>>>>>>>> FAILED TO DOWNLOADED HTML FILE <<<<<<<<<<<<<<<<<<<<<")
                    output = sp.getstatusoutput(ssh+"systemctl start httpd")
                    if output[0]==0:
                        print(output[1])
                        prGreen("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>> HTTPD SERVICE STARTED SUCESSFULLY <<<<<<<<<<<<<<<<<<<\n\n")
                        nd="/var/www/html/"
                        st1=1
                    else:
                        prRed("\n>>>>>>>>>>>>>>>>>>>>>>>>>> FAILED TO START HTTPD SERVICE <<<<<<<<<<<<<<<<<<<<<\n\n")
                else:
                    prRed(output[1])
                    prRed("\n>>>>>>>>>>>>>>>>>>>>>>>>>> FAILED TO INSTALL HTTPD <<<<<<<<<<<<<<<<<<<<<\n\n")
                if exclusive == 1:
                    op1="10"
                    return nd

            if "2" in op1:
                service = input("\n   Which service do you want to start enter its name: ")
                output = sp.getstatusoutput(ssh+"systemctl start {0}".format(service))
                if output[0]==0:
                    print(output[1])
                    prGreen("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>> *{0}* SERVICE STARTED SUCESSFULLY <<<<<<<<<<<<<<<<<<<\n".format(service))
                else:
                    prRed("\n>>>>>>>>>>>>>>>>>>>>>>>>>> FAILED TO START THIS SERVICE <<<<<<<<<<<<<<<<<<<<<\n")
            if "3" in op1:
                service = input("\n   Which service do you want to STOP enter its name: ")
                output = sp.getstatusoutput(ssh+"systemctl stop {0}".format(service))
                if output[0]==0:
                    print(output[1])
                    prGreen("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>> *{0}* SERVICE STOPPED SUCESSFULLY <<<<<<<<<<<<<<<<<<<\n".format(service))
                else:
                    prRed("\n>>>>>>>>>>>>>>>>>>>>>>>>>> FAILED TO STOP THIS SERVICE <<<<<<<<<<<<<<<<<<<<<\n")
            if "4" in op1:
                prYellow("\n>>>>>>>>>>>>>>>>>>>>>>>>>> SCP FILE TRANSFER <<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
                frm = input("    Enter file name to be transfered with path: ")
                to = input("    Enter destination file name: ")
                output = sp.getstatusoutput("scp -i {0} {1} {2}@{3}:/home/{2}/{4}".format(ky,frm,un,ip_ad,to))
                if output[0]==0:
                    print(output[1])
                    prGreen("\n>>>>>>>>>>>>>>>>>>> FILE TRANSFER OF *{0}* SUCESSFULLY AT HOME DIRECTORY OF THE USER <<<<<<<<<<<<<<<<<<<\n".format(to))
                else:
                    prRed("\n>>>>>>>>>>>>>>>>>>>>>>>>>> FAILED TO TRANSFER THE FILE <<<<<<<<<<<<<<<<<<<<<\n")
            if "5" in op1:
                user = input("  Enter the username to be created: ")
                os.system(ssh+"useradd "+user)
                os.system(ssh+"passwd "+user)

            if "6" in op1:
                prYellow("\n>>>>>>>>>>>>>>>>>>>>>> Linux Static Partition Operations <<<<<<<<<<<<<<<<<<<<<<")
                output =  sp.getstatusoutput(ssh+"lsblk")
                prLightGray("\n█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█\n"+output[1]+"\n█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█\n")
                disk = input("     Enter the disk name from the above to create its partition: /dev/")
                os.system(ssh+"fdisk /dev/"+disk)
                output =  sp.getstatusoutput(ssh+"lsblk")
                prLightGray("\n█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█\n"+output[1]+"\n█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█\n")
                op6 = input("   Is the required partition created sucessfully?(y/n): ")
                if "y" in op6:
                    part_no = input("   Enter the partion number just created /dev/"+disk)
                    part = disk+part_no
                    output =  sp.getstatusoutput(ssh+"mkfs.ext4 /dev/"+part)
                    if output[0]==0:
                        prGreen(output[1])
                        prGreen(">>>>>>>>>>>>>>>>>>>>>>>> PARTITION SUCESSFULLY CREATED AND FORMATED <<<<<<<<<<<<<<<<<<<<<")
                    else:
                        prRed(output[1])
                        prRed(">>>>>>>>>>>>>>>>>>>>>>>> FAILED TO FORMAT THE PARTITION <<<<<<<<<<<<<<<<<<<<<")
                else:
                    prRed(">>>>>>>>>>>>>>>>>>>>>>>> TRY AGAIN TO CREATE PARTITION <<<<<<<<<<<<<<<<<<<<")
                if exclusive == 1:
                    op1="10"
                    return part
            if "7" in op1:
                prYellow("\n>>>>>>>>>>>>>>>>>>>>>> MOUNT TO PARTITION <<<<<<<<<<<<<<<<<<<<<<<<<<\n")
                if nd==None:
                    op7 = input("    Do you want to create new directory?(y/n): ")
                    if "y" in op7:
                        nd = input("    Enter the name of the new directory with path: ")
                        os.system(ssh+"rm -rf {}".format(nd))
                        os.system(ssh+"mkdir {}".format(nd))
                    else:
                        nd = input("    Enter the name of the exesisting directory with path: ")
                output =  sp.getstatusoutput(ssh+"lsblk")
                prLightGray("\n█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█\n"+output[1]+"\n█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█\n")
                if part==None:
                    part = input("   Enter the partition name with number: /dev/")
                else:
                    prLightGray("   Mounting the folder with the partition /dev/"+part)
                output =  sp.getstatusoutput(ssh+"mount /dev/{0} {1}".format(part,nd))
                if output[0]==0:
                    prGreen(output[1])
                    prGreen(">>>>>>>>>>>>>>>>>>>>>>>> MOUNT SUCESSFULL  <<<<<<<<<<<<<<<<<<<<<")
                else:
                    prRed(output[1])
                    prRed(">>>>>>>>>>>>>>>>>>>>>>>> FAILED TO MOUNT WITH THE PARTITION <<<<<<<<<<<<<<<<<<<<")
                if exclusive == 1:
                    op1="10"

            if "8" in op1:
                prYellow("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>> LOGICAL VOLUME MANAGEMENT <<<<<<<<<<<<<<<<<<<<<<<<\n")
                output =  sp.getstatusoutput(ssh+"yum install lvm2 -y")
                while op8!="10":
                    prCyan("""What operation you want to perform in LVM:
[To enter multiple option seprate it with ","]\n
            1. Display all disks.\n
            2. Create Physical Volume. \n
            3. Display all physical volumes. \n
            4. Create Volume Group.\n
            5. Display all Volume Groups. \n
            6. Create a dynamic LVM partition.\n
            7. Display all Logical volumes.\n
            8. Extend/Reduce Volume group.\n
            9. Extend/Reduce Logical Volume.\n
           10. Exit LVM menu""")
                    op8 = input("Enter your option: ")
                    if op8=="10":
                        prLightPurple("Quiting lvm menu......")
                    else:
                        if "1" in op8:
                            output =  sp.getstatusoutput(ssh+"fdisk -l")
                            prLightGray(output[1])
                        if ("2" in op8):
                            output =  sp.getstatusoutput(ssh+"fdisk -l | grep 'Disk /'")
                            prLightGray("\n█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█\n"+output[1]+"\n█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█\n")
                            pvs = input("""         Enter the disk name from above to create its physical volume
        [Note: to give multiple disks seperate it with space ' ' ]: """)
                            output =  sp.getstatusoutput(ssh+"pvcreate "+pvs)
                            prLightGray(output[1])
                            output =  sp.getstatusoutput(ssh+"pvdisplay -C")
                            prLightGray("\n█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█\n"+output[1]+"\n█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█\n")
                        if "3" in op8:
                            os.system(ssh+"pvdisplay")
                        if ("4" in op8):
                            output =  sp.getstatusoutput(ssh+"pvdisplay -C")
                            prLightGray("\n█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█\n"+output[1]+"\n█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█\n")
                            if not("2" in op8):
                                pvs = input("""         Enter the physical volume disk name from above to create its VG
        [Note: to give multiple disks seperate it with space ' ' ]: """)

                            vgn = input("         Enter the volume group Name: ")
                            output =  sp.getstatusoutput(ssh+"vgcreate {} ".format(vgn)+pvs)
                            if output[0]==0:
                                prGreen(">>>>>>>>>>>>>>>>>>> VG CREATED SUCESSFULLY <<<<<<<<<<<<<")
                                prGreen(output[1])
                                output =  sp.getstatusoutput(ssh+"vgdisplay -C")
                                prLightGray("\n█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█\n"+output[1]+"\n█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█\n")
                        if "5" in op8:
                            os.system(ssh+"vgdisplay")
                        if "6" in op8:
                            output =  sp.getstatusoutput(ssh+"vgdisplay -C")
                            prLightGray("\n█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█\n"+output[1]+"\n█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█\n")
                            if not("4" in op8):
                                vgn = input("""         Enter the volume group name from above to create its Logical volume
        [Note: to give multiple disks seperate it with space ' ' ]: """)
                            lvn = input("         Enter the Logical volume Name: ")
                            size = input("         Enter the Logical volume SIZE: ")
                            output =  sp.getstatusoutput(ssh+"lvcreate --size {0} --name {1} {2}".format(size,lvn,vgn))
                            if output[0]==0:
                                prGreen(">>>>>>>>>>>>>>>>>>> Logical Volume/Dynamic partition */dev/{}/{}* CREATED SUCESSFULLY <<<<<<<<<<<<<".format(vgn,lvn))
                                prGreen(output[1])
                                output =  sp.getstatusoutput(ssh+"lvdisplay -C")
                                prLightGray("\n█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█\n"+output[1]+"\n█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█▒█\n")
                                output =  sp.getstatusoutput(ssh+'mkfs.ext4 /dev/{}/{}'.format(vgn,lvn))
                                if output[0]==0:
                                    prGreen(">>>>>>>>>>>>>>>>>>> Logical Volume  Formated SUCESSFULLY and Ready to Mount <<<<<<<<<<<<<")

                        if "7" in op8:
                            os.system(ssh+"lvdisplay")

            if "9" in op1:
                os.system(ssh[:-6])
            
                            
            op1="0"



##############################################################################################################################################

op="0"
while(op!="5"):
    os.system("clear")
    prYellow(" 🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟")
    prPurple("""
    ▒█░░▒█ ▒█▀▀▀ ▒█░░░ ▒█▀▀█ ▒█▀▀▀█ ▒█▀▄▀█ ▒█▀▀▀ 　 　 ▀▀█▀▀ ▒█▀▀▀█ 　 　 
    ▒█▒█▒█ ▒█▀▀▀ ▒█░░░ ▒█░░░ ▒█░░▒█ ▒█▒█▒█ ▒█▀▀▀ 　 　 ░▒█░░ ▒█░░▒█ 　 　 
    ▒█▄▀▄█ ▒█▄▄▄ ▒█▄▄█ ▒█▄▄█ ▒█▄▄▄█ ▒█░░▒█ ▒█▄▄▄ 　 　 ░▒█░░ ▒█▄▄▄█ 　 　 

    ▒█▀▀█ ▒█░░▒█ ▀▀█▀▀ ▒█░▒█ ▒█▀▀▀█ ▒█▄░▒█ 　 ░█▀▀█ ▒█░▒█ ▀▀█▀▀ ▒█▀▀▀█ ▒█▀▄▀█ ░█▀▀█ ▀▀█▀▀ ▀█▀ ▒█▀▀▀█ ▒█▄░▒█ 
    ▒█▄▄█ ▒█▄▄▄█ ░▒█░░ ▒█▀▀█ ▒█░░▒█ ▒█▒█▒█ 　 ▒█▄▄█ ▒█░▒█ ░▒█░░ ▒█░░▒█ ▒█▒█▒█ ▒█▄▄█ ░▒█░░ ▒█░ ▒█░░▒█ ▒█▒█▒█ 
    ▒█░░░ ░░▒█░░ ░▒█░░ ▒█░▒█ ▒█▄▄▄█ ▒█░░▀█ 　 ▒█░▒█ ░▀▄▄▀ ░▒█░░ ▒█▄▄▄█ ▒█░░▒█ ▒█░▒█ ░▒█░░ ▄█▄ ▒█▄▄▄█ ▒█░░▀█\n\n""")
    prYellow("🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟")
    prPurple("""
        1. HADOOP                2. DOCKER             3. AWS              4. LINUX              5. EXIT

           → Install hadoop                               → Key Pair          → WEB SERVER
           → Name Node                                    → Security Grp      → LVM PARTITION
           → Data Node                                    → EC2 Instance      → FORMAT AND MOUNT
           → Hadoop Report                                → EBS Volume        → CREATE/REMOVE FILE/DIRECTORY

        Enter your options:""")
    op=input()
    if op=="1":
        os.system("clear")
        prCyan("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> HADOOP CONFIGURATION <<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
        ip=input("Enter the  ip address of the node: ")
        key=input("Enter key path with name [Ex. /home/key.pem]: ")
        un=input("Enter the user name: ")
        hadoopf("0",ip,key,un)
    elif op=="3":
        os.system("clear")
        prCyan("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> AWS MENU <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")
        awsf()
    elif op=="4":
        os.system("clear")
        linuxf()
