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
        circle.addClass('map-circle-edit')attr({id: 'map-circle-new', cx: circleX, cy: circleY, r: 3});
        $('#edit-farm-map-svg').append(circle);
    };
});

$(document).ready(function(){
    // If an image is selected as the profile image, unset any previously selected image
    $('form').on('click', '.is-default-image', function() {
        $('.is-default-image').not(this).prop('checked', false);
    });
    
    // Make inputs for adding a new key-value pair clickable
    $('.new-subkey').keypress(function (e) {
        var key = e.which;
        if(key == 13) {
            addKeyValuePair(e.target);
            return false;
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
        var circleX = (evtRelX / canvasElem.clientWidth) * 253.38666;
        var circleY = (evtRelY / canvasElem.clientHeight) * 317.33331;

        var input = $('#editfarm-coords-container').children('input:first');
        input.val(circleX + ',' + circleY);

        addCircle(circleX, circleY);
    });
    
    % coords = content.get('coords', [''])[0].split(',')
    % if len(coords) == 2:
        addCircle({{coords[0]}}, {{coords[1]}});
    % end
});
</script>

<form method="post" enctype="multipart/form-data" action="{{root_rel_dir}}edit/{{farm}}">
    <!-- Including the farmname as a hidden input allows for error checking in the post function -->
    <input type="hidden" name="farmname" value="{{farm}}">

    % keys = data_layout['order']
    % textarea_inputs = data_layout['textarea-inputs']
    % single_value_inputs = data_layout['single-value-inputs']
    % nested_inputs = data_layout['nested-inputs']
    % required_nested_inputs = data_layout['required-nested-inputs']


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

            %if key == 'coords':
            <!-- Special container for farm coords -->
            <div class="edit-farm-coords-container" id="editfarm-coords-container">
                <!-- These are the hard-coded dimensions of the SVG map we're using :( -->
                <div class="edit-farm-coords-svg-container svg-container">
                    <!-- The canvas is required to make resizing the SVG work on IE -->
                    <canvas class="dummy-canvas" width="253.38666" height="317.33331"></canvas>
                    <svg id="edit-farm-map-svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" viewbox="0 0 253.38666 317.33331" preserveAspectRatio="xMaxYMax meet">
                        <image id="edit-farm-map-img" width="253.38666" height="317.33331" xlink:href="{{root_rel_dir}}images/map/map-all-blank-no-dots-no-frame-fill.svg"></image>
                    </svg>
                </div>

                % coords = content.get('coords', [''])[0]
                <input type="hidden" name="coords" value="{{coords}}">
            </div>
            <!-- End of farm coords container -->
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
                        % else:
                            % if key == "images":
                                % checked = "checked" if (content.get('default-image', '') == item) else ""
                                <input type="text" name="{{key}}$existing" value="{{item}}" style="background-color:#e3ede9" readonly>
                                <img src="{{root_rel_dir}}{{item}}"/>
                                <div class="edit-farm-align-right">
                                    <span class="edit-farm-control-no-hover">Select as profile image<input type="checkbox" class="is-default-image" name="is-default-img-{{item}}" {{checked}}/></span>
                                </div>
                            % else:
                                <input type="text" name="{{key}}" value="{{item}}">
                            % end
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
                    % else:
                        % if key == "images":
                            <span class="edit-farm-control" onclick="addInput(this, '{{key}}', 'image')">Add entry</span>
                        % else:
                            <span class="edit-farm-control" onclick="addInput(this, '{{key}}', 'input')">Add entry</span>
                        % end
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