import subprocess as sp
import os
import getpass

red = "\033[0;31m"
powder_blue = "\033[1;36m" #with bold
blue = "\033[1;34m"
normal = "\033[0m"
white = "\033[97m"
dark_blue = "\033[0;34m"
green = "\033[0;32m"


def docker_menu():
	
	os.system('clear')
	print("\n\n\n\t\t\t\t                   {} ##      {} .         ".format(red, blue))
	print("\t\t\t\t             {} ## ## ##      {} ==         ".format(red, blue))
	print("\t\t\t\t           {}## ## ## ##      {}===         ".format(red, blue))
	print("\t\t\t\t       /\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\"\\\___/ ===       ")
	print("\t\t\t\t  {0}~~~ {1}!{0}~~ ~~~~ ~~~ ~~~~ ~~ ~ {1} /  ===- {0}~~~{1}".format(dark_blue, blue))
	print("\t\t\t\t       \______{} o {}          __/           ".format(white, blue))
	print("\t\t\t\t         \    \        __/            ")
	print("\t\t\t\t          \____\______/               ")
	print("\t\t\t\t{}                                          ".format(powder_blue))
	print("\t\t\t\t          |          |                    ")
	print("\t\t\t\t       __ |  __   __ | _  __   _          ")
	print("\t\t\t\t      /  \| /  \ /   |/  / _\ |     ")
	print("\t\t\t\t      \__/| \__/ \__ |\_ \__  |  \n")
	print("{}================================================================================================".format(green))
	print("\n\n \t\t 1. Download docker Image " + "\t\t 2. Show Available Local Images" )
	print("\n \t\t 3. Launch New Container " + "\t\t 4. Show All Containers " )
	print("\n \t\t 5. Start Container " + "\t\t\t 6. Stop Container " )
	print("\n \t\t 7. Attach to Container [get CLI] " + "\t 0. Exit " )
	print("\n\n{}================================================================================================".format(green))
	ch = int(input("\n\n \tEnter your choise : "))
	return ch






