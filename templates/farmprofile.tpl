% rebase('base.tpl')

<div class="profile-top-container">
    <h2>{{farm_content["title"][0]}}</h2>
    
    %if len(farm_content["images"]) > 0:
        <div class="profile-img-container">
            <!-- E.g. "images/profile/profile-cloughjordan.jpg" -->
            % profile_image = get_profile_image(farm_content)
            % if profile_image:
                <img src="{{root_rel_dir}}{{profile_image}}"/>
            % end
        </div>
    %end

    <div class="profile-flex-container">
        <div class="profile-left-container">
            <div class="profile-map-container">
                <!-- TODO: we could just have each farm input their coordinates here -->
                <!-- E.g. "images/map-cloughjordan.png" -->
                <img src="{{root_rel_dir}}images/maps/map-{{farm}}.png"/>
            </div>
            
            <!-- TODO: we could put "Representative" first if required -->
            % subkeys = order_info_keys(farm_content["info"].keys())
            %for subkey in subkeys:
                <%
                # fixup_url should have been passed to render()
                convert_to_a = lambda x: '<a href="%s">%s</a>' % (fixup_url(x), fixup_url(x))
                values = farm_content["info"][subkey]
                values = [convert_to_a(x) for x in values] if (subkey == "Website") else values
                value = "<br>".join(values)
                %>
                <p>
                    <span class="profile-info-key">{{subkey}}</span>
                    <br>
                    <span class="profile-info-value">
                    {{!value}}
                    % if subkey == "Rep":
                        <a href="{{root_rel_dir}}edit/{{farm}}"><i title="Click to edit this farm profile" class="fa fa-edit"></i></a>
                    % end
                    </span>
                </p>
            %end
        </div>
        
        <div class="profile-right-container">
        % for para in farm_content["description"]:
            <p>
            {{para}}
            </p>
        % end
        </div>
    </div>

</div>
