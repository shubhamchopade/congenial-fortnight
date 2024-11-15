from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os
from config_manager import ConfigManager
from html_template import HTMLTemplate
import re

class ConfigHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            config = ConfigManager.read_config()
            html = HTMLTemplate.get_html_form(config)
            self.wfile.write(html.encode())
        elif self.path.startswith('/static/'):
            self.serve_static_file()
            
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        pattern = re.compile(r'name="([^"]+)"\r\n\r\n([^-\r\n]+)')
        matches = pattern.findall(post_data)

        params_dict = {key: value for key, value in matches}

        print(params_dict)

        
        config = ConfigManager.read_config()
        config['HDMI']['ch1_hue'] = params_dict['ch1_hue']
        config['HDMI']['ch1_saturation'] = params_dict['ch1_saturation']
        config['HDMI']['ch1_brightness'] = params_dict['ch1_brightness']
        config['HDMI']['ch2_hue'] = params_dict['ch2_hue']
        config['HDMI']['ch2_saturation'] = params_dict['ch2_saturation']
        config['HDMI']['ch2_brightness'] = params_dict['ch2_brightness']
        config['HDMI']['f1'] = params_dict['file_f1']
        config['HDMI']['f2'] = params_dict['file_f2']
        config['IPSTREAM']['url'] = params_dict['ipstream_url']
        # config['AUDIO']['ch1_enabled'] = params_dict['audio_ch1']
        # config['AUDIO']['ch2_enabled'] = params_dict['audio_ch2'] 
        config['AUDIO']['pgm_enabled'] = params_dict['audio_pgm']
        # config['RECORDING']['video_ch1'] = params_dict['rec_video_ch1']
        # config['RECORDING']['video_ch2'] = params_dict['rec_video_ch2']
        # config['RECORDING']['video_pgm'] = params_dict['rec_video_pgm']
        # config['RECORDING']['audio_ch1'] = params_dict['rec_audio_ch1']
        # config['RECORDING']['audio_ch2'] = params_dict['rec_audio_ch2']
        config['RECORDING']['audio_pgm'] = params_dict['audio_pgm']
        config['RECORDING']['path'] = params_dict['rec_path']
        config['RECORDING']['patient_id'] = params_dict['patient_id']
        config['NETWORK']['ip_address'] = params_dict['ip_address']
        config['NETWORK']['static_ip'] = params_dict['static_ip']
        config['NETWORK_STREAMING']['link'] = params_dict['network_streaming_link']
        config['NETWORK_STREAMING']['rtmp_key'] = params_dict['rtmp_key']
        config['NETWORK_STREAMING']['rtsp_url'] = params_dict['rtsp_url']
        config['NETWORK_STREAMING']['rtsp_name'] = params_dict['rtsp_name']
       
        ConfigManager.save_config(config)
        
        # Redirect back to the form
        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()
    
    def serve_static_file(self):
        try:
            file_path = self.path[1:]
            with open(file_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            if self.path.endswith('.css'):
                self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, 'File not found')

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ConfigHandler)
    print(f'Server running on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    if not os.path.exists(ConfigManager.CONFIG_FILE):
        ConfigManager.create_default_config()
    run_server()