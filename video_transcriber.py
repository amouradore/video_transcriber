import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
import speech_recognition as sr
import os
import threading
from pydub import AudioSegment
from urllib.parse import urlparse, parse_qs
import yt_dlp

# Définition des langues supportées
LANGUAGES = {
    "العربية": "ar-AR",
    "English": "en-US",
    "Français": "fr-FR",
    "中文": "zh-CN",
    "Italiano": "it-IT"
}

class TranscriberApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("برنامج تحويل الفيديو إلى نص")
        self.root.geometry("800x600")
        ctk.set_appearance_mode("dark")
        
        # Variables
        self.current_file = None
        self.is_processing = False
        self.selected_language = tk.StringVar(value="Français")
        
        self.setup_ui()

    def setup_ui(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Titre
        title_label = ctk.CTkLabel(
            main_frame, 
            text="برنامج تحويل الفيديو إلى نص",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=20)

        # Zone de sélection de la langue
        language_frame = ctk.CTkFrame(main_frame)
        language_frame.pack(fill="x", padx=20, pady=10)
        
        language_label = ctk.CTkLabel(
            language_frame,
            text="اختر اللغة:",
            font=("Arial", 14)
        )
        language_label.pack(side="right", padx=10)

        language_menu = ctk.CTkOptionMenu(
            language_frame,
            values=list(LANGUAGES.keys()),
            variable=self.selected_language
        )
        language_menu.pack(side="left", padx=10)

        # Entrée URL YouTube
        self.url_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="ضع رابط اليوتيوب هنا",
            width=400
        )
        self.url_entry.pack(pady=20)

        # Bouton de traitement
        self.process_btn = ctk.CTkButton(
            main_frame,
            text="بدء التحويل",
            command=self.process_youtube
        )
        self.process_btn.pack(pady=10)

        # Zone de progression
        self.progress_bar = ctk.CTkProgressBar(main_frame)
        self.progress_bar.pack(fill="x", padx=20, pady=20)
        self.progress_bar.set(0)

        # Zone de texte pour la transcription
        self.text_area = ctk.CTkTextbox(
            main_frame,
            width=700,
            height=200
        )
        self.text_area.pack(pady=20)

        # Bouton de sauvegarde
        self.save_btn = ctk.CTkButton(
            main_frame,
            text="حفظ النص",
            command=self.save_transcription
        )
        self.save_btn.pack(pady=10)

    def process_youtube(self):
        if not self.url_entry.get():
            messagebox.showerror("خطأ", "الرجاء إدخال رابط اليوتيوب")
            return
        
        threading.Thread(target=self._process_youtube_thread).start()

    def transcribe_audio(self, wav_file):
        """Transcrit l'audio en gérant les chunks"""
        try:
            # Charger le fichier audio avec pydub
            audio = AudioSegment.from_wav(wav_file)
            
            # Durée en millisecondes
            duration = len(audio)
            
            # Créer des chunks de 30 secondes
            chunk_length = 30 * 1000  # 30 secondes en millisecondes
            chunks = []
            
            for i in range(0, duration, chunk_length):
                chunk = audio[i:i + chunk_length]
                chunk_file = f"temp/chunk_{i}.wav"
                chunk.export(chunk_file, format="wav")
                chunks.append(chunk_file)
            
            # Transcription par chunks
            r = sr.Recognizer()
            full_text = []
            
            for i, chunk_file in enumerate(chunks):
                try:
                    with sr.AudioFile(chunk_file) as source:
                        audio_data = r.record(source)
                        
                    # Ajuster la sensibilité de la reconnaissance
                    r.energy_threshold = 300
                    r.dynamic_energy_threshold = True
                    r.dynamic_energy_adjustment_damping = 0.15
                    r.dynamic_energy_ratio = 1.5
                    
                    # Transcription avec timeout et gestion d'erreurs
                    try:
                        text = r.recognize_google(
                            audio_data,
                            language=LANGUAGES[self.selected_language.get()],
                            show_all=False
                        )
                        full_text.append(text)
                        
                        # Mise à jour progressive du texte
                        self.text_area.delete("1.0", tk.END)
                        self.text_area.insert("1.0", " ".join(full_text))
                        self.root.update()
                        
                    except sr.RequestError:
                        # Réessayer une fois en cas d'erreur
                        text = r.recognize_google(
                            audio_data,
                            language=LANGUAGES[self.selected_language.get()],
                            show_all=False
                        )
                        full_text.append(text)
                        
                finally:
                    # Nettoyage du chunk
                    try:
                        os.remove(chunk_file)
                    except:
                        pass
            
            return " ".join(full_text)
            
        except Exception as e:
            raise Exception(f"خطأ في التعرف على الكلام: {str(e)}")

    def _process_youtube_thread(self):
        try:
            self.set_processing_state(True)
            url = self.url_entry.get()
            
            if not self._is_valid_youtube_url(url):
                messagebox.showerror("خطأ", "رابط يوتيوب غير صالح")
                return
                
            temp_dir = "temp"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
                
            try:
                # Configuration yt-dlp
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'wav',
                        'preferredquality': '192',
                    }],
                    'outtmpl': os.path.join(temp_dir, 'temp_audio.%(ext)s'),
                    'quiet': True
                }
                
                # Téléchargement avec yt-dlp
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                wav_file = os.path.join(temp_dir, 'temp_audio.wav')
                
                # Transcription avec la nouvelle méthode
                text = self.transcribe_audio(wav_file)
                
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", text)
                
            finally:
                # Nettoyage
                try:
                    if os.path.exists(wav_file):
                        os.remove(wav_file)
                except Exception:
                    pass
                    
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
        finally:
            self.set_processing_state(False)

    def _is_valid_youtube_url(self, url):
        try:
            parsed_url = urlparse(url)
            if parsed_url.netloc in ['www.youtube.com', 'youtube.com', 'youtu.be']:
                if parsed_url.path == '/watch':
                    return bool(parse_qs(parsed_url.query).get('v'))
                elif parsed_url.netloc == 'youtu.be':
                    return len(parsed_url.path) > 1
                return True
            return False
        except:
            return False

    def save_transcription(self):
        text = self.text_area.get("1.0", tk.END)
        if not text.strip():
            messagebox.showwarning("تنبيه", "لا يوجد نص للحفظ")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)
            messagebox.showinfo("نجاح", "تم حفظ النص بنجاح")

    def set_processing_state(self, is_processing):
        self.is_processing = is_processing
        state = "disabled" if is_processing else "normal"
        self.process_btn.configure(state=state)
        self.url_entry.configure(state=state)
        self.save_btn.configure(state=state)
        
        if is_processing:
            self.progress_bar.start()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", "جاري المعالجة...")
        else:
            self.progress_bar.stop()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TranscriberApp()
    app.run()