import customtkinter as ctk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
import pymongo
import os

# Connect to the database
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['application_opener']
collection = db['applications']
print("Connection successful!")

# Event handlers
def show_remove_info():
    showinfo("Alert!","Removed the application")


def show_add_info():
    showinfo("Alert!","Added the application")


def add_applications():
    filename = askopenfilename()
    print(filename)

    if filename == '':
        return
    else:
        collection.insert_one({'location': filename})
        show_add_info()


# Window
window = ctk.CTk()
window.title("Application Opener")
window.geometry("600x500")

add_application_btn = ctk.CTkButton(master=window, text="Add Application", command=add_applications)
add_application_btn.pack(pady=10)

applications = collection.find()

application_to_launch_location = {}
application_to_remove_id = {}

scrollable_frame = ctk.CTkScrollableFrame(master=window, height=1980, fg_color='#f0ecec')
scrollable_frame.pack(fill=ctk.BOTH)

for application in applications:

    def launch_application(location):
        os.startfile(location)


    def remove_application(id):
        collection.delete_one({'_id': id})
        show_remove_info()


    application_location_ent = ctk.CTkEntry(master=scrollable_frame)
    application_location_ent.insert(1, f"{application['location']}")
    application_location_ent.configure(state="disabled")
    application_location_ent.pack(fill=ctk.X, pady=10, padx=10)

    application_launch_btn = ctk.CTkButton(master=scrollable_frame, text="Launch Application", command=lambda location=application['location']: launch_application(location))
    application_launch_btn.pack(pady=5)

    remove_application_btn = ctk.CTkButton(master=scrollable_frame, text="Remove Application", command=lambda id=application['_id']: remove_application(id))
    remove_application_btn.pack(pady=5)

    application_to_launch_location[application['location']] = application_launch_btn
    application_to_remove_id[application['_id']] = remove_application_btn


window.mainloop()