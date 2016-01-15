from tkinter import *
import random, time, threading, subprocess
from tkinter import messagebox
import datetime
import subprocess
import webbrowser

# Control the threads
stop = False
pause = True

# Control the speed
speed = 1

# Denote the number of Productor and Consumer threads 
putThreadNum,moveThreadNum,getThreadNum = 0,2,0

# Record the id of threads
threads = []

# Record time
currentTime = datetime.datetime.now()

# Create a file object
fout = open('dataLog.txt','a')
fout.write('#'*59)
fout.write(' ')
fout.write(str(currentTime))
fout.write(' ')
fout.write('#'*59)
fout.write('\n')
fout.write('\n生产者产生的数据:\n')

play = True
def playMusic():
	global stop
	while True:
		if stop:
			break

		if play:
			subprocess.call(['mpg123','-q','Building.mp3'])
		else:
			time.sleep(2)

playThr = threading.Thread(target=playMusic)
playThr.start()
# Create a string object to save producted data
str_ = ''

class Buffer:
	def __init__(self,max_buffer):
		self.arr = [0 for i in range(max_buffer)]
		self.counter = 0

def stop_f():
	global stop
	global str_

	stop = True
	
	subprocess.call(['killall','mpg123'])

	if len(str_) != 0:
		fout.write(str_)
		fout.write('\n\n')
		fout.write('汇总数据:\n')
		fout.write('生产数量: {0}\n移动数量: {1}\n消费数量: {2}\n\n'.format(total_put,total_move,total_get))
		fout.write('#'*146)
		fout.write('\n\n')
	fout.close()
	messagebox.showinfo("汇总信息","生产数量: {0} \n移动数量: {1} \n消费数量: {2}".format(total_put,total_move,total_get))

firstStart = True
thr1,thr2 = threading.Thread(),threading.Thread()
def start_f():
	global speed
	global pause
	global MAX_BUFFER
	global putThreadNum
	global getThreadNum
	global threads
	global firstStart
	global thr1,thr2

	pause = False
	speed = float(e.get())
	MAX_BUFFER = int(bufferSizeEntry.get())

	
	if firstStart:
		putThreadNum = int(putEntryNum.get())
		getThreadNum = int(getEntryNum.get())

		# `Put` threads
		for i in range(putThreadNum):
			threads.append(threading.Thread(target=put))
		
		# `Get` threads
		for i in range(getThreadNum):
			# i is odd
			if i & 1:
				threads.append(threading.Thread(target=get,args=(buffer3,)))
			# i is even
			else:
				threads.append(threading.Thread(target=get,args=(buffer2,)))

		
		# Start threads
		for thr in threads:
			thr.start()

		# `Move` threads
		thr1 = threading.Thread(target=move,args=(buffer2,))
		if getThreadNum > 1:
			thr2 = threading.Thread(target=move,args=(buffer3,))

		thr1.start()
		if getThreadNum > 1:
			thr2.start()

		firstStart = False


def pause_f():
	global pause
	pause = True

English = False
def LanguageSwitch():
	global English
	if not English:
		tmp1.config(text='Productor')
		tmp3.config(text="Mover")
		tmp6.config(text="Consumer")
		tmp7.config(text='Begin')
		tmp8.config(text='Pause')
		tmp9.config(text='Stop')
		tmp10.config(text='Speed:')
		tmp11.config(text='Buffer Size(1-6):')
		tmp12.config(text='BlockedNum:')
		tmp13.config(text='Productor:')
		tmp14.config(text='Consumer:')
		tmp15.config(text='Help')
		English = True
	else:
		tmp1.config(text='生产者')
		tmp3.config(text="移动")
		tmp6.config(text="消费者")
		tmp7.config(text='开始')
		tmp8.config(text='暂停')
		tmp9.config(text='停止')
		tmp10.config(text='速度')
		tmp11.config(text='Buffer大小(1-6):')
		tmp12.config(text='阻塞线程数:')
		tmp13.config(text='生产者数量:')
		tmp14.config(text='消费者数量:')
		tmp15.config(text='帮助')
		English = False
		
		master.update_idletasks()
	
def openBrowser():
	url = 'http://www.StudyAndShare.info/osTaskHelp.html'
	webbrowser.open(url)

#################################### Tkinter #################################

master = Tk()

# Set Main Window's title
master.title("生产者-消费者问题")
# Set Main Window's size
master.geometry('700x500')
# Fix size
master.resizable(width=FALSE,height=FALSE)

