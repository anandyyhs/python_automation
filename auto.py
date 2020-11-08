
import subprocess as sp

def prRed(skk): print("\033[91m {}\033[00m" .format(skk)) 
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk)) 
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk)) 
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk)) 
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk)) 
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
                else:
                    prYellow(">>>>>>>HADOOP IS ALREADY INSTALLED<<<<<<<")
                    op1="0"
            if "1" in op1:
                prLightPurple(">>>>>>>>INSTALLING HADOOP .......<<<<<<<<<")
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
                prLightPurple("Coniguring named node.....")
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
                output = sp.getstatusoutput("mkdir /dn")
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
                prLightPurple("STARTING NAME NODE.....")
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
                prLightPurple("STARTING DATA NODE.....")
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
                prLightPurple(">>>PRINTING HADOOP REPORT.......")
                output = sp.getstatusoutput(ssh+"hadoop dfsadmin -report")
                prLightGray(output[1])
            op1="0"


prPurple("""Welcome to python automation
        1. HADOOP
        2. DOCKER
        3. AWS""")
op=input("enter ur options: ")
if op=="1":
    ip=input("enter ip address: ")
    key=input("enter key path with name [Ex. /home/key.pem]: ")
    un=input("enter user name: ")
    hadoopf("0",ip,key,un)

