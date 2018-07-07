% rebase('base.tpl')

<script>
var setup = function() {
    setupLinks();
};
window.onload = setup;
</script>


% for farm in farms:
    <div>
        <p>Cloughjordan <a href="editfarm/{{farm}}">Edit</a></p>
    </div>
% end

<p>
<a href="logout">logout</a>
</p>
