#!/usr/bin/env python3
"""

TEMPLATE TP4 DDP1 Semester Gasal 2019/2020

Author: 
Ika Alfina (ika.alfina@cs.ui.ac.id)
Evi Yulianti (evi.yulianti@cs.ui.ac.id)
Meganingrum Arista Jiwanggi (meganingrum@cs.ui.ac.id)

Last update: 26 November 2019

"""
from budayaKB_model import BudayaItem, BudayaCollection
from flask import Flask, request, render_template

app = Flask(__name__)
app.secret_key ="tp4"

#inisialisasi objek budayaData
databasefilename = ""
budayaData = BudayaCollection()


#merender tampilan default(index.html)
@app.route('/')
def index():
    return render_template("index.html")

# Bagian ini adalah implementasi fitur Impor Budaya, yaitu:
# - merender tampilan saat menu Impor Budaya diklik	
# - melakukan pemrosesan terhadap isian form setelah tombol "Import Data" diklik
# - menampilkan notifikasi bahwa data telah berhasil diimport 

@app.route('/getStarted')
def appInfo():
    return render_template("getStarted.html")

@app.route('/imporBudaya', methods=['GET', 'POST'])
def importData():
    if request.method == "GET":
        return render_template("imporBudaya.html")

    elif request.method == "POST":
        f = request.files['file']
        global databasefilename
        databasefilename=f.filename
        budayaData.importFromCSV(f.filename)
        n_data = len(budayaData.koleksi)
        return render_template("imporBudaya.html", result=n_data, fname=f.filename)

@app.route('/eksporBudaya', methods=['GET', 'POST'])
def exportData():
    if request.method == "GET":
        return render_template("eksporBudaya.html")
    
    elif request.method == "POST":
        aName = request.form['Ekspor']
        if len(budayaData.koleksi) != 0:
            budayaData.exportToCSV(aName)
            return render_template("eksporBudaya.html", result="True")
        elif len(budayaData.koleksi) == 0:
            return render_template("eksporBudaya.html", result="False")


@app.route('/tambahBudaya', methods=['GET','POST'])
def addData():
    if request.method == "GET":
        return render_template("tambahBudaya.html")

    elif request.method == "POST":
        aName = request.form["Nama"]
        aType = request.form["Tipe"]
        aProv = request.form["Provinsi"]
        anURL = request.form["URL"]
        adder = budayaData.tambah(aName,aType,aProv,anURL)
        return render_template("tambahBudaya.html", name=aName, result=adder)

@app.route('/ubahBudaya', methods=['GET','POST'])
def changeData():
    if request.method == "GET":
        return render_template("ubahBudaya.html")

    elif request.method == "POST":
        aName = request.form["Nama"]
        aType = request.form["Tipe"]
        aProv = request.form["Provinsi"]
        anURL = request.form["URL"]
        adder = budayaData.ubah(aName, aType, aProv, anURL)
        return render_template("ubahBudaya.html", name=aName, result=adder)

@app.route('/hapusBudaya', methods=['GET','POST'])
def eraseData():
    if request.method == "GET":
        return render_template("hapusBudaya.html")

    elif request.method == "POST":
        aName = request.form["Nama"]
        adder = budayaData.hapus(aName)
        return render_template("hapusBudaya.html", name=aName, result=adder)

@app.route('/cariBudaya', methods=['GET','POST'])
def searchData():
    if request.method == "GET":
        return render_template("cariBudaya.html")

    elif request.method == "POST":
        aSearch = request.form['aSearch']
        aType = request.form['SearchType']
        if aType == "NamaBudaya":
            search = budayaData.cariByNama(aSearch)
            n_data = len(search)
            return render_template("cariNama.html", name=aSearch, result=search, length=n_data)
        elif aType == "TipeBudaya":
            search = budayaData.cariByTipe(aSearch)
            n_data = len(search)
            return render_template("cariTipe.html", name=aSearch, result=search,length=n_data)
        elif aType == "ProvinsiBudaya":
            search = budayaData.cariByProv(aSearch)
            n_data = len(search)
            return render_template("cariProv.html", name=aSearch, result=search, length=n_data)
        else:
            pesan = "Data yang anda cari tidak ditemukan!"
            return render_template("cariNama.html", msg=pesan)

@app.route('/statsBudaya', methods=['GET','POST'])
def statsData():
    if request.method == "GET":
        return render_template("statsBudaya.html")

    elif request.method == "POST":
        aType = request.form["StatType"]
        if aType == "SemuaBudaya":
            stats = budayaData.stat()
            return render_template("statSemua.html", length = stats)
        elif aType == "TipeBudaya":
            stats = budayaData.statByTipe()
            n_data = len(stats)
            return render_template("statTipe.html", length = n_data, result=stats)
        elif aType == "ProvinsiBudaya":
            stats = budayaData.statByProv()
            n_data = len(stats)
            return render_template("statProv.html", length = n_data, result=stats)
        else:
            pesan = "Tidak ada Data di Dalam Kamus"
            return render_template("cariNama.html", msg= pesan)

# run main app
if __name__ == "__main__":
    app.run(debug=True)



