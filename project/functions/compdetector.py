from ..models import Component
import numpy as np

# Menghapus Whitespace di depan
def bersih(salt):
    index   = [0,1, len(salt)-1, len(salt)-2]
    s       = np.delete(salt, index)
    for i in range(len(s)):
        con = True
        inc = 0
        while con:
            if s[i][inc] == " ":            
                inc+=1
            else :
                con = False
        s[i] = s[i][inc:len(s[i])]
        s[i] = s[i].replace("\r","")
        s[i] = s[i].replace("\n","")
        s[i] = s[i].replace("\t","")
    return s

def cleanFirst(baris):
    con = True
    inc = 0
    while con:
        if baris[inc] == " ":            
            inc+=1
        else :
            con = False
    baris = baris[inc:len(baris)]
    baris = baris.replace("\r","")
    baris = baris.replace("\n","")
    baris = baris.replace("\t","")
    return baris

def checkbox(salt, id):
    ubox = "[]"
    cbox = "[X]"    
    for i in range(len(salt)):
        # Deteksi Unchecked Box
        if ubox in salt[i]:
            print("Unchecked Box found")
            print(salt[i])
            ubox = salt[i].replace("[","")
            mInner = ubox.replace("]","")
            mInner = cleanFirst(mInner)
            db = Component(type_component="unchecked_box",value=salt[i],wireframe_id=id, inner=mInner)
            db.save()
        # Deteksi Checked Box
        elif cbox in salt[i]:
            print("Checked Box found")
            print(salt[i])
            cbox = salt[i].replace(cbox,"")
            mInner = cleanFirst(cbox)
            db = Component(type_component="checked_box",value=salt[i],wireframe_id=id, inner=mInner)
            db.save()
            
def radio(salt, id):
    uradio = "()"
    cradio = "(X)"
    for i in range(len(salt)):
        # Deteksi Unchecked Radio
        if cradio in salt[i]:
            print("Checked-Radio found :")
            print(salt[i])
            ubox = salt[i].replace("(" ,"")
            ubox = ubox.replace(")" ,"")
            mInner = cleanFirst(ubox)
            db = Component(type_component="checked_radio",value=salt[i],wireframe_id=id, inner=mInner)
            db.save()
        # Deteksi Checked Radio
        elif uradio in salt[i]:
            print("Unchecked-Radio found :")
            print(salt[i])
            cbox = salt[i].replace(uradio,"")
            mInner = cleanFirst(cbox)
            db = Component(type_component="unchecked_radio",value=salt[i],wireframe_id=id, inner=mInner)
            db.save()
            
def droplist(salt, id):
    dl = "^"
    for i in range(len(salt)):
        # Deteksi Droplist
        if dl in salt[i]:
            print("Droplist found")
            print(salt[i])
            dl = salt[i].replace(dl,"")
            mInner = cleanFirst(dl)
            db = Component(type_component="droplist",value=salt[i],wireframe_id=id, inner=mInner)
            db.save()

def strings(salt, id):
    for i in range(len(salt)):
        # Deteksi String
        teks = salt[i].replace(" ","")
        if teks.isalnum():
            print("Text found")
            print(salt[i])
            db = Component(type_component="strings",value=salt[i],wireframe_id=id, inner=salt[i])
            db.save()

def inputfield(salt, id):
    for i in range(len(salt)):
        # Deteksi Textarea
        ta = "\""
        if ta in salt[i]:
            print("Form Field found")
            print(salt[i])
            ta = salt[i].replace(ta,"")
            mInner = cleanFirst(ta)
            db = Component(type_component="input_field",value=salt[i],wireframe_id=id, inner=mInner)
            db.save()
            
def button(salt, id):
    for i in range(len(salt)):
        # Deteksi Button
        fi = "["
        la = "]"
        if fi == salt[i][0] and la == salt[i][len(salt[i])-1]:
            print("Button found")
            print(salt[i])
            btn = salt[i].replace("[","")
            btn = btn.replace("]","")
            mInner = cleanFirst(btn)
            db = Component(type_component="button",value=salt[i],wireframe_id=id, inner=mInner)
            db.save()

def inspectcomp(salt, id):
    strings(salt, id)
    button(salt, id)
    checkbox(salt, id)
    radio(salt, id)
    inputfield(salt, id)
    droplist(salt, id)
