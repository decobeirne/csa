<!DOCTYPE html>
<html>
    <head>
        <head>
            <meta property='og:image' content='http://communitysupportedagriculture.ie/images/slideshow/leaf-and-root.jpg'/>
        </head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css?family=Work+Sans" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css?family=Playfair+Display" rel="stylesheet">
        <link href="static/csaireland-style.css" type="text/css" rel="stylesheet"/>
        <script src="static/setup-links.js" type="text/javascript"></script>
    </head>
    <body>
        <div id="top-level-container">
            <div id="banner-container-top">
                <img class="banner-img" src="../images/veg-header.png"/>
            </div>
            <div id="heading-container" onclick="location.href='home'" style="cursor:pointer">
                <h1>CSA Network Ireland</h1>
            </div>
            <div id="links-container">
                % for title, vals in links.iteritems():
                    % if vals['link'] == page_name:
                        <div class="active-link-item">{{title}}</div>
                    % else:
                        <div class="link-item"><a href="{{vals['link']}}" {{!vals.get('tags', '')}}>{{title}}</a></div>
                    % end
                % end
            </div>
            <div class="body-container">
                % for msg in flash_messages:
                    <p class="flash">{{msg}}</p>
                % end
                {{!base}}
            </div>
            <div id="banner-container-bottom">
                <img class="banner-img" src="../images/veg-footer.png"/>
            </div>
        </div>
    </body>
</html>