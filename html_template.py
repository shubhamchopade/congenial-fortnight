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
        return template.render(config=config, sidebar_items=sidebar_items, usb_devices=usb_devices)