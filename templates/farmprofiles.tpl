% rebase('base.tpl')

<!-- Override style instead of defining new classes. margin-top here matches the margin around a h2. -->
<div class="profile-top-container" style="margin-top:40px;">
    <div class="profile-flex-container">
        <div class="profile-left-container" style="width:60%;">
            <div class="profile-map-container">
                <img src="images/map-all.png"/>
            </div>
        </div>
        <div class="profile-right-container" style="width:40%;">
            <p>
                Follow the links below to see profiles of some of the CSA farms in Ireland. There are up to ten active CSA farms known to us.
            </p>
            % for farmname in sorted(permissions_dict['farms']):
                <p style="text-align:left;margin:0px">
                        % title = get_farm_title(farmname)
                        <a href="farms/{{farmname}}">{{title}}</a>
                </p>
            % end
        </div>
    </div>
</div>
