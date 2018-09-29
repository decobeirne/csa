% rebase('base.tpl')

<script>
var setup = function() {
    setupSlideEvents();
};
window.onload = setup;
</script>

<h2>What is a CSA?</h2>
<div class="slideshow-container" style="line-height: 25em;">
    % is_first = True
    % for (image, caption) in images:
        % fig_class = 'class=show' if is_first else ''
        % is_first = False
        <figure {{fig_class}}>
            <img src="{{root_rel_dir}}{{image}}" style="max-height: 25em;">
            % if caption != '':
                <figcaption>{{caption}}</figcaption>
            % end
        </figure>
    % end
    <span class="prev non-selectable">«</span><span class="next non-selectable">»</span><span class="pause non-selectable">pause</span>
</div>
<p>
Community Supported Agriculture is a partnership between a group of
people and a farmer. The members receive a share in the CSA when they
commit to pay an agreed fee to the farmer for the duration of a season,
and in return they get healthy, local food produced in an agroecological*
way. This partnership allows everyone to share both the rewards and
also the challenges that our independent farmers face every year. The
CSA model is a way to self-organise food distribution systems. This is
more than a model to feed you with healthy, local and organic food; it is
a commitment, and encourages learning and community engagement.
Although CSAs are a relatively new concept in Ireland, they have been
thriving in other parts of the world for many years. For more information
you can read the report: Overview of Community Supported Agriculture
in Europe.
</p>
<p class="footnote">
*Agroecology uses ecological processes and applies them to agriculture. Not
all Irish CSAs are registered organic, but all the growers are committed to
growing food without chemicals and in close discussion and collaboration
with the community.
</p>