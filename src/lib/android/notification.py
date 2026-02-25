"""
Android notification helper
"""

try:
    from jnius import autoclass, cast
    
    # Java classes
    String = autoclass("java.lang.String")
    Context = autoclass("android.content.Context")
    
    # Try to get service first, then activity
    try:
        PythonService = autoclass("org.kivy.android.PythonService")
        CurrentContext = PythonService.mService
    except:
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        CurrentContext = PythonActivity.mActivity
    
    AppContext = CurrentContext.getApplication().getApplicationContext()
    
    HAS_ANDROID = True
except:
    HAS_ANDROID = False


def create_notify_channel(
        channel_id: str, channel_name: str, channel_description: str) -> None:
    """Creates notification channel for Android 8+"""
    if not HAS_ANDROID:
        return
    
    try:
        NotificationManager = autoclass("android.app.NotificationManager")
        NotificationChannel = autoclass("android.app.NotificationChannel")
        
        # Only create channel for Android 8+
        from jnius import autoclass as jni_autoclass
        Build = jni_autoclass("android.os.Build$VERSION")
        if Build.SDK_INT >= 26:
            channel = NotificationChannel(
                String(channel_id),
                cast("java.lang.CharSequence", String(channel_name)),
                NotificationManager.IMPORTANCE_HIGH,
            )
            channel.setDescription(String(channel_description))
            channel.enableLights(True)
            channel.enableVibration(True)
            
            notification_manager = AppContext.getSystemService(NotificationManager)
            notification_manager.createNotificationChannel(channel)
    except Exception as e:
        print(f"Error creating notification channel: {e}")


def notify(id: int, channel_id: str, title: str, text: str, ticker: str = "") -> None:
    """Send Android notification"""
    if not HAS_ANDROID:
        print(f"[Notification] {title}: {text}")
        return
    
    try:
        Builder = autoclass("android.app.Notification$Builder")
        Notification = autoclass("android.app.Notification")
        NotificationManager = autoclass("android.app.NotificationManager")
        
        # Get system service
        mNManager = CurrentContext.getSystemService(Context.NOTIFICATION_SERVICE)
        
        # Create notification builder with channel for Android 8+
        Build = autoclass("android.os.Build$VERSION")
        if Build.SDK_INT >= 26:
            mBuilder = Builder(CurrentContext, String(channel_id))
        else:
            mBuilder = Builder(CurrentContext)
        
        # Set notification properties
        mBuilder.setContentTitle(String(title))
        mBuilder.setContentText(String(text))
        if ticker:
            mBuilder.setTicker(String(ticker))
        
        # Try to get app icon
        try:
            app_info = AppContext.getApplicationInfo()
            mBuilder.setSmallIcon(app_info.icon)
        except:
            pass
        
        mBuilder.setAutoCancel(True)
        mBuilder.setDefaults(Notification.DEFAULT_SOUND | Notification.DEFAULT_VIBRATE)
        
        # Build and show notification
        notification = mBuilder.build()
        mNManager.notify(id, notification)
        
    except Exception as e:
        print(f"Error sending notification: {e}")
