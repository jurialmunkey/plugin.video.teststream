# -*- coding: utf-8 -*-
# Module: default
# Author: jurialmunkey
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
import sys
import xbmc
import xbmcgui
import xbmcplugin
from urllib.parse import unquote_plus
from infotagger.listitem import ListItemInfoTag

TEST_CONTAINERCONTENT = 'episodes'
TEST_LABEL = 'Item_{x}_Label'
TEST_URL = 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'
TEST_ITEM = {
    'label': TEST_LABEL,
    'label2': 'Item_{x}_Label2',
    'path': 'plugin://plugin.video.teststream/?info=play&x={x}',
    'isFolder': False,
    'infolabels': {'mediatype': 'episode'},
    'infoproperties': {'isPlayable': 'true'}
}


def parse_paramstring(paramstring):
    """ helper to assist to standardise urllib parsing """
    params = dict()
    paramstring = paramstring.replace('&amp;', '&')  # Just in case xml string
    for param in paramstring.split('&'):
        if '=' not in param:
            continue
        k, v = param.split('=')
        params[unquote_plus(k)] = unquote_plus(v)
    return params


class Plugin(object):
    def __init__(self):
        self.handle = int(sys.argv[1])
        self.paramstring = sys.argv[2][1:]
        self.params = parse_paramstring(self.paramstring)
        self.update_listing = False
        self.container_content = TEST_CONTAINERCONTENT
        self.sort_methods = [{'sortMethod': xbmcplugin.SORT_METHOD_UNSORTED}]
        self.plugin_category = 'Test Case'

    def play(self):
        x = self.params.get('x')
        baseitem = {k: v.format(x=x) if isinstance(v, str) else v for k, v in TEST_ITEM.items()}
        baseitem['infolabels']['path'] = baseitem['path'] = TEST_URL
        listitem = self.make_listitem(baseitem)
        xbmc.log('Attempting to play {TEST_URL}', level=xbmc.LOGINFO)
        xbmcplugin.setResolvedUrl(self.handle, True, listitem)

    @staticmethod
    def make_listitem(baseitem):
        listitem = xbmcgui.ListItem(label=baseitem['label'], label2=baseitem['label2'], path=baseitem['path'])
        info_tag = ListItemInfoTag(listitem)
        info_tag.set_info(baseitem['infolabels'])
        listitem.setProperties(baseitem['infoproperties'])
        return listitem

    def make_listing(self):
        for x in range(20):
            baseitem = {k: v.format(x=x) if isinstance(v, str) else v for k, v in TEST_ITEM.items()}
            listitem = self.make_listitem(baseitem)
            xbmcplugin.addDirectoryItem(
                handle=self.handle,
                url=baseitem['path'],
                listitem=listitem,
                isFolder=baseitem['isFolder'])

        xbmcplugin.setPluginCategory(self.handle, self.plugin_category)  # Container.PluginCategory
        xbmcplugin.setContent(self.handle, self.container_content)  # Container.Content
        for i in self.sort_methods:
            xbmcplugin.addSortMethod(self.handle, **i)
        xbmcplugin.endOfDirectory(self.handle, updateListing=self.update_listing)

    def run(self):
        info = self.params.get('info')
        if info == 'play':
            return self.play()
        return self.make_listing()