def docker():
	ch=0
	while ch!=3:
		os.system('clear')
		print("1. Manage Docker on Local Host \n" +
		"2. Manage Docker on Remote Host \n" +
		"3. Exit \n")  

		ch = int(input("Enter your choise : "))

		if ch == 2:
			ssh_IP = input("Enter IP Adress or Host Name :")
			ssh_Password = getpass.getpass("Enter Password :")
			ssh = "sshpass -p {} ssh {} ".format(ssh_Password, ssh_IP)
			output = sp.getstatusoutput(ssh+"date")
			if output[0] == 0:
				output = sp.getstatusoutput(ssh+" rpm -q docker-ce")
				while output[0] != 0:
					os.system('clear')
					print("\n\n\n\t\t\t  !!! Docker is Not Installed on {0} !!!\n\n".format(ssh_IP) +
					      "\t\t\t  Press < i > to Install Docker on {0}\n\n".format(ssh_IP) + 
					      "\t\t\t  Press < e > to Exit \n")
					ch = input("Enter your choise : ")
					if ch == "e":
						break
					elif ch == "i":
						os.system('clear')
						print("\n\n\n\t\t >>> Creatin Repository to install docker    ...   ", end = "\t")
						output = sp.getstatusoutput(ssh+" \" echo -e [docker-d] \\\\\\nbaseurl=https://download.docker.com/linux/centos/7/x86_64/stable/ \\\\\\ngpgcheck=0 > /etc/yum.repos.d/docker.repo \" ")
						if output[0] == 0:
							print(" created ...      [Done]")
						else:
							print("\t\t\t [Faild] \n \t Error : {}".format(output[1]))

						sp.getstatusoutput(ssh+" yum clean all")
						print("\n\n\t\t >>> Installing Docker-ce    ...   ", end = "\t")
						output = sp.getstatusoutput(ssh+" yum install docker-ce --nobest -y")
						if output[0] == 0:
							print(" please wait...  Installed  ...     [Done]\n\n \n\n\t\t\t # Docker Installed Successfully #")
							
						else:
							
							print("\t\t\t [Faild] \n\n\n \t\t\t !!! Failed to Install Docker !!! \n\n\t Error : {}".format(output[1]))

						

					input("\n\n \t\t -> Press any key to Continue .....")
				
				else:
					output = sp.getstatusoutput(ssh+" systemctl status docker")
					while output[0] != 0:
						os.system('clear')
						print("\n\n\n\t\t\t  !!! Docker is Not Running on {0} !!!\n\n".format(ssh_IP) +
						      "\t\t\t  Press < s > to Start Docker on {0}\n\n".format(ssh_IP) + 
						      "\t\t\t  Press < e > to Exit \n")
						ch = input("Enter your choise : ")
						if ch == "e":
							break
						elif ch == "s":
							print("\n\n\t\t >>> Starting Docker Service (Daemon)  ...  Please Wait  ...   ", end = "\t")
							output = sp.getstatusoutput(ssh+" systemctl start docker")
							if output[0] == 0:
								print("\tStarted  ...    [Done]\n\n \n\n\t\t\t # Docker is Successfully Started #")
							
							
							else:
				
								print("\t\t [Faild] \n\n\n \t\t\t !!! Failed to Start Docker !!! \n\n\t Error : {}".format(output[1]))
						input("\n\n \t\t -> Press any key to Continue .....")

					else:	
						while True:
							ch = docker_menu()
						
							if ch == 0:
								break

		
							if ch == 1:
								img_name = input("\n\tEnter Image Name to Download : ")
								print("\n\n \t >>> downloading Image  ...  Please Wait ....  ", end = "")
								output = sp.getstatusoutput(ssh + " docker pull {}".format(img_name))
								if output[0] == 0:
									print("\t [done] \n\n{}\n\n\t successfuly downloaded < {} docker image>".format(output[1], img_name))
									
								else:
									print("\t [Faild] \n\n \t !!! Faild to downloade < {} > image !!!\n\n\t Error : \n{} ".format(img_name, output[1]))
								input("\n\n \t\t -> Press any key to Continue .....")




							if ch == 2:
								output = sp.getstatusoutput(ssh + " docker images")
								if output[0] == 0:
									print("\n\n {}>".format(output[1]))
									
								else:
									print("\n\n \t !!! Faild to list images !!! \n\n\t Error : \n{} ".format(output[1]))
								input("\n\n \t\t -> Press any key to Continue .....")



							if ch == 3:
								cmd = " docker run "
								login = input("\n\n\tPress < y > if you want to get terminul(CLI) to interact with Container : ")
								if login == "y":
									cmd = cmd + " -it "
								cmd = cmd + " --name "+input("\n\tGive Name to Container : ")
								cmd = cmd + " " + input("\n\tEnter Docker Image Name to Launch Container : ")
								print("\n\n \t >>> Launching Container  ...  Please Wait ....   consol : ", end = "")
								output = os.system(ssh + cmd)
								if output == 0:
									if login != "y":
										print("\t [done] \n\n\t ~ Contaner is successfuly Launched ~ ")
									
								else:
									print("\t [Faild] \n\n \t !!! Faild to launch container !!! ")
								input("\n\n \t\t -> Press any key to Continue .....")



							if ch == 4:
								print("\n\n \t >>> Listing All Containers ...  Please Wait ....  ", end = "")
								output = sp.getstatusoutput(ssh + " docker ps -a")
								if output[0] == 0:
									print("\t [done] \n\n\n{}".format(output[1]))
									
								else:
									print("\t [Faild] \n\n \t !!! Faild to list Containers !!!\n\n\t Error : \n{} ".format(output[1]))
								input("\n\n \t\t -> Press any key to Continue .....")



							if ch == 5:
								con_name = input("\n\tEnter Name of Container to Start it : ")
								print("\n\n \t >>> Starting Container  ...  Please Wait ....  ", end = "")
								output = sp.getstatusoutput(ssh + " docker start {}".format(con_name))
								if output[0] == 0:
									print("\t [done] \n\n{}\n\n\t successfuly Started < {} > Container ".format(output[1], con_name))
									
								else:
									print("\t [Faild] \n\n \t !!! Faild to Start < {} > Container !!!\n\n\t Error : \n{} ".format(con_name, output[1]))
								input("\n\n \t\t -> Press any key to Continue .....")



							if ch == 6:
								con_name = input("\n\tEnter Name of Container to Stop it : ")
								print("\n\n \t >>> Stoping Container  ...  Please Wait ....  ", end = "")
								output = sp.getstatusoutput(ssh + " docker stop {}".format(con_name))
								if output[0] == 0:
									print("\t [done] \n\n{}\n\n\t  < {} > Container is successfuly Stoped ".format(output[1], con_name))
									
								else:
									print("\t [Faild] \n\n \t !!! Faild to Stop < {} > Container !!!\n\n\t Error : \n{} ".format(con_name, output[1]))
								input("\n\n \t\t -> Press any key to Continue .....")



							if ch == 7:
								con_name = input("\n\tEnter Name of Container to which you want to Attach : ")
								print("\n\n \t >>> Attaching to Container and geting CLI  ...  Please Wait .... Consol :  \n\n")
								output = os.system(ssh + " docker attach {}".format(con_name))
								if output == 0:
									pass
								else:
									print(" \n\n \t !!! Faild to Attach to < {} > Container !!!".format(con_name))
								input("\n\n \t\t -> Press any key to Continue .....")





				
			else:
				print("\n\n \t !!! Faild to connect with {} Host !!!\n\n \t Error : \n\n{}".format(ssh_IP, output[1]))
				input("\n\t ~ Please Check Host IP and Password ~\n\n\t -> Press any key to Continue .....")		
		  




