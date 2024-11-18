from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os
from config_manager import ConfigManager
from html_template import HTMLTemplate
import re


class ConfigHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            config = ConfigManager.read_config()
            html = HTMLTemplate.get_html_form(config)
            self.wfile.write(html.encode())
        elif self.path.startswith("/static/"):
            self.serve_static_file()

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        pattern = re.compile(r'name="([^"]+)"\r\n\r\n([^-\r\n]+)')
        matches = pattern.findall(post_data)

        params_dict = {key: value for key, value in matches}

        config = ConfigManager.read_config()
        config["HDMI"]["ch1_hue"] = params_dict["ch1_hue"]
        config["HDMI"]["ch1_saturation"] = params_dict["ch1_saturation"]
        config["HDMI"]["ch1_brightness"] = params_dict["ch1_brightness"]
        config["HDMI"]["ch2_hue"] = params_dict["ch2_hue"]
        config["HDMI"]["ch2_saturation"] = params_dict["ch2_saturation"]
        config["HDMI"]["ch2_brightness"] = params_dict["ch2_brightness"]
        config["HDMI"]["f1"] = params_dict["file_f1"]
        config["HDMI"]["f2"] = params_dict["file_f2"]
        if params_dict["source-type"] == "cam0cam1":
            config["SOURCE"]["type"] = "CAM-0 & CAM-1"
        elif params_dict["source-type"] == "cam0file":
            config["SOURCE"]["type"] = "CAM-0 & File"
        elif params_dict["source-type"] == "cam1file":
            config["SOURCE"]["type"] = "CAM-1 & File"
        elif params_dict["source-type"] == "cam0ipstream":
            config["SOURCE"]["type"] = "CAM-0 & IP Stream"
        elif params_dict["source-type"] == "cam1ipstream":
            config["SOURCE"]["type"] = "CAM-1 & IP Stream"
        config["IPSTREAM"]["url"] = params_dict["ipstream_url"]
        if 'audio_ch1' in params_dict:
            config["AUDIO"]["channel1"] = "true"
        else:
            config["AUDIO"]["channel1"] = "false"

        if 'audio_ch2' in params_dict:
            config["AUDIO"]["channel2"] = "true"
        else:
            config["AUDIO"]["channel2"] = "false"
        # config["AUDIO"]["pgm_enabled"] = params_dict["audio_pgm"]
        if 'audio_pgm' in params_dict:
            config["AUDIO"]["pgm_enabled"] = params_dict["audio_pgm"]
        if 'rec_video_ch1' in params_dict:
            config["RECORDING"]["video_ch1"] = "true"
        else:
            config["RECORDING"]["video_ch1"] = "false"
        if 'rec_video_ch2' in params_dict:
            config["RECORDING"]["video_ch2"] = "true"
        else:
            config["RECORDING"]["video_ch2"] = "false"
        if 'rec_video_pgm' in params_dict:
            config["RECORDING"]["video_pgm"] = "true"
        else:
            config["RECORDING"]["video_pgm"] = "false"

        if 'rec_audio_ch1' in params_dict:
            config["RECORDING"]["audio_ch1"] = "true"
        else:
            config["RECORDING"]["audio_ch1"] = "false"

        if 'rec_audio_ch2' in params_dict:
            config["RECORDING"]["audio_ch2"] = "true"
        else:
            config["RECORDING"]["audio_ch2"] = "false"
        config["RECORDING"]["audio_pgm"] = params_dict["audio_pgm"]
        if "usb_device_recording" in params_dict:
            config["RECORDING"]["usb_device_recording"] = params_dict["usb_device_recording"]
        config["RECORDING"]["patient_id"] = params_dict["patient_id"]
        config["NETWORK"]["ip_address"] = params_dict["ip_address"]
        config["NETWORK"]["static_ip"] = params_dict["static_ip"]
        # config["NETWORK_STREAMING"]["rtmp_link"] = params_dict["rtmp_link"]
        if "rtmp_key" in params_dict:
            config["NETWORK_STREAMING"]["rtmp_key"] = params_dict["rtmp_key"]
        if "rtmp_link" in params_dict:
            config["NETWORK_STREAMING"]["rtmp_link"] = params_dict["rtmp_link"]
        if "rtsp_url" in params_dict:
            config["NETWORK_STREAMING"]["rtsp_url"] = params_dict["rtsp_url"]
        if "rtsp_name" in params_dict:
            config["NETWORK_STREAMING"]["rtsp_name"] = params_dict["rtsp_name"]

        if "rtsp_enabled" in params_dict:
            config["NETWORK_STREAMING"]["rtsp_enabled"] = "true"
        else:
            config["NETWORK_STREAMING"]["rtsp_enabled"] = "false"
        if "rtmp_enabled" in params_dict:
            config["NETWORK_STREAMING"]["rtmp_enabled"] = "true"
        else:
            config["NETWORK_STREAMING"]["rtmp_enabled"] = "false"

        ConfigManager.save_config(config)

        # Redirect back to the form
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

    def serve_static_file(self):
        try:
            file_path = self.path[1:]
            with open(file_path, "rb") as f:
                content = f.read()

            self.send_response(200)
            if self.path.endswith(".css"):
                self.send_header("Content-type", "text/css")
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "File not found")


def run_server(port=8000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, ConfigHandler)
    print(f"Server running on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    if not os.path.exists("static"):
        os.makedirs("static")
    if not os.path.exists(ConfigManager.CONFIG_FILE):
        ConfigManager.create_default_config()
    run_server()
