# -*- coding: utf-8 -*-
# ToDo:
#   - Comment all functions
#   - Write all functions of class MediaFireLib
#   - Add error handling
#   - Add support of xml response format

# MediaFire.com REST API link: http://developers.mediafire.com/index.php/REST_API

__author__ = "Dasister"

import urllib, urllib2
import json, hashlib, os
import mimetypes, mimetools, itertools
import time

class MediaFireLib(object):
    userMail, userPassword, appID, apiKey = "", "", -1, ""
    sessionToken = ""
    signature = ""
    secure = 0
    timeout = 30

    expiresIn = -1

    userAgent = "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)"
    responseFormat = "json"

    apiVersion = "2.9"

    USER_ACCEPT_TOS = "http://www.mediafire.com/api/user/accept_tos.php"
    USER_FETCH_TOS = "http://www.mediafire.com/api/user/fetch_tos.php"
    USER_GET_INFO = "http://www.mediafire.com/api/user/get_info.php"
    USER_GET_LOGIN_TOKEN = "https://www.mediafire.com/api/user/get_login_token.php"
    USER_GET_SESSION_TOKEN = "https://www.mediafire.com/api/user/get_session_token.php"
    USER_LOGIN = "http://www.mediafire.com/api/user/login_with_token.php"
    USER_MYFILES = "http://www.mediafire.com/api/user/myfiles.php"
    USER_MYFILES_REVISION = "http://www.mediafire.com/api/user/myfiles_revision.php"
    USER_REGISTER = "https://www.mediafire.com/api/user/register.php"
    USER_RENEW_SESSION_TOKEN = "http://www.mediafire.com/api/user/renew_session_token.php"
    USER_UPDATE = "http://www.mediafire.com/api/user/update.php"
    FILE_COLLABORATE = "http://www.mediafire.com/api/file/collaborate.php"
    FILE_COPY = "http://www.mediafire.com/api/file/copy.php"
    FILE_GET_INFO = "http://www.mediafire.com/api/file/get_info.php"
    FILE_GET_LINKS = "http://www.mediafire.com/api/file/get_links.php"
    FILE_DELETE = "http://www.mediafire.com/api/file/delete.php"
    FILE_MOVE = "http://www.mediafire.com/api/file/move.php"
    FILE_ONE_TIME_DOWNLOAD = "http://www.mediafire.com/api/file/one_time_download.php"
    FILE_CONFIGURE_ONE_TIME_DOWNLOAD = "http://www.mediafire.com/api/file/configure_one_time_download.php"
    FILE_UPDATE = "http://www.mediafire.com/api/file/update.php"
    FILE_UPDATE_PASSWORD = "http://www.mediafire.com/api/file/update_password.php"
    FILE_UPDATE_FILE = "http://www.mediafire.com/api/file/update_file.php"
    FILE_UPLOAD = "http://www.mediafire.com/api/upload/upload.php"
    FILE_UPLOAD_CONFIG = "http://www.mediafire.com/basicapi/uploaderconfiguration.php"
    FILE_UPLOAD_POLL = "http://www.mediafire.com/api/upload/poll_upload.php"
    FILE_UPLOAD_GETTYPE = "http://www.mediafire.com/basicapi/getfiletype.php"
    FOLDER_ATTACH_FOREIGN = "http://www.mediafire.com/api/folder/attach_foreign.php"
    FOLDER_DELETE = "http://www.mediafire.com/api/folder/delete.php"
    FOLDER_DETACH_FOREIGN = "http://www.mediafire.com/api/folder/detach_foreign.php"
    FOLDER_CREATE = "http://www.mediafire.com/api/folder/create.php"
    FOLDER_GET_CONTENT = "http://www.mediafire.com/api/folder/get_content.php"
    FOLDER_GET_DEPTH = "http://www.mediafire.com/api/folder/get_depth.php"
    FOLDER_GET_INFO = "http://www.mediafire.com/api/folder/get_info.php"
    FOLDER_GET_REVISION = "http://www.mediafire.com/api/folder/get_revision.php"
    FOLDER_GET_SIBLINGS = "http://www.mediafire.com/api/folder/get_siblings.php"
    FOLDER_SEARCH = "http://www.mediafire.com/api/folder/search.php"
    FOLDER_MOVE = "http://www.mediafire.com/api/folder/move.php"
    FOLDER_UPDATE = "http://www.mediafire.com/api/folder/update.php"
    SYSTEM_GET_EDITABLE_MEDIA = "http://www.mediafire.com/api/system/get_editable_media.php"
    SYSTEM_GET_INFO = "http://www.mediafire.com/api/system/get_info.php"
    SYSTEM_GET_MIME_TYPES = "http://www.mediafire.com/api/system/get_mime_types.php"
    SYSTEM_GET_SUPPORTED_MEDIA = "http://www.mediafire.com/api/system/get_supported_media.php"
    SYSTEM_GET_VERSION = "http://www.mediafire.com/api/system/get_version.php"
    MEDIA_CONVERSION = "http://www.mediafire.com/conversion_server.php"

    mcStatusCode = {}
    mcStatusCode["200"] = "Conversion is ready. The pdf is sent with the response"
    mcStatusCode["202"] = "Request is accepted and in progress"
    mcStatusCode["204"] = "Unable to fulfill request. The document will not be converted"
    mcStatusCode["400"] = "Bad request. Check your arguments"
    mcStatusCode["404"] = "Unable to find file from quickkey"

    #mcSizeId = {}
    #mcSizeId["d"] = list("0", "1", "2")
    #mcSizeId["i"] = list("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f")


