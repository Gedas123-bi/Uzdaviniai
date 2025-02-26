import pickle
import os
from datetime import datetime
class Filmai :
    def __init__(self, pavadinimas, trukme, zanras, rezisierius,isleidimo_metai, reitingas):
        self.pavadinimas = pavadinimas
        self.trukme = trukme
        self.zanras = zanras
        self.rezisierius = rezisierius
        self. isleidimo_metai = isleidimo_metai
        self.reitingas = reitingas
        self.ziurovo_reitingas = []
    def update(self, pavadinimas = None, trukme= None, zanras= None, rezisierius= None, isleidimo_metai= None, reitingas= None):
        if pavadinimas:
            self.pavadinimas = pavadinimas
        if trukme:
            self.trukme = trukme
        if zanras:
            self.zanras = zanras
        if rezisierius:
            self.rezisierius = rezisierius
        if isleidimo_metai:
            self.isleidimo_metai = isleidimo_metai
        if reitingas:
            self.reitingas = reitingas
    def average_ratingas(self):
        return sum(self.ziurovo_reitingas)/len(self.ziurovo_reitingas) if len(self.ziurovo_reitingas) > 0 else 0
class Seansas :
    def __init__(self, filmas, data_laikas, vietos):
            self.filmas = filmas
            self.data_laikas = data_laikas
            self.vietos = vietos
            self.rezervacija = []
    def rezervuotos_vietos(self):
            if self.rezervacija < self.vietos:
               self.rezervacija += 1
               return True
            return False
class Vartotojas :
    def __init__(self, vardas, tipas):
        self.vardas = vardas
        self.tipas = tipas
class Festivalis :
    def __init__(self):
        self.filmai = {}
        self.seansai = {}
        self.vartotojai = {}
    def load_data (self):   # Įraunami duomenys iš Pickle failo
        if os.path.exists( "Festivalio_duomenys.pkl"): 
            try:
                with open ("Festivalio_duomenys.pkl", "rb") as file:
                    data = pickle.load(file)
                    self.filmai = data.get("filmai", {})
                    self.seansai = data.get("seansai", {})
                    self.vartotojai = data.get("vartotojai", {})
            except:       
                    print( "Klaida atidarant failą")
    def save_data(self):   # Išsaugomi duomenys į Pickle failą   
            try :
                with open ("Festivalio_duomenys.pkl", "wb") as file:
                    data = {"filmai": self.filmai, "seansai": self.seansai, "vartotojai": self.vartotojai}
                pickle.dump(data, file)
            except :
               print ("Klaida išsaugant duomenis")   
    def prideti_filma(self, pavadinimas, trukme, zanras, rezisierius, isleidimo_metai, reitingas):
            try :
                if pavadinimas in self.filmai:
                        print ("Filmas jau egzistuoja")
                        return
                Naujas_filmas = Filmai(pavadinimas, trukme, zanras, rezisierius, isleidimo_metai, reitingas) 
                self.filmai[pavadinimas] = Naujas_filmas
                print (f"Filmas {pavadinimas} pridėtas")
            except :
                print ("Klaida pridedant filmą")
    def  pasalinti_filma(self, pavadinimas):
            try :
                if pavadinimas in self.filmai:
                    del self.filmai[pavadinimas]
                    print (f"Filmas {pavadinimas} pašalintas")  
                else:
                    print ("Filmas neegzistuoja")
            except :
                print ("Klaida pašalinant filmą") 
    def atnaujinti_duomenis(self, pavadinimas, **kwargs):
            try :
                if pavadinimas in self.filmai:
                    filmas = self.filmai[pavadinimas]
                    filmas.update(**kwargs)
                    print (f"Filmas {pavadinimas} atnaujintas")
                else:
                    print ("Filmas neegzistuoja")
            except :
                print ("Klaida atnaujinant filmą")
                   
    def visi_filmai(self):
            try:
                if not self.filmai:
                  print ("Filmas nėra įtrauktas į programą")
                  return
                
                for pavadinimas, filmas in self.filmai.values():
                    reitingas = filmas.average_ratingas()
                    print (f"{pavadinimas} {filmas.pavadinimas} {filmas.trukme} {filmas.zanras} {filmas.rezisierius} {filmas.isleidimo_metai} {filmas.reitingas} {reitingas}")
            except :
                print ("Klaida atspausdinant filmus")
    def prideti_seansa(self, filmas, data_laikas, vietos):
            try :
                if filmas not in self.filmai:
                    print ("Filmas neegzistuoja")
                    return 
                filmo_seansas = (f"{filmas}_{data_laikas}")
                if filmo_seansas in self.seansai:
                    print ("Seansas jau egzistuoja")
                    return
                naujas_seansas = Seansas(filmas, data_laikas, vietos)
                self.seansai[filmo_seansas] = naujas_seansas
                print (f"Seansas {filmas} pridėtas")
            except :
                print ("Klaida pridedant seansą")
    def rezervuoti_vietas(self, filmas, data_laikas, vardas, vietos):
            try :
                if vardas not in self.vartotojai:
                    print ("Vartotojas neegzistuoja")
                    return
                filmo_seansas = (f"{filmas}_{data_laikas}")
                if filmo_seansas not in self.seansai:
                    print ("Seansas neegzistuoja")
                    return
                naujas_seansas = Seansas(self.seansai[filmo_seansas], data_laikas, vietos)
                self.seansai[filmo_seansas] = naujas_seansas
                print (f"Vietos {vietos} rezervuotos")
            except :
                print ("Klaida rezervuojant vietą")
    def rezervuoti_bilieta(self, filmas, data_laikas, vardas, vietos):
            try :
                if vardas not in self.vartotojai:
                    print ("Vartotojas neegzistuoja")
                    return
                filmo_seansas = (f"{filmas}_{data_laikas}")
                if filmo_seansas not in self.seansai:
                    print ("Seansas neegzistuoja")
                    return
                Seansas = self.seansai[filmo_seansas]
                if Seansas.rezervuotos_vietos():
                    Seansas.rezervacija.append((vardas, vietos))
                    print (f"Vietos {vietos} rezervuotos")
                else:
                    print ("Vietų nėra")
            except :
                print ("Klaida rezervuojant bilietą")
    def     filmo_reitingas(self, filmas,vardas, reitingas):
            try :
                if filmas not in self.filmai:
                    print ("Filmas neegzistuoja")
                    return
                if vardas not in self.vartotojai:
                    print ("Vartotojas neegzistuoja")
                    return 
                filmas = self.filmai[filmas]
                if reitingas < 1 or reitingas > 10:
                    print ("Reitingas turi būti tarp 1 ir 10")
                    return
                filmas.ziurovo_reitingas.append(reitingas)
                print (f"Reitingas {reitingas} pridėtas")
            except :
                print ("Klaida pridedant reitingą")
