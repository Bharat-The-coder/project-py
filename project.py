import tkinter as tk
from tkinter import filedialog
from PIL import Image,ImageTk
import PIL.Image
from pytesseract import image_to_string
import pytesseract
import threading
import img2pdf
import os.path
import threading
import cv2
import img_pro
headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 12)
entryfont = ('Garamond', 12)
class InvoiceApp:
    def __init__(self, master):
        global selected_file,img_list,pdf_list,invoice_list
        self.master = master
        master.title("INVOICE HANDLING")
        master.geometry('950x600')
        photo=ImageTk.PhotoImage(file = r"asset/icon.png")
        master.iconphoto(False, photo)
        master.resizable(False,False)
        master['bg'] = 'Sky blue'
        self.tpo_lebel= tk.Label(master, text="INVOICE HANDLING", width=80, font=headlabelfont, bg='Black',fg='White').place(relx=0.00, rely=0.0)
        len_file=0
        self.converted_file_len=0
        self.folder_path=""
        # Path Selection
        self.path_label = tk.Label(master, text="Select Path",font=labelfont,bg="Sky blue")
        self.path_label.place(relx=0.05, rely=0.1)
        self.path_entry = tk.Label(master,width=60,font=entryfont,text=self.folder_path)
        self.path_entry.place(x=160, rely=0.1)
        self.browse_button = tk.Button(master, text="Browse",font=labelfont, width=15, bg='Purple',fg='White', command=self.browse_folder)
        self.browse_button.place(relx=0.80, rely=0.09)
        #File process 
        self.file_label = tk.Label(master, text="File Process",font=labelfont,bg="Sky blue").place(relx=0.05, rely=0.19)
        self.file_listbox = tk.Listbox(master,width=20,font=entryfont)
        self.file_listbox.place(x=30, rely=0.25, height=195)
        #selected_file= self.file_listbox.get(self.file_listbox.curselection()) 
        self.count_label = tk.Label(master, text="Count",font=labelfont,bg="Sky blue").place(relx=0.03, rely=0.60)
        self.count_entry = tk.Label(master,width=10,font=entryfont,text=len_file)
        self.count_entry.place(x=82, rely=0.60)
        
        # Table Creation
        self.table_label = tk.Label(master, text="Converted Files",bg="Sky blue",font=labelfont)
        self.table_label.place(relx=0.250, rely=0.38)
        #list of file names
        self.file_name_label = tk.Label(master, text="File Name",bg="Sky blue",font=labelfont)
        self.file_name_label.place(relx=0.265, rely=0.45)
        self.file_name_listbox = tk.Listbox(master,width=20)
        self.file_name_listbox.place(relx=0.250, rely=0.52, height=195)
        #list of invoice number
        self.invoice_label = tk.Label(master, text="Invoice Number",bg="Sky blue",font=labelfont)
        self.invoice_label.place(relx=0.400, rely=0.45)
        self.invoice_listbox = tk.Listbox(master,width=18)
        self.invoice_listbox.place(relx=0.400, rely=0.52, height=195)
        #list of converted files
        self.created_label = tk.Label(master, text="Converted PDF",bg="Sky blue",font=labelfont)
        self.created_label.place(relx=0.600, rely=0.45)
        self.created_listbox = tk.Listbox(master,width=23)
        self.created_listbox.place(relx=0.600, rely=0.52, height=195)
        self.table_count_label = tk.Label(master, text="Converted File Count",bg="Sky blue",font=labelfont)
        self.table_count_label.place(relx=0.250, rely=0.88)
        self.count_all_entry = tk.Label(master,width=8,font=entryfont,text=0)
        self.count_all_entry.place(x=395, rely=0.88)
        # Scan Button
        self.scan_button = tk.Button(master, text="Scan",font=labelfont, width=15, bg='Purple',fg='White', command=threading.Thread(target=self.scan).start)
        self.scan_button.place(relx=0.250, rely=0.28)
        self.message_label = tk.Label(master, text="",bg="Sky blue",font=labelfont)
        self.message_label.place(relx=0.50, rely=0.28)
    #delete files of temp folder
    def delete_all_files(self):
        dir="temp/"
        for file in os.listdir(dir):
            os.remove(os.path.join(dir,file))
    #function to upload a folder
    def browse_folder(self):        
        folder_path = filedialog.askdirectory()
        self.folder_path=folder_path
        #if folder path is not empty
        if folder_path: 
            self.file_listbox.delete(0,tk.END)
            self.path_entry.config(text=folder_path)
            self.file_list = os.listdir(folder_path)
            for file_name in self.file_list:
                #image from different extension can be access 
                if (file_name.endswith(".png")) or (file_name.endswith(".jpg")) or (file_name.endswith(".jpeg")) or (file_name.endswith(".btp")):
                    self.file_listbox.insert(tk.END,file_name)
            self.count_entry.configure(text=len(self.file_list))
            self.path_entry.configure(text=self.folder_path)
    def scan(self):
        global img,img_name
        # Code to scan data
        for file_name in range(len(self.file_list)):  
                #Get all files 
                img_name=self.file_listbox.get(file_name)
                img=self.folder_path+"/"+img_name
                if img_name!="":
                    img_pro.process_img(img)
                    self.message_label.configure(text="Image Scanned successfully")
                    #img=r"C://Users/Bharat/OneDrive/Documents/PROJECT/temp/inverted.jpg"
                    threading.Thread(target=self.convert(img)).start
                    self.delete_all_files() 
        self.message_label.configure(text="All files processed") 
    #This function to Convert OCR image and Search Invoice number
    def convert(self,img):
        global output
        cnf=r"--psm 11 --oem 3"
        #code for ocr engine to convert image to text
        try:
            output =pytesseract.image_to_string(PIL.Image.open(img),config=cnf,lang='eng')
            if output !="":
                text=("Convertion in Process")
                self.file_name_listbox.insert(tk.END,img_name)
                threading.Thread(target=self.search()).start
        except:
            text=("Error! Can not convert image to text \ntry to scan image first")
        self.message_label.configure(text=text)
    def search(self):
        word=output.split()
        #searching invoice no code                          
        invoice=['invoiceno.:','invoicenumber','invoice_no','invoice-no','invoice_no.','invoiceno:']
        list=[]
        for index in range(len(word)):
                if word[index].lower() in invoice:
                        list.append(word[index+1].lower())
                        list.append(word[index+2].lower())
                        list.append(word[index+3].lower())
                        list.append(word[index+4].lower())
                elif word[index].lower() =="invoice":
                        if word[index+1].lower()=='no.' or word[index+1].lower()=='no:' or word[index+1].lower()=='no':
                            list.append(word[index+2].lower())
                            list.append(word[index+3].lower())
                            list.append(word[index+4].lower())
        for item in list:
                if item.isnumeric()==True and len(item)==10:
                    file_name=item
                elif item.isnumeric()==True and len(item)==11:
                    file_name=item[1:]
                elif item.isnumeric()==True and len(item)==7:
                    file_name=item
                elif item.isnumeric()==True and len(item)>=3:
                    file_name=item
        #print(list)
         # if file name is not empty this block store pdf
        if file_name!="":
            self.invoice_listbox.insert(tk.END,file_name)
            threading.Thread(target=self.store(file_name)).start
        else:
            text=("Error! Invoice Number not Recognized,\n Rescan the Document")
            self.invoice_listbox.insert(tk.END,"Not found")
    #This is used to store a file created
    def store(self,file_name):
                    try:
                        #saving pdf with invoice no name          
                        # storing image path
                        img_path =img
                        # storing pdf path
                        pdf_path = r"invoice/"+file_name+"_INVOICE"+'.pdf'
                        #opening image
                        image = Image.open(img_path)
                        file_exists = os.path.exists(pdf_path)
                        if file_exists:
                            text=("["+pdf_path+"] file already present,\n Could not save this file")
                            self.created_listbox.insert(tk.END,"file already present")
                        else:  
                            self.converted_file_len+=1
                            self.created_listbox.insert(tk.END,"invoice/"+file_name+".pdf")
                            self.count_all_entry.configure(text=self.converted_file_len)
                            # converting into chunks using img2pdf
                            pdf_bytes = img2pdf.convert(image.filename)
                            # opening or creating pdf file
                            file = open(pdf_path, "wb")
                            # writing pdf files with chunks
                            file.write(pdf_bytes)
                            text=("["+pdf_path+"] stored successfully")
                    except:
                        text=("Error! File cant stored")
                    self.message_label.configure(text=text)    
root = tk.Tk()
app = InvoiceApp(root)
root.mainloop()
