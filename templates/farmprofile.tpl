% rebase('base.tpl')

<script>
var setup = function() {
    setupSlideEvents();
};
window.onload = setup;
</script>

<h2>{{farm_content["title"][0]}}</h2>

%if len(farm_content["images"]) > 0:
    <div class="slideshow-container" style="line-height: 25em;">
        % is_first = True
        % for image in farm_content["images"]:
            % fig_class = 'class=show' if is_first else ''
            % is_first = False
            <figure {{fig_class}}>
                <img src="{{root_rel_dir}}{{image}}" style="max-height: 25em;">
                % caption = captions.get(image, '')
                % if caption != '':
                    <figcaption>{{caption}}</figcaption>
                % end
            </figure>
        % end
        <span class="prev non-selectable">«</span><span class="next non-selectable">»</span><span class="pause non-selectable">pause</span>
    </div>
%end

<div class="profile-flex-container">
    <div class="profile-left-container">
        <div class="profile-map-container svg-container">
            % dimensions = map_settings['image-dimensions']
            % coords = farm_content.get('coords', [''])[0].split(',')
            % if len(coords) == 2:
                <!-- The canvas is required to make resizing the SVG work on IE -->
                <canvas class="dummy-canvas" width="{{dimensions[0]}}" height="{{dimensions[1]}}"></canvas>
                <svg id="edit-farm-map-svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" viewbox="0 0 {{dimensions[0]}} {{dimensions[1]}}" preserveAspectRatio="xMaxYMax meet">
                    <image id="edit-farm-map-img" width="{{dimensions[0]}}" height="{{dimensions[1]}}" xlink:href="{{root_rel_dir}}images/map/{{map_settings['image-filename']}}"></image>
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
