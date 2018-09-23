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
            <div class="profile-map-container svg-container">
                % coords = farm_content.get('coords', [''])[0].split(',')
                % if len(coords) == 2:
                    <!-- The canvas is required to make resizing the SVG work on IE -->
                    <canvas class="dummy-canvas" width="253.38666" height="317.33331"></canvas>
                    <svg id="edit-farm-map-svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" viewbox="0 0 253.38666 317.33331" preserveAspectRatio="xMaxYMax meet">
                        <image id="edit-farm-map-img" width="253.38666" height="317.33331" xlink:href="{{root_rel_dir}}images/map/map-all-blank-no-dots-no-frame-fill.svg"></image>
                        <circle cx="{{coords[0]}}" cy="{{coords[1]}}" r="3"></circle>
                    </svg>
                % end
            </div>
            
            <!-- TODO: we could put "Representative" first if required -->
            % subkeys = order_info_keys(farm_content["info"].keys())
            % for subkey in subkeys:
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