# Class constructor
    def __init__(self, _userMail = "", _userPassword = "", _appID = -1, _apiKey = ""):
        self.userMail, self.userPassword, self.appID, self.apiKey = _userMail, _userPassword, _appID, _apiKey
        self.signature = hashlib.sha1(self.userMail + self.userPassword + str(self.appID) + self.apiKey).hexdigest()

# Stuff.
    def setSecure(self, _secure):
        self.secure = _secure

    def checkSessionToken(self):
        if (self.expiresIn <= time.time()):
            self.user_renewSessionToken()

# User's API
    def user_getSessionToken(self):
        data = urllib.urlencode({'email':self.userMail,'password':self.userPassword,'application_id':self.appID, 'signature':self.signature,'response_format':self.responseFormat})
        res = urllib2.urlopen(self.USER_GET_SESSION_TOKEN, data)
        js = json.load(res)
        js = js['response']
        if (js['result'] == "Error"):
            return js['message']
        self.sessionToken = js['session_token']
        self.expiresIn = time.time() + 60 * 10
        return self.sessionToken

    def user_renewSessionToken(self):
        data = urllib.urlencode({'session_token':self.sessionToken, 'response_format':self.responseFormat})
        res = urllib2.urlopen(self.USER_RENEW_SESSION_TOKEN, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        self.sessionToken = js['session_token']
        self.expiresIn = time.time() + 60 * 10
        return self.sessionToken

    def user_getLoginToken(self):
        data = urllib.urlencode({'email': self.userMail, 'password': self.userPassword,
                                 'application_id': self.appID, 'signature': self.signature,
                                 'response_fromat': self.responseFormat})
        res = urllib2.urlopen(self.USER_GET_LOGIN_TOKEN, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js['login_token']

    def user_getInfo(self):
        self.checkSessionToken()
        data = urllib.urlencode({'session_token': self.sessionToken, 'response_format': self.responseFormat})
        res = urllib2.urlopen(self.USER_GET_INFO, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js

    def user_update(self, display_name = None, first_name = None, last_name = None, birth_date = None, gender = None, website = None, location = None, newsletter = None, primary_usage = None):
        self.checkSessionToken()
        data = {'session_token': self.sessionToken, 'response_format': self.responseFormat, }
        if (display_name != None):
            data['display_name'] = display_name
        if (first_name != None):
            data['first_name'] = first_name
        if (last_name != None):
            data['last_name'] = last_name
        if (birth_date != None):
            data['birth_date'] = birth_date
        if (gender != None):
            data['gender'] = gender
        if (website != None):
            data['website'] = website
        if (location != None):
            data['location'] = location
        if (newsletter != None):
            data['newsletter'] = newsletter
        if (primary_usage != None):
            data['primary_usage'] = primary_usage
        data = urllib.urlencode(data)
        res = urllib2.urlopen(self.USER_UPDATE, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js

    def user_myfilesRevision(self):
        self.checkSessionToken()
        data = urllib.urlencode({'session_token': self.sessionToken, 'response_format': self.responseFormat})
        res = urllib2.urlopen(self.USER_MYFILES_REVISION, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js

    def user_fetchTos(self):
        self.checkSessionToken()
        data = urllib.urlencode({'session_token': self.sessionToken, 'response_format': self.responseFormat})
        res = urllib2.urlopen(self.USER_FETCH_TOS, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js

    def user_acceptTos(self, acceptance_token):
        self.checkSessionToken()
        data = urllib.urlencode({'session_token': self.sessionToken, 'response_format': self.responseFormat, 'acceptance_token': acceptance_token})
        res = urllib2.urlopen(self.USER_ACCEPT_TOS, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js

# File API
    def file_getInfo(self, quick_key):
        self.checkSessionToken()
        data = urllib.urlencode({'quick_key': quick_key, 'session_token': self.sessionToken, 'response_format': self.responseFormat})
        res = urllib2.urlopen(self.FILE_GET_INFO, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js

    def file_delete(self, quick_key):
        data = urllib.urlencode({'quick_key': quick_key, 'session_token': self.sessionToken, 'response_format': self.responseFormat})
        res = urllib2.urlopen(self.FILE_DELETE, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js

    def file_move(self, quick_key, folder_key = "myfiles"):
        self.checkSessionToken()
        data = urllib.urlencode({'quick_key': quick_key, 'session_token': self.sessionToken, 'folder_key': folder_key, 'response_format': self.responseFormat})
        res = urllib2.urlopen(self.FILE_MOVE, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js

    def file_update(self, quick_key, filename = None, description = None, tags = None, privacy = "private", note_subject = None, note_description = None, timezone = None):
        self.checkSessionToken()
        data = {'quick_key': quick_key, 'session_token': self.sessionToken, 'response_format': self.responseFormat, 'privacy': privacy}
        if (filename != None):
            data['filename'] = filename
        if (description != None):
            data['description'] = description
        if (tags != None):
            data['tags'] = tags
        if (note_subject != None):
            data['note_subject'] = note_subject
        if (note_description != None):
            data['note_description'] = note_description
        if (timezone != None):
            data['timezone'] = timezone
        data = urllib.urlencode(data)
        res = urllib2.urlopen(self.FILE_UPDATE, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js

    def file_updatePassword(self, quick_key, password):
        self.checkSessionToken()
        data = urllib.urlencode({'quick_key': quick_key, 'password': password, 'session_token': self.sessionToken, 'response_format': self.responseFormat})
        res = urllib2.urlopen(self.FILE_UPDATE_PASSWORD, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js

    def file_updateFile(self, from_quickkey, to_quickkey):
        self.checkSessionToken()
        data = urllib.urlencode({'from_quickey': from_quickkey, 'to_quickkey': to_quickkey, 'session_token': self.sessionToken, 'response_format': self.responseFormat})
        res = urllib2.urlopen(self.FILE_UPDATE_FILE, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js

    def file_copy(self, quick_key, folder_key = "myfiles"):
        self.checkSessionToken()
        data = urllib.urlencode({'quick_key': quick_key, 'folder_key': folder_key, 'session_token': self.sessionToken, 'response_format': self.responseFormat})
        res = urllib2.urlopen(self.FILE_COPY, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js

#   link_type can be: 'view', 'edit', 'normal_download', 'direct_download', 'one_time_download'

    def file_getLinks(self, quick_key, link_type = "direct_download"):
        self.checkSessionToken()
        data = urllib.urlencode({'quick_key': quick_key, 'link_type': link_type, 'session_token': self.sessionToken, 'response_format': self.responseFormat})
        res = urllib2.urlopen(self.FILE_GET_LINKS, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js

    def file_collaborate(self, quick_key, emails = "", duration = 60 * 24 * 30, message = "", public = "no", email_notification = "no"):
        self.checkSessionToken()
        data = urllib.urlencode({'quick_key': quick_key, 'emails': emails, 'duration': str(duration), 'message': message, 'public': public,
                                 'email_notification': email_notification, 'session_token': self.sessionToken, 'response_format': self.responseFormat})
        res = urllib2.urlopen(self.FILE_COLLABORATE, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js

    def file_oneTimeDownload(self, quick_key = None, duration = None, email_notification = "no", success_callback_url = "", error_callback_url = "", bind_ip = "", burn_after_use = "yes", get_counts_only = "no"):
        self.checkSessionToken()
        data = {'session_token': self.sessionToken, 'response_fromat': self.responseFormat, 'email_notification': email_notification,
                'success_callback_url': success_callback_url, 'error_callback_url': error_callback_url, 'bind_ip': bind_ip,
                'burn_after_use': burn_after_use, 'get_counts_only': get_counts_only}
        if (quick_key != None):
            data['quick_key'] = quick_key
        if (duration != None):
            data['duration'] = str(duration)
        data = urllib.urlencode(data)
        res = urllib2.urlopen(self.FILE_ONE_TIME_DOWNLOAD, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js['token']


    def file_configure_oneTimeDownload(self, token, duration = None, email_notification = "no", success_callback_url = "", error_callback_url = "", bind_ip = "", burn_after_use = "yes"):
        self.checkSessionToken()
        data = {'session_token': self.sessionToken, 'response_format': self.responseFormat, 'token': token,
                'email_notification': email_notification, 'success_callback_url': success_callback_url, 'error_callback_url': error_callback_url,
                'bind_ip': bind_ip, 'burn_after_use': burn_after_use}
        if (duration != None):
            data['duration'] = str(duration)
        data = urllib.urlencode(data)
        res = urllib2.urlopen(self.FILE_CONFIGURE_ONE_TIME_DOWNLOAD, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js
# Folder API
    def folder_GetInfo(self, folderKey):
        self.checkSessionToken()
        data = urllib.urlencode({'folder_key': folderKey, 'session_token': self.sessionToken, 'response_format': self.responseFormat})
        res = urllib2.urlopen(self.FOLDER_GET_INFO, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js

    def folder_delete(self, folderKey):
        self.checkSessionToken()
        data = urllib.urlencode({'session_token': self.sessionToken, 'folder_key': folderKey, 'response_format': self.responseFormat})
        res = urllib2.urlopen(self.FOLDER_DELETE, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js

    def folder_move(self, folderKey_src, folderKey_dst = ""):
        self.checkSessionToken()
        data = urllib.urlencode({'session_token': self.sessionToken, 'folder_key_src': folderKey_src, 'folder_key_dst': folderKey_dst, 'response_format': self.responseFormat})
        res = urllib2.urlopen(self.FOLDER_MOVE, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js

    def folder_create(self, folderName, parentKey = ""):
        data = urllib.urlencode({'session_token': self.sessionToken, 'foldername': folderName, 'parent_key': parentKey, 'response_format': self.responseFormat})
        res = urllib2.urlopen(self.FOLDER_CREATE, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js

    def folder_update(self, folder_key, foldername = None, description = None, tags = None, privacy = "private", privacy_recursive = "no", note_subject = None, note_description = None):
        self.checkSessionToken()
        data = {'session_token': self.sessionToken, 'response_format': self.responseFormat, 'folder_key': folder_key,
                'privacy': privacy, 'privacy_recursive': privacy_recursive}
        if (foldername != None):
            data['foldername'] = foldername
        if (description != None):
            data['description'] = description
        if (tags != None):
            data['tags'] = tags
        if (note_subject != None):
            data['note_subject'] = note_subject
        if (note_description != None):
            data['note_description'] = note_description
        data = urllib.urlencode(data)
        res = urllib2.urlopen(self.FOLDER_UPDATE, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return js['message']
        return js

    def folder_attachForeign(self, folder_key):
        pass

    def folder_detachForeign(self, folder_key):
        pass

    def folder_getRevision(self, folder_key):
        pass

    def folder_getDepth(self, folder_key):
        pass

    def folder_getSiblings(self, folderKey, content_filter, start, limit):
        pass

    def folder_search(self, search_text, folder_key = "myfiles"):
        pass

    def folder_getContent(self, folder_key, content_type, order_by, order_direction, chunk):
        pass
# Upload API
    def upload_UploadFile(self, filePath, folderKey = "myfiles", x_filename = ""):
        self.checkSessionToken()
        fp = open(filePath, 'rb')
        fSize = os.path.getsize(filePath)
        mheaders = {'x-filename': os.path.basename(filePath), 'x-filesize': int(fSize), 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22'}
        data = {'session_token': self.sessionToken, 'uploadkey': folderKey, 'response_format': self.responseFormat}

        form = MultiPartForm()
        form.add_file('fileUpload', os.path.basename(filePath), fp)

        request = urllib2.Request(self.FILE_UPLOAD + '?' + urllib.urlencode(data), None, mheaders)
        body = str(form)
        request.add_header('Content-Type', form.get_content_type())
        request.add_header('Content-Length', len(body))
        request.add_data(body)
        res = urllib2.urlopen(request)
        js = json.load(res)['response']
        fp.close()
        if (js['result'] == "Error"):
            return js['message']
        return js['doupload']['key']


    def Upload_PollUpload(self, key):
        self.checkSessionToken()
        data = urllib.urlencode({'session_token': self.sessionToken, 'key': key, 'response_format': self.responseFormat})
        res = urllib2.urlopen(self.FILE_UPLOAD_POLL, data)
        js = json.load(res)['response']
        if (js['result'] == "Error"):
            return False
        return js['doupload']['status']

# Download API
    def download_getLinks(self, quick_key, link_type):
        pass

# System API
    def system_getVersion(self):
        pass

    def system_getInfo(self):
        pass

    def system_getSupportedMedia(self, group_by_filetype = "no"):
        pass

    def system_getEditableMedia(self, group_by_filetype = "no"):
        pass

    def system_getMimeTypes(self):
        pass

# eCommerce API
    def ecommerce_oneTimeDownload(self, quick_key = None, duration = None, email_notification = "no", success_callback_url = "", error_callback_url = "", bind_ip = "", burn_after_use = "yes", get_counts_only = "no"):
        return self.file_oneTimeDownload(quick_key, duration, email_notification, success_callback_url, error_callback_url, bind_ip, burn_after_use, get_counts_only)

    def ecommerce_configure_oneTimeDownload(self, token, duration = None, email_notification = "no", success_callback_url = "", error_callback_url = "", bind_ip = "", burn_after_use = "yes"):
        return self.file_configure_oneTimeDownload(token, duration, email_notification, success_callback_url, error_callback_url, bind_ip, burn_after_use)

# MediaFireLib Class end

# For this class thanks to site http://pymotw.com.
class MultiPartForm(object):
    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.form_fields = []
        self.files = []
        self.boundary = mimetools.choose_boundary()
        return

    def get_content_type(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def add_field(self, name, value):
        """Add a simple field to the form data."""
        self.form_fields.append((name, value))
        return

    def add_file(self, fieldname, filename, fileHandle, mimetype=None):
        """Add a file to be uploaded."""
        body = fileHandle.read()
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        self.files.append((fieldname, filename, mimetype, body))
        return

    def __str__(self):
        """Return a string representing the form data, including attached files."""
        # Build a list of lists, each containing "lines" of the
        # request.  Each part is separated by a boundary string.
        # Once the list is built, return a string where each
        # line is separated by '\r\n'.
        parts = []
        part_boundary = '--' + self.boundary

        # Add the form fields
        parts.extend(
            [ part_boundary,
              'Content-Disposition: form-data; name="%s"' % name,
              '',
              value,
              ]
            for name, value in self.form_fields
        )

        # Add the files to upload
        parts.extend(
            [ part_boundary,
              'Content-Disposition: file; name="%s"; filename="%s"' % \
              (field_name, filename),
              'Content-Type: %s' % content_type,
              '',
              body,
              ]
            for field_name, filename, content_type, body in self.files
        )

        # Flatten the list and add closing boundary marker,
        # then return CR+LF separated data
        flattened = list(itertools.chain(*parts))
        flattened.append('--' + self.boundary + '--')
        flattened.append('')
        return '\r\n'.join(flattened)

