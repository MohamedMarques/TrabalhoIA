from tkinter import * # para fazer a interface grafica do meu jogo
from Solver import Solver
from State import State
#from Euclidean import Euclidean APAGAR
from Profundidade import Profundidade
from Extensao import Extensao
import os
import sys

class Main:
                
	def __init__(self):  #função para iniciar janela
		self.started = False
		self.homePage = False

		self.frame1 = Tk() #crio janela 
		self.frame1.title("Trabalho IA") #nomeia o titulo da janela
		
		Grid.rowconfigure(self.frame1, 0, weight=1)
		Grid.columnconfigure(self.frame1, 0, weight=1)

		self.boardFrame = Frame(self.frame1,bg = "white") #cor do fundo do frame
		a = int(input("C(1),L(1) :")) # define numero na linha 1 coluna 1
		b = int(input("C(2),L(1) :")) # define numero na linha 1 coluna 2
		c = int(input("C(3),L(1) :")) # define numero na linha 1 coluna 3
		d = int(input("C(1),L(2) :")) # define numero na linha 2 coluna 1
		e = int(input("C(2),L(2) :")) # define numero na linha 2 coluna 2
		f = int(input("C(3),L(2) :")) # define numero na linha 2 coluna 3
		g = int(input("C(1),L(3) :")) # define numero na linha 3 coluna 1
		h = int(input("C(2),L(3) :")) # define numero na linha 3 coluna 2
		i = int(input("C(3),L(3) :")) # define numero na linha 3 coluna 3
		print(f"[{a}] [{b}] [{c}]\n[{d}] [{e}] [{f}]\n[{g}] [{h}] [{i}]")
		resposta = str(input("y/n:")) #recebe o que foi digitado
		exit(0) if resposta == "n" else print("Sucess,continua na janela...") if resposta == "y" else print("Error")
		self.board = [[a,b,c],[d,e,f],[g,h,i]] # recebe a matriz
		
		self.labels = [[0 for x in range(3)] for y in range(3)] # Define as labels e suas posições em cima do fundo branco,labels= quadradinhos
		for i in range(0,3):
			Grid.rowconfigure(self.boardFrame, i, weight=1)
			for j in range(0,3):
                        
				Grid.columnconfigure(self.boardFrame, j, weight=1)
				if not (i == 0 and j == 0):
					self.labels[i][j] = Button(self.boardFrame,text=str(i*3+j),height = 10, width = 30,bg='BLACK',fg='WHITE')
                                         # cada label vira um botão
		
		self.labels[0][1].config(command = lambda:self.move(1))
		self.labels[0][2].config(command = lambda:self.move(2))

		self.labels[1][0].config(command = lambda:self.move(3))
		self.labels[1][1].config(command = lambda:self.move(4))
		self.labels[1][2].config(command = lambda:self.move(5))

		self.labels[2][0].config(command = lambda:self.move(6))
		self.labels[2][1].config(command = lambda:self.move(7))
		self.labels[2][2].config(command = lambda:self.move(8))

		self.BottomFrame = Frame(self.frame1,bg = "white")
		self.labelsFrame = Frame(self.BottomFrame,bg = "white")
		self.ButtonsFrame = Frame(self.BottomFrame,bg = "gray")
		Grid.rowconfigure(self.BottomFrame, 0, weight=1)
		Grid.columnconfigure(self.BottomFrame, 0, weight=1)
		

		self.startButton = Button(self.ButtonsFrame,bg='white',fg='RED',font=('Times 18 bold'),text='Start',command =lambda:self.start())
		


		#Empacotando label e botões

		self.startButton.pack(side=RIGHT)		
		
		self.labelsFrame.grid(row=0,column=0,sticky="nsew")
		self.ButtonsFrame.grid(row=1,column=0,sticky="nsew")

		

		




	def start(self): #função que recebe os botões  e encaminha cada função pertinente e atualiza apos o start
		self.started = True
		self.homePage = False
		self.startButton.pack_forget()
		self.initialBoard = self.board		
		self.buttons = []
		for i in range(0,4):
			button = Button(self.ButtonsFrame,bg='white',fg='#444488',font=('Times 18 bold'))
			self.buttons.append(button) 
			self.buttons[i].pack(side=LEFT,expand=YES,fill=BOTH)
		initialState = State(self.board,'',None)
		self.buttons[0].config(text=' Profundidade ',command =lambda: self.solveButtonAction(Profundidade(initialState)))
		self.buttons[1].config(text=' Extensao ',command =lambda: self.solveButtonAction(Extensao(initialState)))
		
		self.nextButton = Button(self.ButtonsFrame,bg='white',fg='#444488',text=' PROXIMO >>',font=('Times 18 bold'),command =lambda:self.nextButtonAction())
		self.previousButton = Button(self.ButtonsFrame,bg='white',fg='#444488',text='<< VOLTAR ',font=('Times 18 bold'),state=DISABLED,command =lambda:self.previousButtonAction())
		self.endButton = Button(self.ButtonsFrame,bg='white',fg='#444488',text=' FIM ',font=('Times 18 bold'),command =lambda:self.endButtonAction())
		self.beginButton = Button(self.ButtonsFrame,bg='white',fg='#444488',text=' COMEÇO ',font=('Times 18 bold'),command =lambda:self.beginButtonAction())

		self.costLabel = Label(self.labelsFrame,bg='white',fg='#888888')
		self.exploredLabel = Label(self.labelsFrame,bg='white',fg='#888888')
		self.depthLabel = Label(self.labelsFrame,bg='white',fg='#888888')
		self.timeLabel = Label(self.labelsFrame,bg='white',fg='#888888')
		self.stepsLabel = Label(self.labelsFrame,bg='white',fg='#444488')	


	def display(self):    #função responsavel por mapear as labels
		for i in range(0,3):
			for j in range(0,3):
				if (self.board[i][j] != 0):
					x,y = divmod(self.board[i][j],3)
					self.labels[x][y].grid(row=i,column=j,sticky="nsew")
					

	def position(self,number):   #função responsavel por 
		for i in range(0,3):
			for j in range(0,3):
				if self.board[i][j] == number:
					return [i,j]
		return [0,0]


	def move(self,no):           # função responsavel por mover as labels e atualizar o frame
		if not self.started:
			x,y = map(int,self.position(0))
			i,j = map(int,self.position(no))
			if((i==x-1 and j==y) or (i==x+1 and j==y) or (i==x and j==y-1) or (i==x and j==y+1) ):
				self.board[i][j],self.board[x][y]=self.board[x][y],self.board[i][j]
			self.display()
	

	def solveButtonAction(self,solver):
		self.homePage = False
		self.solver = solver
		self.solver.solve()
		self.solutionPath = self.solver.finalState.getPath()
		self.noOfSteps = len(self.solutionPath)-1
		if self.noOfSteps == 0:
			self.nextButton.config(state=DISABLED) #botão de proximo normalmente desabilitado
			self.endButton.config(state=DISABLED) #botão de ultimo normalmente desabilitado
		self.currentStep = 0

		for i in range(0,4):
			self.buttons[i].pack_forget()
		self.costLabel.config(text='custo do caminho:: {}'.format(solver.finalState.f)) # label do custo do caminho
		self.exploredLabel.config(text='    nós expandidos: {}'.format(solver.expandedNodes)) # label de nos expandidos
		self.depthLabel.config(text='    profundidade de pesquisa: {}'.format(solver.depth)) #label de profundade de pesquisa
		self.timeLabel.config(text='     tempo de execução: {}'.format(solver.runningTime) + ' seconds') #label de tempo de execução
		self.stepsLabel.config(text='MOVIMENTOS: {}/{}'.format(self.currentStep,self.noOfSteps)) #label de movimentos
		
		self.costLabel.pack(side=LEFT) #Empacotando label do custo do caminho
		self.exploredLabel.pack(side=LEFT) #Empacotando label de nos expandidos
		self.depthLabel.pack(side=LEFT) #Empacotando label de profundade de pesquis
		self.timeLabel.pack(side=LEFT) #Empacotando label de tempo de execução
		self.stepsLabel.pack(side=RIGHT) #Empacotando label de movimentos	 

		self.nextButton.pack(side=RIGHT) #Empacotando botão de proximo
		self.previousButton.pack(side=RIGHT) #Empacotando botão de anterior	
		self.beginButton.pack(side=RIGHT) #Empacotando botão de primeiro
		self.endButton.pack(side=RIGHT) #Empacotando botão de ultimo


	def nextButtonAction(self): #visualizar e ir ao movimento proximo
			if self.currentStep < self.noOfSteps:
				self.currentStep += 1
				self.stepsLabel.config(text = 'MOVIMENTOS: {}/{}'.format(self.currentStep,self.noOfSteps))
				if self.currentStep == self.noOfSteps:
					self.nextButton.config(state=DISABLED)
					self.endButton.config(state=DISABLED)
				self.board = self.solutionPath[self.currentStep].board
				self.display()
				if self.currentStep > 0:
					 self.beginButton.config(state="normal")
					 self.previousButton.config(state="normal")
			else:
				self.endButton.config(state=DISABLED)
				self.nextButton.config(state=DISABLED)

	def previousButtonAction(self): #visualizar e ir ao movimento anterior
			if self.currentStep > 0:
				self.currentStep -= 1
				self.stepsLabel.config(text = 'MOVIMENTOS: {}/{}'.format(self.currentStep,self.noOfSteps))
				if self.currentStep == 0:
					self.previousButton.config(state=DISABLED)
					self.beginButton.config(state=DISABLED)
				self.board = self.solutionPath[self.currentStep].board
				self.display()
				if self.currentStep < self.noOfSteps:
					 self.endButton.config(state="normal")
					 self.nextButton.config(state="normal")
			else:
				self.previousButton.config(state=DISABLED)
				self.beginButton.config(state=DISABLED)

	def beginButtonAction(self): # função para ir e visualizar o primeiro movimento posivel
			self.currentStep = 0
			self.stepsLabel.config(text = 'MOVIMENTOS: {}/{}'.format(self.currentStep,self.noOfSteps))
			self.board = self.solutionPath[self.currentStep].board
			self.display()
			self.beginButton.config(state=DISABLED)
			self.previousButton.config(state=DISABLED)
			self.endButton.config(state="normal")
			self.nextButton.config(state="normal")

	def endButtonAction(self): # função para ir e visualizar ate o ultimo movimento posivel
			self.currentStep = self.noOfSteps
			self.stepsLabel.config(text = 'MOVIMENTOS: {}/{}'.format(self.currentStep,self.noOfSteps))
			self.board = self.solutionPath[self.currentStep].board
			self.display()
			self.endButton.config(state=DISABLED)
			self.nextButton.config(state=DISABLED)
			self.beginButton.config(state="normal")
			self.previousButton.config(state="normal")

	def run(self):
		self.display()
		self.boardFrame.grid(row=0,column=0,sticky="nsew")
		self.BottomFrame.grid(row=1,column=0,sticky="nsew")
		self.frame1.mainloop()

exe = Main()
exe.run()
