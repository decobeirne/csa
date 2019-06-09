% rebase('base.tpl')

<script>
$(function () {
    addKeyValuePair = function (elm) {
        var subKey = $(elm).val();
        if (subKey == "") {
            return;
        }

        var key = $(elm).parent().parent().attr('id');
        var newFullKey = key + '$' + subKey;
        var newSubKeyContainer = $('<div class="subkey-container"></div>');
        var newPara = $('<p class="edit-farm-sub-key">' + subKey + '</p>');
        var newInputContainer = $('<div class="input-container"><input type="text" name="' + newFullKey + '" value=""><div class="edit-farm-align-right"><span class="edit-farm-control" onclick="deleteInput(this)">Delete entry</span></div>');
        var newAddEntryPara = $('<p><span class="edit-farm-control" onclick="addInput(this, \'' + newFullKey + '\', \'input\')">Add entry</span><br><span class="edit-farm-control" onclick="deleteKeyValuePair(this)">Delete this key-value pair</span></p>');
        newSubKeyContainer.append(newPara);
        newSubKeyContainer.append(newInputContainer);
        newSubKeyContainer.append(newAddEntryPara);

        var para = $(elm).parent();
        var lastSubKey = para.prevAll('div.subkey-container:first');
        newSubKeyContainer.insertAfter(lastSubKey);

        $(elm).val("");
    };
});

$(function () {
    addKeyValuePairFromSpan = function (elm) {
        var para = $(elm).parent().prev();
        var input = para.children('input:first');
        addKeyValuePair(input.get(0));
    };
});

$(function () {
    deleteKeyValuePair = function (elm) {
        var subKeyContainer = $(elm).parent().parent();  // E.g. <div class="subkey-container"><p>
        subKeyContainer.remove();
    };
});

$(function () {
    deleteInput = function (elm) {
        var inputContainer = $(elm).parent().parent();  // E.g. <div class="input-container"><div class="edit-farm-align-right">
        inputContainer.remove();
    };
});

$(function () {
    // Add input, e.g. <textarea rows="8" name= "{key}">{item}</textarea>
    addInput = function (elm, inputName, type) {
        var parent = elm.parentNode;  // E.g. <div class="input-container">
        var newContainer = $('<div class="input-container"></div>');
        if (type == "textarea") {
            newContainer.append('<textarea rows="8" name="' + inputName + '"></textarea>');
        } else if (type == "image") {
            newContainer.append('<input type="file" class="image-input" name="' + inputName + '">');
        } else {
            newContainer.append('<input type="text" name="' + inputName + '" value="">');
        }
        newContainer.append('<div class="edit-farm-align-right"><span class="edit-farm-control" onclick="deleteInput(this)">Delete entry</span></div>');
        newContainer.insertBefore(parent);
    };
});

$(function () {
    addCircle = function (circleX, circleY) {
        $('.map-circle').remove();

        // Create the element using JavaScript, as not well supported by jQuery
        // https://stackoverflow.com/questions/3642035/jquerys-append-not-working-with-svg-element
        var circleElem = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        var circle = $(circleElem);
        circle.addClass('map-circle').attr({cx: circleX, cy: circleY, r: 3});
        $('#edit-farm-map-svg').append(circle);
    };
});

$(function () {
    removeCircle = function () {
        $('.map-circle').remove();
    };
});

$(function () {
    mapToGps = function (mapX, mapY) {
        // A point clicked on the map has an (x,y) coordinate, measured from the top-left of the image.
        // The x coordinate is translated to latitude, and the y coordinate to longitude.

        // latitudeOrigin (top of map) - latitude = mapY * latitudeScale
        // latitude = latitudeOrigin - mapY * latitudeScale
        var latitude = {{map_settings['latitude-origin']}} - mapY * {{map_settings['latitude-scale']}};

        // longitude - longitudeOrigin = mapX * longitudeScale
        // longitude = longitudeOrigin + mapX * longitudeScale
        var longitude = {{map_settings['longitude-origin']}} + mapX * {{map_settings['longitude-scale']}};
        return [latitude, longitude];
    };
});

$(function () {
    gpsToMap = function (gpsLatitude, gpsLongitude) {
        // A point clicked on the map has an (x,y) coordinate, measured from the top-left of the image.
        // The x coordinate is translated to latitude, and the y coordinate to longitude.

        // latitudeOrigin (top of map) - latitude = mapY * latitudeScale
        // mapY = (latitudeOrigin - latitude) / latitudeScale
        var mapY = ({{map_settings['latitude-origin']}} - gpsLatitude) / {{map_settings['latitude-scale']}};

        // longitude - longitudeOrigin = mapX * longitudeScale
        // mapX = (longitude - longitudeOrigin) / longitudeScale
        var mapX = (gpsLongitude - {{map_settings['longitude-origin']}}) / {{map_settings['longitude-scale']}};
        return [mapX, mapY];
    };
});

