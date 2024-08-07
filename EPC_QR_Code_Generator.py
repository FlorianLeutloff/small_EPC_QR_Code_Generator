from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage
import qrcode
import os.path
import os


class MainWindow():
    def __init__(self, mainframe):
        entry_field_width = 40
        self.user_data_entry_startup = False
        self.service_tag = StringVar()
        self.version = StringVar()
        self.character_set = StringVar()
        self.identification = StringVar()
        self.bic = StringVar()
        self.payname = StringVar()
        self.iban = StringVar()
        self.amount = StringVar()
        self.purpose = StringVar() #optional
        self.remittance_reference = StringVar() #optional
        self.remittance_text = StringVar() #optional
        self.information = StringVar() #optional

        if(os.path.exists("settings.txt")):
            settings_file = open("settings.txt","r")
            lines = settings_file.readlines()
            settings_dictionary = {"service_tag":lines[0].replace("\n",""),"character_set":lines[1].replace("\n",""),"identification":lines[2].replace("\n","")}
            settings_file.close()
        else:
            settings_dictionary = {"service_tag":"BCD","character_set":"1","identification":"SCT"}
            new_settings_file = open("settings.txt","a")
            new_settings_file.write(settings_dictionary["service_tag"]+"\n")
            new_settings_file.write(settings_dictionary["character_set"]+"\n")
            new_settings_file.write(settings_dictionary["identification"])
            new_settings_file.close()
            pass
        self.service_tag.set(settings_dictionary["service_tag"])
        self.character_set.set(settings_dictionary["character_set"])
        self.identification.set(settings_dictionary["identification"])

        if(os.path.exists("user_data.txt")):
            user_data_file = open("user_data.txt","r")
            lines = user_data_file.readlines()
            user_data_dictionary = {"BIC":lines[0].replace("\n",""),"Payname":lines[1].replace("\n",""),"IBAN":lines[2].replace("\n","")}
            self.iban.set(user_data_dictionary["IBAN"])
            self.payname.set(user_data_dictionary["Payname"])
            self.bic.set(user_data_dictionary["BIC"])
            user_data_file.close()
        else:
            self.user_data_entry_startup = True
            pass

        ### USER INFORMATION ###
        ttk.Label(mainframe, text="Zahlungsempfänger-Name:").grid(column=1, row=1, sticky=(W))
        self.payname_entry = ttk.Entry(mainframe, width = entry_field_width, textvariable=self.payname , state=DISABLED)
        self.payname_entry.grid(column=1, row=2, sticky=(W))        

        ttk.Label(mainframe, text="IBAN:").grid(column=1, row=3, sticky=(W))
        self.iban_entry = ttk.Entry(mainframe, width = entry_field_width, textvariable=self.iban, state=DISABLED)
        self.iban_entry.grid(column=1, row=4, sticky=(W))

        ttk.Label(mainframe, text="BIC:").grid(column=1, row=5, sticky=(W))
        self.bic_entry = ttk.Entry(mainframe, width = entry_field_width, textvariable=self.bic, state=DISABLED)
        self.bic_entry.grid(column=1, row=6, sticky=(W))

        self.edit_userdata_button = ttk.Button(mainframe, text="Bearbeiten", command=self.editData)
        self.edit_userdata_button.grid(column=1, row=7, sticky=(W))

        self.save_userdata_button = ttk.Button(mainframe, text="Speichern", command=self.saveData, state=DISABLED)
        self.save_userdata_button.grid(column=1, row=8, sticky=(W))


        ### USER INPUT ###
        ttk.Label(mainframe, text="Geldbetrag:").grid(column=2, row=1, sticky=(W),padx=(20,20))
        self.amount_entry = ttk.Entry(mainframe, width = entry_field_width, textvariable=self.amount)
        self.amount_entry.grid(column=2, row=2, sticky=(W),padx=(20,20))

        ttk.Label(mainframe, text="Verwendungszweck (Remittance (Text) ):").grid(column=2, row=3, sticky=(W),padx=(20,20))
        self.remittance_text_entry = ttk.Entry(mainframe, width = entry_field_width, textvariable=self.remittance_text)
        self.remittance_text_entry.grid(column=2, row=4, sticky=(W),padx=(20,20))

        ttk.Label(mainframe, text="Wirtschaftsraum:").grid(column=2, row=5, sticky=(W),padx=(20,20))
        self.option_list = ("keine Auswahl","Nur-Europäischer-Wirtschaftsraum", "EWR und Nicht-Europäischer-Wirtschaftsraum")
        self.version.set(self.option_list[0])
        self.version_entry = ttk.OptionMenu(mainframe, self.version, *self.option_list)
        self.version_entry.grid(column=2,row=6,sticky=(W),padx=(20,20))

        self.create_QR_Code_Button = ttk.Button(mainframe, text="QRCode erstellen", command=self.createQRCode)
        self.create_QR_Code_Button.grid(column=2, row=7, sticky=(W),padx=(20,20))

        self.creation_notification_label = ttk.Label(mainframe, text="QR-Code wurde erstellt!!!")
        #self.creation_notification_label.grid(column=2,row=8, sticky=(W),padx=(20,20))

        ### Start Up Situation ###
        if(self.user_data_entry_startup):
            self.bic_entry.config(state="ENABLED")
            self.iban_entry.config(state="ENABLED")
            self.payname_entry.config(state="ENABLED")
            self.amount_entry.config(state=DISABLED)
            self.remittance_text_entry.config(state=DISABLED)
            self.version_entry.configure(state=DISABLED)
            self.create_QR_Code_Button.configure(state=DISABLED)
            self.edit_userdata_button.configure(state=DISABLED)
            self.save_userdata_button.configure(state="ENABLED")
            
            self.startup_label = ttk.Label(mainframe, text="Keine Nutzerdaten vorhanden, bitte hinterlegen Sie Ihre Daten")
            self.startup_label.grid(column=1, row=9, sticky=(W))
            pass           
        pass

    def saveData(self):
        try:
            save_bic = self.bic.get()
            save_payname = self.payname.get()
            save_iban = self.iban.get()
        except:
            #print("Error 1: Exception during Retrieval of Data in saveData()")
            pass
        if((not(save_bic is None) and save_bic!="") and (not(save_payname is None) and save_payname!="") and (not(save_iban is None) and save_iban!="")):
            self.iban.set(save_iban)
            self.payname.set(save_payname)
            self.bic.set(save_bic)

            ### Clearing previous writings on the file ###
            if(os.path.exists("user_data.txt")):
                open("user_data.txt","w").close()
                pass

            ### Appending User Data onto the clear file ###
            user_data_file = open("user_data.txt","a")
            user_data_file.write(save_bic+"\n")
            user_data_file.write(save_payname+"\n")
            user_data_file.write(save_iban)
            user_data_file.close()

            self.bic_entry.config(state=DISABLED)
            self.iban_entry.config(state=DISABLED)
            self.payname_entry.config(state=DISABLED)
            self.amount_entry.config(state="ENABLED")
            self.remittance_text_entry.config(state="ENABLED")
            self.version_entry.configure(state="ENABLED")
            self.create_QR_Code_Button.configure(state="ENABLED")
            self.edit_userdata_button.configure(state="ENABLED")
            self.save_userdata_button.configure(state=DISABLED)
            if(self.user_data_entry_startup):
                self.startup_label.grid_remove()
            pass
        pass

    def editData(self):
        self.bic_entry.config(state="ENABLED")
        self.iban_entry.config(state="ENABLED")
        self.payname_entry.config(state="ENABLED")
        self.amount_entry.config(state=DISABLED)
        self.remittance_text_entry.config(state=DISABLED)
        self.version_entry.configure(state=DISABLED)
        self.create_QR_Code_Button.configure(state=DISABLED)
        self.edit_userdata_button.configure(state=DISABLED)
        self.save_userdata_button.configure(state="ENABLED")
        pass

    def destroyNotification(self):
        self.creation_notification_label.grid_remove()
        pass

    def createQRCode(self):
        def createQRString(optional_array, mandatory_array):
            def checkOptional(optional_array):
                counter = 0
                for entry in optional_array:
                    if(not(entry is None) and (entry!="")):
                        counter = counter + 1
                    pass
                pass
                if(counter > 0):
                    if(optional_array[3]=="" or optional_array[3] is None):
                        optional_array.pop(3)
                        if(optional_array[2]=="" or optional_array[2] is None):
                            optional_array.pop(2)
                            if(optional_array[1]=="" or optional_array[1] is None):
                                optional_array.pop(1)
                            return optional_array
                        else:
                            return optional_array
                    else:
                        return optional_array
                    pass
                else:
                    optional_array = []
                    return optional_array
                pass
            pass

            QR_string = ""
            for entry in mandatory_array:
                QR_string = QR_string + entry + "\n"
                pass
            optional_array = checkOptional(optional_array=optional_array)
            for entry in optional_array:
                QR_string = QR_string + entry + "\n"
                pass
            QR_string = QR_string[:len(QR_string)-1]
            return QR_string
        pass

        try:
            service_tag_var = self.service_tag.get()
            version_var = self.version.get()
            character_set_var = self.character_set.get()
            identification_var = self.identification.get()
            bic_var = self.bic.get()
            payname_var = self.payname.get()
            iban_var = self.iban.get()
            amount_var = "EUR"+self.amount.get()
            amount_var = amount_var.replace(",",".")

            if(version_var =="Nur-Europäischer-Wirtschaftsraum"):
                version_var = "002"
            else:
                version_var = "001"
                pass

            mandatory_array = [service_tag_var,version_var,character_set_var,identification_var,bic_var,payname_var,iban_var,amount_var]
            for entry in mandatory_array:
                if(entry is None or entry==""):
                    #print("Entry is missing")
                    return "404" 
                pass
        except:
            #print("Error happened, figure it out for yourself")
            pass
        try:
            purpose_var = self.purpose.get()
            remittance_reference_var = self.remittance_reference.get()
            remittance_text_var = self.remittance_text.get()
            information_var = self.information.get()

            optional_array = [purpose_var,remittance_reference_var,remittance_text_var,information_var]
        except:
            #print("Error in optional Entries")
            pass
        QR_String = createQRString(optional_array=optional_array,mandatory_array=mandatory_array)
        #print(QR_String)
        qrcode.make(QR_String)
        image2 = qrcode.make(QR_String)
        image2.save("file.png")

        if(os.path.exists("file.png")):
            self.creation_notification_label.grid(column=2,row=8, sticky=(W),padx=(20,20))
            self.creation_notification_label.after(2000,self.destroyNotification)



        ### Creates Label to notify User of QR-Code having been created ###
        #There is no functionality or checking attached to this yet, so it will probably appear even if generation fails :)
        self.creation_notification_label.grid(column=2,row=8, sticky=(W),padx=(20,20))
        self.creation_notification_label.after(2000,self.destroyNotification)
    pass    
 
def main():
    root = Tk()
    root.title("EPC-QR-Code Generator")
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)    
    MainWindow(mainframe)
    root.mainloop()
    

if __name__=="__main__":
    main() 
