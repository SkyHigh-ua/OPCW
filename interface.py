import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy.linalg import det
from math import floor, ceil
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.ttk import *
import re
from Cramer import Cramer
from Gauswithsingdiagonal import Gauswithsingdiagonal
from Gauswithmainelement import Gauswithmainelement

class AppInterface(tk.Tk):
    '''
    Вікно програми
    '''
    def __init__(self):
        tk.Tk.__init__(self)
        container = self.container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        frame = self.menuframe = MainMenu(container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    # Створення фрейму розв'язку
    def create_resultmenu(self):
        frame = self.resultframe = ResultMenu(self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    # Виведення фрейму головного меню
    def show_mainmenu(self):
        frame = self.menuframe
        frame.tkraise()

class MainMenu(Frame):
    '''
    Головне меню програми
    '''
    def __init__(self, parent, root):
        Frame.__init__(self, parent)
        self.root = root
        widdata = self.widdata = []
        label = Label(self, text="Mетод:")
        label.place(x=20, y=12)
        combo = self.__combo = Combobox(self, values=["Крамера", "Гауса з одиничною діагоналлю", "Гауса з вибором головного елементу"], state="readonly") # Випадаючий список для вибору метода розв'язку
        combo.current(0)
        combo.place(x=70, y=10, width=275)
        bt = Button(self, text='Ok', command=self.dimension)
        bt.place(x=350, y=10)
        widdata.append(label)
        widdata.append(combo)
        widdata.append(bt)

    # Створення віджетів для вибору розмірності
    def dimension(self):
        self.clean()
        widdata = self.widdata
        label2 = Label(self, text="Розмірність:")
        label2.place(x=20, y=40)
        dmnsn = self.__dmnsn = Spinbox(self, from_=2, to_=7, width=2) 
        dmnsn.set('3')
        dmnsn.place(x=160, y=40)
        btn1 = Button(self, text="Ok", command=self.inputdata)
        btn1.place(x=280, y=40)
        widdata.append(dmnsn)
        widdata.append(btn1)
        widdata.append(label2)

    # Створення полів для введення системи
    def inputdata(self):
        self.clean()
        method = self.method = self.__combo.get()
        n = self.n = int(self.__dmnsn.get())
        if not n or not (n in range(2, 8)):
            messagebox.showerror("Помилка", "Неправильно введена розмірність")
            return
        matrixofstr = self.__matrixofstr = [[0] * n for i in range(0, n)]
        lstofstr = self.__lstofstr = [[0] for i in range(0, n)]
        if method == "Крамера":
            label4 = Label(self, text="=")
            label4.place(x=60+n*50, y=100 + n * 15)
            for i in range(0, n):
                for j in range(0, n):
                    matrixofstr[i][j] = Entry(self, justify = tk.CENTER)
                    matrixofstr[i][j].place(x=60 + j * 50, y=110 + i * 30, width=40, height=30)
                lstofstr[i] = Entry(self, justify = tk.CENTER)
                lstofstr[i].place(x=85+n*50, y=110 + i * 30, width=40, height=30)
        else: 
            for i in range(n):
                for j in range(n):                 
                    if j == (n - 1):
                        str = "x{}=".format(j+1)
                    else:
                        str = "x{}+".format(j+1)
                    label4 = Label(self, text=str)
                    matrixofstr[i][j] = Entry(self, justify = tk.CENTER)
                    label4.place(x=120 + j * 65, y=110 + i * 30, width=40, height=30)
                    matrixofstr[i][j].place(x=80 + j * 65, y=110 + i * 30, width=40, height=30)
                lstofstr[i] = Entry(self, justify = tk.CENTER)
                lstofstr[i].place(x=80 + n * 65, y=110 + 30 * i, width=40, height=30)
        label3 = Label(self, text="Введіть коефіцієнти нижче:")
        label3.place(x=20, y=80)
        btn3 = Button(self, text="Розв'язати", command = self.readdata)
        btn3.place(x=475, y=350)   

    # Зчитування системи
    def readdata(self):
        # Округлення числа за математичними правилами
        def roundnum(num):
            tnum = num * 10 ** 3
            if abs(tnum) - abs(floor(tnum)) < 0.5:
                return floor(tnum) / 10 ** 3
            return ceil(tnum) / 10 ** 3
        method = self.method
        n = self.n
        root = self.root
        MatrixA = self.MatrixA = [[0] * n for i in range(n)]
        LstB = self.LstB = [0 * n for i in range(n)]
        matrixofstr = self.__matrixofstr
        lstofstr = self.__lstofstr
        for i in range(n):
            for j in range(n):
                num = matrixofstr[i][j].get()
                val = self.validatenum(num)
                if val[0]:
                    MatrixA[i][j] = roundnum(float(num))
                else: 
                    return val[1]
        for i in range(n):
            num = lstofstr[i].get()
            val = self.validatenum(num)
            if val[0]:
                LstB[i] = roundnum(float(num))
            else: 
                return val[1]
        if det(MatrixA) == 0:
            messagebox.showerror("Помилка", "Визначник рівен 0")  
        else:
            if method == "Гауса з одиничною діагоналлю":
                if self.validatea():
                    messagebox.showerror("Помилка", "CЛАР неможливо розв'язати даним методом")
                else:
                    self.clean()
                    root.create_resultmenu() 
            else:
                self.clean()
                root.create_resultmenu()    
         
    # Валідація введеної системи для розв'язку методом Гауса з одиничною діагоналлю
    def validatea(self):
        MatrixA = self.MatrixA
        LstB = self.LstB
        n = self.n
        for i in range(n):
            if MatrixA[i][i] == 0:
                for j in range(i+1,n):
                    if MatrixA[j][i] != 0:
                        MatrixA[i], MatrixA[j] = MatrixA[j], MatrixA[i]
                        LstB[i], LstB[j] = LstB[j], LstB[i]
                    elif j==n-1:
                        return True 
        return False

    # Валідація числа
    def validatenum(self, num):
        if not num:
            return False, messagebox.showerror("Помилка", "Не всі поля заповнені")
        elif re.fullmatch(r'[-+]?\d+\.?\d*', num)==None:
            return False, messagebox.showerror("Помилка", "Введені некоректні символи")
        elif float(num)>=float(10**6) or float(num)<=-float(10**6):
            return False, messagebox.showerror("Помилка", "Введене {} число".format("завелике" if float(num)>0 else "замале"))
        else:
            return True, None

    # Очищення фрейму від віджетів
    def clean(self):
        widdata = self.widdata
        for widget in self.winfo_children():
                if widget not in widdata:
                    widget.destroy()

class ResultMenu(Frame):
    '''
    Меню результатів розв'язку
    '''
    def __init__(self, parent, root):
        Frame.__init__(self, parent)
        self.root = root
        self.MatrixA = root.menuframe.MatrixA
        self.LstB = root.menuframe.LstB
        self.n = root.menuframe.n
        self.method = root.menuframe.method
        self.__plotwinisopen = False
        self.__text = tk.Text(self, wrap=tk.NONE, highlightthickness = 0)
        self.__text.place(x=0, y=13, width= 600, height= 360)
        self.insmatrix()
        scrl = Scrollbar(self, orient='horizontal')
        scrl.pack(side = tk.TOP, fill = tk.X)
        scrl.config(command=self.__text.xview)
        self.__text.config(xscrollcommand= scrl.set)
        btn1 = Button(self, text="Меню", command = self.option)
        btn2 = Button(self, text="Зберегти", command = self.savefile)
        btn1.place(x=475, y=373)
        btn2.place(x=35, y=373)
        if self.method == "Крамера":
            self.Cramer()
        elif self.method == "Гауса з одиничною діагоналлю":
            self.Gauswsd()
        else:
            self.Gauswme()
        if self.n == 2:
            self.__btn3 = Button(self, text="Графік", command=self.plotwin)
            self.__btn3.place(x=135, y=373)
        root.protocol('WM_DELETE_WINDOW', lambda: self.option("DELETE_WINDOW"))

    # Розв'язок СЛАР методом Крамера
    def Cramer(self):
        MatrixA = self.MatrixA
        LstB = self.LstB
        n = self.n
        result = Cramer(MatrixA, LstB)
        x = self.x = result.solve()
        text = self.__text
        for i in range(n):
            text.insert(tk.END, "x{} = {:.3g}\n".format(i+1,x[i]))
        text.insert(tk.END, "\nСумарна кількість ітерацій  алгоритму: {}".format(n**3))

    # Розв'язок СЛАР методом Гауса з одиничною діагоналлю
    def Gauswsd(self):
        MatrixA = self.MatrixA
        LstB = self.LstB
        n = self.n
        result = Gauswithsingdiagonal(MatrixA, LstB)
        x = self.x = result.solve()
        text = self.__text
        for i in range(n):
            text.insert(tk.END, "x{} = {:.3g}\n".format(i+1,x[i]))
        text.insert(tk.END, "\nСумарна кількість ітерацій  алгоритму: {}".format(sum([(1+n)*(n-i)+(1+i) for i in range(n)])))

    # Розв'язок СЛАР методом Гауса з вибором головного елементу
    def Gauswme(self):
        MatrixA = self.MatrixA
        LstB = self.LstB
        n = self.n
        result = Gauswithmainelement(MatrixA, LstB)
        x = self.x = result.solve()
        text = self.__text
        for i in range(n):
            text.insert(tk.END, "x{} = {:.3g}\n".format(i+1,x[i]))
        text.insert(tk.END, "\nСумарна кількість ітерацій  алгоритму: {}".format(sum((n-k+1)*(n-k) for k in range(n-1))+n**2))

    # Створення вікна графічного розв'язку системи 2 на 2
    def plotwin(self):
        MatrixA = self.MatrixA
        LstB = self.LstB
        res = self.x
        feq = "{:g}x₁{:+g}x₂={:g}".format(MatrixA[0][0], MatrixA[0][1], LstB[0])
        seq = "{:g}x₁{:+g}x₂={:g}".format(MatrixA[1][0], MatrixA[1][1], LstB[1])
        plotwindow = self.plotwindow = tk.Tk()
        plotwindow.title("Графік")
        plotwindow.geometry('400x400+150+150')
        plotwindow.resizable(False, False)
        self.__btn3["state"] = tk.DISABLED
        self.__plotwinisopen = True
        tk.Button(plotwindow, text = "Зберегти", width=10, height=1, command = lambda: self.savefile("plot")).pack(side=tk.BOTTOM)
        fig = self.fig = plt.Figure(figsize=(10, 10), dpi=80)
        x = [res[0]-10, res[0]+10]
        y = lambda j: [(LstB[j] - MatrixA[j][0]*x[i])/MatrixA[j][1] for i in range(2)]
        fpl = fig.add_subplot()
        fpl.set_title('Графічний розв\'язок системи 2x2')
        for i in range(2):
            if MatrixA[i][1] == 0:
                fpl.plot([LstB[i]/MatrixA[i][0], LstB[i]/MatrixA[i][0]], x)
            else:
                fpl.plot([res[0]-5, res[0]+5], y(i))
        fpl.plot(res[0], res[1], 'ro')
        fpl.set_xlabel('x1')
        fpl.set_ylabel('x2')
        fpl.legend([feq, seq, "Розв'язок системи"])
        canvas = FigureCanvasTkAgg(fig, plotwindow)
        canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH)
        self.plotwindow.protocol('WM_DELETE_WINDOW', lambda: self.option("close_plot"))
        self.plotwindow.mainloop()

    # Вставка в віджет Text введеної системи
    def insmatrix(self):
        # Визначення відступу між елементами
        def maxincols():
            lst = [0 for i in range(n+1)]
            for i in range(n):
                lst[i] = max([len(str(MatrixA[j][i])) for j in range(n)])+1
            lst[n] = max([len(str(i)) for i in LstB])
            lst = [10 if i>10 else i for i in lst]
            return lst
        MatrixA = self.MatrixA
        LstB = self.LstB
        n = self.n
        setw = maxincols()
        text = self.__text
        text.insert(tk.END, "Введена система:\n")
        for i in range(n):
            text.insert(tk.END, "| ")
            for j in range(n+2):
                if j == n:
                    text.insert(tk.END, " | ")
                else:
                    if j == self.n+1:
                        text.insert(tk.END, "{:>{}}".format(LstB[i], setw[n]))
                    else:
                        text.insert(tk.END, "{:>{}}".format(MatrixA[i][j], setw[j]))
            text.insert(tk.END, " |\n")

    # Збереження файлу (текстового або графічного розв'язку)
    def savefile(self, type = "text"):
        if type == "plot":
            file = filedialog.asksaveasfile(initialfile = 'Untitled.png',defaultextension=".png")
            if file:
                self.fig.savefig(file.name)
        else:
            method = "Cramer" if self.method == "Крамера" else "Gaussian"
            file = filedialog.asksaveasfile(mode='w', initialfile = '{}.txt'.format(method), defaultextension=".txt")
            if file:
                file.write(self.__text.get("1.0",tk.END))
                file.close()
    
    # Метод відповідальний за коректне закриття меню результатів
    def option(self, stat = "show_mainmenu"):
        if self.__plotwinisopen:
            self.__plotwinisopen = False
            self.plotwindow.destroy()
        if stat == "DELETE_WINDOW":
            self.root.destroy()
        elif stat == "close_plot":
            self.__btn3["state"] = tk.NORMAL
        else:
            self.root.show_mainmenu()
            self.destroy()


app = AppInterface()
app.title("Калькулятор СЛАР")
app.geometry('600x400+325+150')
app.resizable(False, False)
app.mainloop()