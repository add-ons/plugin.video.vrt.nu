import xbmc
import xbmcaddon
import inputstreamhelper
from resources.lib.kodiwrappers import kodiwrapper

class DrmMonitor(xbmc.Monitor):

    def __init__(self):
        xbmc.Monitor.__init__(self)
        addon = xbmcaddon.Addon()
        self._kodi_wrapper = kodiwrapper.KodiWrapper(addon)
        self._is_helper = inputstreamhelper.Helper('mpd', drm='com.widevine.alpha')

    def onSettingsChanged(self):
        self._kodi_wrapper.log_notice('VRT NU Addon: settings changed')
        if self._kodi_wrapper.get_setting('usedrm') == 'true':
            if self._is_helper.check_inputstream():
                 self._kodi_wrapper.log_notice('VRT NU Addon: drm installed')

if __name__ == '__main__':

    monitor = DrmMonitor()
    
    while not monitor.abortRequested():
        if monitor.waitForAbort(10):
            break
