#Ini adalah program untuk berbicara dengan model gpt3.5
#konteks pembicaraan akan disimpan untuk mensimulasikan pembicaraan yang lebih immersive

'''import seluruh package'''
import os
import time
import pyaudio
#saya menggunakan playsound versi 1.2.2 karena versi terbarunya tidak dapat memutar output gTTS
import playsound
from gtts import gTTS
import openai
import speech_recognition as sr
import uuid


'''register API key'''
api_key='isi API key'
openai.api_key=api_key


'''inisiasi list messages agar dapat menyimpan konteks pembicaraan
dan setup gaya chatbot yang diinginkan'''
messages=[]
#contoh input system-msg: adik lucu, dokter, dsb
system_msg=input('what kind of chatbot you want to talk to?')
messages.append({"role":"system","content":system_msg})
print('your new chatbot is ready')


'''proses komunikasi dengan openai menggunakan suara'''
while True:
    r=sr.Recognizer()
    # silakan bereksperimen untuk device_index karena akan beda tiap device yang digunakan
    with sr.Microphone(device_index=1) as source:
        audio=r.listen(source)
        said=""
        try:
            # silakan berbicara menggunakan bahasa Indonesia
            said=r.recognize_google(audio,language="id-ID")
            print(said)
            # komunikasi hanya dapat berjalan jika nama AI (dalam kasus ini adalah Queen) disebut
            # contoh: Queen, tolong hapalkan nama depan dan belakang saya
            if 'Queen' in said:
                new_string=said.replace('Queen',"")
                new_string=new_string.strip()
                print(new_string)
                #suara kita akan diconvert menjadi text dan menjadi input bernama new_string
                messages.append({"role": "user", "content": new_string})
                #input diterima model
                completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
                #model akan membuat reply
                text = completion.choices[0].message.content
                print(text)
                #model akan merekam konteks pembicaraan
                messages.append({"role": "assistant", "content": text})
                #reply dari model akan diconvert menjadi suara menggunakan gTTS
                speech = gTTS(text=text, lang='id', slow=False)
                file_name=f"welcome_{str(uuid.uuid4())}.mp3"
                #suara akan disimpan sebagai file mp3
                speech.save(file_name)
                #suara akan diputar secara otomatis
                playsound.playsound(file_name,block=False)
        except Exception as e:
            print(f"{str(e)}")
