% rebase('base.tpl')

<script>
function addKeyValuePair(clickedElement, key) {
    var paraParent = clickedElement.parentNode; // <p>
    var newSubkeyInput = paraParent.firstElementChild;
    var newSubkey = newSubkeyInput.value;
    if (newSubkey == "") {
        return;
    }
    
    var topContainer = paraParent.parentNode; // <div class="edit-farm-container">
    
    var subkeyContainer = document.createElement("div");
    subkeyContainer.classList.add("subkey-container");
    
    var subkeyPara = document.createElement("p");
    subkeyPara.classList.add("edit-farm-sub-key");
    
    var subkeyTextNode = document.createTextNode(newSubkey);
    subkeyPara.appendChild(subkeyTextNode);
    
    var controlsPara = document.createElement("p");
    
    var addInputId = key + '$' + newSubkey;
    var addInputSpan = document.createElement("span");
    addInputSpan.classList.add("edit-farm-control");
    addInputSpan.onclick = function(){addInput(addInputSpan, addInputId, false)};
    addInputSpan.innerHTML = "Add entry";
    
    var breakTextNode = document.createElement("br");
    
    var deleteKeyValuePairSpan = document.createElement("span");
    deleteKeyValuePairSpan.classList.add("edit-farm-control");
    deleteKeyValuePairSpan.onclick = function(){deleteKeyValuePair(deleteKeyValuePairSpan)};
    deleteKeyValuePairSpan.innerHTML = "Delete this key-value pair";
    
    
    controlsPara.appendChild(addInputSpan);
    controlsPara.appendChild(breakTextNode);
    controlsPara.appendChild(deleteKeyValuePairSpan);
    
    subkeyContainer.appendChild(subkeyPara);
    subkeyContainer.appendChild(controlsPara);
    
    topContainer.insertBefore(subkeyContainer, paraParent);
    
    // Blank the input
    newSubkeyInput.value = "";
}

function deleteKeyValuePair(clickedElement) {
    var paraParent = clickedElement.parentNode; // <p>
    var subKeyCont = paraParent.parentNode; // <div class="subkey-container">
    subKeyCont.parentNode.removeChild(subKeyCont)
}

function deleteInput(elm) {
    // No advantage to using jquery here
    var inputContainer = elm.parentNode.parentNode;  // E.g. <div class="input-container"><div class="edit-farm-align-right">
    var subkeyContainer = inputContainer.parentNode;  // E.g. <div class="subkey-container">, <div class="edit-farm-container">
    subkeyContainer.removeChild(inputContainer);
}

$(function () {
    addInput = function (elm, inputName, type) {
        // E.g. <textarea rows="8" name= "{key}">{item}</textarea>
        var parent = elm.parentNode;  // E.g. <div class="input-container">
        var newContainer = $('<div class="input-container"></div>');

        if (type == "textarea") {
            newContainer.append('<textarea rows="8" name="' + inputName + '"></textarea>');
        } else if (type == "image") {
            newContainer.append('<input type="file" class="image-input" name="' + inputName + '">');
        } else {
            newContainer.append('<input type="text" name="' + inputName + '" value="">');
        }

        if (type == "image") {
            newContainer.append('<div class="edit-farm-align-right"><span class="edit-farm-control-no-hover">Select as profile image<input type="checkbox" class="is-default-image" name="" disabled></span></div>');
        }
        newContainer.append('<div class="edit-farm-align-right"><span class="edit-farm-control" onclick="deleteInput(this)">Delete entry</span></div>');

        newContainer.insertBefore(parent);
    };
});

$(document).ready(function(){
    // If an image is selected as the profile image, unset any previously selected image
    $('form').on('click', '.is-default-image', function() {
        $('.is-default-image').not(this).prop('checked', false);
    });
    
    //If a file is selected for upload, enable the checkbox beside this
    $('form').on('change', '.image-input', function(e) {
        var disabled = (this.files.length == 0);
        var input = $(this).parent().children('div:first').children('span:first').children('input:first');
        input.prop('disabled', disabled);
        if (disabled) {
            input.prop('checked', false);
        }
    });
});
</script>

<form method="post" enctype="multipart/form-data" action="editfarm">
    <!-- Including the farmname as a hidden input allows for error checking in the post function -->
    <input type="hidden" name="farmname" value="{{farmname}}">

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
        % value = content[key]
        <!-- Key "{{key}}" -->

        <div class="edit-farm-container">
            % title = key.capitalize()
            <p class="edit-farm-key">{{title}}</p>
            <p class="edit-farm-instruction">{{!instruction}}</p>

            % if key in nested_inputs:
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
                        %end
                    </div>

                <!-- End of subkey "{{subkey}}" -->
                % end

                <p class="edit-farm-instruction">
                    % instruction = format_instructions(instructions["add-key-value-pair"])
                    {{!instruction}}
                </p>
                <p>
                    <!-- Control to add new key-value pair -->
                    <input type="text" name="new-subkey">
                </p>
                <p>
                    <span class="edit-farm-control" onclick="addKeyValuePair(this, '{{key}}')">Add key-value pair</span>
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
                                <img src="{{item}}"/>
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
                        %end
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
        <input class="edit-farm-submit" type="submit" value="Update farm">
        <input class="edit-farm-submit" type="submit" formmethod="GET" value="Cancel">
    </div>
</form>