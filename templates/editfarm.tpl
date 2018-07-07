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
    % for key in keys:
        % instruction = instructions[key]
        % value = content[key]
        
        <div class="edit-farm-container">
            % title = key.capitalize()
            <p class="edit-farm-key">{{title}}</p>
            <p class="edit-farm-instruction">{{instruction}}</p>
            
            % if type(value) == list:
                % if len(value) == 0:
                    <!-- If there is nothing in the list currently, then assume it should contain strings, e.g. "desc" -->
                    <div class="input-container">
                        % if key in textarea_inputs:
                            <textarea rows="8" name= "{{key}}"></textarea>
                        % else:
                            <input type="text" name="{{key}}">
                        % end
                    </div>
                % else:
                    % for item in value:
                        %if type(item) == list:
                            <!-- The items within the list are lists, e.g. under "info", the first item might be ["Website", "cloughjordancommunityfarm.ie"] -->
                            % subkey = item[0]
                            % subvalue = item[1]
                            <p class="edit-farm-sub-key">{{subkey}}</p>
                            
                            % if type(subvalue) == list:
                                % if len(subvalue) == 0:
                                    <!-- There is nothing in the sublist, so add one input -->
                                    <div class="input-container">
                                        <input type="text" name="{{subkey}}">
                                    </div>

                                % else:
                                    <!-- For this subkey, the value may be a list, e.g. under "info", we may have a list ["Address", ["Foo", "Bar"]] -->
                                    % for subitem in subvalue:
                                        <div class="input-container">
                                            <input type="text" name="{{subkey}}" value="{{subitem}}">
                                        </div>
                                    % end
                                % end
                            
                            % else:
                                <!-- If not a list then must be a string, e.g. the paragraphs under "desc" -->
                                <div class="input-container">
                                    <input type="text" name="{{subkey}}" value="{{subvalue}}">
                                </div>
                            % end
                        
                        <!-- End of sub type list -->
                        % else:
                            <!-- If the item is not a list, then assume it is a string, e.g. a paragraph in "desc" -->
                            <div class="input-container">
                                % if key in textarea_inputs:
                                    <textarea rows="8" name= "{{key}}">{{item}}</textarea>
                                % else:
                                    <input type="text" name="{{key}}" value="{{item}}">
                                % end
                            </div>
                        % end
                        
                    <!-- End of item in value -->
                    % end
                
                <!-- End of len(value) != 0 -->
                % end

            <!-- End type list -->
            % else:
                <!-- There is just a single string for this key, e.g. "title" -->
                <div class="input-container">
                    <input type="text" name="{{key}}" value="{{value}}">
                </div>
            % end
            
        </div>
        
    <!-- End of key in keys -->
    % end
    <div class="input-container">
        <input type="submit" value="Update farm">
    </div>
</form>


<p>
<a href="logout">logout</a>
</p>