# ---------------------------------- Manage Docker on Local Host ----------------------------------------------------------------------  
		if ch == 1:
			output = sp.getstatusoutput("sudo rpm -q docker-ce")
			
			while output[0] != 0:
				os.system('clear')
				print("\n\n\n\t\t\t  !!! Docker is Not Installed on Loacl ost !!!\n\n" +
				      "\t\t\t  Press < i > to Install Docker on Local Host \n\n" + 					      "\t\t\t  Press < e > to Exit \n")
				ch = input("Enter your choise : ")
				if ch == "e":
					break
				elif ch == "i":
					os.system('clear')
					print("\n\n\n\t\t >>> Creatin Repository to install docker    ...   ", end = "\t")
					output = sp.getstatusoutput("sudo echo -e [docker-d] \\\\nbaseurl=https://download.docker.com/linux/centos/7/x86_64/stable/ \\\\ngpgcheck=0 > /etc/yum.repos.d/docker.repo ")
					if output[0] == 0:
						print(" created ...      [Done]")
					else:
						print("\t\t\t [Faild] \n \t Error : {}".format(output[1]))

					sp.getstatusoutput("sudo yum clean all")
					print("\n\n\t\t >>> Installing Docker-ce    ...   ", end = "\t")
					output = sp.getstatusoutput("sudo yum install docker-ce --nobest -y")
					if output[0] == 0:
						print(" please wait...  Installed  ...     [Done]\n\n \n\n\t\t\t # Docker Installed Successfully #")
							
					else:
							
						print("\t\t\t [Faild] \n\n\n \t\t\t !!! Failed to Install Docker !!! \n\n\t Error : {}".format(output[1]))

				input("\n\n \t\t -> Press any key to Continue .....")
				
			else:
				output = sp.getstatusoutput("sudo systemctl status docker")
				while output[0] != 0:
					os.system('clear')
					print("\n\n\n\t\t\t  !!! Docker is Not Running on Local Host !!!\n\n" +
					      "\t\t\t  Press < s > to Start Docker on Local Host\n\n" + 
					      "\t\t\t  Press < e > to Exit \n")
					ch = input("Enter your choise : ")
					if ch == "e":
						break
					elif ch == "s":
						print("\n\n\t\t >>> Starting Docker Service (Daemon)  ...  Please Wait  ...   ", end = "\t")
						output = sp.getstatusoutput("sudo systemctl start docker")
						if output[0] == 0:
							print("\tStarted  ...    [Done]\n\n \n\n\t\t\t # Docker is Successfully Started #")
							
							
						else:
				
							print("\t\t [Faild] \n\n\n \t\t\t !!! Failed to Start Docker !!! \n\n\t Error : {}".format(output[1]))
					input("\n\n \t\t -> Press any key to Continue .....")

				else:

					while True:
						ch = docker_menu()
					
						if ch == 0:
							break

	
						if ch == 1:
							img_name = input("\n\tEnter Image Name to Download : ")
							print("\n\n \t >>> downloading Image  ...  Please Wait ....  ", end = "")
							output = sp.getstatusoutput("sudo docker pull {}".format(img_name))
							if output[0] == 0:
								print("\t [done] \n\n{}\n\n\t successfuly downloaded < {} docker image>".format(output[1], img_name))
								
							else:
								print("\t [Faild] \n\n \t !!! Faild to downloade < {} > image !!!\n\n\t Error : \n{} ".format(img_name, output[1]))
							input("\n\n \t\t -> Press any key to Continue .....")




						if ch == 2:
							output = sp.getstatusoutput("sudo docker images")
							if output[0] == 0:
								print("\n\n {}>".format(output[1]))
								
							else:
								print("\n\n \t !!! Faild to list images !!! \n\n\t Error : \n{} ".format(output[1]))
							input("\n\n \t\t -> Press any key to Continue .....")



						if ch == 3:
							cmd = "sudo docker run "
							login = input("\n\n\tPress < y > if you want to get terminul(CLI) to interact with Container : ")
							if login == "y":
								cmd = cmd + " -it "
							cmd = cmd + "-d --name "+input("\n\tGive Name to Container : ")
							cmd = cmd + " " + input("\n\tEnter Docker Image Name to Launch Container : ")
							print("\n\n \t >>> Launching Container  ...  Please Wait ....   consol : ", end = "")
							output = os.system(cmd)
							if output == 0:
								if login != "y":
									print("\t [done] \n\n\t ~ Contaner is successfuly Launched ~ ")
								
							else:
								print("\t [Faild] \n\n \t !!! Faild to launch container !!! ")
							input("\n\n \t\t -> Press any key to Continue .....")



						if ch == 4:
							print("\n\n \t >>> Listing All Containers ...  Please Wait ....  ", end = "")
							output = sp.getstatusoutput("sudo docker ps -a")
							if output[0] == 0:
								print("\t [done] \n\n\n{}".format(output[1]))
								
							else:
								print("\t [Faild] \n\n \t !!! Faild to list Containers !!!\n\n\t Error : \n{} ".format(output[1]))
							input("\n\n \t\t -> Press any key to Continue .....")



						if ch == 5:
							con_name = input("\n\tEnter Name of Container to Start it : ")
							print("\n\n \t >>> Starting Container  ...  Please Wait ....  ", end = "")
							output = sp.getstatusoutput("sudo docker start {}".format(con_name))
							if output[0] == 0:
								print("\t [done] \n\n{}\n\n\t successfuly Started < {} > Container ".format(output[1], con_name))
								
							else:
								print("\t [Faild] \n\n \t !!! Faild to Start < {} > Container !!!\n\n\t Error : \n{} ".format(con_name, output[1]))
							input("\n\n \t\t -> Press any key to Continue .....")



						if ch == 6:
							con_name = input("\n\tEnter Name of Container to Stop it : ")
							print("\n\n \t >>> Stoping Container  ...  Please Wait ....  ", end = "")
							output = sp.getstatusoutput("sudo docker stop {}".format(con_name))
							if output[0] == 0:
								print("\t [done] \n\n{}\n\n\t  < {} > Container is successfuly Stoped ".format(output[1], con_name))
								
							else:
								print("\t [Faild] \n\n \t !!! Faild to Stop < {} > Container !!!\n\n\t Error : \n{} ".format(con_name, output[1]))
							input("\n\n \t\t -> Press any key to Continue .....")



						if ch == 7:
							con_name = input("\n\tEnter Name of Container to which you want to Attach : ")
							print("\n\n \t >>> Attaching to Container and geting CLI  ...  Please Wait .... Consol :  \n\n")
							output = os.system("sudo docker attach {}".format(con_name))
							if output == 0:
					                        pass
							else:
								print(" \n\n \t !!! Faild to Attach to < {} > Container !!!".format(con_name))
							input("\n\n \t\t -> Press any key to Continue .....")









