
import streamlit as st
from calArea import CalcArea, CalcRiser
import csv 

def savecsv_gating(filename):
    # field names 
    fields = ['Head', 'LossFactor', 'FlowRate', 'CastingHeight_P', 'TotalCasting_C', 'Name', 'Area', 'Width', 'Height']  
    # data rows of csv file 
    data = CalcArea.data
    # writing to csv file 
    with open(filename, 'w', encoding='UTF8', newline='') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
        # writing the fields 
        csvwriter.writerow(fields)
        csvwriter.writerows(data)

def savecsv_riser(riser_file,riser_data):
    riser_header = ['Material','CastingWt','CastingMod','ColdRiser',
                            'NeckMod','RiserMod',
                            'NeckW','NeckH','NeckL',
                            'RiserBase','RiserTop','RiserH','RiserWt','RiserFeed'] 
    riser_data = CalcRiser.data

    with open(riser_file, 'w', encoding='UTF8', newline='') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(riser_header)
        csvwriter.writerows(riser_data)
ch = st.radio("รายก่รคำนวณ",("CalGating","CatRiser","Other"))

if ch == "CalGating":
    h = st.number_input("กรุณาเลือกตัวเลขความสูง",min_value=0,max_value=400,value=200,step=5)
    f = st.number_input("กรุณาเลือกตัวเลข f",min_value=0.0,max_value=0.9,value=0.4,step=0.1)
    q = st.number_input("กรุณาเลือกตัวเลข flowrate",min_value=0.0,max_value=10.0,value=1.0,step=0.1)
    p = st.number_input("กรุณาเลือกตัวเลขความสูงงานด้านบน",min_value=0,max_value=200,value=30,step=10)
    c = st.number_input("กรุณาเลือกตัวเลขความสูงงานทั้งหมด",min_value=0,max_value=250,value=100,step=10)
    name = st.text_input("กรอกชื่อ runner_n/choke_n/ingate_n")
    fname = st.text_input("กรอกชื่อไฟล์ที่จะบันทึก")
    st.text("ข้อมูลของคุณ คือ : " + str(h)+ " " + str(f)+ " " + str(q)+ " "+ str(p)+ " "+ str(c)+ " "+ name)
    c1 = CalcArea(h=h,f=f,q=q,p=p,c=c,name=name)

    calc = st.button("คำนวณ gating")
    label_res = st.empty()
    label_res.text("คุณยังไม่ได้กดปุ่มcalc")
    save = st.button("บันทึกลงไฟล์")
    label_save = st.empty()
    label_save.text("คุณยังไม่ได้กดปุ่มsave")

    if calc:
        result = c1.save()
        label_res.text("ผลการคำนวณ: "+f'name:{result[5]} , area:{result[6]:.0f} mm2 , width:{result[7]:.0f} mm , height:{result[8]:.1f} mm')

    if save:
        savecsv_gating(fname,CalcArea.data)
        label_save.text("บันทึกผลคำนวณลงไฟล์ "+ fname + "เรียบร้อยแล้ว")







