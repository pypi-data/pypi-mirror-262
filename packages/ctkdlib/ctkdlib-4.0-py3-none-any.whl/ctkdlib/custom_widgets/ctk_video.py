import gc
import warnings
import logging

try:
    import av
    import pyaudio
    logging.getLogger('libav').setLevel(logging.ERROR)  # removes warning: deprecated pixel format used
    missing = False
except ImportError:
    missing = True
    
import time
import threading
import tkinter as tk
from PIL import ImageTk, Image, ImageOps
from typing import Tuple, Dict
import customtkinter

"""
Originally taken from TkVideoPlayer made by PaulleDemon (shared under MIT)
Modified by Akascape
"""

class CTkVideo(tk.Label):

    def __init__(self,
                 master,
                 width=300,
                 height=150,
                 scaled: bool = True,
                 consistant_frame_rate: bool = True,
                 keep_aspect: bool = False,
                 audio=True,
                 bg_color=None,
                 fg_color="black",
                 **kwargs):

        self.ctk = customtkinter.CTkLabel(master)
        
        super(CTkVideo, self).__init__(master, text="", bg=self.ctk._apply_appearance_mode(fg_color), **kwargs)
        self.width = int(self.ctk._apply_widget_scaling(width))
        self.height = int(self.ctk._apply_widget_scaling(height))

        self.default_img = ImageTk.PhotoImage(Image.new("RGBA", (width, height), (0, 0, 0, 0)))
        self.config(width=self.width, height=self.height, image=self.default_img)
        
        self.path = ""
        self._load_thread = None
        self.fg = fg_color
        
        self._paused = True
        self._stop = True

        self.consistant_frame_rate = consistant_frame_rate # tries to keep the frame rate consistant by skipping over a few frames

        self._container = None

        self._current_img = None
        self._current_frame_Tk = None
        self._frame_number = 0
        self._time_stamp = 0

        self._current_frame_size = (0, 0)

        self._seek = False
        self._seek_sec = 0

        self._audio = audio
        
        self._video_info = {
            "duration": 0, # duration of the video
            "framerate": 0, # frame rate of the video
            "framesize": (0, 0) # tuple containing frame height and width of the video

        }   

        self.set_scaled(scaled)
        self._keep_aspect_ratio = keep_aspect
        self._resampling_method: int = Image.NEAREST

        self.bind("<<Destroy>>", self.stop)
        self.bind("<<FrameGenerated>>", self._display_frame)

        if missing:
            warnings.warn("You are using CTkVideo without installing pyav and pyaudio, please install them!")
            
    def keep_aspect(self, keep_aspect: bool):
        """ keeps the aspect ratio when resizing the image """
        self._keep_aspect_ratio = keep_aspect

    def set_resampling_method(self, method: int):
        """ sets the resampling method when resizing """
        self._resampling_method = method

    def set_size(self, size: Tuple[int, int], keep_aspect: bool=False):
        """ sets the size of the video """
        self.set_scaled(False, self._keep_aspect_ratio)
        self._current_frame_size = size
        self._keep_aspect_ratio = keep_aspect

    def _resize_event(self, event):

        self._current_frame_size = event.width, event.height

        if self._paused and self._current_img and self.scaled:
            if self._keep_aspect_ratio:
                proxy_img = ImageOps.contain(self._current_img.copy(), self._current_frame_size)

            else:
                proxy_img = self._current_img.copy().resize(self._current_frame_size)
            
            self._current_imgtk = ImageTk.PhotoImage(proxy_img)
            self.config(width=self.width, height=self.height, image=self._current_imgtk)


    def set_scaled(self, scaled: bool, keep_aspect: bool = False):
        self.scaled = scaled
        self._keep_aspect_ratio = keep_aspect
        
        if scaled:
            self.bind("<Configure>", self._resize_event)

        else:
            self.unbind("<Configure>")
            self._current_frame_size = self.video_info()["framesize"]


    def _set_frame_size(self, event=None):
        """ sets frame size to avoid unexpected resizing """

        self._video_info["framesize"] = (self._container.streams.video[0].width, self._container.streams.video[0].height)

        self.current_imgtk = ImageTk.PhotoImage(Image.new("RGBA", self._video_info["framesize"], (255, 0, 0, 0)))
        self.config(width=self.width, height=self.height, image=self.current_imgtk)

    def _load(self, path):
        """ load's file from a thread """

        current_thread = threading.current_thread()

        try:
            with av.open(path) as self._container:

                self._container.streams.video[0].thread_type = "AUTO"
                
                self._container.fast_seek = True
                self._container.discard_corrupt = True

                stream = self._container.streams.video[0]

                try:
                    self._video_info["framerate"] = int(stream.average_rate)

                except TypeError:
                    raise TypeError("Not a video file")
                
                try:

                    self._video_info["duration"] = float(stream.duration * stream.time_base)
                    self.event_generate("<<Duration>>")  # duration has been found

                except (TypeError, tk.TclError):  # the video duration cannot be found, this can happen for mkv files
                    pass

                self._frame_number = 0

                self._set_frame_size()

                try:
                    if self._audio:
                        audio_stream = self._container.streams.audio[0]

                        samplerate = audio_stream.rate # this samplerate will work as the video clock
                        channels = audio_stream.channels
                  
                        p = pyaudio.PyAudio()
                        audio_device = p.open(format=pyaudio.paFloat32,
                                              channels=channels,
                                              rate=samplerate,
                                              output=True)
                    else:
                        audio_device = False
                except:
                    audio_device = False
                
                try:
                    self.event_generate("<<Loaded>>") # generated when the video file is opened
                
                except tk.TclError:
                    pass

                now = time.time_ns() // 1_000_000  # time in milliseconds
                then = now

                time_in_frame = (1/self._video_info["framerate"])*1000 # second it should play each frame

                while self._load_thread == current_thread and not self._stop:
                    if self._seek: # seek to specific second
                        self._container.seek(self._seek_sec*1000000 , whence='time', backward=True, any_frame=False) # the seek time is given in av.time_base, the multiplication is to correct the frame
                        self._seek = False
                        self._frame_number = self._video_info["framerate"] * self._seek_sec

                        self._seek_sec = 0

                    if self._paused:
                        time.sleep(0.0001) # to allow other threads to function better when its paused
                        continue
                    
                    self.frame_buffers = [] # flush all previous buffers
                    
                    # print("Frame: ", frame.time, frame.index, self._video_info["framerate"])
                    try:
                        if audio_device and self._audio:
                            
                            dont_seek = False
                    
                            last_audio_buffer = False
                            last_video_buffer = False
                            
                            while True:
                                frame = next(self._container.decode(video=0, audio=0))
                                
                                if 'Video' in repr(frame):
                                    if last_audio_buffer:
                                        if round(float(frame.pts * stream.time_base), 2)<=last_audio_buffer:
                                            self.frame_buffers.append(frame)
                                        else:
                                            break # break if the last audio buffer pts matches the final video buffer pts
                                        if not last_video_buffer:
                                            break
                                        dont_seek = True
                                    else:
                                        self.frame_buffers.append(frame)
                                        last_video_buffer = True
                                        
                                else:
                                    if dont_seek: # avoid excessive buffering, can cause stuttering frames
                                        break
                                    self.frame_buffers.append(frame)
                                    last_audio_buffer = round(float(frame.pts * audio_stream.time_base), 2)
                     
                    
                            self.frame_buffers = sorted(self.frame_buffers, key=lambda f: f.pts * stream.time_base if 'Video' in repr(f) else f.pts * audio_stream.time_base) # sort all the frames based on their presentation time
                        
                            for frame in self.frame_buffers:
                                if 'Video' in repr(frame):
                                    #print("video_frame at",  round(float(frame.pts * stream.time_base), 2))
                                    width = self._current_frame_size[0]
                                    height = self._current_frame_size[1]
                                    if self._keep_aspect_ratio:
                                        im_ratio = frame.width / frame.height
                                        dest_ratio = width / height
                                        if im_ratio != dest_ratio:
                                            if im_ratio > dest_ratio:
                                                new_height = round(frame.height / frame.width * width)
                                                height = new_height
                                            else:
                                                new_width = round(frame.width / frame.height * height)
                                                width = new_width

                                    self._current_img = frame.to_image(width=width, height=height, interpolation="FAST_BILINEAR")

                                    self._frame_number += 1
                            
                                    self.event_generate("<<FrameGenerated>>")

                                    if self._frame_number % self._video_info["framerate"] == 0:
                                        self.event_generate("<<SecondChanged>>")
                                
                                else:
                                    #print("audio_frame at",  round(float(frame.pts * audio_stream.time_base), 2))
                                    self._time_stamp = float(frame.pts * audio_stream.time_base)
                                    audio_data = frame.to_ndarray().astype('float32')
                                    interleaved_data = audio_data.T.flatten().tobytes()
                                    audio_device.write(interleaved_data)
                                    
                                if self._stop or self._paused:
                                    break
                                    
                        else:
                            now = time.time_ns() // 1_000_000  # time in milliseconds
                            delta = now - then  # time difference between current frame and previous frame
                            then = now
                             
                            frame = next(self._container.decode(video=0))

                            self._time_stamp = float(frame.pts * stream.time_base)

                            width = self._current_frame_size[0]
                            height = self._current_frame_size[1]
                            if self._keep_aspect_ratio:
                                im_ratio = frame.width / frame.height
                                dest_ratio = width / height
                                if im_ratio != dest_ratio:
                                    if im_ratio > dest_ratio:
                                        new_height = round(frame.height / frame.width * width)
                                        height = new_height
                                    else:
                                        new_width = round(frame.width / frame.height * height)
                                        width = new_width

                            self._current_img = frame.to_image(width=width, height=height, interpolation="FAST_BILINEAR")

                            self._frame_number += 1
                    
                            self.event_generate("<<FrameGenerated>>")

                            if self._frame_number % self._video_info["framerate"] == 0:
                                self.event_generate("<<SecondChanged>>")

                            if self.consistant_frame_rate:
                                time.sleep(max((time_in_frame - delta)/1000, 0))

                            # time.sleep(abs((1 / self._video_info["framerate"]) - (delta / 1000)))

                    except (StopIteration, av.error.EOFError, tk.TclError):
                        break

            # print("Container: ", self._container.c)
            if self._container:
                self._container.close()
                stream.close()
                self._container = None

            if audio_device:
                audio_device.stop_stream()
                audio_device.close()
                p.terminate()
                audio_stream.close()
            
        finally:
            self._cleanup()
            gc.collect()

    def _cleanup(self):
        self._frame_number = 0
        self._paused = True
        self._stop = True
        self.frame_buffers = []
        
        if self._load_thread:
            self._load_thread = None
        if self._container:
            self._container.close()
            self._container = None
        try:
            self.event_generate("<<Ended>>")
        except tk.TclError:
            pass

    def load(self, path: str):
        """ loads the file from the given path """
        self.stop()
        self.path = path

    def stop(self):
        """ stops reading the file """
        self._paused = True
        self._stop = True
        self._cleanup()

    def pause(self):
        """ pauses the video file """
        self._paused = True

    def play(self):
        """ plays the video file """
        self._paused = False
        self._stop = False

        if not self._load_thread:
            # print("loading new thread...")
            self._load_thread = threading.Thread(target=self._load,  args=(self.path, ), daemon=True)
            self._load_thread.start()

    def mute(self):
        self._audio = False

    def unmute(self):
        self._audio = True
        
    def is_paused(self):
        """ returns if the video is paused """
        return self._paused

    def video_info(self) -> Dict:
        """ returns dict containing duration, frame_rate, file"""
        return self._video_info

    def metadata(self) -> Dict:
        """ returns metadata if available """
        if self._container:
            return self._container.metadata

        return {}

    def current_frame_number(self) -> int:
        """ return current frame number """
        return self._frame_number

    def current_duration(self) -> float:
        """ returns current playing duration in sec """
        return self._time_stamp
    
    def current_img(self) -> Image:
        """ returns current frame image """
        return self._current_img
    
    def _display_frame(self, event):
        """ displays the frame on the label """

        if self.current_imgtk.width() == self._current_img.width and self.current_imgtk.height() == self._current_img.height:
            self.current_imgtk.paste(self._current_img)
        else:
            self.current_imgtk = ImageTk.PhotoImage(self._current_img)
        self.config(width=self.width, height=self.height, image=self.current_imgtk)

    def seek(self, sec: int):
        """ seeks to specific time""" 

        self._seek = True
        self._seek_sec = sec            

    def configure(self, **kwargs):
        if "keep_aspect" in kwargs:
           self._keep_aspect_ratio = kwargs.pop("keep_aspect")
        if "audio" in kwargs:
           self._audio = kwargs.pop("audio")
        if "fg_color" in kwargs:
           super().config(bg=self.ctk._apply_appearance_mode(kwargs.pop("fg_color")))
        if "bg_color" in kwargs:
            kwargs.pop("bg_color")
        if "width" in kwargs:
            self.width = kwargs["width"]
        if "height" in kwargs:
            self.height = kwargs["height"]
        super().config(**kwargs)
    
    def cget(self, param):
        if param=="text":
            raise ValueError
        if param=="justify":
            raise ValueError
        if param=="image":
            raise ValueError
        if param=="font":
            raise ValueError
        if param=="padx":
            raise ValueError
        if param=="pady":
            raise ValueError
        if param=="keep_aspect":
            return self._keep_aspect_ratio
        if param=="audio":
            return self._audio
        if param=="fg_color":
            return super().cget("bg")
        if param=="bg_color":
            return "transparent"
        return super().cget(param)

