import pip

try:
    import customtkinter
    import requests
    import tkinter
    import PIL
    print("modulo encontrado")
except ModuleNotFoundError:
    print("modulo não encontrado.. Tentativa de instalação a caminho.")
    pip.main(["install", "customtkinter"])
    pip.main(["install", "requests" ])
    pip.main(["install", "tkinter"])
    pip.main(["install", "pillow"])
else:
    from tkinter import Tk, PhotoImage, messagebox
    import customtkinter as ctk
    import requests
    from PIL import ImageTk, Image
    from urllib.request import urlopen
    import pickle



if __name__ == "__main__":
    main_w =  ctk.CTk()

    class App():
        def __init__(self):
            #self.pokemon_bd()
            self.pokemon_db_open()
            self.win_config()
            self.main_screen()
            main_w.mainloop()

        def win_config(self):
            main_w.title("Pokedex_App")
            main_w.geometry("800x800")
            main_w.resizable(False, False)
            main_w.iconbitmap("icon_pk.ico")
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("dark-blue")
            self.info_size_max = (800, 800)
            self.info_size_min = (600, 600)
        
        def pokemon_bd(self):
            self.api_cursor = requests.get(url="https://pokeapi.co/api/v2/pokedex/2/")
            self.dic_info = dict(self.api_cursor.json())
            self.pokemon_lista = tuple(enumerate([str(x["pokemon_species"]["name"]).title() for x in self.dic_info["pokemon_entries"]], start=1))
            self.dic_gen_pk = {x:{"name":y} for (x,y) in self.pokemon_lista}
            self.cr_lista_info = []
            self.sprite_lista = []

            for x in self.pokemon_lista:
                self.cursorget_pk_cr = requests.get(url=f"https://pokeapi.co/api/v2/pokemon-species/{x[0]}/").json()
                self.cr_lista_info.append(self.cursorget_pk_cr["capture_rate"])

            self.cr_lista_info = list(enumerate(self.cr_lista_info, start=1))

            for x, y in self.cr_lista_info:
                self.dic_gen_pk[x]["catch_rate"] = y

            for x in self.dic_gen_pk.keys():
                cursor_sprite = dict(requests.get(url=f"https://pokeapi.co/api/v2/pokemon/{x}/").json())
                self.sprite_lista.append(cursor_sprite["sprites"]["other"]["official-artwork"]["front_default"])

            self.sprite_lista = list(enumerate(self.sprite_lista, start=1))

            for x, y in self.sprite_lista:
                self.dic_gen_pk[x]["sprite"] = y

            #/----serialização----/
            #serialização aplicada para otimizar o tempo de leitura das compreensões criadas
            with open("pk_db.pickle", "wb") as file:
                pickle.dump(self.dic_gen_pk, file)

            for x in self.dic_gen_pk.items():
                print(f"\n{x}\n")
            
        def pokemon_db_open(self):
            try:
                with open("pk_db.pickle", "rb") as file:
                    self.pk_db = pickle.load(file)  
            except Exception as err:
                print(err)
                print("Arquivo não encontrado...")
                print("Criando arquivo...")
                self.pokemon_bd()
            
            else:
                print(self.pk_db)
                self.pk_db = dict(self.pk_db)
          

        #/-----/------Telas------/-----/   

        def main_screen(self):
            def start():
                main_frame.pack_forget()
                self.pokedex_frame()
                if main_w.winfo_width() == "600" and main_w.winfo_height() == "600":
                    min_win()


            def max_win():
                main_w.geometry(f"{self.info_size_max[0]}x{self.info_size_max[1]}")
                main_frame.configure(width=self.info_size_max[0], height=self.info_size_max[1])
                main_frame.update()
                image_title.place(x=posi_title_og[0], y=posi_title_og[1])
                start_buttom.place(x=posi_start_og[0], y=posi_start_og[1])
                credit_info.place(x=posi_desc_og[0], y=posi_desc_og[1])
            
            def min_win():
                main_w.geometry(f"{self.info_size_min[0]}x{self.info_size_min[1]}")
                main_frame.configure(width=self.info_size_min[0], height=self.info_size_min[1])
                main_frame.update()
                image_title.place(x=posi_title_ct[0], y=posi_title_ct[1])
                start_buttom.place(x=posi_start_ct[0], y=posi_start_ct[1])
                credit_info.place(x=posi_desc_ct[0], y=posi_desc_ct[1])

            posi_title_og = (185, 100)
            posi_title_ct = (82, 50)

            posi_start_og = (300, 400)
            posi_start_ct = (200, 300)

            posi_desc_og = (175, 700)
            posi_desc_ct = (75, 500)


            main_frame = ctk.CTkFrame(master=main_w, width=self.info_size_max[0], height=self.info_size_max[1])
            main_frame.pack()

            max_w_buttom = ctk.CTkButton(master=main_frame, text="+", font=("Arial", 20, "bold"), width=30, height=20, fg_color="goldenrod2", hover_color="goldenrod3", corner_radius=5, command=max_win)
            max_w_buttom.place(x=10, y=10)
            min_w_buttom = ctk.CTkButton(master=main_frame, text="-", font=("Arial", 20, "bold"), width=30, height=20, fg_color="SpringGreen3", hover_color="SpringGreen4", corner_radius=5, command=min_win)
            min_w_buttom.place(x=60, y=10)
            
            img = PhotoImage(file="title.png")
            image_title = ctk.CTkLabel(master=main_frame, image=img, text="")
            image_title.place(x=posi_title_og[0], y=posi_title_og[1])

            start_buttom = ctk.CTkButton(master=main_frame, command=start, text="INICIAR", fg_color="firebrick1", hover_color="firebrick3", font=("Roboto", 30, "bold"), corner_radius=40, width=200, height=100)
            start_buttom.place(x=posi_start_og[0], y=posi_start_og[1])

            credit_info = ctk.CTkLabel(master=main_frame, text="criado por: Gustavo Moreira\ngithub: https://github.com/Gustav0Moreira\nlinkedin: in/gustavo-moreira-brito-da-silva-34203b229/\nEste é um projeto sem fins lucrativos e de finalidade academica", font=("Roboto", 15))
            credit_info.place(x=posi_desc_og[0], y=posi_desc_og[1])


        def pokedex_frame(self):

            def max_win():
                main_w.geometry(f"{self.info_size_max[0]}x{self.info_size_max[1]}")
                pk_main.configure(width=self.info_size_max[0], height=self.info_size_max[1])
                pk_main.update()
                layout_1.configure(width=frame1_layout_og[0], height=frame1_layout_og[1])
                layout_1.update()
                layout_2.configure(width=frame2_layout_og[0], height=frame2_layout_og[1])
                layout_2.update()
                frame_h_title.configure(width=frame1_layout_og[0])
                frame_h_title.update()
                frame_h_crate.configure(width=frame1_layout_og[0])
                frame_h_crate.update()
                pk_id_label.configure(font=(fonte_og[0], fonte_og[1], fonte_og[2]))
                pk_id_label.update()
                pk_name_title.configure(font=(fonte_og[0], fonte_og[1], fonte_og[2]))
                pk_name_title.update()
                pk_id_label.place(x=posi_id_label_og[0], y=posi_id_label_og[1])  
                pk_img_label.place(x=posi_pk_img_og[0], y=posi_pk_img_og[1])
                pk_crate_label.configure(font=(fonte2_og[0], fonte2_og[1], fonte2_og[2]))
              
            
            def min_win():
                main_w.geometry(f"{self.info_size_min[0]}x{self.info_size_min[1]}")
                pk_main.configure(width=self.info_size_min[0], height=self.info_size_min[1])
                pk_main.update()
                layout_1.configure(width=frame1_layout_cu[0], height=frame1_layout_cu[1])
                layout_1.update()
                layout_2.configure(width=frame2_layout_cu[0], height=frame2_layout_cu[1])
                layout_2.update()
                frame_h_title.configure(width=frame1_layout_cu[0])
                frame_h_title.update()
                frame_h_crate.configure(width=frame1_layout_cu[0])
                frame_h_crate.update()
                pk_id_label.configure(font=(fonte_ct[0], fonte_ct[1], fonte_ct[2]))
                pk_id_label.update()
                pk_name_title.configure(font=(fonte_ct[0], fonte_ct[1], fonte_ct[2]))
                pk_name_title.update()
                pk_id_label.place(x=posi_id_label_ct[0], y=posi_id_label_ct[1])  
                pk_img_label.place(x=posi_pk_img_ct[0], y=posi_pk_img_ct[1])
                pk_crate_label.configure(font=(fonte2_ct[0], fonte2_ct[1], fonte2_ct[2]))
                

            frame1_layout_og = (380, 720)
            frame1_layout_cu = (280, 520)

            frame2_layout_og = (380, 773)
            frame2_layout_cu = (280, 558)

            pk_id_buttom_og = (350, 100)

            fonte_og = ("Roboto", 51, "bold")
            fonte_ct = ("Roboto", 40, "bold")
            fonte2_og = ("Roboto", 31, "bold")
            fonte2_ct = ("Roboto", 20, "bold") 
            
            posi_id_label_og = (80, 25)
            posi_id_label_ct = (70, 15)  

            posi_pk_img_og = (85, 150)
            posi_pk_img_ct = (35, 100)

            
            pk_main = ctk.CTkFrame(master=main_w, width=self.info_size_max[0], height=self.info_size_max[1])
            pk_main.pack()
            
            max_w_buttom = ctk.CTkButton(master=pk_main, command=max_win, text="+", font=("Arial", 20, "bold"), width=30, height=20, fg_color="goldenrod2", hover_color="goldenrod3", corner_radius=5)
            max_w_buttom.place(x=10, y=10)
            min_w_buttom = ctk.CTkButton(master=pk_main, command=min_win, text="-", font=("Arial", 20, "bold"), width=30, height=20, fg_color="SpringGreen3", hover_color="SpringGreen4", corner_radius=5)
            min_w_buttom.place(x=60, y=10)

            #Main_Frame---------------------------------------------------------------------------------------------

            layout_1 = ctk.CTkFrame(master=pk_main, width=frame1_layout_og[0], height=frame1_layout_og[1])
            layout_1.place(relx=0, rely=0.08)

            frame_h_title = ctk.CTkFrame(master=layout_1, width=frame1_layout_og[0], height=100, fg_color="gray28")
            frame_h_title.place(relx=0, rely=0.6)

            frame_h_crate = ctk.CTkFrame(master=layout_1, width=frame1_layout_og[0], height=100, fg_color="gray10")
            frame_h_crate.place(relx=0, rely=0.8)

            url_default = ("https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png")
            id_default = (f'#{1}')
            title_default = ("bulbasaur".title())
            crate_default = "Dificil"

            pk_img = Image.open(urlopen(url_default))
            pk_img = pk_img.resize((200,200))
            pk_img = ImageTk.PhotoImage(pk_img)

            pk_img_label =  ctk.CTkLabel(master=layout_1, image=pk_img, text="")
            pk_img_label.place(x=posi_pk_img_og[0], y=posi_pk_img_og[1])

            pk_ball_img = PhotoImage(file="pk_ball.png")
            pk_ball_label = ctk.CTkLabel(master=layout_1, image=pk_ball_img, text="")
            pk_ball_label.place(relx=0.02, rely=0.03)

            pk_id_label = ctk.CTkLabel(master=layout_1, text=id_default, font=(fonte_og[0], fonte_og[1], fonte_og[2]))
            pk_id_label.place(x=posi_id_label_og[0], y=posi_id_label_og[1])  

            pk_name_title = ctk.CTkLabel(master=frame_h_title, text=title_default, font=(fonte_og[0], fonte_og[1], fonte_og[2]), fg_color="gray28", corner_radius=20)
            pk_name_title.place(relx=0.5, rely=0.5, anchor="center")
            
            pk_crate_label = ctk.CTkLabel(master=frame_h_crate, text=crate_default, height=70, font=(fonte2_og[0], fonte2_og[1], fonte2_og[2]), fg_color="firebrick2", corner_radius=20)
            pk_crate_label.place(relx=0.5, rely=0.5, anchor="center")


            #Sub_Frame----------------------------------------------------------------------------------------------

            layout_2 = ctk.CTkScrollableFrame(master=pk_main, width=frame2_layout_og[0], height=frame2_layout_og[1])
            layout_2.place(relx=0.5, y=0)
            

            buttom_dict = {}
            pk_dict = self.pk_db

            for x in pk_dict:
                def pk_id(i = x):
                    print(pk_dict[i]["sprite"])
                    pk_img = Image.open(urlopen(pk_dict[i]["sprite"]))
                    pk_img = pk_img.resize((200,200))
                    pk_img = ImageTk.PhotoImage(pk_img)
                    pk_img_label.configure(image=pk_img)
                    pk_img_label.update()
                    pk_id_label.configure(text=f"#{i}")
                    pk_id_label.update()
                    pk_name_title.configure(text=pk_dict[i]["name"])
                    pk_name_title.update()
                    if pk_dict[i]["catch_rate"] <= 5:
                        cr = "Impossivel"
                        color = "purple1"
                    elif pk_dict[i]["catch_rate"] <= 45:
                        cr = "Dificil"
                        color = "firebrick2"
                    elif pk_dict[i]["catch_rate"] <= 150:
                        cr = "Desafiador"
                        color = "goldenrod3"
                    elif pk_dict[i]["catch_rate"] <= 350:
                        cr = "Facil"
                        color = "SpringGreen4"
                    pk_crate_label.configure(text=cr, fg_color=color)
                    pk_crate_label.update()


                id = x
                name = pk_dict[x]["name"]
                buttom_dict[x] = ctk.CTkButton(master=layout_2, command=pk_id, text=f"{name} #{id}", font=("Roboto", 20, "bold"), fg_color="firebrick3", hover_color="firebrick4", width=pk_id_buttom_og[0], height=pk_id_buttom_og[1])
                buttom_dict[x].pack(pady=10)
            



    App()