$(function () {
    checkGpsCoords = function (gpsLat, gpsLong) {
        var gpsLatFloat = parseFloat(gpsLat);
        var gpsLongFloat = parseFloat(gpsLong);
        if (isNaN(gpsLatFloat) || isNaN(gpsLongFloat)) {
            return false;
        }

        // Check that latitude is within {{map_settings['latitude-valid-limits'][0]}},{{map_settings['latitude-valid-limits'][1]}}
        // Check that longitude is within {{map_settings['longitude-valid-limits'][0]}},{{map_settings['longitude-valid-limits'][1]}}
        if ((gpsLat < {{map_settings['latitude-valid-limits'][1]}} || gpsLat > {{map_settings['latitude-valid-limits'][0]}}) ||
            (gpsLong < {{map_settings['longitude-valid-limits'][0]}} || gpsLong > {{map_settings['longitude-valid-limits'][1]}})) {
            return false;
        }
        return true;
    };
});

$(function () {
    checkMapCoords = function (mapX, mapY) {
        if ((mapX < 0 || mapX > {{map_settings['image-dimensions'][0]}}) ||
            (mapY < 0 || mapY > {{map_settings['image-dimensions'][1]}})) {
            return false;
        }
        return true;
    };
});

$(function () {
    setGpsCoords = function () {
        // If enter key is pressed, then update coords in SVG map
        var input = $('#edit-farm-coords-input');
        var report = $('#edit-farm-coords-report');
        var inputText = input.val();
        var gpsCoords = inputText.split(",");
        if (gpsCoords.length == 2) {
            if (checkGpsCoords(gpsCoords[0], gpsCoords[1])) {
                var mapCoords = gpsToMap(gpsCoords[0], gpsCoords[1]);
                if (checkMapCoords(mapCoords[0], mapCoords[1])) {
                    addCircle(mapCoords[0], mapCoords[1]);
                    input.val(gpsCoords[0] + "," + gpsCoords[1]);
                    var reportText = "Map location [" + mapCoords[0].toFixed(3) + "," + mapCoords[1].toFixed(3) + "], GPS coordinates [" + parseFloat(gpsCoords[0]).toFixed(3) + "," + parseFloat(gpsCoords[1]).toFixed(3) + "]";
                    report.text(reportText);
                } else {
                    report.text("Something went wrong. GPS coords look OK, but map location could not be established");
                }
            } else {
                report.text("GPS coords do not seem to be within permitted bounds");
            }
        } else {
            report.text("GPS coords don't seem to be in a correct format, should be e.g. 53.123,-6.123");
        }
    };
});