# Set Label
tmp1 = Label(master,text="生产者",height=3,width=15)
tmp1.grid(row=0,column=0)
tmp2 = Label(master,text="Buffer1",height=3,width=15)
tmp2.grid(row=0,column=1)
tmp3 = Label(master,text="移动",height=3,width=15)
tmp3.grid(row=0,column=2)
tmp4 = Label(master,text="Buffer2",height=3,width=15)
tmp4.grid(row=0,column=3)
tmp5 = Label(master,text="Buffer3",height=3,width=15)
tmp5.grid(row=0,column=4)
tmp6 = Label(master,text="消费者",height=3,width=15)
tmp6.grid(row=0,column=5)

# Set Speed Entry
tmp10 = Label(master, text="速度:")
tmp10.place(x=580,y=350)
e = Entry(master,width=8)
# Set `Entry` default value
e.insert(0,'0.05')
e.place(x=620, y=350)

# Set Button
tmp15 = Button(text='帮助',command=openBrowser)
tmp15.place(x=100,y=400)
tmp7 = Button(text="开始",command=start_f)
tmp7.place(x=200,y=400)
tmp8 = Button(text="暂停",command=pause_f)
tmp8.place(x=300,y=400)
tmp9 = Button(text="停止",command=stop_f)
tmp9.place(x=400,y=400)
Button(text='中文/English',command=LanguageSwitch).place(x=480,y=400)

# Set Productor and Consumer thread number
tmp13 = Label(master,text="生产者数量:")
tmp13.place(x=10,y=350)
putEntryNum = Entry(master,width=8)
putEntryNum.place(x=80,y=350)
putEntryNum.insert(0,"3")
tmp14 = Label(master,text="消费者数量:")
tmp14.place(x=175,y=350)
getEntryNum = Entry(master,width=8)
getEntryNum.place(x=245,y=350)
getEntryNum.insert(0,"2")

# Set block Label
tmp12 = Label(master,text="阻塞线程数:")
tmp12.place(x=10,y=300)
blocked_num = Label(master,text="0")
blocked_num.place(x=85, y=300)

# Set Label denote Buffer size
tmp11 = Label(master,text="Buffer大小(1-6):")
tmp11.place(x=400,y=350)
bufferSizeEntry = Entry(master,width=8)
bufferSizeEntry.place(x=495,y=350)
bufferSizeEntry.insert(0,"5")

# Set Label to denote `put` thread
putLabel1 = Label(master,height=1,width=5,bg='green')
putLabel1.place(x=35,y=150)
putLabel2 = Label(master,height=1,width=5,bg='green')
putLabel2.place(x=35,y=100)
putLabel3 = Label(master,height=1,width=5,bg='green')
putLabel3.place(x=35,y=50)

# Set Label to denote `move` thread
moveLabel1 = Label(master,height=1,width=5,bg='green')
moveLabel1.place(x=255,y=50)
moveLabel2 = Label(master,height=1,width=5,bg='green')
moveLabel2.place(x=255,y=100)

# Set Label to denote `Get` thread
getLabel1 = Label(master,height=1,width=5,bg='green')
getLabel1.place(x=580,y=100)
getLabel2 = Label(master,height=1,width=5,bg='green')
getLabel2.place(x=580,y=50)

# Set Label to denote `Buffer1`
buffer1Label = Label(master,height=8,width=5,text="",bg='#0DB0DE')
buffer1Label.place(x=140,y=50)

# Set Label to denote `Buffer2`
buffer2Label = Label(master,height=8,width=5,text="",bg='#0DB0DE')
buffer2Label.place(x=360,y=50)

# Set Label to denote `Buffer3`
buffer3Label = Label(master,height=8,width=5,text="",bg='#0DB0DE')
buffer3Label.place(x=470,y=50)

############################## End Tkinter ####################################


################################ Productor-Consumer  ################################

# Summary 
total_put = 0
total_move = 0
total_get = 0


# Denote the number of blocked thread
blocked_thread = 1

# Set buffer1
MAX_BUFFER = 6
buffer1 = [0 for i in range(MAX_BUFFER)]
buffer1_counter = 0

# Set buffer2 and buffer3
buffer2 = Buffer(MAX_BUFFER)
buffer3 = Buffer(MAX_BUFFER)

# Declare lock
lock1 = threading.Lock()
lock2 = threading.Lock()

