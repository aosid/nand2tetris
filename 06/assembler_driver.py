from tkinter import filedialog
import assembler

filename = filedialog.askopenfilename()
initialfile=filename[:len(filename)-4]+".hack"

file = open(filename,"r")
lines = file.readlines()
file.close()

converted_file = assembler.ConvertFile(lines)

newfilename = filedialog.asksaveasfilename(initialfile=initialfile,defaultextension=".hack")
newfile = open(newfilename,"w")

for line in converted_file:
    newfile.write(line+"\n")
newfile.close()