$(document).ready(function(){
    // Make inputs for adding a new key-value pair clickable
    $('.new-subkey').keypress(function (e) {
        var key = e.which;
        if(key == 13) {
            addKeyValuePair(e.target);
            return false;
        }
    });

    // Do not submit the form when the user hits enter. Allow enter to be used on:
    // * Text areas
    // * The input for setting the GPS coordinates
    // * The input for adding a new key-value pair.
    // https://stackoverflow.com/questions/895171/prevent-users-from-submitting-a-form-by-hitting-enter/11560180
    $(document).on("keyup keydown keypress", ":input:not(textarea,.new-subkey,#edit-farm-coords-input)", function(event) {
        if (event.key == "Enter") {
            event.preventDefault();
        }
    });

    $('.edit-farm-coords-svg-container').click(function (e) {
        // Recall that clientWidth is the width of the image on screen while naturalWidth is the width of the image file
        // Use hard-coded bounds of actual map for drawing
        var mapImg = $('#edit-farm-map-img');
        var mapImgElem = mapImg[0];
        var offset = mapImg.offset();
        var evtRelX = e.pageX - offset.left;
        var evtRelY = e.pageY - offset.top;
        var canvas = $('.dummy-canvas');
        var canvasElem = canvas[0];
        var circleX = (evtRelX / canvasElem.clientWidth) * {{map_settings['image-dimensions'][0]}};
        var circleY = (evtRelY / canvasElem.clientHeight) * {{map_settings['image-dimensions'][1]}};

        //var input = $('#edit-farm-coords-container-id').children('input:first');
        var input = $('#edit-farm-coords-input');
        var report = $('#edit-farm-coords-report');

        var gpsCoords = mapToGps(circleX, circleY)
        if (checkGpsCoords(gpsCoords[0], gpsCoords[1])) {
            addCircle(circleX, circleY);
            var coordsText = gpsCoords[0] + "," + gpsCoords[1];
            input.val(coordsText);
            var reportText = "Map location [" + circleX.toFixed(3) + "," + circleY.toFixed(3) + "] set to GPS coordinates [" + gpsCoords[0].toFixed(3) + "," + gpsCoords[1].toFixed(3) + "]";
            report.text(reportText);
        } else {
            removeCircle();
            input.val("");
            var reportText = "Map location [" + circleX.toFixed(3) + "," + circleY.toFixed(3) + "] could not be set to GPS coordinates";
            report.text(reportText);
        }
    });
    
    $('.edit-farm-coords-input').keypress(function (e) {
        // If enter key is pressed, then update coords in SVG map,
        // and store in ??????
    });
    
    $('#edit-farm-coords-input').keypress(function (e) {
        var key = e.which;
        if(key == 13) {
            setGpsCoords();
            // Do not propagate
            return false;
        }
    });

    var input = $('#edit-farm-coords-input');
    var report = $('#edit-farm-coords-report');
    var coordsText = "";
    var reportText = "GPS coordinates or map location are not set";
    % gpsCoords = content.get('coordinates', [''])[0].split(',')
    % if len(gpsCoords) == 2:
        if (checkGpsCoords({{gpsCoords[0]}}, {{gpsCoords[1]}})) {
            var mapCoords = gpsToMap({{gpsCoords[0]}}, {{gpsCoords[1]}});
            if (checkMapCoords(mapCoords[0], mapCoords[1])) {
                addCircle(mapCoords[0], mapCoords[1]);
                coordsText = {{gpsCoords[0]}} + "," + {{gpsCoords[1]}};
                reportText = "Map location [" + mapCoords[0].toFixed(3) + "," + mapCoords[1].toFixed(3) + "], GPS coordinates [" + {{gpsCoords[0]}}.toFixed(3) + "," + {{gpsCoords[1]}}.toFixed(3) + "]";
            }
        }
    % end
    input.val(coordsText);
    report.text(reportText);
});
</script>

