from jinja2 import Environment, FileSystemLoader
import subprocess

class HTMLTemplate:
    env = Environment(loader=FileSystemLoader('templates'))

    @staticmethod
    def get_sidebar_items():
        return [
            "Source",
            "Audio",
            "Recording",
            "Network Settings",
            "Network Streaming"
        ]
    
    @staticmethod
    def get_usb_devices():
        try:
            result = subprocess.run(['lsusb'], stdout=subprocess.PIPE)
            devices = result.stdout.decode('utf-8').strip().split('\n')
            return devices
        except FileNotFoundError:
            return []

    @staticmethod
    def get_html_form(config):
        # Convert boolean strings to actual booleans
        # for section in ['AUDIO', 'RECORDING']:
        #     for key in config[section]:
        #         if config[section][key].lower() in ['true', 'false']:
        #             config[section][key] = config[section][key].lower() == 'true'
        template = HTMLTemplate.env.get_template('form.html')
        sidebar_items = HTMLTemplate.get_sidebar_items()
        usb_devices = HTMLTemplate.get_usb_devices()

        # list of mp4 files for each usb device
        usb_devices = ["1", "2", "3", "4"] # sample - to be replaced with actual usb devices by the naming 1_name, 2_name, 3_name, 4_name
        mp4_1 = ["file1.mp4", "file2.mp4"] # sample
        mp4_2 = ["file3.mp4", "file4.mp4"] # sample
        mp4_3 = ["file5.mp4", "file6.mp4"] # sample
        mp4_4 = ["file7.mp4", "file8.mp4"] # sample 
        return template.render(config=config, sidebar_items=sidebar_items, usb_devices=usb_devices, mp4_1=mp4_1, mp4_2=mp4_2, mp4_3=mp4_3, mp4_4=mp4_4)
    
    @staticmethod
    def get_login_form():
        template = HTMLTemplate.env.get_template('login.html')
        return template.render()