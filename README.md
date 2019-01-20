# plugin.video.vrt.nu

**plugin.video.vrt.nu** is a [Kodi][1] add-on used to watch all live video streams *and* all video-on-demand
content available on [VRT NU][2].

VRT NU is the video-on-demand platform of VRT, Flanders' public broadcasting service.

## Installing

In Kodi, simply search for `VRT NU`, and install the add-on.

Alternatively, you can download a ZIP archive from the [Kodi plugin page][3] and install it directly in Kodi
using the **Install via Zip** option.

#### Installing V1.5.x on Kodi 17.x
If you get errors while installing V1.5.0 on Kodi 17.x make sure the inputstream.adaptive addon is enabled.
To check on this go to addons -> video player inputstream -> inputstream adaptive and enable the addon.

## Using the plugin

The [VRT NU][2] platform requires users to sign in before gaining access to video-on-demand content. Users can
sign in with a user name and password, or sign in with their Google, or Facebook account.

This plugin currently only supports signing in using the first method (user name and password). If you already
have a VRT NU account and sign in with another method, it's easy to get a password:

- Sign out of your VRT NU account;
- Click **Inloggen met e-mail**;
- Click the **Wachtwoord vergeten?** hyperlink, and enter your email address.

You'll receive an email that allows you to set a password. Use that password to enter in the plugin when
prompted.

## Reporting issues
you can report issues here at github or you can send a message to the facebook page https://www.facebook.com/kodivrtnu/

## Releases | when not installing see the installing section above
#### v1.5.1 (20-01-2019)
- Fixed subtitle issue where subtitles would always be visible (Thanks mediaminister)
- Fixed categories (Thanks mediaminister)
- Roaming support added (Thanks mediaminister)
#### v1.5.0 (27-12-2018)
 - 720p Livestreams when enabling in settings + having kodi 18 + having widevine.dll present (Thanks mediaminister)
 - Fixed bug where watched icon was not showing in Kodi 18
 - Implemented different way of working with subtitles (Thanks mediaminister)
#### v1.4.3 (07-11-2018)
 - Livestreams working again

#### v1.4.2 (11-10-2018)
 - Changed way of working with urls when a season is refering to href="#"

#### v1.4.1 (24-09-2018)
- Adapted plugin to new vrtnu layout for showing multiple seasons

#### v1.4.0 (20-09-2018)
- Using the new vrtnu login method and video services
- Fixed bug where some videos would not be able to play (Thanks dagwieers)

#### v1.3.4 (10-09-2018)
- Fixed A-Z menu to parse the new vrtnu layout

#### v1.3.3 (02-09-2018)
- Fixed bug where some items would not want to play
- Fixed bug where some videos would only show one episodes while multiple episodes are present
- Updated Requests and Beautifulsoup modules

#### v1.3.2 (03-08-2018)
- Changed way of selecting multiple episodes, this fixes a bug where the "active" episodes would not be shown

#### v1.3.1 (20-07-2018)
- Changed way of selecting item title for single video's

#### v1.3.0 (14-07-2018)
- Adapted code to new vrtnu website layout, this fixes a bug where only the first episode would be shown while multiple episodes are present

#### v1.2.0 (17-06-2018)
- Changed live streaming mechanism

#### v1.1.2 (14-06-2018)
- New stream links for live streaming (Thanks yorickps)

#### v1.1.1 (13-03-2018)
- Fixed bug where seasons do not show when there is one malfunctioning

#### v1.1.0 (15-12-2017)
- Refactored internal code

#### v1.0.0 (01-10-2017)
- Fixed issue where all the videos would not be able to play, implemented new way of getting the streaming urls
- Fixed bug where a single video would not be listed when there is also a part "ANDEREN BEKEKEN OOK" present
- New versioning system now starting from 1.0.0

#### v0.0.7 (09-09-2017)
- Fixed bug where dates were not always shown

#### v0.0.6 (06-08-2017)
- Fixed ordering bug for videos

#### v0.0.5 (24-07-2017)
- Fixed broken Sporza logo 

#### v0.0.4 (20-07-2017)
- Added Sporza livestream
- Added dates to videos (Thanks stevenv)
- Fixed bug where seasons did not get listed

#### v0.0.3 (22-05-2017)

- Fixed broken livestreams

#### v0.0.2 (07-05-2017)

- Fixed installation issue

#### v0.0.1 (01-05-2017)

- Initial working release

[1]: https://kodi.tv
[2]: https://www.vrt.be/vrtnu
[3]: https://kodi.tv/addon/plugins-video-add-ons/vrt-nu-0
