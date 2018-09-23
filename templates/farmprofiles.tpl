% rebase('base.tpl')

<script>
$(document).ready(function(){
    $('.map-circle-main').on('mouseenter', function() {
        var linkId = '#link-' + this.id.split('-')[2];
        $(linkId).addClass('hovered-link');
    });

    $('.map-circle-main').on('mouseleave', function() {
        var linkId = '#link-' + this.id.split('-')[2];
        $(linkId).removeClass('hovered-link');
    });

    $('.map-circle-main').on('click', function() {
        var url = '{{root_rel_dir}}farms/' + this.id.split('-')[2]
        window.location.href = url;
    });

    $('.farm-links').on('mouseenter', function() {
        var circleId = '#map-circle-' + this.id.split('-')[1];
        $(circleId).addClass('map-circle-main-active');
    });

    $('.farm-links').on('mouseleave', function() {
        var circleId = '#map-circle-' + this.id.split('-')[1];
        $(circleId).removeClass('map-circle-main-active');
    });
});
</script>

<!-- Override style instead of defining new classes. margin-top here matches the margin around a h2. -->
<div class="profile-top-container" style="margin-top:40px;">
    <div class="profile-flex-container">
        <div class="profile-left-container" style="width:60%;">
            <div class="profile-map-container svg-container">

                <!-- These are the hard-coded dimensions of the SVG map we're using :( -->
                <!-- The canvas is required to make resizing the SVG work on IE -->
                <canvas class="dummy-canvas" width="253.38666" height="317.33331"></canvas>
                <svg id="edit-farm-map-svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" viewbox="0 0 253.38666 317.33331" preserveAspectRatio="xMaxYMax meet">
                    <image width="253.38666" height="317.33331" xlink:href="{{root_rel_dir}}images/map/map-all-blank-no-dots-no-frame-fill.svg"></image>
                    % for farmname in permissions_dict['farms']:
                        % coords = get_farm_coords(farmname)
                        % if len(coords) == 2:
                            <circle class="map-circle-main" id="map-circle-{{farmname}}" cx="{{coords[0]}}" cy="{{coords[1]}}" r="3"></circle>
                        % end
                    % end
                </svg>

            </div>
        </div>
        <div class="profile-right-container" style="width:40%;">
            <p>
                Follow the links below to see profiles of some of the CSA farms in Ireland. There are up to ten active CSA farms known to us.
            </p>
            % for farmname in sorted(permissions_dict['farms']):
                <p style="text-align:left;margin:0px">
                    % title = get_farm_title(farmname)
                    <a href="farms/{{farmname}}" class="farm-links" id="link-{{farmname}}">{{title}}</a>
                </p>
            % end
        </div>
    </div>
</div>
