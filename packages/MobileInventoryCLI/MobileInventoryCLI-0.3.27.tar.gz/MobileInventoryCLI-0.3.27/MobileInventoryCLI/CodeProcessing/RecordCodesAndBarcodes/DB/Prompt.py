#Prompt.py
from colored import Fore,Style 

class Prompt:
	state=True
	def __init__(self,func,ptext='do what',helpText='',data={}):
		while True:
			cmd=input(f'{Fore.light_yellow}{ptext}{Style.reset}:{Fore.light_green} ')
			print(Style.reset,end='')
			
			if cmd.lower() in ['q','quit']:
				exit('quit')
			elif cmd.lower() in ['b','back']:
				return
			elif cmd.lower() in ['?','h','help']:
				print(helpText)
			else:
				func(cmd,data)

	def __init2__(self,func,ptext='do what',helpText='',data={}):
		while True:
			cmd=input(f'{Fore.light_yellow}{ptext}{Style.reset}:{Fore.light_green} ')
			print(Style.reset,end='')
			
			if cmd.lower() in ['q','quit']:
				exit('quit')
			elif cmd.lower() in ['b','back']:
				return
			elif cmd.lower() in ['h','help']:
				print(helpText)

			else:
				return func(cmd,data)	
	#since this will be used statically, no self is required 
	#example filter method
	def cmdfilter(text,data):
		print(text)
if __name__ == "__main__":	
	Prompt(func=Prompt.cmdfilter,ptext='code|barcode',helpText='test help!',data={})
		

	