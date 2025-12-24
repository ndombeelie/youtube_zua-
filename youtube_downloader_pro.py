import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import re
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("yt-dlp n'est pas installé. Installez-le avec: pip install yt-dlp")

class YouTubeDownloaderPro:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 YouTube Downloader Pro")
        self.root.geometry("500x350") 
        self.root.resizable(False, False)
        
        # Variables - Définir le dossier Downloads par défaut
        default_download_folder = str(Path.home() / "Downloads")
        self.selected_folder = tk.StringVar(value=default_download_folder)
        self.youtube_url = tk.StringVar()
        self.format_var = tk.StringVar(value="MP4")
        self.quality_var = tk.StringVar(value="720p")
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="État: Prêt")
        self.download_info = tk.StringVar(value="")
        
        self.is_downloading = False
        self.is_paused = False
        self.should_cancel = False
        self.download_thread = None
        self.current_ydl = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Fond noir pur
        self.root.configure(bg='#000000')
        
        # Style personnalisé
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configuration des styles
        style.configure('Red.TButton', 
                       background='#ff0000',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Arial', 9, 'bold'))
        style.map('Red.TButton',
                 background=[('active', '#cc0000')])
        
        style.configure('Dark.TButton',
                       background='#1a1a1a',
                       foreground='white',
                       borderwidth=1,
                       font=('Arial', 8))
        style.map('Dark.TButton',
                 background=[('active', '#2a2a2a')])
        
        # Combobox style
        style.configure('TCombobox',
                       fieldbackground='#1a1a1a',
                       background='#1a1a1a',
                       foreground='white',
                       arrowcolor='white',
                       borderwidth=1)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#000000')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # 1️⃣ Sélection de dossier
        folder_frame = tk.Frame(main_frame, bg='#000000')
        folder_frame.pack(fill=tk.X, pady=(0, 10))
        
        folder_btn = ttk.Button(folder_frame, text="📁 Dossier", 
                               style='Red.TButton',
                               command=self.select_folder)
        folder_btn.pack(side=tk.LEFT, padx=(0, 8), ipadx=5, ipady=1)
        
        folder_label = tk.Label(folder_frame, 
                               textvariable=self.selected_folder,
                               bg='#000000',
                               fg='white',
                               font=('Arial', 8))
        folder_label.pack(side=tk.LEFT)
        
        # 2️⃣ Lien YouTube
        url_frame = tk.Frame(main_frame, bg='#000000')
        url_frame.pack(fill=tk.X, pady=(0, 10))
        
        url_label = tk.Label(url_frame, 
                            text="Lien YouTube:",
                            bg='#000000',
                            fg='white',
                            font=('Arial', 8, 'bold'))
        url_label.pack(side=tk.LEFT, padx=(0, 8))
        
        url_entry = tk.Entry(url_frame,
                            textvariable=self.youtube_url,
                            bg='#1a1a1a',
                            fg='white',
                            font=('Arial', 9),
                            insertbackground='white',
                            relief=tk.SOLID,
                            borderwidth=1)
        url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        
        # 3️⃣ Format & Qualité + Bouton Télécharger
        controls_frame = tk.Frame(main_frame, bg='#000000')
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Format dropdown
        format_combo = ttk.Combobox(controls_frame,
                                   textvariable=self.format_var,
                                   values=['MP4', 'MP3', 'WEBM'],
                                   state='readonly',
                                   width=7,
                                   font=('Arial', 8))
        format_combo.pack(side=tk.LEFT, padx=(0, 5))
        
        # Qualité dropdown
        quality_combo = ttk.Combobox(controls_frame,
                                    textvariable=self.quality_var,
                                    values=['1080p', '720p', '480p', 'Audio'],
                                    state='readonly',
                                    width=7,
                                    font=('Arial', 8))
        quality_combo.pack(side=tk.LEFT, padx=(0, 8))
        
        # Bouton Télécharger
        download_btn = ttk.Button(controls_frame,
                                 text="⬇️ Télécharger",
                                 style='Red.TButton',
                                 command=self.start_download)
        download_btn.pack(side=tk.LEFT, ipadx=8, ipady=1)
        
        # 4️⃣ Barre de progression
        progress_frame = tk.Frame(main_frame, bg='#000000')
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Style pour la barre de progression verte
        style.configure('Green.Horizontal.TProgressbar',
                       background='#00ff00',
                       troughcolor='#1a1a1a',
                       bordercolor='#000000',
                       lightcolor='#00ff00',
                       darkcolor='#00cc00')
        
        self.progress_bar = ttk.Progressbar(progress_frame,
                                           variable=self.progress_var,
                                           maximum=100,
                                           mode='determinate',
                                           style='Green.Horizontal.TProgressbar')
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.progress_label = tk.Label(progress_frame,
                                      text="0%",
                                      bg='#000000',
                                      fg='#00ff00',
                                      font=('Arial', 8, 'bold'),
                                      width=4)
        self.progress_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 5️⃣ Contrôles du téléchargement
        action_frame = tk.Frame(main_frame, bg='#000000')
        action_frame.pack(fill=tk.X, pady=(0, 10))
        
        status_label = tk.Label(action_frame,
                               textvariable=self.status_var,
                               bg='#000000',
                               fg='white',
                               font=('Arial', 8))
        status_label.pack(side=tk.LEFT)
        
        # Boutons d'action à droite
        buttons_frame = tk.Frame(action_frame, bg='#000000')
        buttons_frame.pack(side=tk.RIGHT)
        
        self.pause_btn = ttk.Button(buttons_frame,
                                   text="⏸️",
                                   style='Dark.TButton',
                                   command=self.pause_download,
                                   state=tk.DISABLED,
                                   width=3)
        self.pause_btn.pack(side=tk.LEFT, padx=2)
        
        self.cancel_btn = ttk.Button(buttons_frame,
                                    text="❌",
                                    style='Dark.TButton',
                                    command=self.cancel_download,
                                    state=tk.DISABLED,
                                    width=3)
        self.cancel_btn.pack(side=tk.LEFT, padx=2)
        
        clear_btn = ttk.Button(buttons_frame,
                              text="🗑️",
                              style='Red.TButton',
                              command=self.clear_fields,
                              width=3)
        clear_btn.pack(side=tk.LEFT, padx=2)
        
        # 6️⃣ Informations de téléchargement
        info_frame = tk.Frame(main_frame, bg='#1a1a1a', relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        info_label = tk.Label(info_frame,
                             textvariable=self.download_info,
                             bg='#1a1a1a',
                             fg='white',
                             font=('Consolas', 8),
                             justify=tk.LEFT,
                             anchor='nw')
        info_label.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder.set(folder)
            
    def validate_youtube_url(self, url):
        youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        return re.match(youtube_regex, url) is not None
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
            elif 'total_bytes_estimate' in d:
                percent = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
            else:
                percent = 0
                
            self.progress_var.set(percent)
            self.progress_label.config(text=f"{int(percent)}%")
            
            # Informations de téléchargement
            speed = d.get('speed', 0)
            speed_str = f"{speed / 1024 / 1024:.2f} MB/s" if speed else "N/A"
            
            downloaded = d.get('downloaded_bytes', 0)
            downloaded_str = f"{downloaded / 1024 / 1024:.2f} MB"
            
            eta = d.get('eta', 0)
            eta_str = f"{eta}s" if eta else "N/A"
            
            info_text = f"Vitesse: {speed_str}\n"
            info_text += f"Téléchargé: {downloaded_str}\n"
            info_text += f"Temps restant: {eta_str}\n"
            info_text += f"Progression: {int(percent)}%"
            
            self.download_info.set(info_text)
            self.status_var.set("État: Téléchargement en cours...")
            
        elif d['status'] == 'finished':
            self.progress_var.set(100)
            self.progress_label.config(text="100%")
            self.status_var.set("État: Terminé ✓")
            self.download_info.set("Téléchargement terminé avec succès!")
            self.is_downloading = False
            self.pause_btn.config(state=tk.DISABLED)
            self.cancel_btn.config(state=tk.DISABLED)

    def start_download(self):
        if self.is_downloading:
            messagebox.showwarning("Attention", "Un téléchargement est déjà en cours!")
            return
            
        url = self.youtube_url.get().strip()
        folder = self.selected_folder.get()
        
        # Validation
        if not url:
            messagebox.showerror("Erreur", "Veuillez entrer un lien YouTube!")
            return
            
        if not self.validate_youtube_url(url):
            messagebox.showerror("Erreur", "URL YouTube invalide!")
            return
            
        if not folder or folder == "Aucun dossier sélectionné":
            messagebox.showerror("Erreur", "Veuillez sélectionner un dossier de destination!")
            return
            
        if not os.path.exists(folder):
            messagebox.showerror("Erreur", "Le dossier sélectionné n'existe pas!")
            return
        
        # Démarrer le téléchargement dans un thread séparé
        self.is_downloading = True
        self.is_paused = False
        self.should_cancel = False
        self.pause_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.NORMAL)
        self.progress_var.set(0)
        self.progress_label.config(text="0%")
        self.status_var.set("État: Initialisation...")
        self.download_info.set("Préparation du téléchargement...")
        
        self.download_thread = threading.Thread(target=self.download_video, args=(url, folder))
        self.download_thread.daemon = True
        self.download_thread.start()
    
    def download_video(self, url, folder):
        try:
            format_choice = self.format_var.get()
            quality = self.quality_var.get()
            
            # Chemin vers ffmpeg et cookies locaux
            current_dir = os.path.dirname(os.path.abspath(__file__))
            ffmpeg_path = os.path.join(current_dir, 'ffmpeg.exe')
            cookies_path = os.path.join(current_dir, 'cookies.txt')
            
            # Configuration yt-dlp
            ydl_opts = {
                'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'quiet': False,
                'no_warnings': False,
            }
            
            # Ajouter le chemin ffmpeg si le fichier existe
            if os.path.exists(ffmpeg_path):
                ydl_opts['ffmpeg_location'] = current_dir
            
            # Ajouter les cookies si le fichier existe
            if os.path.exists(cookies_path):
                ydl_opts['cookiefile'] = cookies_path
                self.root.after(0, lambda: self.download_info.set("Cookies détectés ✓\nPréparation du téléchargement..."))
            
            # Configuration selon le format
            if format_choice == 'MP3' or quality == 'Audio':
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            elif format_choice == 'MP4':
                if quality == '1080p':
                    ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
                elif quality == '720p':
                    ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
                elif quality == '480p':
                    ydl_opts['format'] = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
                else:
                    ydl_opts['format'] = 'best'
                ydl_opts['merge_output_format'] = 'mp4'
            elif format_choice == 'WEBM':
                ydl_opts['format'] = 'bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]'
            
            # Téléchargement avec vérification d'annulation
            self.current_ydl = yt_dlp.YoutubeDL(ydl_opts)
            
            # Vérifier si annulé avant de commencer
            if self.should_cancel:
                self.is_downloading = False
                self.should_cancel = False
                return
                
            self.current_ydl.download([url])
            
            # Si terminé sans erreur et pas annulé
            if not self.should_cancel:
                self.root.after(0, lambda: self.status_var.set("État: Terminé ✓"))
                self.root.after(0, lambda: self.download_info.set("Téléchargement terminé avec succès!"))
                
        except Exception as e:
            if not self.should_cancel:
                error_msg = str(e)
                self.root.after(0, lambda: self.status_var.set(f"État: Erreur"))
                self.root.after(0, lambda: self.download_info.set(f"Erreur:\n{error_msg}"))
                self.root.after(0, lambda: messagebox.showerror("Erreur de téléchargement", error_msg))
        finally:
            self.is_downloading = False
            self.should_cancel = False
            self.current_ydl = None
            self.root.after(0, lambda: self.pause_btn.config(state=tk.DISABLED))
            self.root.after(0, lambda: self.cancel_btn.config(state=tk.DISABLED))
    
    def pause_download(self):
        """Note: yt-dlp ne supporte pas la pause native, cette fonction simule le comportement"""
        if self.is_paused:
            self.is_paused = False
            self.pause_btn.config(text="⏸️")
            self.status_var.set("État: Reprise du téléchargement...")
            # Dans une implémentation complète, il faudrait relancer le téléchargement
        else:
            self.is_paused = True
            self.pause_btn.config(text="▶️")
            self.status_var.set("État: En pause")
            # Note: yt-dlp continue en arrière-plan, pause réelle nécessiterait d'arrêter le thread
    
    def cancel_download(self):
        """Annule le téléchargement en cours"""
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment annuler le téléchargement?"):
            self.should_cancel = True
            self.is_downloading = False
            self.is_paused = False
            
            # Arrêter yt-dlp si possible
            if self.current_ydl:
                try:
                    # Forcer l'arrêt en levant une exception
                    self.current_ydl._download_retcode = 1
                except:
                    pass
            
            self.status_var.set("État: Annulé")
            self.download_info.set("Téléchargement annulé par l'utilisateur")
            self.pause_btn.config(state=tk.DISABLED, text="⏸️")
            self.cancel_btn.config(state=tk.DISABLED)
            self.progress_var.set(0)
            self.progress_label.config(text="0%")
    
    def clear_fields(self):
        """Efface le lien YouTube et le terminal, mais garde le chemin du dossier"""
        # Ne pas effacer si un téléchargement est en cours
        if self.is_downloading:
            if not messagebox.askyesno("Attention", "Un téléchargement est en cours. Voulez-vous l'annuler et tout effacer?"):
                return
            # Annuler le téléchargement d'abord
            self.should_cancel = True
            self.is_downloading = False
            if self.current_ydl:
                try:
                    self.current_ydl._download_retcode = 1
                except:
                    pass
        
        # Effacer seulement le lien YouTube et le terminal (pas le dossier)
        self.youtube_url.set("")
        self.download_info.set("")
        self.progress_var.set(0)
        self.progress_label.config(text="0%")
        self.status_var.set("État: Prêt")
        self.is_paused = False
        self.should_cancel = False
        
        # Désactiver les boutons de contrôle
        self.pause_btn.config(state=tk.DISABLED, text="⏸️")
        self.cancel_btn.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = YouTubeDownloaderPro(root)
    root.mainloop()

if __name__ == "__main__":
    main()