<form method="post" enctype="multipart/form-data" action="{{root_rel_dir}}edit/{{farm}}">
    <!-- Including the farmname as a hidden input allows for error checking in the post function -->
    <input type="hidden" name="farmname" value="{{farm}}">

    % keys = data_layout['order']
    % checkbox_inputs = data_layout['checkbox-inputs']
    % textarea_inputs = data_layout['textarea-inputs']
    % single_value_inputs = data_layout['single-value-inputs']
    % nested_inputs = data_layout['nested-inputs']
    % required_nested_inputs = data_layout['required-nested-inputs']
    % captions = content.get('captions', {})

    % top_instructions = format_instructions(instructions['top'])
    <p class="edit-farm-instruction">
        {{!top_instructions}}
    </p>

    <!-- Iterate through keys as listed in instruction dict -->
    % for key in keys:
        % instruction = format_instructions(instructions[key])
        % value = content.get(key, [])
        <!-- Key "{{key}}" -->

        <div class="edit-farm-container" id="{{key}}">
            % title = key.capitalize()
            <p class="edit-farm-key">{{title}}</p>
            <p class="edit-farm-instruction">{{!instruction}}</p>

            %if key == 'coordinates':
            % coords = content.get('coordinates', [''])[0]
            <div class="edit-farm-coords-container" id="edit-farm-coords-container-id">
                <!-- The exact dimensions of the SVG map are required to display and scale correctly. -->
                <!-- These should be written into the json file from which map_settings is read. -->
                % dimensions = map_settings['image-dimensions']
                <div class="edit-farm-coords-svg-container svg-container">
                    <!-- The canvas is required to make resizing the SVG work on IE -->
                    <canvas class="dummy-canvas" width="{{dimensions[0]}}" height="{{dimensions[1]}}"></canvas>
                    <svg id="edit-farm-map-svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" viewbox="0 0 {{dimensions[0]}} {{dimensions[1]}}" preserveAspectRatio="xMaxYMax meet">
                        <image id="edit-farm-map-img" width="{{dimensions[0]}}" height="{{dimensions[1]}}" xlink:href="{{root_rel_dir}}images/map/{{map_settings['image-filename']}}"></image>
                    </svg>
                </div>
            </div>
            <p class="edit-farm-instruction" id="edit-farm-coords-report"></p>
            <div class="input-container">
                <input type="text" name="coordinates" id="edit-farm-coords-input" value="{{coords}}">
            </div>
            <p>
                <span class="edit-farm-control" onclick="setGpsCoords()">Set GPS coordinates</span>
            </p>
            % elif key in checkbox_inputs:
            % checked = "checked" if (content.get(key, ["no"])[0] == "yes") else ""
            <div class="input-container">
                <span class="edit-farm-control-no-hover">{{title}}<input type="checkbox" name="{{key}}" {{checked}}/></span>
            </div>
            % elif key in nested_inputs:
            <!-- Key "{{key}}" contains nested values, e.g. key is "info" in "info": {"Website": ["cloughjordancommunityfarm.ie"]} -->

                % subkeys = sorted(value.keys())
                % for subkey in subkeys:
                <!-- Subkey "{{subkey}}" under key "{{key}}", e.g. "Website" in "info": {"Website": ["cloughjordancommunityfarm.ie"]} -->

                    <div class="subkey-container">
                        % subvalue = value[subkey]
                        <p class="edit-farm-sub-key">{{subkey}}</p>

                        % for subitem in subvalue:
                            <div class="input-container">
                                <!-- E.g. info$0$Address$1 if we have {"info'": ["Address", ["Foo", "Bar"]]} -->
                                <input type="text" name="{{key}}${{subkey}}" value="{{subitem}}">

                                % if subkey not in required_nested_inputs:
                                    <!-- Control to delete this value under the subkey -->
                                    <div class="edit-farm-align-right">
                                        <span class="edit-farm-control" onclick="deleteInput(this)">Delete entry</span>
                                    </div>
                                % end
                            </div>
                        % end

                        % if subkey not in required_nested_inputs:
                        <p>
                            <!-- Control to add new entry under subkey "{{subkey}}" -->
                            <span class="edit-farm-control" onclick="addInput(this, '{{key}}${{subkey}}', 'input')">Add entry</span>
                            <br>
                            <!-- Control to delete the key-value pair -->
                            <span class="edit-farm-control" onclick="deleteKeyValuePair(this)">Delete this key-value pair</span>
                        </p>
                        % end
                    </div>

                <!-- End of subkey "{{subkey}}" -->
                % end

                <p class="edit-farm-instruction">
                    % instruction = format_instructions(instructions["add-key-value-pair"])
                    {{!instruction}}
                </p>
                <p>
                    <!-- Control to add new key-value pair -->
                    <input type="text" class="new-subkey">
                </p>
                <p>
                    <span class="edit-farm-control" onclick="addKeyValuePairFromSpan(this)">Add key-value pair</span>
                </p>
            
            <!-- End of key "{{key}}" with nested values -->
            % else:
            <!-- Key "{{key}}" doesn't contain nested values, i.e. just a list of strings, e.g. "description": ["Foo", "Bar"] -->

                % for item in value:

                    <div class="input-container">
                        % if key in textarea_inputs:
                            <textarea rows="8" name= "{{key}}">{{item}}</textarea>
                        % elif key == "images":
                            % checked = "checked" if (content.get('default-image', '') == item) else ""
                            <input type="text" name="{{key}}$existing" value="{{item}}" style="background-color:#e3ede9" readonly>
                            <img src="{{root_rel_dir}}{{item}}"/>
                            % caption = captions.get(item, '')
                            <div>
                                <span class="edit-farm-control-no-hover edit-farm-span-dont-expand">Caption</span>
                                <span class="edit-farm-span-expand"><input type="text" style="" name="caption${{item}}" value="{{caption}}"/></span>
                            </div>
                        % else:
                            <input type="text" name="{{key}}" value="{{item}}">
                        % end

                        % if key not in single_value_inputs:
                        <!-- Control to remove this input -->
                        <div class="edit-farm-align-right">
                            <span class="edit-farm-control" onclick="deleteInput(this)">Delete entry</span>
                        </div>
                        % end
                    </div>

                <!-- End of item in list for "{{key}}" -->
                % end
                
                % if key not in single_value_inputs:
                <!-- Control to add a new string -->
                <p>
                    % if key in textarea_inputs:
                        <span class="edit-farm-control" onclick="addInput(this, '{{key}}', 'textarea')">Add entry</span>
                    % elif key == "images":
                        <span class="edit-farm-control" onclick="addInput(this, '{{key}}', 'image')">Add entry</span>
                    % else:
                        <span class="edit-farm-control" onclick="addInput(this, '{{key}}', 'input')">Add entry</span>
                    % end
                </p>
                % end

            <!-- End of key "{{key}}" that doesn't contain nested values -->
            % end

        </div>
        <!-- End of key "{{key}}" -->
    % end
    <!-- End of key in keys -->

    % instruction = format_instructions(instructions['bottom'])
    <p class="edit-farm-instruction">
        {{!instruction}}
    </p>

    <div class="input-container">
        <input type="submit" value="Update farm">
        <span class="edit-farm-control" onclick="window.location.href = '{{root_rel_dir}}edit/{{farm}}'">Cancel</span>
    </div>
</form>