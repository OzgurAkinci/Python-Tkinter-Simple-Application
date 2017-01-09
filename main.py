'''
IMDB - Python
'''

import tkinter
import tkinter.messagebox
import tkinter.ttk as ttk
import tkinter.font as tkFont
import tkinter as tk
from tkinter import *
import os.path
import sqlite3

class ImdbApplication(tkinter.Frame):
	results = ["","","","","","","","","","","","", 0, 0, 0, 0]
	selectID = 0
    
	def __init__(self, parent):
		tkinter.Frame.__init__(self, parent)
		self.conn = sqlite3.connect('imdb.db') #create a connection
		self.curse = self.conn.cursor()
		self.CreateImdbApplicationTable()
		self.parent = parent
		self.parent.title('IMDB')
		self.initUI()
		self.pack(expand=True, fill=tkinter.BOTH)
		
		
	def initUI(self):

		titles = ['Film Adı:','Yap. Yılı:','Yönetmen:']
	
		self.searchlabel = tkinter.Label(self, text = "Film Ara:")
		self.searchlabel.pack()
		self.searchlabel.place(x = 20, y = 30, height=25)
		
		for i in range(3):
			l = tkinter.Label(self, text=titles[i], fg='black')
			l.place(x = 20, y = 30 + (i+2)*30, height=25)

		self.eFName = tkinter.Entry()
		self.eFName.place(x = 160, y = 90, width=140, height=25)
		self.eFName.configure(background="#fff", highlightbackground="#333", highlightcolor="#fff",font=("Arial", 10, "bold"))
		self.eLName = tkinter.Entry()
		self.eLName.place(x = 160, y = 120, width=140, height=25)
		self.eLName.configure(background="#fff", highlightbackground="#333", highlightcolor="#fff",font=("Arial", 10, "bold"))
		self.ePhone = tkinter.Entry()
		self.ePhone.place(x = 160, y = 150, width=140, height=25)
		self.ePhone.configure(background="#fff", highlightbackground="#333", highlightcolor="#fff",font=("Arial", 10, "bold"))
		self.SearchEntry = tkinter.Entry()
		self.SearchEntry.place(x = 160, y = 30, width=140, height=25)
		self.SearchEntry.configure(background="#fff", highlightbackground="#333", highlightcolor="#fff",font=("Arial", 10, "bold"))
		
		self.imdb_puan = tkinter.Spinbox(values=("IMDB PUANI","9+", "8+", "7+", "6+"))
		self.imdb_puan.place(x = 460, y = 30, width=140, height=25)
		self.imdb_puan.configure(background="#fff", highlightbackground="#333", highlightcolor="#fff",font=("Arial", 10, "bold"))
        
		self.searchButton = tkinter.Button(text = "Ara", fg='#fff', command=self.bSearch)
		self.searchButton.configure(background="#333",highlightbackground="#0CD9E8", highlightcolor="#0DFFCC",font=("Arial", 10, "bold"))
		self.searchButton.pack()
		self.searchButton.place(x = 330, y = 30, width=80, height=25)
		
		self.clearButton = tkinter.Button(self, text = "Temizle", fg='#fff', command=self.clearInputs)
		self.clearButton.configure(background="#333",highlightbackground="#0CD9E8", highlightcolor="#0DFFCC",font=("Arial", 10, "bold"))
		self.clearButton.pack()
		self.clearButton.place(x = 330, y = 190, width=80, height=25)
		self.saveButton = tkinter.Button(self, text = "Kaydet", fg='#fff', command=self.addB)
		self.saveButton.configure(background="#333", highlightbackground="#0CD9E8", highlightcolor="#0DFFCC",font=("Arial", 10, "bold"))
		self.saveButton.pack()
		self.saveButton.place(x = 160, y = 190, width=70, height=25)
		self.removeButton = tkinter.Button(self, text = "Kaldır", fg='#fff', command=self.deleteB)
		self.removeButton.configure(background="#333",highlightbackground="#0CD9E8", highlightcolor="#0DFFCC",font=("Arial", 10, "bold"))
		self.removeButton.pack()
		self.removeButton.place(x = 240, y = 190, width=60, height=25)
		
		self.tree_header = ['Film Adı', 'Yapım Yılı', 'Yönetmen']
		self.tree_list = self.getFilms()
		self.tree = ttk.Treeview(columns=self.tree_header, show="headings")  
		vsb = ttk.Scrollbar(orient="vertical",command=self.tree.yview)
		hsb = ttk.Scrollbar(orient="horizontal",command=self.tree.xview)
		self.tree.configure(yscrollcommand=vsb.set,xscrollcommand=hsb.set)
		ttk.Style().configure("Treeview", background="#fff",foreground="#333", fieldbackground="#eee",font=("Arial", 12, "bold"))
		self.tree.pack()
		self.tree.place(x = 20, y = 250, width=700, height=210)
		self._build_tree()


	def CreateImdbApplicationTable(self):
		sql = '''CREATE TABLE IF NOT EXISTS films (film_adi text, yapim_yili text, yonetmen text,ozet text, imdb_puani text, ID integer PRIMARY KEY AUTOINCREMENT)'''
		self.curse.execute(sql)
		self.conn.commit()
        
	def getFilms(self):
		connx = sqlite3.connect('imdb.db')
		c = connx.cursor()
		films = c.execute('SELECT film_adi,yapim_yili,yonetmen,ozet,imdb_puani FROM films').fetchall()
		return films

	def bSearch(self):
		if (len(self.SearchEntry.get()) == 0) and (self.imdb_puan.get() == 'IMDB PUANI'):
			tkinter.messagebox.showinfo('Mesaj', 'Bir arama kriteri belirleyin.')
		else:
			if (len(self.SearchEntry.get()) != 0) and (self.imdb_puan.get() != 'IMDB PUANI'): #Yani ikiside doluysa
				tkinter.messagebox.showinfo('Mesaj', 'Tek kriter belirleyin..')
			else:
				if self.imdb_puan.get() == 'IMDB PUANI': #Yani sadece film_adi kriteri doluysa
					film_adi = (self.SearchEntry.get(),)
					sql = '''SELECT * FROM films where film_adi = ?'''
					self.curse.execute(sql, film_adi)
					rows = self.curse.fetchall()
					if rows:		
						for i in self.tree.get_children():
		   					self.tree.delete(i)
						for item in rows:
							self.tree.insert('', 'end', values=item)
							self.tree.bind("<ButtonRelease-1>", self.clickItem)
							self.tree.bind("<Double-1>", self.selectItem)
					else:
						self.initUI()
						tkinter.messagebox.showinfo('Mesaj', 'Sonuç bulunamadı..')
				else: #Yani sadece IMDB kriteri doluysa
					imdb_pu = self.imdb_puan.get()[:-1] # [:-1] son karakteri yani +'yi silmek icin kullandik
					sql = '''SELECT * FROM films where imdb_puani >= ?'''
					self.curse.execute(sql, imdb_pu)
					rows = self.curse.fetchall()
					if rows:		
						for i in self.tree.get_children():
		   					self.tree.delete(i)
						for item in rows:
							self.tree.insert('', 'end', values=item)
							self.tree.bind("<ButtonRelease-1>", self.clickItem)
							self.tree.bind("<Double-1>", self.selectItem)

	def bFill(self, n):
		self.SetEntryText(self.eFName, self.results[n])
		self.SetEntryText(self.eLName, self.results[n+4])
		self.SetEntryText(self.ePhone, self.results[n+8])

	def addB(self):
		if self.eFName.get() != '':
			new_record = [(self.eFName.get(),self.eLName.get(),self.ePhone.get())]
			#Film adinin bulunup bulunmadiginin kontrolu yapiliyor.
			connx = sqlite3.connect('imdb.db')
			c = connx.cursor()
			c.execute('SELECT COUNT(*) FROM films WHERE film_adi = ?',(self.eFName.get(),))
			films = c.fetchone()[0]
			if films==0:
				for item in new_record:
						self.tree.insert('', 'end', values=item)
				db = sqlite3.connect('imdb.db')
				cursor = db.cursor()
				cursor.execute('''INSERT INTO films (film_adi, yapim_yili, yonetmen, ozet, imdb_puani) VALUES(?,?,?,?,?)''', (self.eFName.get(), self.eLName.get(), self.ePhone.get(), "","0"))
				db.commit()
				tkinter.messagebox.showinfo('Mesaj', 'Başarıla Eklendi..')
			else:
				tkinter.messagebox.showinfo('Mesaj', '""'+self.eFName.get()+'""'+' filmi zaten bulunuyor..')
		else:
			tkinter.messagebox.showinfo('Mesaj', '"Film Adı" boş olamaz.')

	def deleteB(self):
		try:
			selected_item = self.tree.selection()[0]
			film_adi = self.tree.item(self.tree.selection())['values'][0]
			tkinter.messagebox.showinfo('Mesaj', '"'+film_adi+'"'+ ' kaldırıldı.. ')
			sql = '''DELETE FROM films WHERE film_adi = ? '''
			self.curse.execute(sql, (film_adi,))
			self.conn.commit()
			self.tree.delete(self.tree.selection()[0])
		except IndexError:
			tkinter.messagebox.showinfo('Mesaj', 'Seçilmedi !')

		
		
	def CreateIMDBTable(self):
		sql = '''CREATE TABLE IF NOT EXISTS films (film_adi text, yapim_yili text, yonetmen text, ozet text, imdb_puani text)'''
		self.curse.execute(sql)
		self.conn.commit()

	def SetEntryText(self, txtObject, value):
		txtObject.delete(0, tkinter.END)
		txtObject.insert(0, value)
	
	def __del__(self):
		self.conn.close() #close the connection when the Window is closed
    
	def _build_tree(self):
		for col in self.tree_header:
			self.tree.heading(col, text=col.title(),command=lambda c=col: self.tree,anchor=tk.W)
			self.tree.column(col,width=140,anchor=tk.W)
		for item in self.tree_list:
			self.tree.insert('', 'end', values=item)
			self.tree.bind("<ButtonRelease-1>", self.clickItem)
			self.tree.bind("<Double-1>", self.selectItem)


	def selectItem(self, event):
			curItem = self.tree.focus()
			t_new = tk.Toplevel(takefocus = True)
			t_new.geometry('400x500')
			t_new.resizable(width='FALSE', height='FALSE')
			t_new.wm_title("%s - %s" % (self.tree.item(curItem)['values'][0], self.tree.item(curItem)['values'][1]))

			connx = sqlite3.connect('imdb.db')
			c = connx.cursor()
			films = c.execute('SELECT * FROM films WHERE film_adi = ?',(self.tree.item(curItem)['values'][0],)).fetchall()


			l1 = tkinter.Label(t_new, text="Film Adı", fg='black')
			l1.place(x = 7, y = 10, height=25)
			self.e1 = tkinter.Entry(t_new)
			self.e1.place(x = 10, y = 30, width=190, height=25)
			self.e1.configure(background="#fff", highlightbackground="#333", highlightcolor="#fff",font=("Arial", 10, "bold"))
			self.SetEntryText(self.e1,self.tree.item(curItem)['values'][0])
			
			l2 = tkinter.Label(t_new, text="Film Yapımcısı", fg='black')
			l2.place(x = 7, y = 60, height=25)
			self.e2 = tkinter.Entry(t_new)
			self.e2.place(x = 10, y = 80, width=190, height=25)
			self.e2.configure(background="#fff", highlightbackground="#333", highlightcolor="#fff",font=("Arial", 10, "bold"))
			self.SetEntryText(self.e2,self.tree.item(curItem)['values'][2])

			l3 = tkinter.Label(t_new, text="Film Tarihi", fg='black')
			l3.place(x = 7, y = 110, height=25)
			self.e3 = tkinter.Entry(t_new)
			self.e3.place(x = 10, y = 130, width=190, height=25)
			self.e3.configure(background="#fff", highlightbackground="#333", highlightcolor="#fff",font=("Arial", 10, "bold"))
			self.SetEntryText(self.e3,self.tree.item(curItem)['values'][1])

			l3 = tkinter.Label(t_new, text="Film Özet,", fg='black')
			l3.place(x = 7, y = 160, height=25)
			self.e4 = tkinter.Text(t_new)
			self.e4.place(x = 10, y = 180, width=290, height=85)
			self.e4.configure(background="#fff", highlightbackground="#333", highlightcolor="#fff",font=("Arial", 10, "bold"))
			self.e4.insert(INSERT, films[0][3])


			l4 = tkinter.Label(t_new, text="IMDB Puanı", fg='black')
			l4.place(x = 7, y = 270, height=25)
			self.e5 = tkinter.Entry(t_new)
			self.e5.place(x = 10, y = 290, width=190, height=25)
			self.e5.configure(background="#fff", highlightbackground="#333", highlightcolor="#fff",font=("Arial", 10, "bold"))
			imdb_p = films[0][4]
			if imdb_p is None:
				imdb_p = '0.0'
			self.SetEntryText(self.e5,imdb_p)

			self.saveDetailButton = tkinter.Button(t_new, text = "Kaydet", fg='#fff', command=self.saveDetail)
			self.saveDetailButton.configure(background="#333", highlightbackground="#0CD9E8", highlightcolor="#0DFFCC",font=("Arial", 10, "bold"))
			self.saveDetailButton.pack()
			self.saveDetailButton.place(x = 10, y = 320, width=108, height=25)
 
	def saveDetail(self):
		film_adi = self.e1.get()
		film_tarihi = self.e3.get()
		film_yapimcisi = self.e2.get()
		film_ozeti = self.e4.get("1.0",END)
		film_imdb_puani = self.e5.get()
		db = sqlite3.connect('imdb.db')
		cursor = db.cursor()
		cursor.execute('UPDATE films SET film_adi=?, yapim_yili=?, yonetmen=?, ozet=?, imdb_puani=? WHERE film_adi=?',(film_adi,film_tarihi,film_yapimcisi,film_ozeti,film_imdb_puani,film_adi,))
		db.commit()

		for i in self.tree.get_children():
			self.tree.delete(i)
		for item in self.getFilms():
			self.tree.insert('', 'end', values=item)
			self.tree.bind("<ButtonRelease-1>", self.clickItem)
			self.tree.bind("<Double-1>", self.selectItem)

		tkinter.messagebox.showinfo('Mesaj', 'Değişiklikler gerçekleştirildi..')

	def clickItem(self, event):
		curItem = self.tree.focus()
		film_adi = str(self.tree.item(curItem)['values'][0])
		yapim_yili = str(self.tree.item(curItem)['values'][1])
		yonetmen = str(self.tree.item(curItem)['values'][2])
		self.SetEntryText(self.eFName, film_adi)
		self.SetEntryText(self.eLName, yapim_yili)
		self.SetEntryText(self.ePhone, yonetmen)

	def clearInputs(self):
		self.SetEntryText(self.eFName, "")
		self.SetEntryText(self.eLName, "")
		self.SetEntryText(self.ePhone, "")
		self.SetEntryText(self.SearchEntry, "")

		for i in self.tree.get_children():
			self.tree.delete(i)
		for item in self.getFilms():
			self.tree.insert('', 'end', values=item)
			self.tree.bind("<ButtonRelease-1>", self.clickItem)
			self.tree.bind("<Double-1>", self.selectItem)


def main():
	root = tkinter.Tk()
	root.geometry('750x500')
	root.resizable(width='FALSE', height='FALSE')
	root.option_add("*background", "#fff373")
	app = ImdbApplication(root)
	
	root.mainloop()
	
	
if __name__ == "__main__":
	main()
