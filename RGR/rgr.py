import io
import speech_recognition as sr
from gtts import gTTS
import pygame
import customtkinter as ctk
from threading import Thread

class VoiceTextConverter:
    def __init__(self):

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.window = ctk.CTk()
        self.window.title("Конвертер Текст ⇄ Голос")
        self.window.geometry("900x750")
        
        pygame.mixer.init()
        
        self.create_widgets()
        
    def create_widgets(self):

        self.tabview = ctk.CTkTabview(self.window)
        self.tabview.pack(expand=True, fill="both", padx=20, pady=20)
    
        self.tabview.add("Текст → Голос")
        self.tabview.add("Голос → Текст")
        
        self.setup_text_to_speech_tab(self.tabview.tab("Текст → Голос"))

        self.setup_speech_to_text_tab(self.tabview.tab("Голос → Текст"))
    
    def setup_text_to_speech_tab(self, tab):

        content_frame = ctk.CTkFrame(tab)
        content_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
        title = ctk.CTkLabel(content_frame, text="Перетворення тексту в голос", 
                           font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=10)
        
        input_label = ctk.CTkLabel(content_frame, text="Введіть текст для озвучення:",
                                 font=ctk.CTkFont(size=14))
        input_label.pack(pady=5)
        
        self.text_input = ctk.CTkTextbox(content_frame, width=700, height=200,
                                       font=ctk.CTkFont(size=14))
        self.text_input.pack(pady=10)
        
        options_frame = ctk.CTkFrame(content_frame)
        options_frame.pack(pady=10)
        
        lang_label = ctk.CTkLabel(options_frame, text="Мова тексту:", 
                                font=ctk.CTkFont(size=14))
        lang_label.pack(side="left", padx=10)
        
        self.language_var = ctk.StringVar(value="uk")
        languages = {"Українська": "uk", "English": "en", "Русский": "ru"}
        
        language_menu = ctk.CTkOptionMenu(options_frame, values=list(languages.keys()),
                                        command=lambda x: self.language_var.set(languages[x]))
        language_menu.pack(side="left", padx=10)
        
        voice_label = ctk.CTkLabel(options_frame, text="Голос:", 
                                font=ctk.CTkFont(size=14))
        voice_label.pack(side="left", padx=10)
        
        self.voice_var = ctk.StringVar(value="slow")
        voices = {"Повільний": "slow", "Нормальний": "normal"}
        
        voice_menu = ctk.CTkOptionMenu(options_frame, values=list(voices.keys()),
                                        command=lambda x: self.voice_var.set(voices[x]))
        voice_menu.pack(side="left", padx=10)
        

        button_frame = ctk.CTkFrame(content_frame)
        button_frame.pack(pady=20)
        
        convert_button = ctk.CTkButton(button_frame, text="Перетворити в голос",
                                     command=self.text_to_speech,
                                     font=ctk.CTkFont(size=14))
        convert_button.pack(side="left", padx=10)
        
        clear_button = ctk.CTkButton(button_frame, text="Очистити",
                                   command=lambda: self.text_input.delete("1.0", "end"),
                                   font=ctk.CTkFont(size=14))
        clear_button.pack(side="left", padx=10)
        
        self.tts_status_label = ctk.CTkLabel(content_frame, text="",
                                           font=ctk.CTkFont(size=14))
        self.tts_status_label.pack(pady=10)
    
    def text_to_speech(self):
        text = self.text_input.get("1.0", "end").strip()
        if not text:
            self.tts_status_label.configure(text="Будь ласка, введіть текст")
            return
        
        try:
            self.tts_status_label.configure(text="Генерування аудіо...")
            self.window.update()
            
            language = self.language_var.get()
            speed = self.voice_var.get()
            
            audio = io.BytesIO()
            tts = gTTS(text=text, lang=language, slow=(speed == "slow"))
            tts.write_to_fp(audio)
            audio.seek(0)
            
            pygame.mixer.init()
            pygame.mixer.music.load(audio)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                self.window.update()  
            
            pygame.mixer.quit()
            audio.close()
            
            self.tts_status_label.configure(text="Аудіо відтворено")
            
        except Exception as e:
            self.tts_status_label.configure(text=f"Помилка: {str(e)}")
    
    def setup_speech_to_text_tab(self, tab):

        content_frame = ctk.CTkFrame(tab)
        content_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        title = ctk.CTkLabel(content_frame, text="Перетворення голосу в текст",
                           font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=10)
        
        instructions = ctk.CTkLabel(content_frame, 
                                 text="Натисніть кнопку 'Почати запис' та говоріть",
                                 font=ctk.CTkFont(size=14))
        instructions.pack(pady=10)
        
        lang_frame = ctk.CTkFrame(content_frame)
        lang_frame.pack(pady=10)
        
        lang_label = ctk.CTkLabel(lang_frame, text="Мова розпізнавання:", 
                                font=ctk.CTkFont(size=14))
        lang_label.pack(side="left", padx=10)
        
        self.stt_language_var = ctk.StringVar(value="uk-UA")
        stt_languages = {
            "Українська": "uk-UA", 
            "English (US)": "en-US", 
            "English (UK)": "en-GB"
        }
        
        stt_language_menu = ctk.CTkOptionMenu(lang_frame, values=list(stt_languages.keys()),
                                        command=lambda x: self.stt_language_var.set(stt_languages[x]))
        stt_language_menu.pack(side="left", padx=10)
        
        button_frame = ctk.CTkFrame(content_frame)
        button_frame.pack(pady=20)
        
        self.record_button = ctk.CTkButton(button_frame, text="Почати запис",
                                         command=self.toggle_recording,
                                         font=ctk.CTkFont(size=14))
        self.record_button.pack(side="left", padx=10)
        
        clear_button = ctk.CTkButton(button_frame, text="Очистити",
                                   command=lambda: self.speech_output.delete("1.0", "end"),
                                   font=ctk.CTkFont(size=14))
        clear_button.pack(side="left", padx=10)
        

        output_label = ctk.CTkLabel(content_frame, text="Розпізнаний текст:",
                                  font=ctk.CTkFont(size=14))
        output_label.pack(pady=5)
        
        self.speech_output = ctk.CTkTextbox(content_frame, width=700, height=200,
                                          font=ctk.CTkFont(size=14))
        self.speech_output.pack(pady=10)
        
        self.stt_status_label = ctk.CTkLabel(content_frame, text="",
                                           font=ctk.CTkFont(size=14))
        self.stt_status_label.pack(pady=10)
        
        self.is_recording = False
    
    def toggle_recording(self):
        if not self.is_recording:
            self.record_button.configure(text="Зупинити запис")
            self.is_recording = True
            self.stt_status_label.configure(text="Запис...")
            Thread(target=self.record_audio).start()
        else:
            self.record_button.configure(text="Почати запис")
            self.is_recording = False
            self.stt_status_label.configure(text="")
    
    def record_audio(self):
        r = sr.Recognizer()
        while self.is_recording:
            with sr.Microphone() as source:
                try:
                    r.adjust_for_ambient_noise(source, duration=0.5)  
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    
                    language = self.stt_language_var.get()
                    text = r.recognize_google(audio, language=language)
                    
                    self.speech_output.insert("end", text + "\n")
                    self.stt_status_label.configure(text="Текст розпізнано")
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    self.stt_status_label.configure(text="Не вдалося розпізнати мову")
                except Exception as e:
                    self.stt_status_label.configure(text=f"Помилка: {str(e)}")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = VoiceTextConverter()
    app.run()