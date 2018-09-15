<!DOCTYPE html>
<html>
    <head>
        <head>
            <meta property='og:image' content='http://communitysupportedagriculture.ie/images/slideshow/leaf-and-root.jpg'/>
        </head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css?family=Work+Sans" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css?family=Playfair+Display" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
        <link href="{{root_rel_dir}}static/csaireland-style.css" type="text/css" rel="stylesheet"/>
        <script src="{{root_rel_dir}}static/slideshow.js" type="text/javascript"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    </head>
    <body>
        <div id="top-level-container">
            <div id="banner-container-top">
                <img class="banner-img" src="../images/veg-header.png"/>
            </div>
            <div id="heading-container" onclick="location.href='{{root_rel_dir}}home'" style="cursor:pointer">
                <h1>CSA Network Ireland</h1>
            </div>
            <div id="links-container">
                % for title, vals in links.iteritems():
                    % if vals['link'] == page_name:
                        <div class="active-link-item">{{title}}</div>
                    % else:
                        <div class="link-item"><a href="{{root_rel_dir}}{{vals['link']}}" {{!vals.get('tags', '')}}>{{title}}</a></div>
                    % end
                % end
            </div>
            <div class="body-container">
                <div class="flash">
                    % for message in messages_to_flash:
                        <p class="flash">{{!message}}</p>
                    % end
                </div>
                
                % if username:
                    <div class="admin-info-container">
                        <p>
                            Signed in as user <b>{{username}}</b>, with role <b>{{role}}</b>
                            <br>
                            % if role == 'admin':
                                <a href="{{root_rel_dir}}admin">Admin page</a>
                                <br>
                            % elif role == 'editor' and farmname:
                                <a href="{{root_rel_dir}}edit/{{farmname}}">Edit {{farmname}} profile</a>
                                <br>
                            % end
                            <a href="{{root_rel_dir}}logout">Logout</a>
                        </p>
                    </div>
                % end
                
                {{!base}}
            </div>
            <div id="banner-container-bottom">
                <img class="banner-img" src="../images/veg-footer.png"/>
            </div>
        </div>
    </body>
</html>