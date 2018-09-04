% rebase('base.tpl')

<script>
var setup = function() {
    setupLinks();
};
window.onload = setup;

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
}


function deleteKeyValuePair(clickedElement) {
    var paraParent = clickedElement.parentNode; // <p>
    var subKeyCont = paraParent.parentNode; // <div class="subkey-container">
    subKeyCont.parentNode.removeChild(subKeyCont)
}

function deleteInput(clickedElement) {
    var parent = clickedElement.parentNode;  // E.g. <div class="input-container"> -- want to delete this
    var subkeyContainer = parent.parentNode;  // E.g. <div class="subkey-container">, <div class="edit-farm-container">
    subkeyContainer.removeChild(parent);
}

function addInput(clickedElement, inputName, isTextarea) {
    // E.g. <textarea rows="8" name= "{key}">{item}</textarea>
    var parent = clickedElement.parentNode;  // E.g. <div class="input-container">
    var subkeyContainer = parent.parentNode;  // E.g. <div class="subkey-container">, <div class="edit-farm-container">
    
    var inputContainer = document.createElement("div");
    inputContainer.classList.add("input-container")

    if (isTextarea === true) {
        var textarea = document.createElement("textarea")
        textarea.rows = "8"
        textarea.name = inputName;
        inputContainer.appendChild(textarea)
    } else {
        var input = document.createElement("input")
        input.type = "text";
        input.name = inputName;
        input.value = "";
        inputContainer.appendChild(input)
    }
    
    var deletePara = document.createElement("span");
    deletePara.classList.add("edit-farm-control")
    deletePara.classList.add("edit-farm-control-right")
    deletePara.onclick = function(){deleteInput(deletePara)};
    
    var deleteTextNode = document.createTextNode("Delete entry");
    deletePara.appendChild(deleteTextNode)
    inputContainer.appendChild(deletePara)
    
    subkeyContainer.insertBefore(inputContainer, parent)
}
</script>

<form method="post" action="editfarm">
    <!-- Including the farmname as a hidden input allows for error checking in the post function -->
    <input type="hidden" name="farmname" value="{{farmname}}">

    % keys = data_layout['order']
    % textarea_inputs = data_layout['textarea-inputs']
    % single_value_inputs = data_layout['single-value-inputs']
    % nested_inputs = data_layout['nested-inputs']
    % required_nested_inputs = data_layout['required-nested-inputs']

    <!-- Iterate through keys as listed in instruction dict -->
    % for key in keys:
        % instruction = instructions[key]
        % value = content[key]
        <!-- Key "{{key}}" -->

        <div class="edit-farm-container">
            % title = key.capitalize()
            <p class="edit-farm-key">{{title}}</p>
            <p class="edit-farm-instruction">{{instruction}}</p>

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
                                <span class="edit-farm-control edit-farm-control-right" onclick="deleteInput(this)">Delete entry</span>
                                %end
                            </div>
                        % end

                        % if subkey not in required_nested_inputs:
                        <p>
                            <!-- Control to add new entry under subkey "{{subkey}}" -->
                            <span class="edit-farm-control" onclick="addInput(this, '{{key}}${{subkey}}', false)">Add entry</span>
                            <br>
                            <!-- Control to delete the key-value pair -->
                            <span class="edit-farm-control" onclick="deleteKeyValuePair(this)">Delete this key-value pair</span>
                        </p>
                        %end
                    </div>

                <!-- End of subkey "{{subkey}}" -->
                % end
                
                <p>
                    <!-- Control to add new key-value pair -->
                    <input type="text" name="new-subkey">
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
                            <input type="text" name="{{key}}" value="{{item}}">
                        % end
                        
                        % if key not in single_value_inputs:
                        <!-- Control to remove this input -->
                        <span class="edit-farm-control edit-farm-control-right" onclick="deleteInput(this)">Delete entry</span>
                        %end
                    </div>

                <!-- End of item in list for "{{key}}" -->
                % end
                
                % if key not in single_value_inputs:
                <!-- Control to add a new string -->
                <p>
                    % if key in textarea_inputs:
                        <span class="edit-farm-control" onclick="addInput(this, '{{key}}', true)">Add entry</span>
                    % else:
                        <span class="edit-farm-control" onclick="addInput(this, '{{key}}', false)">Add entry</span>
                    %end
                </p>
                %end

            <!-- End of key "{{key}}" that doesn't contain nested values -->
            % end

        </div>
        <!-- End of key "{{key}}" -->
    % end
    <!-- End of key in keys -->
    <div class="input-container">
        <input class="edit-farm-submit" type="submit" value="Update farm">
        <input class="edit-farm-submit" type="submit" formmethod="GET" value="Cancel">
    </div>
</form>