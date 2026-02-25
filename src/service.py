"""
Service for running DDoS attacks in background
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from kivy.app import App
from kivy.logger import Logger
from kivy.clock import Clock

try:
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    
    # Java classes for Android
    PythonService = autoclass('org.kivy.android.PythonService')
    Service = autoclass('android.app.Service')
    Intent = autoclass('android.content.Intent')
    Context = autoclass('android.content.Context')
    Notification = autoclass('android.app.Notification')
    NotificationManager = autoclass('android.app.NotificationManager')
    
    HAS_ANDROID = True
except:
    HAS_ANDROID = False

class DDOSService(App):
    def build(self):
        Logger.info("DDOSService: Service started")
        
        if HAS_ANDROID:
            self.setup_foreground_service()
        
        return None
    
    def setup_foreground_service(self):
        """Set up Android foreground service"""
        try:
            # Create notification channel
            self.create_notification_channel()
            
            # Create notification
            notification = self.create_notification(
                "DDOS Attack Service",
                "Service is running in background"
            )
            
            # Start as foreground service
            PythonService.startForeground(1, notification)
            
            Logger.info("DDOSService: Started as foreground service")
        except Exception as e:
            Logger.error(f"DDOSService: Error setting up service: {e}")
    
    def create_notification_channel(self):
        """Create notification channel for Android 8+"""
        try:
            if autoclass('android.os.Build$VERSION').SDK_INT >= 26:
                NotificationChannel = autoclass('android.app.NotificationChannel')
                NotificationManager = autoclass('android.app.NotificationManager')
                
                channel = NotificationChannel(
                    "ddos_service_channel",
                    "DDOS Service",
                    NotificationManager.IMPORTANCE_LOW
                )
                channel.setDescription("Background service for DDOS attacks")
                
                notification_manager = PythonService.getSystemService(
                    Context.NOTIFICATION_SERVICE
                )
                notification_manager.createNotificationChannel(channel)
        except:
            pass
    
    def create_notification(self, title, text):
        """Create Android notification"""
        try:
            if autoclass('android.os.Build$VERSION').SDK_INT >= 26:
                Builder = autoclass('android.app.Notification$Builder')
                builder = Builder(PythonService, "ddos_service_channel")
            else:
                Builder = autoclass('android.app.Notification$Builder')
                builder = Builder(PythonService)
            
            builder.setContentTitle(title)
            builder.setContentText(text)
            builder.setSmallIcon(PythonService.getApplicationInfo().icon)
            builder.setAutoCancel(False)
            
            return builder.build()
        except:
            return None
    
    def on_stop(self):
        Logger.info("DDOSService: Service stopping")
        if HAS_ANDROID:
            PythonService.stopForeground(True)
            PythonService.stopSelf()

# Service entry point
def main():
    DDOSService().run()

if __name__ == '__main__':
    main()
