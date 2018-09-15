% rebase('base.tpl')

<!-- Override style instead of defining new classes. margin-top here matches the margin around a h2. -->
<div class="profile-top-container" style="margin-top:40px;">
    <div class="profile-flex-container">
        <div class="profile-left-container" style="width:70%;">
            <div class="profile-map-container">
                <img src="images/map-all.png"/>
            </div>
        </div>
        <div class="profile-right-container" style="width:30%;">
            <p>
This page profiles some CSA farms in Ireland. There are up to ten active CSA farms known to us.
            </p>
        </div>
    </div>
</div>

% for farmname in sorted(farm_content_dict):
<!-- Content for farmname "{{farmname}}" -->
% farm_content = farm_content_dict[farmname]

    <div class="profile-top-container">
        <h2>{{farm_content["title"][0]}}</h2>
        
        %if len(farm_content["images"]) > 0:
            <div class="profile-img-container">
                <!-- E.g. "images/profile/profile-cloughjordan.jpg" -->
                % profile_image = get_profile_image(farm_content)
                % if profile_image:
                    <img src="{{profile_image}}"/>
                % end
            </div>
        %end

        <div class="profile-flex-container">
            <div class="profile-left-container">
                <div class="profile-map-container">
                    <!-- TODO: we could just have each farm input their coordinates here -->
                    <!-- E.g. "images/map-cloughjordan.png" -->
                    <img src="images/maps/map-{{farmname}}.png"/>
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
                            <a href="edit/{{farmname}}"><i title="Click to edit this farm profile" class="fa fa-edit"></i></a>
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

<!-- End of content for "{{farmname}}" -->
%end