# Put data to Buffer1
def put():
	global blocked_thread
	global buffer1_counter
	global total_put
	global str_

	while True:
		if not stop:
			if pause:
				time.sleep(1)
				continue
			
			# If not pause, then lock
			lock1.acquire()

			# Update the number of blocked threads
			blocked_thread = putThreadNum - 1 + moveThreadNum

			# Buffer1 is not full
			if buffer1_counter < MAX_BUFFER:
				c = chr(random.randint(65,90))
				str_ += c
				str_ += ' '
				if len(str_) == 50:
					fout.write(str_)
					str_ = ''
				buffer1[buffer1_counter] = c
				buffer1_counter += 1
				total_put += 1

				# Unlock
				lock1.release()


			# Buffer1 is full
			else:

				# Unlock 
				lock1.release()


				time.sleep(1)
			
			# Control the speed
			time.sleep(speed)

		# Program is stop
		else:
			break

# Move data from Buffer1
def move(buf):
	global blocked_thread
	global buffer1_counter
	global total_move
	global total_put
	while True:
		if not stop:
			if pause:
				time.sleep(1)
				continue

			# if not pause, then lock buffer1
			lock1.acquire()

			blocked_thread = putThreadNum + moveThreadNum -1 + (getThreadNum // 2)

			# Buffer1 is not empty
			if buffer1_counter > 0:
				buffer1_counter -= 1
				c = buffer1[buffer1_counter]

				# Unlock Buffer1
				lock1.release()

				# Lock buf
				lock2.acquire()

				# buf is not full
				if buf.counter < MAX_BUFFER:
					buf.arr[buf.counter] = c
					buf.counter += 1
					total_move += 1

					# Unlock buf
					lock2.release()

				# buf is full
				else:
					total_put -= 1

					# Unlock buf
					lock2.release()

					time.sleep(1)

			# Buffer1 is empty
			else:

				# Unlock buffer1
				lock1.release()
					


				time.sleep(1)

			# Control the speed
			time.sleep(speed)

		# The program is stop
		else:
			break
	
# Get data from buffer
def get(buf):
	global blocked_thread
	global total_get
	while True:
		if not stop:
			if pause:
				time.sleep(1)
				continue

			# The program is not pause, then lock 
			lock2.acquire()

			blocked_thread = 1

			# buf is not empty
			if buf.counter > 0:
				buf.counter -= 1
				total_get += 1

				# Unlock buf
				lock2.release()


			# buf is empty
			else:

				# Unlock buf
				lock2.release()

				time.sleep(1)

			# Control the program speed
			time.sleep(speed)
		
		# The program is stop
		else:
			break

# Show information
def show():
	interval = int(speed * 2000)
	if not stop:
		if pause:
			time.sleep(1)
			master.after(600,show)

		# When program pause
		else:
			t = '' 
			tmp = buffer1_counter
			for i in range(tmp):
				t += buffer1[i]
				t += '\n'

			t1 = ''
			tmp = buffer2.counter
			for i in range(tmp):
				t1 += buffer2.arr[i]
				t1 += '\n'

			t2 = ''
			tmp = buffer3.counter
			for i in range(tmp):
				t2 += buffer3.arr[i]
				t2 += '\n'

			# Update `buffer1Label`
			buffer1Label.config(text=t)

			# Update `buffer2Label`
			buffer2Label.config(text=t1)

			# Update `buffer3Label`
			buffer3Label.config(text=t2)

			# Update `blocked_num`
			blocked_num.config(text=str(blocked_thread))

			putLabel1.config(text='',bg='green')
			putLabel2.config(text='',bg='green')
			putLabel3.config(text='',bg='green')
			moveLabel1.config(text='',bg='green')
			moveLabel2.config(text='',bg='green')
			getLabel1.config(text='',bg='green')
			getLabel2.config(text='',bg='green')
			master.update_idletasks()

			# Change the put, move, get label's color
			select1 = random.randint(0,2)
			if select1 == 0:
				putLabel1.config(text='===>',fg='red',bg='white')
			elif select1 == 1:
				putLabel2.config(text='===>',fg='red',bg='white')
			else:
				putLabel3.config(text='===>',fg='red',bg='white')

			select2 = random.randint(0,1)
			if select2 == 0:
				moveLabel1.config(text='===>',fg='red',bg='white')
			else:
				moveLabel2.config(text='===>',fg='red',bg='white')

			select3 = random.randint(0,1)
			if select3 == 0:
				getLabel1.config(text='===>',fg='red',bg='white')
			else:
				getLabel2.config(text='===>',fg='red',bg='white')

			# Redraw the Main Window
			master.update_idletasks()

			# Clear the screen
			#subprocess.call(['clear'])
			master.after(interval,show)
		
############################## End Productor-Consumer #################################

if __name__ == '__main__':
	""" Begin """

	show()

	master.mainloop()

	thr1.join()
	if getThreadNum > 1:
		thr2.join()
	for thread in threads:
		thread.join()
	playThr.join()