def main():
    festivalis = Festivalis()
    while True:
        print ("\nPasirinkite veiksmą:")
        print ("1. Pridėti filmą")
        print ("2. Pašalinti filmą")
        print ("3. Atnaujinti filmą")
        print ("4. Visi filmai")
        print ("5. Pridėti seansą")
        print ("6. Rezervuoti bilietą") 
        print ("7. Pridėti reitingą")
        print ("8. Išeiti")
        pasirinkimas = input("Įveskite pasirinkimą: ")
        try:
            if pasirinkimas == "1":
                pavadinimas = input("Įveskite pavadinimą: ")
                trukme = input("Įveskite trukmę: ")
                zanras = input("Įveskite žanrą: ")
                rezisierius = input("Įveskite rezisierių: ")
                isleidimo_metai = input("Įveskite išleidimo metus: ")
                reitingas = input("Įveskite reitingą: ")
                festivalis.prideti_filma(pavadinimas, trukme, zanras, rezisierius, isleidimo_metai, reitingas)
            elif pasirinkimas == "2":
                pavadinimas = input("Įveskite pavadinimą: ")
                festivalis.pasalinti_filma(pavadinimas)
            elif pasirinkimas == "3":
                pavadinimas = input("Įveskite pavadinimą filmo: ")
                festivalis.atnaujinti_duomenis(pavadinimas)
            elif pasirinkimas == "4":
                festivalis.visi_filmai()
            elif pasirinkimas == "5":
                filmas = input("Įveskite filmo pavadinimą: ")
                data_laikas = input("Įveskite datą ir laiką: ")
                vietos = input("Įveskite vietų skaičių: ")
                festivalis.prideti_seansa(filmas, data_laikas, vietos)
            elif pasirinkimas == "6":
                vardas = input("Įveskite vardą: ")
                filmo_pavadinimas = input("Įveskite filmo pavadinimą: ")
                data_laikas = input("Įveskite datą ir laiką: ")
                festivalis.rezervuoti_bilieta(filmas, data_laikas, vardas, vietos )
            elif pasirinkimas == "7":
                vardas = input("Įveskite vardą: ")
                filmas = input("Įveskite filmo pavadinimą: ")
                reitingas = input("Įveskite reitingą: ")
                festivalis.filmo_reitingas(filmas, vardas, reitingas)
            elif pasirinkimas == "8":
                festivalis.save_data()
                break
            else:
                print ("Neteisingas pasirinkimas")
        except ValueError:
            print ("Klaida įvedant duomenis")
        except:
            print ("Klaida atliekant veiksmą")
if __name__ == "__main__":
    main()
     


                
        
          
                 

                

               
                       


            
                       
                        
                  



                
            

        
        
          
                
                
            
    
        