
import subprocess as sp
import json

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
            prCyan("""What you want to do in hadoop
[To enter multiple option seprate it with ","]
        1. Install hadoop software
        2. Configure named node
        3. Configure data node
        4. Start named node
        5. Start data node
        6. Check dfsadmin report
        7. Exit hadoop menu""")
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
                prLightPurple("Coniguring data node.....")
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
    prPurple("NOTE:IT IS ASSUMED THAT AWS CLI IS ALREADY CONFIGURED\n")
    prCyan("""What you want to do in AWS?
[To enter multiple option seprate it with ","]
        1. Create keypair.
        2. Create Security group
        3. Launch an EC2 instance.
        4. Create EBS volume.
        5. Attach EBS volume to EC2 instance.
        6. Install webserver on EC2 instance.
        7. Create Partition and mount it.
        8. 
        9.
        10. EXIT AWS MENU""")
    op1 = input("Enter your option: ")
    #output = sp.getstatusoutput("aws ec2 describe-key-pairs")
    #key_op = json.loads(output[1])
    #print(key_op)
    kn = None
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
    while(op1!="10"):
        if op1=="0":
            prCyan("""What you want to do in AWS?
[To enter multiple option seprate it with ","]""")
            if st1==1:
                prYellow("       1. Create keypair.✅")
            else:
                prCyan("       1. Create keypair.")
            if st2==1:
                prYellow("       2. Create Security group.✅")
            else:
                prCyan("       2. Create Security group.")
            if st3==1:
                prYellow("       3. Launch an EC2 instance.✅")
            else:
                prCyan("       3. Launch an EC2 instance.")
            if st4==1:
                prYellow("       4. Create EBS volume.✅")
            else:
                prCyan("       4. Create EBS volume.")
            if st5==1:
                prYellow("       5. Attach EBS volume to EC2 instance.✅")
            else:
                prCyan("       5. Attach EBS volume to EC2 instance.")
        
            prCyan("""       6. Install webserver on EC2 instance.
        7. Create Partition and mount it.
        8.
        9. RESET THIS MENU
        10. EXIT AWS MENU""")
            op1 = input("Enter your option: ")

        if op1=="10":
            prLightGray("Quiting AWS MENU....")
        else:
            if "9" in op1:
                prBlack(">>>>>RESETING AWS MENU<<<<<<<")
                st1 = 0
                st2 = 0
                st3 = 0
                st4 = 0
                st5 = 0
                st6 = 0
                st7 = 0
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
                    prGreen(">>>>>>>>>KEY PAIR NAMED *{0}* IS SUCESSFULLY CREATED and saved in folder awsfiles/ <<<<<<<<".format(kn))
                    st1==1
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
                prYellow("********************LAUNCHING EC2 INSTANCE*****************")
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
                prLightPurple("*********CREATING AWS EBS***********")
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

            op1="0"






prPurple("""Welcome to python automation
        1. HADOOP
        2. DOCKER
        3. AWS
        Enter your options:""")
op=input()
if op=="1":
    prCyan(">>>>>>HADOOP CONFIGURATION<<<<<<<<")
    ip=input("Enter the  ip address of the node: ")
    key=input("Enter key path with name [Ex. /home/key.pem]: ")
    un=input("Enter the user name: ")
    hadoopf("0",ip,key,un)
elif op=="3":
    awsf()
