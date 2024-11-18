import configparser
import os
import re

class ConfigManager:
    CONFIG_FILE = 'config.ini'

    @staticmethod
    def create_default_config():
        config = configparser.ConfigParser()
        
        config['SOURCE'] = {
            'audio_play': 'enabled',
            'recording': 'enabled',
            'network_sett': 'enabled',
            'network_stream': 'enabled',
            'status': 'active'
        }
        
        config['HDMI'] = {
            'ch1_hue': '50',
            'ch1_saturation': '50',
            'ch1_brightness': '50',
            'ch2_hue': '50',
            'ch2_saturation': '50',
            'ch2_brightness': '50',
            'path': '/media/user/UBUNTU18_0',
            'f1': '/media/user/UBUNTU18_0/Patient_ID_0/Patient_ID_0_2.mp4',
            'f2': '/media/user/UBUNTU18_0/Patient_ID_0/Patient_ID_0_0.mp4'
        }
        
        config['AUDIO'] = {
            'ch1_enabled': 'true',
            'ch2_enabled': 'true',
            'pgm_enabled': 'true',
            'channel1': 'true',
            'channel2': 'false',
            'mute': 'false'
        }
        
        config['RECORDING'] = {
            'video_ch1': 'false',
            'video_ch2': 'false',
            'video_pgm': 'false',
            'audio_ch1': 'false',
            'audio_ch2': 'false',
            'audio_pgm': 'false',
            'path': '/media/recordings',
            'patient_id': 'P1213',
            'usb_device_recording': '/media/user/UBUNTU18_0/Patient_ID_0/Patient_ID_0_2.mp4'
        }
        
        config['NETWORK'] = {
            'ip_address': '192.168.0.115',
            'static_ip': '192.168.0.100'
        }
        
        config['NETWORK_STREAMING'] = {
            'rtmp_link': 'http://example.com/stream',
            'rtmp_key': 'your_rtmp_key',
            'rtsp_url': 'rtsp://example.com/stream',
            'rtsp_name': 'your_rtsp_name',
            'rtmp_enabled': 'true',
            'rtsp_enabled': 'true'
        }
        
        with open(ConfigManager.CONFIG_FILE, 'w') as f:
            config.write(f)

    @staticmethod
    def read_config():
        config = configparser.ConfigParser()
        if not os.path.exists(ConfigManager.CONFIG_FILE):
            ConfigManager.create_default_config()
        config.read(ConfigManager.CONFIG_FILE)
        return config

    @staticmethod
    def save_config(config):
        with open(ConfigManager.CONFIG_FILE, 'w') as f:
            config.write(f)