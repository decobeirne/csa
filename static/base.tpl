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
        
            <!-- var headingContainer = document.getElementById("heading-container"); -->
    <!-- headingContainer.setAttribute("onclick", "location.href='index.html'"); // works on all -->
    <!-- headingContainer.style.cursor = "pointer"; -->

    <!-- // Dictionary of links to insert into the "link-container" div in each page. The dictionary -->
    <!-- // maps the link text to the destination page. -->
    <!-- linkMap = { -->
        <!-- "About": "about.html", -->
        <!-- "Farm Profiles": "farmprofiles.html", -->
        <!-- "Farm Profiles Beta": "farmprofiles-beta.html", -->
        <!-- "Resources": "resources.html", -->
        <!-- "Contact": "contact.html", -->
        <!-- "Facebook": "https://www.facebook.com/groups/245019725582313", -->
    <!-- }; -->
        <div id="top-level-container">
            <div id="banner-container-top">
                <img class="banner-img" src="../images/veg-header.png"/>
            </div>
            <div id="heading-container" onclick="location.href='index.html'" style="cursor:'pointer'">
                <h1>CSA Network Ireland</h1>
            </div>
            <div id="links-container"></div>
            <div class="body-container">
                {{!base}}
            </div>
            <div id="banner-container-bottom">
                <img class="banner-img" src="../images/veg-footer.png"/>
            </div>
        </div>
    </body>
</html>