----
## Overview
This is the site for Community Supported Agriculture (CSA) Network Ireland. It contains content updated by the network coordinator, and content updated by a representative from each CSA included.

Due to the requirement to have CSA reps update their own pages, session functionality and some manner of database were put in place.

## Implementation
----
This was written to run on a server with CGI support, no WSGI. Given Python knowledge, and the fact that Python is probably much faster to work with than PHP, the Bottle framework was chosen.

This provides routing and templating, and is written in a single Python file, so very easy to copy to the server. There are additional Bottle modules that provide e.g. session management, but as the requirements were very straight-forward, it seemed as easy to write this from scratch.

The content for each CSA is serialized to a json file under `data`, e.g. `dublin.json`. The layout of the page presented for editing each CSA profile, and the instructions on it, is also read from json - to make the scripts and content slightly less coupled.

## Deploying to a server similar to the current one
----
Copy the contents of `cgi-bin` to `/webspace/cgi-bin`.

Copy everything else to `/webspace/httpdocs/communitysupportedagriculture.ie`. Change the text in `key.txt`, used for session management.

The `.htaccess` file tells Apache to send any requests for a URL under `communitysupportedagriculture.ie` to `/cgi-bin/main.py`.

## Updating content
----
The webpages are generated from `.tpl` files in the template directory. Files for static pages just contain some HTML, and should be straight-forward to update. Use e.g. FileZilla to copy to the server.

Files corresponding to the dynamic pages, e.g. `farms.tpl`, `farmprofiles.tpl`, `admin.tpl` are slightly more convoluted and contain template logic.

Note that, for consistency, the name of each template file, e.g. `about.tpl`, is the same as the corresponding URL, e.g. `communitysupportedagriculture.ie/about`.

### Adding a new page
Add a template. Take care to use the existing naming convention, e.g. for _mypage_ add `templates/mypage.tpl`

A function to instruct the server to use a particular template is required. See `@route('/about')` in `/cgi-bin/main.py` as an example.

To include a link to the page on the top bar, add an entry to the list in `scripts/sessionutils.py`