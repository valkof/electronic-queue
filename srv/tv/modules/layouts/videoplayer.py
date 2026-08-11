import customtkinter as ctk
import vlc
import os
import platform

from sb05_vars import VideoPlayerConfig as Tvpc

class FrameVideoplayer(ctk.CTkFrame):
    """
    Фрейм проигрывания видеофайлов
    """
    def __init__(self, parent, config: Tvpc):
        super().__init__(parent, fg_color=config.bg, overwrite_preferred_drawing_method='direct')
        # self.configure(border_width=1, border_color="blue")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # self._mediator = mediator

        self.instance = vlc.Instance(['--no-xlib', '--ignore-config', '--no-plugins-cache'])
 
        self.player: vlc.MediaPlayer = self.instance.media_player_new()
        self.vls_volume = config.volume
        self.list_player = self.instance.media_list_player_new()

        folder_path = os.path.join(os.getcwd(), "videos")

        video_filesname = []
        video_filesname += os.listdir(folder_path)
        
        self.media_list = self.instance.media_list_new()
        for f in video_filesname:
          media = self.instance.media_new(os.path.join(os.getcwd(), "videos", str(f)))
          self.media_list.add_media(media)

        self.list_player.set_media_list(self.media_list)
        self.list_player.set_media_player(self.player)
        self.list_player.set_playback_mode(vlc.PlaybackMode.loop)

    def play_video(self):
        count_media = self.media_list.count()
        if count_media == 0:
            # self.put_photo()
            return        
        # Воспроизведение
        winfo_id = int(self.winfo_id())
        if platform.system() == 'Windows':
          print('windows')
          self.player.set_hwnd(winfo_id)
        else:
          print('centos')
          self.player.set_xwindow(winfo_id)
        self.list_player.play()
        self.set_vlc_volume(self.vls_volume)

    def set_vlc_volume(self, volume_level: int):
        if self.player.is_playing():
            self.player.audio_set_volume(int(volume_level))
        else:
            self.after(500, lambda: self.set_vlc_volume(volume_level))

