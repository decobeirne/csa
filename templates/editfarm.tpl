% rebase('base.tpl')

<script>
var setup = function() {
    setupLinks();
};
window.onload = setup;
</script>

<form method="post" action="farmprofiles-beta">
    % keys = instructions['order']
    % textarea_inputs = instructions['textarea-inputs']

    <!-- Iterate through keys as listed in instruction dict -->
    % for key in keys:
        % instruction = instructions[key]
        % value = content[key]
        <!-- Key {{key}} -->

        <div class="edit-farm-container">
            % title = key.capitalize()
            <p class="edit-farm-key">{{title}}</p>
            <p class="edit-farm-instruction">{{instruction}}</p>
            
            % if type(value) != list:
            <!-- There is just a single string for this key, e.g. "title" -->

                <div class="input-container">
                    <input type="text" name="{{key}}" value="{{value}}">
                </div>

            <!-- End value != list for {{key}} -->
            % else:
            <!-- The value for {{key}} is a list -->

                % if len(value) == 0:
                <!-- If there is nothing in the list currently, then assume it should contain strings, e.g. "desc" -->
                <!-- We're give this key one empty input. Others may be added by the user, so name this one key£0 -->
                <!-- Use "£" as a separator to (hopefully) avoid needing to escape strings -->

                    <div class="input-container">
                        % if key in textarea_inputs:
                            <textarea rows="8" name="{{key}}£0"></textarea>
                        % else:
                            <input type="text" name="{{key}}£0">
                        % end
                    </div>

                <!-- End of empty list for key {{key}} -->
                % else:
                <!-- Iterate through items in list for key {{key}} -->

                    % count = 0
                    % for item in value:
                    <!-- Item {{count}} in list for {{key}} -->

                        %if type(item) != list:
                        <!-- If the item is not a list, then assume it is a string, e.g. a paragraph in "desc" -->

                            <div class="input-container">
                                % if key in textarea_inputs:
                                    <textarea rows="8" name= "{{key}}£{{count}}">{{item}}</textarea>
                                % else:
                                    <input type="text" name="{{key}}£{{count}}" value="{{item}}">
                                % end
                            </div>

                        <!-- End of single item in list for {{key}} -->
                        % else:
                        <!-- The item within the list for {{key}} is a list, e.g. under "info", the first item might be ["Website", "cloughjordancommunityfarm.ie"] -->

                            % subkey = item[0]
                            % subvalue = item[1]
                            <p class="edit-farm-sub-key">{{subkey}}</p>

                            % if type(subvalue) != list:
                            <!-- The subkey {{subkey}} of {{key}} is a single item -->

                                <div class="input-container">
                                    <input type="text" name="{{key}}£{{count}}£{{subkey}}">
                                </div>

                            <!-- End of single item for subkey {{subkey}} under {{key}} -->
                            % else:
                            <!-- The key {{key}} contains a list, and this item of the list, {{subkey}}, is also a list -->
                            <!-- E.g. the key "info" contains a list, and under the subkey "Farmers" we also have a list, e.g. ["FarmerA", "FarmerB"] -->

                                % if len(subvalue) == 0:
                                <!-- The list for {{subkey}} under {{key}} is empty, so add one input -->

                                    <div class="input-container">
                                        <input type="text" name="{{key}}£{{count}}£{{subkey}}£0}}">
                                    </div>

                                <!-- End of empty list for {{subkey}} under {{key}} -->
                                % else:
                                <!-- The list for {{subkey}} under {{key}} contains values -->

                                    % subcount = 0
                                    % for subitem in subvalue:

                                        <div class="input-container">
                                            <!-- E.g. info$0$Address$1 if we have {"info'": ["Address", ["Foo", "Bar"]]} -->
                                            <input type="text" name="{{key}}£{{count}}£{{subkey}}£{{subcount}}" value="{{subitem}}">
                                        </div>

                                        % subcount += 1
                                    % end

                                <!-- End of going through items in list for {{subkey}} under {{key}} -->
                                % end

                            <!-- End of looking at the list {{subkey}} under {{key}} -->
                            % end

                        <!-- End of looking at item under {{key}}, where that item is also a list -->
                        % end

                        % count += 1
                    <!-- End of item in list for {{key}} -->
                    % end

                <!-- End of len(value) != 0 -->
                % end

            <!-- End looking at list value for {{key}} -->
            % end

        </div>
        <!-- End of key {{key}} -->
    % end
    <!-- End of key in keys -->
    <div class="input-container">
        <input type="submit" value="Update farm">
    </div>
</form>