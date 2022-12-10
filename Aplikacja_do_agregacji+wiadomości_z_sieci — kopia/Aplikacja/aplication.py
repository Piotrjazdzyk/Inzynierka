from tkinter import *
from functions import *

w1 =Tk()

w1.geometry("500x400")

w1.title("Witaj w aplikacji do agragacji")

mode = 0

def random_form():
    global location ,genra ,amount, mode
    mode = 1


    w2 = Toplevel(w1)
    w2.title("Losuj Wiadomości")
    w2.geometry('400x200')
    Label(w2, text="Wypełnij formularz", font="comicsansms 13 bold", pady=15).grid(row=0, column=3)
    name = Label(w2, text="Miejsce")
    phone = Label(w2, text="Temat")
    gender = Label(w2, text="Ilość")
    name.grid(row=1, column=2)
    phone.grid(row=2, column=2)
    gender.grid(row=3, column=2)
    location = StringVar()
    genra = StringVar()
    amount = IntVar()
    loc = Entry(w2, textvariable=location)
    gen = Entry(w2, textvariable=genra)
    amo = Entry(w2, textvariable=amount)
    loc.grid(row=1, column=3)
    gen.grid(row=2, column=3)
    amo.grid(row=3, column=3)


    b5 = Button(w2,text ="wyślij i pokarz wyniki", command = end, compound="c",bg = 'white').grid(row = 4, column = 3 )

def one_sight():


    global single_articale, mode
    mode = 3


    w2 = Toplevel(w1)
    w2.title("Pojednyńczy artykuł")
    w2.geometry('400x200')
    Label(w2, text="Wypełnij formularz", font="comicsansms 13 bold", pady=15).grid(row=0, column=3)
    name = Label(w2, text="Link do artykułu")
    name.grid(row=1, column=2)
    single_articale = StringVar()
    loc = Entry(w2, textvariable=single_articale)
    loc.grid(row=1, column=3)
    b5 = Button(w2,text ="wyślij i pokarz wyniki", command = end, compound="c",bg = 'white').grid(row = 4, column = 3 )


def multi_sight():
    global site , mode

    mode = 2
    w2 = Toplevel(w1)
    w2.title("Strona do analizy")
    w2.geometry('400x200')
    Label(w2, text="Podaj Link do strony", font="comicsansms 13 bold", pady=15).grid(row=0, column=3)
    name = Label(w2, text="Link do artykułu")
    name.grid(row=1, column=2)
    site = StringVar()
    loc = Entry(w2, textvariable=site)
    loc.grid(row=1, column=3)
    b5 = Button(w2,text ="wyślij i pokarz wyniki", command = end, compound="c",bg = 'white').grid(row = 4, column = 3 )

def end():
    w1.destroy()

bt1 = Button(w1, text ="Losuj Wiadomości", command = random_form, compound="c",bg = 'white')
bt2 = Button(w1, text ="Wpisz pojedniczy artykułu", command = one_sight, compound="c",bg = 'white')
bt4 = Button(w1, text ="Wpisz link do strony", command = multi_sight, compound="c",bg = 'white')
bt3 = Button(w1, text ="pokaż wyniki", command = end, compound="c",bg = 'white')

bt3.place(relx=0.5, rely=0.5,anchor='center')
bt4.place(relx=0.5, rely=0.0,anchor='n')
bt1.place(relx=0.0, rely=0.0,anchor='nw')
bt2.place(relx=1.0, rely=0.0,anchor='ne')

w1.mainloop()

if mode == 1:
    try:
        final_location = location.get()
        final_genra = genra.get()
        final_amount = amount.get()
        list_of_urls = get_random_news(final_location,final_genra,final_amount)
        articals_to_save = bulk_artciales_prep(list_of_urls)
        save_to_txt(articals_to_save)


    except:
        master = Tk()
        master.geometry("100x100")
        master.title("error")
        Label(master,text = 'Somthing went wrong').place(relx=0.5, rely=0.5,anchor='center')
        master.mainloop()

elif mode == 2:
    try:
        url = site.get()

        list_of_urls = get_specific_news(url)
        articals_to_save = bulk_artciales_prep(list_of_urls)
        save_to_txt(articals_to_save)

    except:
        master = Tk()
        master.geometry("100x100")
        master.title("error")
        Label(master,text = 'Somthing went wrong').place(relx=0.5, rely=0.5,anchor='center')
        master.mainloop()


elif mode == 3:
    try:
        url = single_articale.get()
        list_of_urls = get_one_articale(url)
        articals_to_save= bulk_artciales_prep(list_of_urls)
        save_to_txt(articals_to_save)


    except:
        master = Tk()
        master.geometry("100x100")
        master.title("error")
        Label(master,text = 'Somthing went wrong').place(relx=0.5, rely=0.5,anchor='center')
        master.mainloop()


