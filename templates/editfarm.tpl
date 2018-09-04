% rebase('base.tpl')

<script>
var setup = function() {
    setupLinks();
};
window.onload = setup;
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

                    % subvalue = value[subkey]
                    <p class="edit-farm-sub-key">{{subkey}}</p>

                    % if subkey not in required_nested_inputs:
                    <!-- Controls to delete the key-value pair -->
                    
                    <!-- End of controls -->
                    %end

                    % for subitem in subvalue:

                        <div class="input-container">
                            <!-- E.g. info$0$Address$1 if we have {"info'": ["Address", ["Foo", "Bar"]]} -->
                            <input type="text" name="{{key}}${{subkey}}" value="{{subitem}}">
                        </div>
                        
                        % if subkey not in required_nested_inputs:
                        <!-- Controls to delete this value under the subkey -->
                        
                        <!-- End of controls -->
                        %end

                    % end

                    % if subkey not in required_nested_inputs:
                    <!-- Controls to add new entry under subkey "{{subkey}}" -->
                    
                    <!-- End of controls -->
                    %end

                <!-- End of subkey "{{subkey}}" -->
                % end
                
                <!-- Controls to add new a key-value pair -->
                
                <!-- End of controls -->
            
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
                        <!-- Controls to remove this input -->
                        
                        <!-- End of controls to remove this input -->
                        %end

                    </div>

                <!-- End of item in list for "{{key}}" -->
                % end
                
                % if key not in single_value_inputs:
                <!-- Controls to add a new string -->
                
                <!-- End of controls -->
                %end

            <!-- End of key "{{key}}" that doesn't contain nested values -->
            % end

        </div>
        <!-- End of key "{{key}}" -->
    % end
    <!-- End of key in keys -->
    <div class="input-container">
        <input type="submit" value="Update farm">
    </div>
</form>